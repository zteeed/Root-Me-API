from api.constants import URL
from api.http_interface import session
from api.http_interface.exceptions import RootMeException
from api.parser.profile import extract_pseudo
from api.parser.stats import extract_stats

def get_user_stats(username):
    r = session.get(URL + username + '?inc=statistiques')
    if r.status_code != 200:
        raise RootMeException(r.status_code)

    txt = r.text.replace('\n', '')
    txt = txt.replace('&nbsp;', '')

    pseudo = extract_pseudo(txt)
    solved_challenges = extract_stats(txt)

    return {
        'pseudo': pseudo,
        'solved_challenges': solved_challenges,
    }
