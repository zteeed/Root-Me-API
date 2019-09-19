import json
from typing import Any, Dict, Optional

import requests

from bot.colors import purple, red
from bot.constants import URL, timeout

response_content_type = Optional[Dict[str, Any]]


def request_to(url: str) -> Optional[requests.models.Response]:
    try:
        return requests.get(url, timeout=timeout)
    except Exception as exception:
        red(exception)
        return None


def extract_json(url: str) -> response_content_type:
    purple(url)
    r = request_to(url)
    if r is None:
        return
    data = json.loads(r.content.decode())
    if 'body' in data.keys():
        return data['body']
    return data


def extract_default() -> response_content_type:
    return extract_json(f'{URL}')


def extract_rootme_profile(user: str) -> response_content_type:
    return extract_json(f'{URL}/{user}/profile')


def extract_rootme_stats(user: str) -> response_content_type:
    return extract_json(f'{URL}/{user}/stats')


def extract_score(user: str) -> response_content_type:
    return extract_rootme_profile(user)[0]['score']


def extract_categories() -> response_content_type:
    return extract_json(f'{URL}/challenges')
