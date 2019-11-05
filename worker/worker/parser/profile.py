from html import unescape

from lxml import html

from worker.constants import URL
from worker.parser.exceptions import RootMeParsingError


def extract_pseudo(content: bytes) -> str:
    tree = html.fromstring(content)
    result = tree.xpath('//meta[@name="author"]/@content')
    if not result:
        raise RootMeParsingError()
    return unescape(result[0])


def extract_score(content: bytes) -> int:
    tree = html.fromstring(content)
    result = tree.xpath('//ul[@class="spip"]/li[3]/span/text()')
    if not result:  # Manage case when score is null (score is not displayed on profile)
        return 0
    if not result[0]:  # result can be equal to [''] with this xpath search
        raise RootMeParsingError()
    result = [int(score) for score in result]
    return result[0]


def extract_avatar_url(content: bytes) -> str:
    tree = html.fromstring(content)
    result = tree.xpath('//div[@class="t-body tb-padding"]/h1[@itemprop="givenName"]/img/@src')
    if not result:
        raise RootMeParsingError()
    return f'{URL}/{result[0]}'
