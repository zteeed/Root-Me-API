from bot.manage.json_data import read_json, update_json
from bot.parser.api.extract_all import extract_default


def default():
    return extract_default()


def is_first():
    data = read_json()
    return data['info']['first']


def update_first_time(boolean):
    data = read_json()
    data['info']['first'] = boolean
    update_json(data)


def launched():
    update_first_time(False)
