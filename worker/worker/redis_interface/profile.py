import json

from worker.constants import URL
from worker.parser.profile import extract_pseudo, extract_score
from worker.redis_interface import session, redis_app
from worker.redis_interface.exceptions import RootMeException


def set_user_profile(username):
    r = session.get(URL + username)
    if r.status_code != 200:
        raise RootMeException(r.status_code)

    pseudo = extract_pseudo(r.text)
    score = extract_score(r.text)
    response = [{
        'pseudo': pseudo,
        'score': score,
    }]
    redis_app.set(f'{username}', json.dumps(response))
    redis_app.set(f'{username}.profile', json.dumps(response))
