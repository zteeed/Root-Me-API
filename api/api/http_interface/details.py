from api.constants import URL
from api.http_interface import session
from api.http_interface.exceptions import RootMeException
from api.parser.details import extract_score, extract_ranking, \
    extract_ranking_category, extract_challenges
from api.parser.profile import extract_pseudo


def get_user_details(username):
    r = session.get(URL + username + '?inc=score')
    if r.status_code != 200:
        raise RootMeException(r.status_code)

    txt = r.text.replace('\n', '')
    txt = txt.replace('&nbsp;', '')
    pseudo = extract_pseudo(txt)
    score, nb_challenges_solved, nb_challenges_tot = extract_score(txt)
    ranking, ranking_tot = extract_ranking(txt)
    ranking_category = extract_ranking_category(txt)
    categories = extract_challenges(txt)

    return [{
        'pseudo': pseudo,
        'score': score,
        'nb_challenges_solved': nb_challenges_solved,
        'nb_challenges_tot': nb_challenges_tot,
        'ranking': ranking,
        'ranking_tot': ranking_tot,
        'ranking_category': ranking_category,
        'categories': categories,
    }]
