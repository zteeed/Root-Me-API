import json

from worker import app, log
from worker.constants import URL
from worker.http_client import http_get
from worker.parser.profile import extract_pseudo
from worker.parser.stats import extract_stats


async def set_user_stats(username):
    html = http_get(URL + username + '?inc=statistiques')
    if html is None:
        log.warning(f'could_not_get_user_stats', username=username)
        return

    pseudo = extract_pseudo(html)
    solved_challenges = extract_stats(html)

    response = {
        'pseudo': pseudo,
        'solved_challenges': solved_challenges,
    }

    await app.redis.set(f'{username}.stats', json.dumps(response))
    log.debug('set_user_stats_success', username=username)
