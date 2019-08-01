import json

from worker import log
from worker.constants import URL
from worker.parser.profile import extract_pseudo, extract_score
from worker.redis_interface import session, redis_app


def set_user_profile(username):
    r = session.get(URL + username)
    if r.status_code != 200:
        log.warning(f'HTTP {r.status_code} for user {username}')
        return

    pseudo = extract_pseudo(r)
    score = extract_score(r)
    response = [{
        'pseudo': pseudo,
        'score': score,
    }]
    redis_app.set(f'{username}', json.dumps(response))
    redis_app.set(f'{username}.profile', json.dumps(response))
