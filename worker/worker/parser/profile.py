from html import unescape

from lxml import html

from worker.parser.exceptions import RootMeParsingError


def extract_pseudo(content):
    tree = html.fromstring(content)
    result = tree.xpath('//meta[@name="author"]/@content')
    if not result:
        raise RootMeParsingError()
    return unescape(result[0])


def extract_score(content):
    tree = html.fromstring(content)
    result = tree.xpath('//ul[@class="spip"]/li[contains(., "Score")]/span/text()')
    if not result:  # Manage case when score is null (score is not displayed on profile)
        return 0
    if not result[0]:  # result can be equal to [''] with this xpath search
        raise RootMeParsingError()
    result = [int(score) for score in result]
    return result[0]
