import asyncio

import aioredis
from typing import List, Tuple
from collections import OrderedDict

from worker import app
from worker.constants import CG_NAME, CONSUMER_NAME, REDIS_STREAM_USERS, REDIS_STREAM_CHALLENGES
from worker.redis_interface.challenges import set_all_challenges
from worker.redis_interface.contributions import set_user_contributions
from worker.redis_interface.ctf import set_user_ctf
from worker.redis_interface.details import set_user_details
from worker.redis_interface.profile import set_user_profile
from worker.redis_interface.stats import set_user_stats


async def use_stream_item(stream_item: List[Tuple[bytes, bytes, OrderedDict]]) -> None:
    for item in stream_item:
        (stream_name, message_id, ordered_dict) = item
        stream_name = stream_name.decode()

        if stream_name == REDIS_STREAM_USERS:
            username = ordered_dict[b'username'].decode()
            await set_user_profile(username)
            await set_user_contributions(username)
            await set_user_details(username)
            await set_user_ctf(username)
            await set_user_stats(username)

        if stream_name == REDIS_STREAM_CHALLENGES:
            await set_all_challenges()

        await app.redis.xack(stream_name, CG_NAME, message_id)


async def main() -> None:
    app.redis = await aioredis.create_redis_pool(('redis', 6379))
    streams = [REDIS_STREAM_USERS, REDIS_STREAM_CHALLENGES]
    while True:
        item = await app.redis.xread_group(CG_NAME, CONSUMER_NAME, streams, count=1, latest_ids=['>'] * len(streams))
        if len(item) > 0:
            await use_stream_item(item)


if __name__ == '__main__':
    asyncio.run(main())
