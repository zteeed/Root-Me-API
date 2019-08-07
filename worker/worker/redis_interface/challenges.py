import json
from multiprocessing.pool import ThreadPool

from worker import log
from worker.constants import URL
from worker.parser.category import extract_categories, extract_category_info
from worker.redis_interface import session, redis_app


def retrieve_category_info(category):
    r = session.get(f'{URL}fr/Challenges/{category}/')
    if r.status_code != 200:
        log.warning(f'HTTP {r.status_code} for category {category}.')
        return

    log.msg(f"Fetched category page '{category}'")

    return extract_category_info(r.content, category)


def set_all_challenges():
    r = session.get(URL + 'fr/Challenges/')
    if r.status_code != 200:
        log.warning(f'HTTP {r.status_code} for challenges.')
        return

    categories = extract_categories(r.content)
    with ThreadPool(len(categories)) as tp:
        response = tp.map(retrieve_category_info, categories)
    redis_app.set('challenges', json.dumps(response))
    redis_app.set('categories', json.dumps(categories))
    for category_data in response:
        redis_app.set(f'categories.{category_data[0]["name"]}', json.dumps(category_data))
