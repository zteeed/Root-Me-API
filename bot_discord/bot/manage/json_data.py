import json
from bot.parser.api.extract_all import extract_default, \
extract_rootme_profile


def read_json():
    with open("data.json", "r") as json_file:
        extract = json_file
        data = json.load(extract)
        return data


def update_json(data):
    with open("data.json", "w") as json_file:
        json.dump(data, json_file)


def default():
    return extract_default()


def is_first():
    data = read_json()
    return data['info']['first']


def update_first_time(boolean):
    data = read_json()
    data['info']['first'] = boolean
    update_json(data)


def launched():
    update_first_time(False)


def user_rootme_exists(user):
    return extract_rootme_profile(user) is not None


def user_json_exists(user_check):
    data = read_json()
    return (True in [ user['name'] == user_check for user in data['team'] ])


def create_user(user):
    data = read_json()
    solved_challenges = extract_rootme_stats(user)['solved_challenges']
    if not solved_challenges:
        last = '?????'
    else:
        last = solved_challenges[-1]['name']
    data['team'].append({'name': user, 'last_solved': last})
    update_json(data)


def update_user_last(user, challenge_name):
    data = read_json()
    for u in data['team']:
        if u['name'] == user:
            u['last_solved'] = challenge_name
    update_json(data)
    return


def delete_user(user):
    data = read_json()
    data['team'].remove([ d for d in data['team'] if d['name'] == user ][0])
    update_json(data)


def select_users():
    return [ d['name'] for d in read_json()['team'] ]


def last_solved(user):
    data = read_json()
    return [ d['last_solved'] for d in data['team'] if d['name'] == user ][0]


