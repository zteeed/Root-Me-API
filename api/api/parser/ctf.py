import re

from api.parser.exceptions import RootMeParsingError


def extract_summary(txt):
    pattern = '<span class=\"color1 txl\".*?>(\d+).*?(\d+).*?<\/span>'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse ctf summary data about a user.")
    num_success, num_try = result[0]
    return num_success, num_try


def check_isLastPage(ctfPages):
    return ctfPages[-1] == '&lt;'


def extract_ctf(txt, ctfs):
    pattern = "<li><a href='.*?inc=ctf.*?class='lien_pagination gris' rel='nofollow'>(.*?)</a></li>"
    ctfPages = re.findall(pattern, txt)
    if not ctfPages:
        raise RootMeParsingError("Could not parse number pages of ctf data about a user.")
    isLastPage = check_isLastPage(ctfPages)

    pattern = '<tr class="row_(odd|even)">(.*?)</tr>'
    ctfs_data = re.findall(pattern, txt)

    pattern = "<td><img src=.*?/img/(.*?).png.*?></td>"
    for i in range(4): 
        pattern += "<td.*?>(.*?)</td>"
    pattern = pattern.replace('/', '\\/')

    for id, ctf_data in enumerate(ctfs_data):
        class_txt, ctf_info = ctf_data
        challenge_info = re.findall(pattern, ctf_info)

        if not challenge_info:
            raise RootMeParsingError("Could not parse ctf data about a user.")

        validated, name, num_success, num_try, solve_duration = challenge_info[0]
        ctf = {
            'validated': validated,
            'name': name,
            'num_success': num_success,
            'num_try': num_try,
            'solve_duration': solve_duration,
        }
        ctfs.append(ctf)

    return ctfs, isLastPage
