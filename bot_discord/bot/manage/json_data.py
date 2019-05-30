import json
from bot.parser.api.extract_all import extract_rootme_profile, \
extract_rootme_stats, extract_score, extract_categories
from bot.colors import red


def read_json():
    with open("data.json", "r") as json_file:
        extract = json_file
        data = json.load(extract)
        return data


def update_json(data):
    with open("data.json", "w") as json_file:
        json.dump(data, json_file)


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


def get_scores(users):
    scores = []
    data = read_json()
    for user in data['team']:
        scores.append(int(extract_score(user['name'])))
    """ Sort users by score desc """
    return [ {'name': x, 'score': int(y) } for y, x in sorted(zip(scores,users), 
                                                    reverse=True) ]


def get_categories():
    categories = extract_categories() 
    result = [] 
    for category in categories:
        result.append(category[0])
    return result


def get_categories_light():
    categories = extract_categories() 
    result = [] 
    for category in categories:
        c = category[0]
        result.append({'name': c['name'], 'challenges_nb': c['challenges_nb']})
    return result


def get_category(category_selected):
    categories = extract_categories() 
    result = [] 
    for category in categories:
        if category[0]['name'] == category_selected:
            return category
    return None


def get_solved_challenges(user):
    solved_challenges_data = extract_rootme_stats(user)
    if solved_challenges_data is None:
        red('user {} name might have changed in rootme profile link'.format(user))
        return None
    return solved_challenges_data['solved_challenges']


def get_diff(solved_user1, solved_user2):
    test1 = [ c['name'] for c in solved_user1 ]
    test2 = [ c['name'] for c in solved_user2 ]
    user1_diff = [ c for c in solved_user1 if c['name'] not in test2 ]
    user2_diff = [ c for c in solved_user2 if c['name'] not in test1 ]
    user1_diff.reverse()
    user2_diff.reverse()
    return user1_diff, user2_diff
