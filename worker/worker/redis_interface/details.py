import json

from datetime import datetime
from typing import Dict, List, Optional

from worker import app, log
from worker.constants import URL
from worker.http_client import http_get
from worker.parser.details import extract_score, extract_nb_challenges_solved, extract_ranking, \
    extract_ranking_category, extract_challenges
from worker.parser.profile import extract_pseudo


def get_user_details_data(username: str) -> Optional[List[Dict[str, str]]]:
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


async def set_user_details(username: str) -> None:
    response = get_user_details_data(username)
    await app.redis.set(f'{username}.details',
                        json.dumps({'body': response, 'last_update': datetime.now().isoformat()}))
    log.debug('set_user_details_success', username=username)
