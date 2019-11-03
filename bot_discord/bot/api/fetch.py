from bot.colors import red
from bot.api.parser import Parser


async def user_rootme_exists(parser: Parser, user: str):
    return await parser.extract_rootme_profile(user) is not None


async def get_scores(parser: Parser, users):
    scores = [await parser.extract_score(user) for user in users]
    scores = [int(score) for score in scores]
    """ Sort users by score desc """
    return [{'name': x, 'score': int(y)} for y, x in sorted(zip(scores, users), reverse=True)]


async def get_categories(parser: Parser):
    categories = await parser.extract_categories()
    result = []
    for category in categories:
        result.append(category[0])
    return result


async def get_categories_light(parser: Parser):
    categories = await parser.extract_categories()
    result = []
    for category in categories:
        c = category[0]
        result.append({'name': c['name'], 'challenges_nb': c['challenges_nb']})
    return result


async def get_category(parser: Parser, category_selected):
    categories = await parser.extract_categories()
    for category in categories:
        if category[0]['name'] == category_selected:
            return category
    return None


async def get_solved_challenges(parser: Parser, user):
    solved_challenges_data = await parser.extract_rootme_stats(user)
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
