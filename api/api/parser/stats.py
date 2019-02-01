import re
from html import unescape

from api.parser.exceptions import RootMeParsingError


def extract_stats(txt):
    """ Evolution du Score """
    pattern = '<script type="text/javascript">(.*?)</script>'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse stats data about a user.")
    result = ''.join(result)
    pattern = 'evolution_data_total.push\(new Array\("(.*?)",(\d+), "(.*?)", "(.*?)"\)\)'
    pattern += 'validation_totale\[(\d+)\]\+\=1;'
    challenges_solved = re.findall(pattern, result)

    result = []
    for id, challenge_solved in enumerate(challenges_solved):
        (date, score_at_date, name, path, difficulty) = challenge_solved
        challenge = {
            'name': unescape(name),
            'score_at_date': score_at_date,
            'date': date,
            'path': path,
            'difficulty': difficulty,
        }
        result.append(challenge)
    return result
