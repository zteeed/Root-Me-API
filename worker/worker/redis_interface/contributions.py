import json

from worker import log
from worker.constants import URL
from worker.parser.contributions import extract_contributions
from worker.parser.profile import extract_pseudo
from worker.redis_interface import session, redis_app


def set_user_contributions(username):
    r = session.get(URL + username + '?inc=contributions')
    if r.status_code != 200:
        log.warning(f'HTTP {r.status_code} for username {username}.')
        return

    pseudo = extract_pseudo(r.text)
    contributions = extract_contributions(r.text)

    response = [{
        'pseudo': pseudo,
        'contributions': contributions,
    }]
    redis_app.set(f'{username}.contributions', json.dumps(response))
