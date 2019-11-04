from typing import Dict, List, Tuple, Optional

from bot.api.parser import Parser
from bot.colors import red


async def user_rootme_exists(user: str, lang: str):
    return await Parser.extract_rootme_profile(user, lang) is not None


async def get_scores(users: List[str], lang: str):
    scores = [await Parser.extract_score(user, lang) for user in users]
    scores = [int(score) for score in scores]
    """ Sort users by score desc """
    return [{'name': x, 'score': int(y)} for y, x in sorted(zip(scores, users), reverse=True)]


async def get_details(username: str, lang: str):
    return await Parser.extract_rootme_details(username, lang)


def get_stats_category(categories_stats: List[Dict], category: str) -> Optional[Dict[str, int]]:
    for category_stats in categories_stats:
        category_name = category_stats['name'].replace(' ', '')
        if category_name == category:
            return category_stats['stats_categories']


async def get_remain(username: str, lang: str, category: Optional[str] = None) -> Tuple[int, int]:
    details = await get_details(username, lang)
    details = details[0]
    if category is None:
        return details['nb_challenges_solved'], details['nb_challenges_tot']
    else:
        category_stats = get_stats_category(details['categories'], category)
        return category_stats['num_challenges_solved'], category_stats['total_challenges_category']


async def get_categories(lang: str):
    categories = await Parser.extract_categories(lang)
    result = []
    for category in categories:
        result.append(category[0])
    return result


async def get_categories_light(lang: str):
    categories = await Parser.extract_categories(lang)
    result = []
    for category in categories:
        c = category[0]
        result.append({'name': c['name'], 'challenges_nb': c['challenges_nb']})
    return result


async def get_category(category_selected: str, lang: str):
    categories = await Parser.extract_categories(lang)
    for category in categories:
        if category[0]['name'] == category_selected:
            return category
    return None


async def get_solved_challenges(user: str, lang: str):
    solved_challenges_data = await Parser.extract_rootme_stats(user, lang)
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
