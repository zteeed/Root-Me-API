import re
from html import unescape

from lxml import html

from worker.parser.exceptions import RootMeParsingError


def extract_pseudo(r):
    tree = html.fromstring(r.content)
    result = tree.xpath('//meta[@name="author"]/@content')
    if not result or not result[0]:
        raise RootMeParsingError()
    return unescape(result[0])


def extract_score(r):
    tree = html.fromstring(r.content)
    result = tree.xpath('//ul[@class="spip"]/li[contains(., "Score")]/span/text()')
    result = [int(score) for score in result if score.isdigit()]
    if not result and not result[0]:
        raise RootMeParsingError()
    return result[0]
