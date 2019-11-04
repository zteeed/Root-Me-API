import json
from datetime import datetime
from typing import Dict, Optional

from worker import app, log
from worker.constants import URL
from worker.http_client import http_get
from worker.parser.profile import extract_pseudo
from worker.parser.stats import extract_stats


def get_user_stats_data(username: str, lang: str) -> Optional[Dict[str, str]]:
    html = http_get(f'{URL}/{username}?inc=statistiques&lang={lang}')
    if html is None:
        log.warning(f'could_not_get_user_stats', username=username)
        return

    pseudo = extract_pseudo(html)
    solved_challenges = extract_stats(html)

    return {
        'pseudo': pseudo,
        'solved_challenges': solved_challenges,
    }


async def set_user_stats(username: str, lang: str) -> None:
    response = get_user_stats_data(username, lang)
    await app.redis.set(f'{lang}.{username}.stats',
                        json.dumps({'body': response, 'last_update': datetime.now().isoformat()}))
    log.debug('set_user_stats_success', username=username, lang=lang)
