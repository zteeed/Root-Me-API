from functools import partial
import itertools
import json
from worker import log
from worker.constants import URL
from worker.parser.contributions import extract_challenges_contributions, extract_solutions_contributions, \
    extract_contributions_page_numbers
from worker.redis_interface import session, redis_app
from multiprocessing.pool import ThreadPool


def get_challenge_contributions(username, page_index):
    url = f'{URL}{username}?inc=contributions&debut_challenges_auteur={5 * page_index}#pagination_challenges_auteur'
    r = session.get(url)
    if r.status_code != 200:
        log.warning(f'HTTP {r.status_code} for username {username}.')
        return
    return extract_challenges_contributions(r.content)


def get_solution_contributions(username, page_index):
    url = f'{URL}{username}?inc=contributions&debut_solutions_auteur={5 * page_index}#pagination_solutions_auteur'
    r = session.get(url)
    if r.status_code != 200:
        log.warning(f'HTTP {r.status_code} for username {username}.')
        return
    return extract_solutions_contributions(r.content)


def format_contributions_challenges(username, nb_challenges_pages):
    #  Retrieve challenges contributions
    challenges_contributions = []
    if nb_challenges_pages == 0:
        return challenges_contributions
    tp_function = partial(get_challenge_contributions, username)
    tp_argument = list(range(nb_challenges_pages))
    with ThreadPool(nb_challenges_pages) as tp:
        response_challenges = tp.map(tp_function, tp_argument)  # list of requests.content
    challenges_contributions = list(itertools.chain(response_challenges))  # concatenate all challenges lists
    return challenges_contributions


def format_contributions_solutions(username, nb_solutions_pages):
    #  Retrieve solutions contributions
    solutions_contributions = []
    if nb_solutions_pages == 0:
        return solutions_contributions
    tp_function = partial(get_solution_contributions, username)
    tp_argument = list(range(nb_solutions_pages))
    with ThreadPool(nb_solutions_pages) as tp:
        response_solutions = tp.map(tp_function, tp_argument)  # list of requests.content
    solutions_contributions = list(itertools.chain(response_solutions))  # concatenate all solutions lists
    return solutions_contributions


def set_user_contributions(username):
    r = session.get(URL + username + '?inc=contributions')
    if r.status_code != 200:
        log.warning(f'HTTP {r.status_code} for username {username}.')
        return

    nb_challenges_pages, nb_solutions_pages = extract_contributions_page_numbers(r.content)
    if nb_challenges_pages == 0 and nb_solutions_pages == 0:
        return  # no challenges or solutions published by this user

    challenges_contributions = format_contributions_challenges(username, nb_challenges_pages)
    solutions_contributions = format_contributions_solutions(username, nb_solutions_pages)

    response = [{
        'contributions': {
            'challenges': challenges_contributions,
            'solutions': solutions_contributions
        }
    }]
    if challenges_contributions is not None:
        redis_app.set(f'{username}.contributions.challenges', json.dumps(challenges_contributions))
    if solutions_contributions is not None:
        redis_app.set(f'{username}.contributions.solutions', json.dumps(solutions_contributions))
    redis_app.set(f'{username}.contributions', json.dumps(response))
