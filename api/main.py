#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import json
import requests as rq
from flask import Flask, redirect
from flask import abort

global url
url = 'https://www.root-me.org/'
app = Flask(__name__)

@app.route("/")
def root():
    paths = ["/", "/username", "/username/profile", "/username/contributions", 
             "/username/score", "/username/ctf", "/username/stats"]
    path_dict = dict()
    for id,path in enumerate(paths): 
        path = dict(id=id, path=path)
        path_dict[id] = path
    send = dict(title="Root-Me-API", author="zTeeed", 
                followme="https://github.com/zteeed",
                paths=path_dict)
    return json.dumps(send, ensure_ascii=False).encode('utf8'), 200

@app.route("/challenges")
def challenges():
    r = rq.get(url+'fr/Challenges/')
    if r.status_code != 200: return r.text, r.status_code
    txt = r.text.replace('\n', '')
    txt = txt.replace('&nbsp;', '')
    pattern = r'<div class="clearfix"></div><span><b>(.*?)</b>.*?</span><p'
    exp = re.findall(pattern, txt)
    if not exp: return '', 500
    challenges_nbs = exp
    pattern = '<li><a class="submenu.*?" href="fr/Challenges/(.*?)/" '
    pattern += 'title="(.*?)"'
    exp = re.findall(pattern, r.text)
    if not exp: return '', 500
    send = dict()
    for key_send, category in enumerate(exp):
        (name, desc) = category
        print(name)
        sub_dict = dict()
        sub_dict['name'] = name
        challenges_nb = challenges_nbs[key_send]
        sub_dict['challenges_nb'] = challenges_nb
        r = rq.get(url + 'fr/Challenges/{}/'.format(name))
        txt = r.text.replace('\n', '')
        txt = txt.replace('&nbsp;', '')
        if r.status_code != 200: return r.text, r.status_code
        pattern = '<img class=\'vmiddle\' alt="" src="(.*?)" .*?/>'
        exp = re.findall(pattern, r.text)
        if not exp: return '', 500
        sub_dict['logo'] = exp[0]
        pattern = '<meta name="Description" content="(.*?)"/>'
        exp = re.findall(pattern, r.text)
        if not exp: return '', 500
        sub_dict['description1'] = exp[0]
        pattern = '<div class="texte crayon rubrique-texte.*?><p>(.*?)</p>'
        exp = re.findall(pattern, r.text)
        if not exp: 
            sub_dict['description2'] = ''
        else:
            sub_dict['description2'] = exp[0]
        send[key_send] = sub_dict
        pattern = '<p>Prérequis\xa0:(.*?)\/p>'
        exp = re.findall(pattern, txt)
        if exp == ['<']:
            pattern = '<p>Prérequis\xa0:(.*?)\/div>'
            exp = re.findall(pattern, txt)
        if not exp: 
            prerequisites = dict()
        else:
            pattern = '><img.*?>\xa0(.*?)<'
            exp = re.findall(pattern, exp[0])
            if not exp: return '', 500
            prerequisites = dict()
            for id, prerequisite in enumerate(exp):
                prerequisite = prerequisite.replace('\xa0', '')
                prerequisites[id] = prerequisite
        sub_dict['prerequisites'] = prerequisites
        challs = dict()
        pattern = '<tr>(.*?)</tr>'
        exp = re.findall(pattern, txt)
        if not exp: return '', 500
        challs = dict()
        for key, chall in enumerate(exp):
            chall_dict = dict()
            pattern = '<td><img.*?><td.*?><a href=\"(.*?)\" title=\"(.*?)\">(.*?)<'
            exp = re.findall(pattern, chall)
            if not exp: return '', 500
            (path, statement, name) = exp[0]
            chall_dict['path'] = path
            chall_dict['statement'] = statement
            chall_dict['name'] = name
            pattern = '<span class="gras left text-left".*?>(.*?)%</span>'
            pattern += '<span class="right"><a.*?>(.*?)</a></span>'
            exp = re.findall(pattern, chall)
            if not exp: return '', 500
            (validations_percentage, validations_nb) = exp[0]
            chall_dict['validations_percentage'] = validations_percentage
            chall_dict['validations_nb'] = validations_nb
            pattern = '<td>(.*?)</td><td class=\".*?\">'
            pattern += '<a href=\".*?\" title=\"(.*?)\">'
            exp = re.findall(pattern, chall)
            if not exp: return '', 500
            for item in exp:
                try:
                    (value, difficulty) = item
                    num = int(value)
                    chall_dict['value'] = value
                    chall_dict['difficulty'] = difficulty.split(':')[0].strip()
                except Exception as exception:
                    pass
            pattern = '<td class="show-for-large-up">(.*?)</td>'
            exp = re.findall(pattern, chall)
            if not exp: 
                chall_dict['author'] = ''
            elif not exp[0]:
                chall_dict['author'] = ''
            else:
                pattern = '<a class=\".*?\"  title=\".*?\" href=\"/(.*?)\?lang=fr\">.*?</a>' 
                exp = re.findall(pattern, exp[0])
                if not exp: return '', 500
                chall_dict['author'] = exp[0]
            pattern = '</td><td><img src="squelettes/img/note/note(\d+).png"' 
            pattern +=' .*?></td><td class=".*?">(\d+)</td>'
            exp = re.findall(pattern, chall)
            if not exp: return '', 500
            (note, solutions_nb) = exp[0]
            chall_dict['note'] = note
            chall_dict['solutions_nb'] = solutions_nb
            challs[key] = chall_dict
        print(sub_dict)
        sub_dict['challenges'] = challs
        print(key_send)
        print()
        send[key_send] = sub_dict
    return json.dumps(send, ensure_ascii=False).encode('utf8'), 200

@app.route("/<username>")
def get_user(username):
    return redirect('/{}/profile'.format(username), code=302)

@app.route('/<username>/profile')
def get_profile(username):
    r = rq.get(url+username)
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
    r = rq.get(url+username+'?inc=contributions')
    if r.status_code != 200: return r.text, r.status_code
    pattern = '<meta name="author" content="(.*?)"/>'
    exp = re.findall(pattern, r.text)
    if not exp: return '', 500
    pseudo = exp[0]
    pattern = '<a class="gris" href="(.*?)">(.*?)</a>\n'
    pattern+= '<a href="(.*?)">(.*?)</a>\n'
    pattern+= '<span class="txs gris italic">(.*?)</span>'
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
    r = rq.get(url+username+'?inc=score')
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

    for id,item in enumerate(exp):
        (sub_id, path, name) = item
        if id in list(range(2,13)): 
            category = dict(id=id-2, path=path, name=name)
            categories[id-2] = category

    """ get score by categories """
    pattern = '<span class="gris">(\d+)Points(\d+)/(\d+)</span>'
    pattern += '<ul(.*?)>(.*?)</ul>'
    exp = re.findall(pattern, txt)
    if not exp: return '', 500
    score_categories = categories
    for id,item in enumerate(exp):
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
    offset = 0; stop = False
    while not stop:
        r = rq.get(url+username+'?inc=ctf&debut_ctf_alltheday_vm_dispo={}'.format(offset))
        if r.status_code != 200: return r.text, r.status_code
        txt = r.text.replace('\n', '')
        txt = txt.replace('&nbsp;', '')
        pattern = "<li><a href='.*?inc=ctf.*?class='lien_pagination gris' rel='nofollow'>(.*?)</a></li>"
        exp = re.findall(pattern, txt)
        if not exp: return '', 500
        stop = (exp[-1]=='<')
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
        CTFS = dict(); key=0
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
            key+=1
        offset += 50 
    send = dict(pseudo=pseudo, description=description, num_success=num_success,
                num_try=num_try, CTFS=CTFS)
    return json.dumps(send, ensure_ascii=False).encode('utf8'), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
