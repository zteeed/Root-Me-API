import json
from multiprocessing.pool import ThreadPool
from datetime import datetime
from typing import Dict, List, Optional
from functools import partial

from worker import app, log
from worker.constants import URL
from worker.http_client import http_get
from worker.parser.category import extract_categories, extract_category_info


def retrieve_category_info(lang: str, category: str) -> Optional[List[Dict[str, str]]]:
    html = http_get(f'{URL}/{lang}/Challenges/{category}/')
    if html is None:
        log.warn('category_not_found', category=category)
        return None

    log.msg(f"Fetched category page '{category}'")
    return extract_category_info(html, category)


async def set_all_challenges(lang: str) -> None:
    html = http_get(f'{URL}/{lang}/Challenges/')
    if html is None:
        log.error('challenges_page_not_found')
        return

    categories = extract_categories(html)
    if not categories:
        log.warn('fetch_all_categories_failed', lang=lang)
        return

    log.debug('fetched_categories', categories=categories, lang=lang)
    tp_func = partial(retrieve_category_info, lang)
    with ThreadPool(len(categories)) as tp:
        response = tp.map(tp_func, categories)

    timestamp = datetime.now().isoformat()
    await app.redis.set(f'{lang}.challenges', json.dumps({'body': response, 'last_update': timestamp}))
    await app.redis.set(f'{lang}.categories', json.dumps({'body': categories, 'last_update': timestamp}))
    for category_data in response:
        await app.redis.set(f'{lang}.categories.{category_data[0]["name"]}',
                            json.dumps({'body': category_data, 'last_update': timestamp}))

    log.debug('set_all_challenges_success', lang=lang)
