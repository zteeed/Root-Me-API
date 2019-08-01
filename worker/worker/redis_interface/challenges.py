import json
from multiprocessing.pool import ThreadPool

from worker import log
from worker.constants import URL
from worker.parser.category import extract_categories, extract_category_logo, extract_category_description, \
    extract_category_prereq, extract_challenges_info
from worker.redis_interface import session, redis_app
from worker.redis_interface.exceptions import RootMeException


def retrieve_category_info(category):
    r = session.get(f'{URL}fr/Challenges/{category}/')
    if r.status_code != 200:
        raise RootMeException(r.status_code)

    logo = extract_category_logo(r.content)
    desc1, desc2 = extract_category_description(r.content)
    prereq = extract_category_prereq(r.content)
    challenges = extract_challenges_info(r.content)

    log.msg(f"Fetched category page '{category}'")

    return [{
        'name': category.strip(),
        'logo': logo.strip(),
        'description1': desc1.strip(),
        'description2': desc2.strip(),
        'prerequisites': prereq,
        'challenges': challenges,
        'challenges_nb': len(challenges),
    }]


def set_all_challenges():
    r = session.get(URL + 'fr/Challenges/')
    if r.status_code != 200:
        raise RootMeException(r.status_code)
    categories = extract_categories(r.content)
    with ThreadPool(len(categories)) as tp:
        response = tp.map(retrieve_category_info, categories)
    redis_app.set('challenges', json.dumps(response))
    redis_app.set('categories', json.dumps(categories))
    for category_data in response:
        redis_app.set(f'categories.{category_data[0]["name"]}', json.dumps(category_data))
