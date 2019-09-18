from lxml import html
from typing import Dict, List, Tuple


def extract_contributions_page_numbers(content: bytes) -> Tuple[int, int]:
    nb_challenges_pages, nb_solutions_pages = 0, 0
    tree = html.fromstring(content)
    div_elements = tree.xpath('//div[@class="t-body tb-padding"]/div')
    h4_elements = [div_element.xpath('h4') for div_element in div_elements]
    if not h4_elements:
        return nb_challenges_pages, nb_solutions_pages

    for div_element in div_elements:
        title = div_element.xpath('h4/text()')[0]
        pages = div_element.xpath('div[@class="pagination-centered"]/ul[@class="pagination"]/li')
        if 'Challenge' in title:
            if not pages:  # pages == []
                nb_challenges_pages = 1
            else:
                nb_challenges_pages = len(pages)
        if 'Solution' in title:
            if not pages:  # pages == []
                nb_solutions_pages = 1
            else:
                nb_solutions_pages = len(pages)
    return nb_challenges_pages, nb_solutions_pages


def extract_challenges_contributions(content: bytes) -> List[Dict[str, str]]:
    tree = html.fromstring(content)
    ul_elements = tree.xpath('//div[@class="t-body tb-padding"]/div/a[contains(@name, "challenge")]/parent::div/ul')
    if not ul_elements:
        return []
    challenges = []
    li_elements = ul_elements[0].xpath('li')
    for li_element in li_elements:
        category = li_element.xpath('a[1]/@href')[0].split('/')[2]
        challenge_name = li_element.xpath('a[2]/text()')[0]
        date = li_element.xpath('span/text()')[0].replace('\xa0', ' ')
        challenges.append({'challenge_name': challenge_name, 'category': category, 'date': date})
    return challenges


def extract_solutions_contributions(content: bytes) -> List[Dict[str, str]]:
    tree = html.fromstring(content)
    ul_elements = tree.xpath('//div[@class="t-body tb-padding"]/div/a[contains(@name, "solution")]/parent::div/ul')
    if not ul_elements:
        return []
    solutions = []
    li_elements = ul_elements[0].xpath('li')
    for li_element in li_elements:
        challenge_name = li_element.xpath('a[1]/@href')[0].split('/')[-1]
        solution_path = li_element.xpath('a[2]/@href')[0]
        solution_title = li_element.xpath('a[2]/text()')[0]
        date = li_element.xpath('span/text()')[0].replace('\xa0', ' ')
        solution = {'challenge_name': challenge_name, 'solution_path': solution_path,
                    'solution_title': solution_title, 'date': date}
        solutions.append(solution)
    return solutions
