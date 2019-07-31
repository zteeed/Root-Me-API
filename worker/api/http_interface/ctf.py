from api.constants import URL
from api.http_interface import session
from api.http_interface.exceptions import RootMeException
from api.parser.ctf import extract_summary, extract_ctf
from api.parser.profile import extract_pseudo


def extract_ctf_page_data(username, offset):
    pattern_url = f'{URL}{username}?inc=ctf&debut_ctf_alltheday_vm_dispo={offset}'
    r = session.get(pattern_url)
    if r.status_code != 200:
        raise RootMeException(r.status_code)
    txt = r.text.replace('\n', '')
    txt = txt.replace('&nbsp;', '')
    return txt


def get_user_ctf(username):
    offset = 0
    is_last_page = False
    ctfs = []

    ctf_page_data = extract_ctf_page_data(username, offset)
    pseudo = extract_pseudo(ctf_page_data)
    num_success, num_try = extract_summary(ctf_page_data)
    description = f'{num_success} machine(s) compromise(s) en {num_try} tentatives'

    while not is_last_page:
        offset += 50
        ctfs, is_last_page = extract_ctf(ctf_page_data, ctfs)
        ctf_page_data = extract_ctf_page_data(username, offset)

    return [{
        'pseudo': pseudo,
        'num_success': num_success,
        'num_try': num_try,
        'description': description,
        'ctfs': ctfs,
    }]
