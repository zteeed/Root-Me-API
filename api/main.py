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


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
