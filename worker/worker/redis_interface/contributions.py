import json

from worker.constants import URL
from worker.parser.contributions import extract_contributions
from worker.parser.profile import extract_pseudo
from worker.redis_interface import session, redis_app
from worker.redis_interface.exceptions import RootMeException


def set_user_contributions(username):
    r = session.get(URL + username + '?inc=contributions')
    if r.status_code != 200:
        raise RootMeException(r.status_code)

    pseudo = extract_pseudo(r.text)
    contributions = extract_contributions(r.text)

    response = [{
        'pseudo': pseudo,
        'contributions': contributions,
    }]
    redis_app.set(f'{username}.contributions', json.dumps(response))
