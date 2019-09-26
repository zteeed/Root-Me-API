from typing import Any, Dict, Optional

import aiohttp
import aiohttp.client_exceptions
import aiohttp.client_reqrep

from bot.colors import green, red
from bot.constants import URL, timeout

response_content_type = Optional[Dict[str, Any]]


async def request_to(url: str) -> response_content_type:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=timeout) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


async def extract_json(url: str) -> response_content_type:
    data = await request_to(url)
    if data is None:
        red(url)
    else:
        green(url)
        if 'body' in data.keys():
            data = data['body']
    return data


async def extract_default() -> response_content_type:
    return await extract_json(f'{URL}')


async def extract_rootme_profile(user: str) -> response_content_type:
    return await extract_json(f'{URL}/{user}/profile')


async def extract_rootme_stats(user: str) -> response_content_type:
    return await extract_json(f'{URL}/{user}/stats')


async def extract_score(user: str) -> int:
    rootme_profile = await extract_rootme_profile(user)
    return rootme_profile[0]['score']


async def extract_categories() -> response_content_type:
    return await extract_json(f'{URL}/challenges')
