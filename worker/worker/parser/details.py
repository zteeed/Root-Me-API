import re
from lxml import html

from worker.zip import zip_equal
from worker.parser.exceptions import RootMeParsingError


def extract_score(content):
    tree = html.fromstring(content)
    score = tree.xpath('//div[@class="small-12 columns"]/ul/li[1]/span[@class="color1 tl"]/text()')
    score = re.findall(r'(\d+)', score[0])[0]
    return int(score)


def extract_nb_challenges_solved(content):
    tree = html.fromstring(content)
    challenges_solved = tree.xpath('//div[@class="small-12 columns"]/ul/li[1]/span[@class="color1 tl"]/span/text()')
    (nb_challenges_solved, nb_challenges_tot) = re.findall(r'(\d+)/(\d+)', challenges_solved[0])[0]
    return int(nb_challenges_solved), int(nb_challenges_tot)


def extract_ranking(content):
    tree = html.fromstring(content)
    li_element = tree.xpath('//div[@class="small-12 columns"]/ul/li[2]')[0]
    ranking = li_element.xpath('span[@class="color1 tl"]/text()')[0]
    ranking_tot = li_element.xpath('span[@class="color1 tl"]/span/text()')[0]
    ranking = re.findall(r'(\d+)', ranking)[0]
    ranking_tot = re.findall(r'(\d+)', ranking_tot)[0]
    return int(ranking), int(ranking_tot)


def extract_ranking_category(content):
    tree = html.fromstring(content)
    ranking_category = tree.xpath('//div[@class="small-12 columns"]/ul/li[3]/span[@class="color1 tl"]/text()')[0]
    ranking_category = re.findall(r'\w+', ranking_category)[0]
    return ranking_category


def extract_challenges(content):
    tree = html.fromstring(content)
    categories = tree.xpath('//div[@class="panel animated_box"]/h4/a/text()')
    categories_path = tree.xpath('//div[@class="panel animated_box"]/h4/a/@href')
    html_categories_stats = tree.xpath('//div[@class="panel animated_box"]/span/text()')
    categories_stats = []
    for html_category_stats in html_categories_stats:
        category_stats = re.findall(r'(\d+)', html_category_stats)
        if len(category_stats) == 1:
            score_category = 0
            num_challenges_solved = 0
            total_challenges_category = int(category_stats[0])
        elif len(category_stats) == 3:
            score_category = int(category_stats[0])
            num_challenges_solved = int(category_stats[1])
            total_challenges_category = int(category_stats[2])
        else:
            raise RootMeParsingError()
        category_stats = {
            'score_category': score_category,
            'num_challenges_solved': num_challenges_solved,
            'total_challenges_category': total_challenges_category,
        }
        categories_stats.append(category_stats)
    result = []
    for name, path, stats in zip_equal(categories, categories_path, categories_stats):
        result.append({'name': name, 'path': path, 'stats_categories': stats})
    return result
