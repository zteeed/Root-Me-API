from worker import log
from worker.redis_interface.challenges import set_all_challenges
from worker.redis_interface.contributions import set_user_contributions
from worker.redis_interface.ctf import set_user_ctf
from worker.redis_interface.details import set_user_details
from worker.redis_interface.profile import set_user_profile
from worker.redis_interface.stats import set_user_stats

from datetime import timedelta
from timeloop import Timeloop


timeloop = Timeloop()


@timeloop.job(interval=timedelta(minutes=30))
def challenge_job_every_timedelta():
    log.info('Timeloop challenge job triggered', timedelta=30, type='minutes')
    set_all_challenges()


def main():
    users = ['zTeeed-115405']
    for username in users:
        set_user_profile(username)
        set_user_contributions(username)
        set_user_details(username)
        set_user_ctf(username)
        set_user_stats(username)


if __name__ == '__main__':
    main()
