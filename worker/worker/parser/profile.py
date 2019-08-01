import re
from html import unescape

from worker.parser.exceptions import RootMeParsingError


def extract_pseudo(txt):
    pattern = '<meta name="author" content="(.*?)"/>'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse the pseudo about a user profile.")
    return unescape(result[0])


def extract_score(txt):
    pattern = '<span>(\d+)</span>'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse the score about a user profile.")
    return result[0]
