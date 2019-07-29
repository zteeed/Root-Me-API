import json
import requests

from bot.colors import purple, red
from bot.constants import URL, timeout


def request_to(url):
    try:
        return requests.get(url, timeout=timeout)
    except Exception as exception:
        red(exception)
        return None


def extract_json(url):
    purple(url)
    r = request_to(url)
    if r is not None:
        return json.loads(r.content.decode())


def extract_default():
    return extract_json(f'{URL}')


def extract_rootme_profile(user):
    return extract_json(f'{URL}/{user}/profile')


def extract_rootme_stats(user):
    return extract_json(f'{URL}/{user}/stats')


def extract_score(user):
    return extract_rootme_profile(user)[0]['score']


def extract_categories():
    return extract_json(f'{URL}/challenges')
