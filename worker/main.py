import asyncio

import aioredis

from worker import app
from worker.redis_interface.challenges import set_all_challenges
from worker.redis_interface.contributions import set_user_contributions
from worker.redis_interface.ctf import set_user_ctf
from worker.redis_interface.details import set_user_details
from worker.redis_interface.profile import set_user_profile
from worker.redis_interface.stats import set_user_stats


async def use_users_stream_item(stream_item):
    (stream_name, message_id, ordered_dict) = stream_item[0]
    username = ordered_dict[b'username'].decode()

    # AttributeError: 'Redis' object has no attribute 'xdel'
    response = await app.redis.execute('XDEL', 'update_users', message_id)
    if response != 1:  # an other worker already took this username for update
        return

    await set_user_profile(username)
    await set_user_contributions(username)
    await set_user_details(username)
    await set_user_ctf(username)
    await set_user_stats(username)


async def use_challenges_stream_item(challenges_stream_item):
    (stream_name, message_id, ordered_dict) = challenges_stream_item[0]

    # AttributeError: 'Redis' object has no attribute 'xdel'
    response = await app.redis.execute('XDEL', 'update_challenges', message_id)
    if response != 1:  # an other worker already took this username for update
        return

    set_all_challenges()


async def main():
    while True:
        users_stream_item = await app.redis.xread(['update_users'], count=1, timeout=1, latest_ids=[0])
        if not users_stream_item:
            challenges_stream_item = await app.redis.xread(['update_challenges'], count=1, timeout=1, latest_ids=[0])
            if challenges_stream_item:
                await use_challenges_stream_item(challenges_stream_item)
        else:
            await use_users_stream_item(users_stream_item)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app.redis = loop.run_until_complete(aioredis.create_redis_pool(('localhost', 6379), loop=loop))
    loop.run_until_complete(main())
    loop.run_forever()
