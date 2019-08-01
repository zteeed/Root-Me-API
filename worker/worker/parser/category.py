import re
from html import unescape

from lxml import html

from worker.zip import zip_equal
from worker.parser.exceptions import RootMeParsingError


def extract_challenge_ids(txt):
    txt = txt.replace('\n', '')
    txt = txt.replace('&nbsp;', '')
    pattern = r'<div class="clearfix"></div><span><b>(.*?)</b>.*?</span><p'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError()
    return result


def extract_categories(content):
    tree = html.fromstring(content)
    result = tree.xpath('//li/a[starts-with(@class, "submenu")][starts-with(@href, "fr/Challenges")]/@href')
    result = [name.split('/')[2] for name in result]
    if not result:
        raise RootMeParsingError()
    return result


def extract_category_logo(content):
    tree = html.fromstring(content)
    result = tree.xpath('//h1/img[@class="vmiddle"][starts-with(@src, "local")]/@src')
    if not result:
        raise RootMeParsingError()
    return result[0]


def extract_category_description(content):
    tree = html.fromstring(content)
    result = tree.xpath('//meta[@name="Description"]/@content')
    if not result:
        raise RootMeParsingError()
    description1 = result[0]

    result = tree.xpath('string(//div[starts-with(@class, "texte crayon rubrique-texte")]//p)')
    if not result or 'Prérequis' in result:
        description2 = ''
    else:
        description2 = result
    return description1, description2


def extract_category_prereq(content):
    tree = html.fromstring(content)
    result = tree.xpath('string(//div[starts-with(@class, "texte crayon rubrique-texte")]/p[2]/following-sibling::p)')
    if not result:  # if prerequisites are not on two "p" html tags
        result = tree.xpath('string(//div[starts-with(@class, "texte crayon rubrique-tex")]/p[contains(., "Préreq")])')
    #  RootMe does not list prerequisites with ul/li HTML tags.
    #  I need to make some chemistry to extract the data i want.
    return [prerequisite for prerequisite in result.split('\xa0')[1:] if '\n' not in prerequisite]


def extract_challenges_url_paths(content):
    tree = html.fromstring(content)
    paths = tree.xpath('//td[@class="text-left"]/a[starts-with(@href, "fr/Challenges")]/@href')
    return [path.strip() for path in paths]


def extract_challenges_statements(content):
    tree = html.fromstring(content)
    statements = tree.xpath('//td[@class="text-left"]/a[starts-with(@href, "fr/Challenges")]/@title')
    return [unescape(statement).strip() for statement in statements]


def extract_challenges_names(content):
    tree = html.fromstring(content)
    names = tree.xpath('//td[@class="text-left"]/a[starts-with(@href, "fr/Challenges")]/text()')
    return [unescape(name.strip()) for name in names]


def extract_challenges_validations_percentages(content):
    tree = html.fromstring(content)
    return tree.xpath('//span[starts-with(@class, "gras left text-left")]/text()')


def extract_challenges_validations_nbs(content):
    tree = html.fromstring(content)
    return tree.xpath('//span[@class="right"]/a/text()')


def extract_challenges_difficulties(content):
    tree = html.fromstring(content)
    difficulties = tree.xpath('//td[@class="show-for-medium-up"]/a[starts-with(@href,"tag")]/@title')
    return [unescape(difficulty.split(':')[0]).strip() for difficulty in difficulties]


def extract_challenges_values(content):
    tree = html.fromstring(content)
    values = tree.xpath('//table[@class="text-center"]/tbody/tr/td[4]/text()')
    return [int(value) for value in values]


def extract_challenges_authors(content):
    tree = html.fromstring(content)
    all_authors = tree.xpath('//td[@class="show-for-large-up"]')
    all_authors = [[elements for elements in td] for td in all_authors]  # match "a" elements in td elements
    authors = []
    for challenge_authors in all_authors:
        result = []
        if challenge_authors:  # challenge_authors != []
            result = [author.get('href') for author in challenge_authors]
            result = [re.match(r'\/(.*?)\?', author_name).group(1) for author_name in result]
        authors.append(result)
    return authors


def extract_challenges_notes(content):
    tree = html.fromstring(content)
    notes = tree.xpath('//td/img[starts-with(@src, "squelettes/img/note")]/@src')
    result = []
    for note in notes:
        note = re.match(r'.*note(.*?)\.png', note).group(1)
        result.append(int(note))
    return result


def extract_challenges_solutions_nbs(content):
    tree = html.fromstring(content)
    solutions = tree.xpath('//td/img[starts-with(@src, "squelettes/img/note")]/parent::td/following-sibling::td/text()')
    return [int(solution) for solution in solutions]


def extract_challenges_info(content):
    paths = extract_challenges_url_paths(content)
    statements = extract_challenges_statements(content)
    names = extract_challenges_names(content)
    validations_percentages = extract_challenges_validations_percentages(content)
    validations_nbs = extract_challenges_validations_nbs(content)
    difficulties = extract_challenges_difficulties(content)
    values = extract_challenges_values(content)
    authors = extract_challenges_authors(content)
    notes = extract_challenges_notes(content)
    solutions_nbs = extract_challenges_solutions_nbs(content)

    #  zip_equal function verifies that every lists have same lengths or raise an exception
    response = []
    for path, statement, name, validations_percentage, validations_nb, value, difficulty, author, solutions_nb, \
        note in zip_equal(paths, statements, names, validations_percentages, validations_nbs, values, difficulties,
                          authors, solutions_nbs, notes):
        response.append({
            'path': path,
            'statement': statement,
            'name': name,
            'validations_percentage': validations_percentage,
            'validations_nb': validations_nb,
            'value': value,
            'difficulty': difficulty,
            'author': author,
            'solutions_nb': solutions_nb,
            'note': note,
        })
    return response
