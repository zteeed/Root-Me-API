import json
from datetime import datetime
from typing import Optional
from aioredis.commands import Redis

from api.constants import REDIS_STREAM_CHALLENGES, REDIS_STREAM_USERS, REQUEST_TIMEOUT, UPDATE_TIMEOUT


def get_timeout(handler_type: str) -> int:
    if handler_type == 'dynamic_user':
        return UPDATE_TIMEOUT
    else:
        return 10 * UPDATE_TIMEOUT


def extract_timestamp_last_update(data: str) -> Optional[datetime]:
    if data is None:
        return
    data = json.loads(data)
    if 'last_update' not in data.keys():
        return
    return datetime.fromisoformat(data['last_update'])


async def send_tasks_to_worker(redis_app: Redis, arg: Optional[str], now: datetime, timestamp: Optional[datetime],
                               timeout: int, handler_type: str) -> None:
    # updates conditions
    condition = timestamp is None or (now - timestamp).total_seconds() > timeout

    # make updates (send tasks to worker)
    if handler_type == 'static' and condition:
        await redis_app.xadd(REDIS_STREAM_CHALLENGES, {b'update': b"ok"})
    elif handler_type == 'dynamic_user' and arg is not None and condition:
        await redis_app.xadd(REDIS_STREAM_USERS, {b'username': arg.encode()})
    elif handler_type == 'dynamic_categories' and arg is not None and condition:
        await redis_app.xadd(REDIS_STREAM_CHALLENGES, {b'update': b"ok"})


def need_waiting_for_update(now: datetime, timestamp: Optional[datetime], timeout: int) -> bool:
    return timestamp is None or (now - timestamp).total_seconds() > 2*timeout


async def force_update(redis_app: Redis, key: str, now: datetime, timestamp: Optional[datetime], timeout: int) -> None:
    condition = timestamp is None or (now - timestamp).total_seconds() > timeout
    while condition and abs(now-datetime.now()).total_seconds() < REQUEST_TIMEOUT:
        data = await redis_app.get(f'{key}')
        timestamp = extract_timestamp_last_update(data)
        condition = timestamp is None or (now - timestamp).total_seconds() > timeout
    return


async def read_from_redis_key(redis_app: Redis, key: str, arg: Optional[str], handler_type: str = 'static'):
    data = await redis_app.get(f'{key}')
    now = datetime.now()
    timestamp = extract_timestamp_last_update(data)
    timeout = get_timeout(handler_type)

    await send_tasks_to_worker(redis_app, arg, now, timestamp, timeout, handler_type)
    response = need_waiting_for_update(now, timestamp, timeout)
    if response:
        await force_update(redis_app, key, now, timestamp, timeout)

    return await redis_app.get(f'{key}')
