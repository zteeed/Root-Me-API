import json
from datetime import datetime
from typing import Optional
from aioredis.commands import Redis

from api.constants import REDIS_STREAM_CHALLENGES, REDIS_STREAM_USERS, REQUEST_TIMEOUT, UPDATE_TIMEOUT


def extract_timestamp_last_update(data: str) -> Optional[datetime]:
    if data is None:
        return
    data = json.loads(data)
    if 'last_update' not in data.keys():
        return
    return datetime.strptime(data['last_update'], '%Y-%m-%d %H:%M:%S.%f')


async def read_from_redis_key(redis_app: Redis, key: str, arg: Optional[str], handler_type: str = 'static'):
    data = await redis_app.get(f'{key}')
    timestamp = extract_timestamp_last_update(data)
    now = datetime.now()
    timeout = 10 * UPDATE_TIMEOUT

    # updates conditions
    condition_user = timestamp is None or (now - timestamp).total_seconds() > UPDATE_TIMEOUT
    condition_challenges = timestamp is None or (now - timestamp).total_seconds() > 10*UPDATE_TIMEOUT

    # make updates (send tasks to worker)
    if handler_type == 'static' and condition_user:
        await redis_app.xadd(REDIS_STREAM_CHALLENGES, {b'update': b"ok"})
    elif handler_type == 'dynamic_user' and arg is not None and condition_user:
        timeout = UPDATE_TIMEOUT
        await redis_app.xadd(REDIS_STREAM_USERS, {b'username': arg.encode()})
    elif handler_type == 'dynamic_categories' and arg is not None and condition_challenges:
        await redis_app.xadd(REDIS_STREAM_CHALLENGES, {b'update': b"ok"})
    else:
        return data

    condition = timestamp is None or (now - timestamp).total_seconds() > timeout
    while condition and abs(now-datetime.now()).total_seconds() < REQUEST_TIMEOUT:
        data = await redis_app.get(f'{key}')
        timestamp = extract_timestamp_last_update(data)
        condition = timestamp is None or (now - timestamp).total_seconds() > timeout

    return data
