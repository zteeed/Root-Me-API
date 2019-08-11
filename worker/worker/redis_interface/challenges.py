import json
from multiprocessing.pool import ThreadPool

from worker import log
from worker.constants import URL
from worker.http_client import http_get
from worker.parser.category import extract_categories, extract_category_info
from worker.redis_interface import redis_app


def retrieve_category_info(category):
    html = http_get(f'{URL}fr/Challenges/{category}/')
    if html is None:
        log.warn('category_not_found', category=category)
        return None

    log.msg(f"Fetched category page '{category}'")
    return extract_category_info(html, category)


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

    log.debug('set_all_challenges_success')
