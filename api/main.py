#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import re
from logging.config import dictConfig

import requests as rq
from flask import Flask, redirect, jsonify

from parser.category import extract_categories, extract_category_logo, extract_category_description, \
    extract_category_prereq, extract_challenges_info
from parser.exceptions import RootMeParsingError

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
app = Flask(__name__)
URL = 'https://www.root-me.org/'
ENDPOINTS = ["/", "/username", "/username/profile", "/username/contributions",
             "/username/score", "/username/ctf", "/username/stats"]


class RootMeException(BaseException):
    def __init__(self, error):
        self.err_code = error


@app.route("/")
def root():
    return jsonify(title="Root-Me-API",
                   author="zTeeed",
                   followme="https://github.com/zteeed",
                   paths=ENDPOINTS)


def retrieve_category_info(category):
    r = rq.get(URL + 'fr/Challenges/{}/'.format(category))
    if r.status_code != 200:
        raise RootMeException(r.status_code)

    logo = extract_category_logo(r.text)
    desc1, desc2 = extract_category_description(r.text)
    prereq = extract_category_prereq(r.text)
    challenges = extract_challenges_info(r.text)

    return [{
        'name': category,
        'logo': logo,
        'description1': desc1,
        'description2': desc2,
        'prerequisites': prereq,
        'challenges': challenges,
        'challenges_nb': len(challenges),
    }]


@app.route("/challenges")
def challenges():
    try:
        r = rq.get(URL + 'fr/Challenges/')
        if r.status_code != 200:
            raise RootMeException(r.status_code)

        categories = extract_categories(r.text)

        response = []
        for category in categories:
            response += retrieve_category_info(category)
            app.logger.info('Fetched category page "{}"'.format(category))

        return jsonify(response)

    except RootMeException as e:
        app.logger.exception("Root-me did not respond 200")
        return "RootMe responded {}".format(e.err_code), 502

    except RootMeParsingError:
        app.logger.exception("Parsing error")
        raise


@app.route("/<username>")
def get_user(username):
    return redirect('/{}/profile'.format(username), code=302)


@app.route('/<username>/profile')
def get_profile(username):
    r = rq.get(URL + username)
    if r.status_code != 200: return r.text, r.status_code
    pattern = '<meta name="author" content="(.*?)"/>'
    pseudo = re.findall(pattern, r.text)
    pattern = '<span>(\d+)</span>'
    score = re.findall(pattern, r.text)
    if not pseudo or not score: return '', 500
    send = dict(pseudo=pseudo[0], score=score[0])
    return json.dumps(send, ensure_ascii=False).encode('utf8'), 200


@app.route('/<username>/contributions')
def get_contributions(username):
    r = rq.get(URL + username + '?inc=contributions')
    if r.status_code != 200: return r.text, r.status_code
    pattern = '<meta name="author" content="(.*?)"/>'
    exp = re.findall(pattern, r.text)
    if not exp: return '', 500
    pseudo = exp[0]
    pattern = '<a class="gris" href="(.*?)">(.*?)</a>\n'
    pattern += '<a href="(.*?)">(.*?)</a>\n'
    pattern += '<span class="txs gris italic">(.*?)</span>'
    exp = re.findall(pattern, r.text)
    if not exp: return '', 500
    contrib = dict()
    send = dict(pseudo=pseudo, contrib=contrib)
    tags = ['path', 'name', 'path_solve', 'solve', 'date']
    for key, item in enumerate(exp):
        solve = dict()
        for tag, data in enumerate(item):
            solve[tags[tag]] = data
        contrib[key] = solve
    return json.dumps(send, ensure_ascii=False).encode('utf8'), 200


@app.route('/<username>/score')
def get_score(username):
    r = rq.get(URL + username + '?inc=score')
    if r.status_code != 200: return 'HTTP Error Code: {}'.format(r.status_code), r.status_code
    txt = r.text.replace('\n', '')
    txt = txt.replace('&nbsp;', '')

    pattern = '<meta name="author" content="(.*?)"/>'
    exp = re.findall(pattern, r.text)
    if not exp: return '', 500
    pseudo = exp[0]

    """ get solved challenge number """
    pattern = '<span class="color1 tl">(\d+)Points<span class="gris tm">(\d+)/(\d+)</span>'
    exp = re.findall(pattern, txt)
    if not exp: return '', 500
    (score_user, nb_solved, nb_tot) = exp[0]

    """ get ranking over all users """
    pattern = '<span class="color1 tl">(\d+)<span class="gris">/(\d+)</span>'
    exp = re.findall(pattern, txt)
    if not exp: return '', 500
    (ranking, ranking_tot) = exp[0]

    """ get rank """
    pattern = '<span class="color1 tl">(\w+)<a'
    exp = re.findall(pattern, txt)
    if not exp: return '', 500
    rank = exp[0]

    """ get categories names """
    pattern = '<li><a class="submenu(\d+)" href="(.*?)".*?>(.*?)</a></li>'
    exp = re.findall(pattern, txt)
    if not exp: return '', 500
    categories = dict()

    for id, item in enumerate(exp):
        (sub_id, path, name) = item
        if id in list(range(2, 13)):
            category = dict(id=id - 2, path=path, name=name)
            categories[id - 2] = category

    """ get score by categories """
    pattern = '<span class="gris">(\d+)Points(\d+)/(\d+)</span>'
    pattern += '<ul(.*?)>(.*?)</ul>'
    exp = re.findall(pattern, txt)
    if not exp: return '', 500
    score_categories = categories
    for id, item in enumerate(exp):
        (score, num, tot, trash, challenges_list) = item
        category = score_categories[id]
        score_category = dict(score=score, num_solved=num, total=tot)
        category['score catégorie'] = score_category
        challenges = dict()
        category['challenges'] = challenges
        pattern_c = '<li><a class="(.*?)" href="(.*?)" title="(\d+) Points">(.*?)</a></li>'
        exp = re.findall(pattern_c, challenges_list)
        for id_c, challenge_data in enumerate(exp):
            (class_value, path, score_value, name) = challenge_data
            name = name.strip()[1:]
            solved = (class_value == 'vert')
            challenge = dict(name=name, score_value=score_value,
                             path=path, solved=solved)
            challenges[id_c] = challenge

    send = dict(pseudo=pseudo, score=score_user, nb_solved=nb_solved, nb_tot=nb_tot,
                ranking=ranking, ranking_tot=ranking_tot, rank=rank,
                categories=categories)
    return json.dumps(send, ensure_ascii=False).encode('utf8'), 200


@app.route('/<username>/ctf')
def get_ctf(username):
    offset = 0;
    stop = False
    while not stop:
        r = rq.get(URL + username + '?inc=ctf&debut_ctf_alltheday_vm_dispo={}'.format(offset))
        if r.status_code != 200: return r.text, r.status_code
        txt = r.text.replace('\n', '')
        txt = txt.replace('&nbsp;', '')
        pattern = "<li><a href='.*?inc=ctf.*?class='lien_pagination gris' rel='nofollow'>(.*?)</a></li>"
        exp = re.findall(pattern, txt)
        if not exp: return '', 500
        stop = (exp[-1] == '<')
        if offset == 0:
            pattern = '<meta name="author" content="(.*?)"/>'
            exp = re.findall(pattern, txt)
            if not exp: return '', 500
            pseudo = exp[0]
            pattern = '<span class=\"color1 txl\".*?>(\d+).*?(\d+).*?<\/span>'
            exp = re.findall(pattern, txt)
            if not exp: return '', 500
            (num_success, num_try) = exp[0]
            description = '{} machine(s) compromise(s) en {} tentatives'.format(num_success, num_try)
        """ extract table solve ctf """
        pattern = '<tr class="row_first gras">(.*?)</tr>'
        exp = re.findall(pattern, txt)
        if not exp: return '', 500
        pattern = '<td.*?>(.*?)</td>'
        columns = re.findall(pattern, exp[0])
        if not columns: return '', 500
        CTFS = dict();
        key = 0
        pattern = '<tr class="row_(odd|even)">(.*?)</tr>'
        ctfs = re.findall(pattern, txt)
        pattern = "<td><img src=.*?/img/(.*?).png.*?></td>"
        for i in range(4): pattern += "<td.*?>(.*?)</td>"
        pattern = pattern.replace('/', '\\/')
        for id, ctf in enumerate(ctfs):
            (class_txt, ctf_data) = ctf
            exp = re.findall(pattern, ctf_data)
            if not exp: return '', 500
            extracted_data = exp[0]
            X = dict()
            for id, item in enumerate(extracted_data):
                X[columns[id]] = item
            CTFS[str(key)] = X
            key += 1
        offset += 50
    send = dict(pseudo=pseudo, description=description, num_success=num_success,
                num_try=num_try, CTFS=CTFS)
    return json.dumps(send, ensure_ascii=False).encode('utf8'), 200


@app.route('/<username>/stats')
def get_stats(username):
    r = rq.get(URL + username + '?inc=statistiques')
    if r.status_code != 200: return r.text, r.status_code
    txt = r.text.replace('\n', '')
    txt = txt.replace('&nbsp;', '')
    pattern = '<meta name="author" content="(.*?)"/>'
    exp = re.findall(pattern, txt)
    if not exp: return '', 500
    pseudo = exp[0]

    """ Evolution du Score """
    pattern = '<script type="text/javascript">(.*?)</script>'
    exp = re.findall(pattern, txt)
    exp = ''.join(exp)
    pattern = 'evolution_data_total.push\(new Array\("(.*?)",(\d+), "(.*?)", "(.*?)"\)\)'
    pattern += 'validation_totale\[(\d+)\]\+\=1;'
    challenges_solved = re.findall(pattern, exp)
    challenges = dict()
    for id, challenge_solved in enumerate(challenges_solved):
        challenge = dict()
        (date, score, name, path, difficulty) = challenge_solved
        challenge = dict(name=name, score=score, path=path,
                         difficulty=difficulty, date=date)
        challenges[id] = challenge
    send = dict(pseudo=pseudo, challenges=challenges)
    return json.dumps(send, ensure_ascii=False).encode('utf8'), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
