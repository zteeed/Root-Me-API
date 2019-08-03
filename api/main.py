from flask import redirect, jsonify
import json

from api.app import app, redis_app
from api.constants import AUTHORS, GITHUB_ACCOUNTS


version = 'v2'


@app.route("/")
def root():
    return redirect(f'/{version}', code=302)


@app.route(f'/{version}')
def root_v1():
    return jsonify(title="Root-Me-API", authors=AUTHORS, follow_us=GITHUB_ACCOUNTS)


@app.route(f'/{version}/categories')
def categories():
    result = redis_app.get('categories')
    return jsonify(json.loads(result))


@app.route(f'/{version}/category/<string:category>')
def category_data(category):
    result = redis_app.get(f'categories.{category}')
    return jsonify(json.loads(result))


@app.route(f'/{version}/challenges')
def challenges():
    result = redis_app.get(f'challenges')
    return jsonify(json.loads(result))


@app.route(f'/{version}/<string:username>')
def get_user(username):
    return redirect(f'/{version}/{username}/profile', code=302)


@app.route(f'/{version}/<string:username>/profile')
def get_profile(username):
    result = redis_app.get(f'{username}.profile')
    return jsonify(json.loads(result))


@app.route(f'/{version}/<string:username>/contributions')
def get_contributions(username):
    result = redis_app.get(f'{username}.contributions')
    return jsonify(json.loads(result))


@app.route(f'/{version}/<string:username>/contributions/challenges')
def get_contributions_challenges(username):
    result = redis_app.get(f'{username}.contributions.challenges')
    return jsonify(json.loads(result))


@app.route(f'/{version}/<string:username>/contributions/solutions')
def get_contributions_solutions(username):
    result = redis_app.get(f'{username}.contributions.solutions')
    return jsonify(json.loads(result))


@app.route(f'/{version}/<string:username>/details')
def get_details(username):
    result = redis_app.get(f'{username}.details')
    return jsonify(json.loads(result))


@app.route(f'/{version}/<string:username>/ctf')
def get_ctf(username):
    result = redis_app.get(f'{username}.ctfs')
    return jsonify(json.loads(result))


@app.route(f'/{version}/<string:username>/stats')
def get_stats(username):
    result = redis_app.get(f'{username}.stats')
    return jsonify(json.loads(result))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
