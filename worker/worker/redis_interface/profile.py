import json
from datetime import datetime
from typing import Dict, List, Optional

from worker import app, log
from worker.constants import URL
from worker.http_client import http_get
from worker.parser.profile import extract_pseudo, extract_score


def get_user_profile_data(username: str, lang: str) -> Optional[List[Dict[str, str]]]:
    html = http_get(f'{URL}/{username}?lang={lang}')
    if html is None:
        log.warning(f'user_profile_not_found', username=username)
        return

    pseudo = extract_pseudo(html)
    score = extract_score(html)
    response = [{
        'pseudo': pseudo,
        'score': score,
    }]
    return response


async def set_user_profile(username: str, lang: str) -> None:
    response = get_user_profile_data(username, lang)
    response = {'body': response, 'last_update': datetime.now().isoformat()}
    await app.redis.set(f'{lang}.{username}', json.dumps(response))
    await app.redis.set(f'{lang}.{username}.profile', json.dumps(response))
    log.debug('set_user_profile_success', username=username, lang=lang)
