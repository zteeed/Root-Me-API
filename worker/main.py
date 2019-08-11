from worker import app, log
from worker.redis_interface.challenges import set_all_challenges
from worker.redis_interface.contributions import set_user_contributions
from worker.redis_interface.ctf import set_user_ctf
from worker.redis_interface.details import set_user_details
from worker.redis_interface.profile import set_user_profile
from worker.redis_interface.stats import set_user_stats

import aioredis
import asyncio
import time
from datetime import timedelta


async def challenge_job_every_timedelta():
    wait_seconds = timedelta(minutes=1).total_seconds()
    while True:
        log.info('Timeloop challenge job triggered', timedelta=30, type='minutes')
        await set_all_challenges()
        time.sleep(wait_seconds)


async def main():
    users = ['zTeeed-115405']
    for username in users:
        await set_user_profile(username)
        await set_user_contributions(username)
        await set_user_details(username)
        await set_user_ctf(username)
        await set_user_stats(username)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    #  loop.run_until_complete(timeloop.start(block=False))  # daemon mode
    app.redis = loop.run_until_complete(
        aioredis.create_redis_pool(('localhost', 6379), loop=loop)
    )
    #  loop.run_until_complete(challenge_job_every_timedelta())
    loop.run_until_complete(main())
    loop.run_forever()
