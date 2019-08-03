import json

from worker import log
from worker.constants import URL
from worker.http_client import http_get
from worker.parser.profile import extract_pseudo, extract_score
from worker.redis_interface import session, redis_app


def set_user_profile(username):
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
    redis_app.set(f'{username}', json.dumps(response))
    redis_app.set(f'{username}.profile', json.dumps(response))
