import json
from datetime import datetime

from worker import app, log
from worker.constants import URL
from worker.http_client import http_get
from worker.parser.details import extract_score, extract_nb_challenges_solved, extract_ranking, \
    extract_ranking_category, extract_challenges
from worker.parser.profile import extract_pseudo


async def set_user_details_data(username):
    html = http_get(URL + username + '?inc=score')
    if html is None:
        log.warning(f'could_not_get_user_details', username=username)
        return

    pseudo = extract_pseudo(html)
    score = extract_score(html)
    if score == 0:  # Manage case when score is null (score is not displayed on profile)
        log.warning(f'could_not_get_user_details', username=username)
        return
    nb_challenges_solved, nb_challenges_tot = extract_nb_challenges_solved(html)
    ranking, ranking_tot = extract_ranking(html)
    ranking_category = extract_ranking_category(html)
    categories = extract_challenges(html)

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

    await app.redis.set(f'{username}.details', json.dumps(response))
    log.debug('set_user_details_success', username=username)


async def set_user_details(username):
    await set_user_details_data(username)
    timestamp = json.dumps({'timestamp': str(datetime.now())})
    await app.redis.set(f'{username}.details.timestamp', timestamp)

