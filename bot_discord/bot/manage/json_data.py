import json
from typing import Any, Dict

from bot.colors import red
from bot.parser.api.extract_all import extract_rootme_profile, extract_rootme_stats, extract_score, extract_categories


def read_json() -> Dict[str, Any]:
    with open("data.json", "r") as json_file:
        extract = json_file
        data = json.load(extract)
        return data


def update_json(data: Any) -> None:
    with open("data.json", "w") as json_file:
        json.dump(data, json_file)


async def user_rootme_exists(user: str):
    return await extract_rootme_profile(user) is not None


def user_json_exists(user_check):
    data = read_json()
    return True in [user['name'] == user_check for user in data['team']]


async def create_user(user):
    data = read_json()
    rootme_stats = await extract_rootme_stats(user)
    solved_challenges = rootme_stats['solved_challenges']
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
    data['team'].remove([d for d in data['team'] if d['name'] == user][0])
    update_json(data)


def select_users():
    return [d['name'] for d in read_json()['team']]


def last_solved(user):
    data = read_json()
    return [d['last_solved'] for d in data['team'] if d['name'] == user][0]


async def get_scores(users):
    scores = [await extract_score(user) for user in users]
    scores = [int(score) for score in scores]
    """ Sort users by score desc """
    return [{'name': x, 'score': int(y)} for y, x in sorted(zip(scores, users), reverse=True)]


async def get_categories():
    categories = await extract_categories()
    result = []
    for category in categories:
        result.append(category[0])
    return result


async def get_categories_light():
    categories = await extract_categories()
    result = []
    for category in categories:
        c = category[0]
        result.append({'name': c['name'], 'challenges_nb': c['challenges_nb']})
    return result


async def get_category(category_selected):
    categories = await extract_categories()
    for category in categories:
        if category[0]['name'] == category_selected:
            return category
    return None


async def get_solved_challenges(user):
    solved_challenges_data = await extract_rootme_stats(user)
    if solved_challenges_data is None:
        red(f'user {user} name might have changed in rootme profile link')
        return None
    return solved_challenges_data['solved_challenges']


def get_diff(solved_user1, solved_user2):
    if solved_user1 == solved_user2:
        return None, None
    test1 = list(map(lambda x: x['name'], solved_user1))
    test2 = list(map(lambda x: x['name'], solved_user2))
    user1_diff = list(filter(lambda x: x['name'] not in test2, solved_user1))[::-1]
    user2_diff = list(filter(lambda x: x['name'] not in test1, solved_user2))[::-1]
    return user1_diff, user2_diff
