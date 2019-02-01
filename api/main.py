#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import math
import re

import requests as rq
from flask import redirect, jsonify

from api import repeater
from api.app import app
from api.cache_wrapper import cached
from api.constants import REFRESH_CACHE_INTERVAL, AUTHORS, ENDPOINTS, GITHUB_ACCOUNTS
from api.http_interface.challenges import get_all_challenges
from api.http_interface.profile import get_user_profile
from api.http_interface.contributions import get_user_contributions
from api.http_interface.details import get_user_details
from api.http_interface.ctf import get_user_ctf
from api.http_interface.stats import get_user_stats


@app.route("/")
@cached(timeout=math.inf)  # Never timeout, this is static.
def root():
    return jsonify(title="Root-Me-API",
                   authors=AUTHORS,
                   follow_us=GITHUB_ACCOUNTS,
                   paths=ENDPOINTS)


@app.route("/challenges")
def challenges():
    return jsonify(get_all_challenges_cached())


@app.route("/<username>")
def get_user(username):
    return redirect('/{}/profile'.format(username), code=302)


@cached(timeout = 10)
@app.route('/<username>/profile')
def get_profile(username):
    return jsonify(get_user_profile(username))


@cached(timeout = 10)
@app.route('/<username>/contributions')
def get_contributions(username):
    return jsonify(get_user_contributions(username))


@cached(timeout = 10)
@app.route('/<username>/details')
def get_score(username):
    return jsonify(get_user_details(username))


@cached(timeout = 10)
@app.route('/<username>/ctf')
def get_ctf(username):
    return jsonify(get_user_ctf(username))


@cached(timeout = 10)
@app.route('/<username>/stats')
def get_stats(username):
    return jsonify(get_user_stats(username))


@cached(key_prefix="challenges")
def get_all_challenges_cached():
    return get_all_challenges()


def update_endpoints():
    get_all_challenges_cached(cache_refresh=True)
    app.logger.info("/challenges cache updated")


if __name__ == "__main__":
    repeater.start(update_endpoints, REFRESH_CACHE_INTERVAL)
    app.run(host='0.0.0.0', debug=True, use_reloader=False)
    repeater.stop()
