import re

from worker.parser.exceptions import RootMeParsingError


def extract_challenge_general_info(txt):
    pattern = '<td><img.*?><td.*?><a href=\"(.*?)\" title=\"(.*?)\">(.*?)<'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse general information about a challenge.")
    return result[0]


def extract_validation_info(txt):
    pattern = '<span class="gras left text-left".*?>(.*?)%</span>'
    pattern += '<span class="right"><a.*?>(.*?)</a></span>'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse validation information.")
    return result[0]


def extract_difficulty(txt):
    pattern = '<td>(.*?)</td><td class=\".*?\">'
    pattern += '<a href=\".*?\" title=\"(.*?)\">'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse difficulty.")

    # TODO: Improve this function
    for item in result:
        try:
            (value, difficulty) = item
            num = int(value)
            return value, difficulty.split(':')[0].strip()
        except Exception as exception:
            pass


def extract_author(txt):
    pattern = '<td class="show-for-large-up">(.*?)</td>'
    result = re.findall(pattern, txt)
    if not result or not result[0]:
        return ''

    pattern = '<a class=\".*?\"  title=\".*?\" href=\"/(.*?)\?lang=fr\">.*?</a>'
    result = re.findall(pattern, result[0])

    if not result:
        raise RootMeParsingError("Could not parse author.")
    return result[0]


def extract_solutions_and_note(txt):
    # TODO: split this function in two.
    pattern = '</td><td><img src="squelettes/img/note/note(\d+).png"'
    pattern += ' .*?></td><td class=".*?">(\d+)</td>'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse solution count and note.")
    return result[0]
