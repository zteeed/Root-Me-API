import json

from worker import log
from worker.constants import URL
from worker.parser.details import extract_score, extract_nb_challenges_solved, extract_ranking, \
    extract_ranking_category, extract_challenges
from worker.parser.profile import extract_pseudo
from worker.redis_interface import session, redis_app


def set_user_details(username):
    r = session.get(URL + username + '?inc=score')
    if r.status_code != 200:
        log.warning(f'HTTP {r.status_code} for username {username}.')
        return

    pseudo = extract_pseudo(r.content)
    score = extract_score(r.content)
    nb_challenges_solved, nb_challenges_tot = extract_nb_challenges_solved(r.content)
    ranking, ranking_tot = extract_ranking(r.content)
    ranking_category = extract_ranking_category(r.content)
    categories = extract_challenges(r.content)

    response = [{
        'pseudo': pseudo,
        'score': score,
        'nb_challenges_solved': nb_challenges_solved,
        'nb_challenges_tot': nb_challenges_tot,
        'ranking': ranking,
        'ranking_tot': ranking_tot,
        'ranking_category': ranking_category,
        'categories': categories,
    }]

    redis_app.set(f'{username}.details', json.dumps(response))
    log.debug('set_user_details_success', username=username)
