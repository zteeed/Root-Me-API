import json, requests
from bot.constants import URL, timeout
from bot.colors import purple, red


def request_to(url):
    try:
        return requests.get(url, timeout=timeout)
    except Exception as exception:
        red(exception)
        return None


def extract_json(url):
    try:
        purple(url)
        r = request_to(url)
        return json.loads(r.content.decode())
    except Exception as exception:
        red(exception)
        return None


def extract_default():
    return extract_json('{}'.format(URL))


def extract_rootme_profile(user):
    return extract_json('{}/{}/profile'.format(URL, user))


def extract_rootme_stats(user):
    return extract_json('{}/{}/stats'.format(URL, user))


def extract_score(user):
    return extract_rootme_profile(user)[0]['score']


def extract_categories():
    return extract_json('{}/challenges'.format(URL))
