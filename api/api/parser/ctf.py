import re
from html import unescape
import time

from api.parser.exceptions import RootMeParsingError


def extract_summary(txt):
    pattern = '<span class=\"color1 txl\".*?>(\d+).*?(\d+).*?<\/span>'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse ctf summary data about a user.")
    (num_success, num_try) = result[0]
    description = '{} machine(s) compromise(s) en {} tentatives'.format(num_success, num_try)
    return num_success, num_try, description


def extract_ctf(txt, CTFs=[]):
    pattern = "<li><a href='.*?inc=ctf.*?class='lien_pagination gris' rel='nofollow'>(.*?)</a></li>"
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse number pages of ctf data about a user.")
    stop = (result[-1] == '&lt;')

    pattern = '<tr class="row_first gras">(.*?)</tr>'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse ctf data about a user.")

    pattern = '<td.*?>(.*?)</td>'
    columns = re.findall(pattern, result[0])
    if not columns:
        raise RootMeParsingError("Could not parse ctf data about a user.")

    pattern = '<tr class="row_(odd|even)">(.*?)</tr>'
    ctfs = re.findall(pattern, txt)
    pattern = "<td><img src=.*?/img/(.*?).png.*?></td>"
    for i in range(4): pattern += "<td.*?>(.*?)</td>"
    pattern = pattern.replace('/', '\\/')

    for id, ctf in enumerate(ctfs):
        (class_txt, ctf_data) = ctf
        exp = re.findall(pattern, ctf_data)
        if not exp:
            raise RootMeParsingError("Could not parse ctf data about a user.")
        (validated, name, num_success, num_try, solve_duration) = exp[0]
        CTF = {
            'validated': validated,
            'name': name,
            'num_success': num_success,
            'num_try': num_try,
            'solve_duration': solve_duration,
        }
        CTFs.append(CTF)

    return CTFs, stop
