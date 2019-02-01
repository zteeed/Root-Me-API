import requests as rq

from api.constants import URL
from api.http_interface.exceptions import RootMeException
from api.parser.profile import extract_pseudo
from api.parser.ctf import extract_summary, extract_ctf


def extract_ctf_page_data(username, offset):
    pattern_url = URL + '{}?inc=ctf&debut_ctf_alltheday_vm_dispo={}'
    r = rq.get(pattern_url.format(username, offset))
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
    description_pattern = '{} machine(s) compromise(s) en {} tentatives'
    description = description_pattern.format(num_success, num_try)

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
