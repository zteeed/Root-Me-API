import json
from multiprocessing.pool import ThreadPool

from worker import log
from worker.constants import URL
from worker.http_client import http_get
from worker.parser.category import extract_categories, extract_category_logo, extract_category_description, \
    extract_category_prereq, extract_challenges_info
from worker.redis_interface import redis_app


def retrieve_category_info(category):
    html = http_get(f'{URL}fr/Challenges/{category}/')
    if html is None:
        log.warn('category_not_found', category=category)
        return None

    logo = extract_category_logo(html)
    desc1, desc2 = extract_category_description(html)
    prereq = extract_category_prereq(html)
    challenges = extract_challenges_info(html)

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
    html = http_get(URL + 'fr/Challenges/')
    if html is None:
        log.error('challenges_page_not_found')
        return

    categories = extract_categories(html)
    log.debug('fetched_categories', categories=categories)

    with ThreadPool(len(categories)) as tp:
        response = tp.map(retrieve_category_info, categories)
    redis_app.set('challenges', json.dumps(response))
    redis_app.set('categories', json.dumps(categories))
    for category_data in response:
        redis_app.set(f'categories.{category_data[0]["name"]}', json.dumps(category_data))
