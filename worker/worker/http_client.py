from typing import Optional

from worker import log
from worker.redis_interface import session


class HTTPBadStatusCodeError(RuntimeError):
    def __init__(self, code: int):
        super().__init__(f'bad http status code {code}')


def http_get(url: str) -> Optional[str]:
    """
    Retrieves the HTML from a page via HTTP(s).

    If the page is present on the server (200 status code), returns the html.
    If the server does not host this page (404 status code), returns None.
    Any other HTTP code are considered as unexpected and raise an HTTPBadStatusCodeError.
    :param url: url to the page
    :return: HTML of the page or None
    """
    r = session.get(url)

    if r.status_code == 200:
        # log.debug(f'http_get_success', status_code=r.status_code, url=url)
        return r.content

    if r.status_code == 404:
        log.info(f'http_get_error', status_code=r.status_code, url=url)
        return None

    raise HTTPBadStatusCodeError(r.status_code)
