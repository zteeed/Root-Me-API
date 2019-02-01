import re

from api.parser.exceptions import RootMeParsingError


def extract_score(txt):
    pattern = '<span class="color1 tl">(\d+)Points<span class="gris tm">(\d+)/(\d+)</span>'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse score.")
    [score, nb_challenges_solved, nb_challenges_tot] = result[0]
    return score


def extract_ranking(txt):
    pattern = '<span class="color1 tl">(\d+)<span class="gris">/(\d+)</span>'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse ranking informations.")
    (ranking, ranking_tot) = result[0]
    return ranking, ranking_tot


def extract_ranking_category(txt):
    pattern = '<span class="color1 tl">(\w+)<a'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse ranking category.")
    return result[0]


def extract_challenges(txt):
    pattern = '<li><a class="submenu.*?" href="(.*?)".*?>(.*?)</a></li>'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse categories.")
    categories = []
    for key1, item in enumerate(result[2:]):
        (path, name) = item
        """ get score by categories """
        pattern = '<span class="gris">(\d+)Points(\d+)/(\d+)</span><ul(.*?)>(.*?)</ul>'
        result = re.findall(pattern, txt)
        if not result:
            raise RootMeParsingError("Could not parse category data.")
        for key2, category_item in enumerate(result):
            (score_category, num, tot, useless, challenges_list) = category_item
            if key1 == key2:
                challenges_stats = {
                    'score_category': score_category,
                    'num_challenges_solved': num,
                    'total_challenges_category': tot,
                }
                category = {
                    'name': name,
                    'path': path,
                    'challenges_stats': challenges_stats,
                }
                categories.append(category)
    return categories
