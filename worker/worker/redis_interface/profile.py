import json
from datetime import datetime

from worker import app, log
from worker.constants import URL
from worker.http_client import http_get
from worker.parser.profile import extract_pseudo, extract_score


async def set_user_profile_data(username):
    html = http_get(URL + username)
    if html is None:
        log.warning(f'user_profile_not_found', username=username)
        return

    pseudo = extract_pseudo(html)
    score = extract_score(html)
    response = [{
        'pseudo': pseudo,
        'score': score,
    }]
    await app.redis.set(f'{username}', json.dumps(response))
    await app.redis.set(f'{username}.profile', json.dumps(response))

    log.debug('set_user_profile_success', username=username)


async def set_user_profile(username):
    await set_user_profile_data(username)
    timestamp = json.dumps({'timestamp': str(datetime.now())})
    await app.redis.set(f'{username}.timestamp', timestamp)
    await app.redis.set(f'{username}.profile.timestamp', timestamp)

