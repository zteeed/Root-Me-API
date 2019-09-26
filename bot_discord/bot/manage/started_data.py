from bot.manage.json_data import read_json, update_json
from bot.parser.api.extract_all import extract_default, response_content_type


async def default() -> response_content_type:
    return await extract_default()


def is_first() -> bool:
    data = read_json()
    return data['info']['first']


def update_first_time(boolean: bool) -> None:
    data = read_json()
    data['info']['first'] = boolean
    update_json(data)


def launched() -> None:
    update_first_time(False)
