import requests as rq

from api.constants import URL
from api.http_interface.exceptions import RootMeException
from api.parser.profile import extract_pseudo
from api.parser.ctf import extract_summary, extract_ctf


def get_user_ctf(username):
    offset = 0; stop = False; CTFs = []
    while not stop:
        r = rq.get(URL + username + '?inc=ctf&debut_ctf_alltheday_vm_dispo={}'.format(offset))
        if r.status_code != 200:
            raise RootMeException(r.status_code)

        txt = r.text.replace('\n', '')
        txt = txt.replace('&nbsp;', '')

        if offset == 0:
            pseudo = extract_pseudo(txt)
            num_success, num_try, description = extract_summary(txt)

        CTFs, stop = extract_ctf(txt, CTFs=CTFs)
        offset += 50

    return [{
        'pseudo': pseudo,
        'num_success': num_success,
        'num_try': num_try,
        'description': description,
        'CTFs': CTFs,
    }]
