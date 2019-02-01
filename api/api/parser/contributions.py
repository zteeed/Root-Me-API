import re
from html import unescape

from api.parser.exceptions import RootMeParsingError


def extract_contributions(txt):
    pattern = '<a class="gris" href="(.*?)">(.*?)</a>\n'
    pattern += '<a href="(.*?)">(.*?)</a>\n'
    pattern += '<span class="txs gris italic">(.*?)</span>'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse contributions data about a user.")
    contributions = []
    for item in result:
        (path, name, path_solve, solve, date) = item
        name = name.replace('\t', '')[1:-1]
        contribution = {
            'path': path,
            'name': unescape(name),
            'path_solve': path_solve,
            'solve': unescape(solve),
            'date': unescape(date),
        }
        contributions.append(contribution)
    return contributions
