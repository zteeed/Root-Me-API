from html import unescape

from lxml import html

from worker.parser.exceptions import RootMeParsingError


def extract_pseudo(content):
    tree = html.fromstring(content)
    result = tree.xpath('//meta[@name="author"]/@content')
    if not result:
        raise RootMeParsingError()
    print(result[0])
    return unescape(result[0])


def extract_score(content):
    tree = html.fromstring(content)
    result = tree.xpath('//ul[@class="spip"]/li[contains(., "Score")]/span/text()')
    result = [int(score) for score in result]
    if not result and not result[0]:  # result can be equal to [''] with this xpath search
        raise RootMeParsingError()
    return result[0]
