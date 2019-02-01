import requests as rq

from api.constants import URL
from api.http_interface.exceptions import RootMeException
from api.parser.profile import extract_pseudo
from api.parser.contributions import extract_contributions


def get_user_contributions(username):
    r = rq.get(URL + username + '?inc=contributions')
    if r.status_code != 200:
        raise RootMeException(r.status_code)

    pseudo = extract_pseudo(r.text)
    contributions = extract_contributions(r.text)

    return [{
        'pseudo': pseudo,
        'contributions': contributions,
    }]
