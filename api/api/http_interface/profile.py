import requests as rq

from api.constants import URL
from api.http_interface.exceptions import RootMeException
from api.parser.profile import extract_pseudo, extract_score


def get_user_profile(username):
    r = rq.get(URL + username)
    if r.status_code != 200:
        raise RootMeException(r.status_code)

    pseudo = extract_pseudo(r.text)
    score = extract_score(r.text)

    return [{
        'pseudo': pseudo,
        'score': score,
    }]
