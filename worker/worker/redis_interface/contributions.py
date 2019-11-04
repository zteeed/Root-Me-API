import itertools
import json
from datetime import datetime
from functools import partial
from multiprocessing.pool import ThreadPool
from typing import Dict, List, Optional, Tuple

from worker import app, log
from worker.constants import URL
from worker.http_client import http_get
from worker.parser.contributions import extract_challenges_contributions, extract_solutions_contributions, \
    extract_contributions_page_numbers

contribution_type = Optional[List[Optional[Dict[str, str]]]]
all_contributions_type = Optional[List[Dict[str, Dict[str, contribution_type]]]]


def get_challenge_contributions(username: str, lang: str, page_index: int) -> Optional[List[Dict[str, str]]]:
    url = f'{URL}/{username}?inc=contributions&lang={lang}&debut_challenges_auteur={5 * page_index}#pagination_challenges_auteur'
    html = http_get(url)
    if html is None:
        log.warning(f'could_not_get_challenge_contributions', username=username, page_index=page_index)
        return
    return extract_challenges_contributions(html)


def get_solution_contributions(username: str, lang: str, page_index: int) -> Optional[List[Dict[str, str]]]:
    url = f'{URL}/{username}?inc=contributions&lang={lang}&debut_solutions_auteur={5 * page_index}#pagination_solutions_auteur'
    html = http_get(url)
    if html is None:
        log.warning(f'could_not_get_solution_contributions', username=username, page_index=page_index)
        return
    return extract_solutions_contributions(html)


def format_contributions_challenges(username: str, lang: str, nb_challenges_pages: int) \
        -> List[Optional[List[Dict[str, str]]]]:
    #  Retrieve challenges contributions
    challenges_contributions = []
    if nb_challenges_pages == 0:
        return challenges_contributions
    tp_function = partial(get_challenge_contributions, username, lang)
    tp_argument = list(range(nb_challenges_pages))
    with ThreadPool(nb_challenges_pages) as tp:
        response_challenges = tp.map(tp_function, tp_argument)
    challenges_contributions = list(itertools.chain(*response_challenges))  # concatenate all challenges lists
    return challenges_contributions


def format_contributions_solutions(username: str, lang: str, nb_solutions_pages: int) -> List[
    Optional[List[Dict[str, str]]]]:
    #  Retrieve solutions contributions
    solutions_contributions = []
    if nb_solutions_pages == 0:
        return solutions_contributions
    tp_function = partial(get_solution_contributions, username, lang)
    tp_argument = list(range(nb_solutions_pages))
    with ThreadPool(nb_solutions_pages) as tp:
        response_solutions = tp.map(tp_function, tp_argument)
    solutions_contributions = list(itertools.chain(*response_solutions))  # concatenate all solutions lists
    return solutions_contributions


def get_user_contributions_data(username: str, lang: str) -> Tuple[contribution_type, contribution_type,
                                                                   all_contributions_type]:
    html = http_get(f'{URL}/{username}?inc=contributions&lang={lang}')
    if html is None:
        log.warning('could_not_get_user_contributions', username=username)
        return None, None, None

    nb_challenges_pages, nb_solutions_pages = extract_contributions_page_numbers(html)
    if nb_challenges_pages == 0 and nb_solutions_pages == 0:
        return None, None, None  # no challenges or solutions published by this user

    challenges_contributions = format_contributions_challenges(username, lang, nb_challenges_pages)
    solutions_contributions = format_contributions_solutions(username, lang, nb_solutions_pages)

    all_contributions = [{
        'contributions': {
            'challenges': challenges_contributions,
            'solutions': solutions_contributions
        }
    }]

    return challenges_contributions, solutions_contributions, all_contributions


async def set_user_contributions(username: str, lang: str) -> None:
    challenges_contributions, solutions_contributions, all_contributions = get_user_contributions_data(username, lang)
    timestamp = datetime.now().isoformat()

    if challenges_contributions is not None:
        await app.redis.set(f'{lang}.{username}.contributions.challenges',
                            json.dumps({'body': challenges_contributions, 'last_update': timestamp}))
    if solutions_contributions is not None:
        await app.redis.set(f'{lang}.{username}.contributions.solutions',
                            json.dumps({'body': solutions_contributions, 'last_update': timestamp}))
    await app.redis.set(f'{lang}.{username}.contributions',
                        json.dumps({'body': all_contributions, 'last_update': timestamp}))
    log.debug('set_user_contributions_success', username=username, lang=lang)
