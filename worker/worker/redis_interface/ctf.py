import json

from worker.constants import URL
from worker.parser.ctf import extract_summary, extract_ctf
from worker.parser.profile import extract_pseudo
from worker.redis_interface import session, redis_app
from worker.redis_interface.exceptions import RootMeException


def extract_ctf_page_data(username, offset):
    pattern_url = f'{URL}{username}?inc=ctf&debut_ctf_alltheday_vm_dispo={offset}'
    r = session.get(pattern_url)
    if r.status_code != 200:
        raise RootMeException(r.status_code)
    txt = r.text.replace('\n', '')
    txt = txt.replace('&nbsp;', '')
    return txt


def set_user_ctf(username):
    offset = 0
    is_last_page = False
    ctfs = []

    ctf_page_data = extract_ctf_page_data(username, offset)
    pseudo = extract_pseudo(ctf_page_data)
    num_success, num_try = extract_summary(ctf_page_data)
    if num_success is None and num_try is None:
        return None

    description = f'{num_success} machine(s) compromise(s) en {num_try} tentatives'
    while not is_last_page:
        offset += 50
        ctfs, is_last_page = extract_ctf(ctf_page_data, ctfs)
        ctf_page_data = extract_ctf_page_data(username, offset)

    response = [{
        'pseudo': pseudo,
        'num_success': num_success,
        'num_try': num_try,
        'description': description,
        'ctfs': ctfs,
    }]

    redis_app.set(f'{username}.ctfs', json.dumps(response))
