import json, requests
from bot.constants import URL


def request_to(url):
    try:
        return requests.get(url)
    except Exception as exception:
        print(exception)
        return None


def extract_json(url):
    try:
        r = request_to(url)
        return json.loads(r.content.decode())
    except Exception as exception:
        print(exception)
        return None


def extract_default():
    return extract_json('{}'.format(URL))
