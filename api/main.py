#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import redirect, jsonify

from api.app import app
from api.constants import AUTHORS, GITHUB_ACCOUNTS
from api.http_interface.challenges import get_all_challenges
from api.http_interface.contributions import get_user_contributions
from api.http_interface.ctf import get_user_ctf
from api.http_interface.details import get_user_details
from api.http_interface.profile import get_user_profile
from api.http_interface.stats import get_user_stats


@app.route("/")
def root():
    return redirect('/v1', code=302)


@app.route("/v1")
def rootv1():
    return jsonify(title="Root-Me-API",
                   authors=AUTHORS,
                   follow_us=GITHUB_ACCOUNTS)


@app.route("/v1/challenges")
def challenges():
    return jsonify(get_all_challenges())


@app.route("/v1/<username>")
def get_user(username):
    return redirect('/v1/{}/profile'.format(username), code=302)


@app.route('/v1/<username>/profile')
def get_profile(username):
    return jsonify(get_user_profile(username))


@app.route('/v1/<username>/contributions')
def get_contributions(username):
    return jsonify(get_user_contributions(username))


@app.route('/v1/<username>/details')
def get_score(username):
    return jsonify(get_user_details(username))


@app.route('/v1/<username>/ctf')
def get_ctf(username):
    return jsonify(get_user_ctf(username))


@app.route('/v1/<username>/stats')
def get_stats(username):
    return jsonify(get_user_stats(username))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
