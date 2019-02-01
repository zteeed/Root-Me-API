import re
from html import unescape

from api.parser.challenge import extract_challenge_general_info, extract_validation_info, extract_difficulty, \
    extract_author, extract_solutions_and_note
from api.parser.exceptions import RootMeParsingError


def extract_challenge_ids(txt):
    txt = txt.replace('\n', '')
    txt = txt.replace('&nbsp;', '')
    pattern = r'<div class="clearfix"></div><span><b>(.*?)</b>.*?</span><p'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse and extract challenge IDs from Root-Me.")
    return result


def extract_categories(txt):
    pattern = '<li><a class="submenu.*?" href="fr/Challenges/(.*?)/" '
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse categories.")
    return result


def extract_category_logo(txt):
    txt = txt.replace('\n', '')
    txt = txt.replace('&nbsp;', '')

    pattern = '<img class=\'vmiddle\' alt="" src="(.*?)" .*?/>'
    result = re.findall(pattern, txt)
    if not result or not result[0]:
        raise RootMeParsingError("Could not parse logo from challenge.")

    return result[0]


def extract_category_description(txt):
    pattern = '<meta name="Description" content="(.*?)"/>'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse description.")

    description1 = result[0]

    pattern = '<div class="texte crayon rubrique-texte.*?><p>(.*?)</p>'
    result = re.findall(pattern, txt)
    description2 = result[0] if result else ''

    return unescape(description1), unescape(description2)


def extract_category_prereq(txt):
    txt = txt.replace('\n', '')
    txt = txt.replace('&nbsp;', '')

    pattern = '<p>Prérequis\xa0:(.*?)\/p>'
    result = re.findall(pattern, txt)

    if result == ['<']:
        pattern = '<p>Prérequis\xa0:(.*?)\/div>'
        result = re.findall(pattern, txt)

    if not result:
        return []

    pattern = '><img.*?>\xa0(.*?)<'
    result = re.findall(pattern, result[0])
    if not result:
        raise RootMeParsingError("Could not parse prerequisites.")

    return [r.replace('\xa0', '') for r in result]


def extract_challenge_rows(txt):
    txt = txt.replace('\n', '')
    txt = txt.replace('&nbsp;', '')
    pattern = '<tr>(.*?)</tr>'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse challenges.")
    return result


def extract_info_from_row(row):
    path, statement, name = extract_challenge_general_info(row)
    validations_percentage, validations_nb = extract_validation_info(row)
    value, difficulty = extract_difficulty(row)
    author = extract_author(row)
    note, solutions_nb = extract_solutions_and_note(row)

    return {
        'path': path,
        'statement': unescape(statement),
        'name': unescape(name),
        'validations_percentage': validations_percentage,
        'validations_nb': validations_nb,
        'value': value,
        'difficulty': unescape(difficulty),
        'author': author,
        'solutions_nb': solutions_nb,
        'note': note,
    }


def extract_challenges_info(txt):
    challenge_rows = extract_challenge_rows(txt)

    challs = []
    for row in challenge_rows:
        challs += [extract_info_from_row(row)]

    return challs
