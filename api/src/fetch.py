import json
from structlog._config import BoundLoggerLazyProxy
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


async def send_tasks_to_worker(log: BoundLoggerLazyProxy, redis_app: Redis, arg: Optional[str], now: datetime,
                               timestamp: Optional[datetime], timeout: int, handler_type: str, lang: str) -> None:
    # updates conditions
    condition = timestamp is None or (now - timestamp).total_seconds() > timeout

    # make updates (send tasks to worker)
    if handler_type == 'static_category' and condition:
        log.info('Send task to worker', stream=REDIS_STREAM_CHALLENGES, lang=lang)
        await redis_app.xadd(REDIS_STREAM_CHALLENGES, {b'lang': lang.encode(), b'update': b"ok"})
    elif handler_type == 'dynamic_user' and arg is not None and condition:
        await redis_app.xadd(REDIS_STREAM_USERS, {b'lang': lang.encode(), b'username': arg.encode()})
        log.info('Send task to worker', stream=REDIS_STREAM_USERS, username=arg, lang=lang)
    elif handler_type == 'dynamic_categories' and arg is not None and condition:
        await redis_app.xadd(REDIS_STREAM_CHALLENGES, {b'lang': lang.encode(), b'update': b"ok"})
        log.info('Send task to worker', stream=REDIS_STREAM_CHALLENGES, lang=lang)


def need_waiting_for_update(now: datetime, timestamp: Optional[datetime], timeout: int) -> bool:
    return timestamp is None or (now - timestamp).total_seconds() > 2*timeout


async def force_update(redis_app: Redis, key: str, now: datetime, timestamp: Optional[datetime], timeout: int) -> None:
    condition = timestamp is None or (now - timestamp).total_seconds() > timeout
    while condition and abs(now-datetime.now()).total_seconds() < REQUEST_TIMEOUT:
        data = await redis_app.get(f'{key}')
        timestamp = extract_timestamp_last_update(data)
        condition = timestamp is None or (now - timestamp).total_seconds() > timeout
    return


async def read_from_redis_key(log: BoundLoggerLazyProxy, redis_app: Redis, key: str, arg: Optional[str] = None,
                              handler_type: str = 'static', lang: str = 'en'):
    data = await redis_app.get(f'{key}')
    now = datetime.now()
    timestamp = extract_timestamp_last_update(data)
    timeout = get_timeout(handler_type)

    await send_tasks_to_worker(log, redis_app, arg, now, timestamp, timeout, handler_type, lang)
    response = need_waiting_for_update(now, timestamp, timeout)
    if response:
        await force_update(redis_app, key, now, timestamp, timeout)

    return await redis_app.get(f'{key}')
