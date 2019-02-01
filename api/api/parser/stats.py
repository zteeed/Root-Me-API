import re
from html import unescape

from api.parser.exceptions import RootMeParsingError


def extract_stats(txt):
    """ Evolution du Score """
    pattern = '<script type="text/javascript">(.*?)</script>'
    stats_data = re.findall(pattern, txt)
    if not stats_data:
        raise RootMeParsingError("Could not parse stats data about a user.")

    stats_data = ''.join(stats_data)
    pattern = ('evolution_data_total.push\(new Array\("(.*?)",(\d+), "(.*?)", "(.*?)"\)\)'
               'validation_totale\[(\d+)\]\+\=1;')
    challenges_solved = re.findall(pattern, result)
    result = []

    for challenge_solved in challenges_solved:
        date, score_at_date, name, path, difficulty = challenge_solved
        challenge = {
            'name': unescape(name),
            'score_at_date': score_at_date,
            'date': date,
            'path': path,
            'difficulty': difficulty,
        }
        result.append(challenge)

    return result
