import re
from html import unescape

from lxml import html

from worker.parser.exceptions import RootMeParsingError


def extract_challenge_ids(txt):
    txt = txt.replace('\n', '')
    txt = txt.replace('&nbsp;', '')
    pattern = r'<div class="clearfix"></div><span><b>(.*?)</b>.*?</span><p'
    result = re.findall(pattern, txt)
    if not result:
        raise RootMeParsingError("Could not parse and extract challenge IDs from Root-Me.")
    return result


def extract_categories(r):
    tree = html.fromstring(r.content)
    result = tree.xpath('//li/a[starts-with(@class, "submenu")][starts-with(@href, "fr/Challenges")]/@href')
    result = [name.split('/')[2] for name in result]
    if not result:
        raise RootMeParsingError("Could not parse categories.")
    return result


def extract_category_logo(r):
    tree = html.fromstring(r.content)
    result = tree.xpath('//h1/img[@class="vmiddle"][starts-with(@src, "local")]/@src')
    if not result or not result[0]:
        raise RootMeParsingError("Could not parse logo from challenge.")
    return result[0]


def extract_category_description(r):
    tree = html.fromstring(r.content)
    result = tree.xpath('//meta[@name="Description"]/@content')
    if not result or not result[0]:
        raise RootMeParsingError('Could not parse description.')
    description1 = result[0]

    result = tree.xpath('string(//div[starts-with(@class, "texte crayon rubrique-texte")]//p)')
    if not result or 'Prérequis' in result:
        description2 = ''
    else:
        description2 = result
    return description1, description2


def extract_category_prereq(r):
    tree = html.fromstring(r.content)
    result = tree.xpath('string(//div[starts-with(@class, "texte crayon rubrique-texte")]/p[starts-with(., '
                        '"Préreq")]/following-sibling::p)')  # if prerequisites are on two "p" html tags
    if not result:
        result = tree.xpath('string(//div[starts-with(@class, "texte crayon rubrique-texte")]/p[starts-with(., '
                            '"Préreq")])')
    result = [prerequisite for prerequisite in result.split('\xa0')[1:] if '\n' not in prerequisite]
    return result


def extract_paths(r):
    tree = html.fromstring(r.content)
    paths = tree.xpath('//td[@class="text-left"]/a[starts-with(@href, "fr/Challenges")]/@href')
    return paths


def extract_statements(r):
    tree = html.fromstring(r.content)
    statements = tree.xpath('//td[@class="text-left"]/a[starts-with(@href, "fr/Challenges")]/@title')
    return statements


def extract_names(r):
    tree = html.fromstring(r.content)
    names = tree.xpath('//td[@class="text-left"]/a[starts-with(@href, "fr/Challenges")]/text()')
    return names


def extract_validations_percentages(r):
    tree = html.fromstring(r.content)
    validations_percentages = tree.xpath('//span[starts-with(@class, "gras left text-left")]/text()')
    return validations_percentages


def extract_validations_nbs(r):
    tree = html.fromstring(r.content)
    validations_nbs = tree.xpath('//span[@class="right"]/a/text()')
    return validations_nbs


def extract_difficulties(r):
    tree = html.fromstring(r.content)
    difficulties = tree.xpath('//td[@class="show-for-medium-up"]/a[starts-with(@href,"tag")]/@title')
    difficulties = [difficulty.split(':')[0].strip() for difficulty in difficulties]
    return difficulties


def extract_values(r):
    tree = html.fromstring(r.content)
    values = tree.xpath('//td[@class="show-for-medium-up"]/a[starts-with(@href,'
                        '"tag")]/parent::td/preceding-sibling::td/text()')
    values = [value for value in values if '\n' not in value]
    values = [int(value) for value in values if value.isdigit()]
    return values


def extract_authors(r):
    tree = html.fromstring(r.content)
    all_authors = tree.xpath('//td[@class="show-for-large-up"]')
    #  all_authors = [author.getchildren() for author in all_authors]  #  getchildren is a deprecated method
    all_authors = [[elements for elements in td] for td in all_authors]  # match "a" elements in td elements
    authors = []
    for challenge_authors in all_authors:
        result = []
        if challenge_authors:  # challenge_authors != []
            result = [author.get('href') for author in challenge_authors]
            result = [re.match('\/(.*?)\?', author_name).group(1) for author_name in result]
        authors.append(result)
    return authors


def extract_notes(r):
    tree = html.fromstring(r.content)
    notes = tree.xpath('//td/img[starts-with(@src, "squelettes/img/note")]/@src')
    notes = [re.match('.*note(.*?)\.png', note).group(1) for note in notes]
    notes = [int(note) for note in notes if note.isdigit()]
    return notes


def extract_solutions_nbs(r):
    tree = html.fromstring(r.content)
    solutions = tree.xpath('//td/img[starts-with(@src, "squelettes/img/note")]/parent::td/following-sibling::td/text()')
    solutions = [int(solution) for solution in solutions if solution.isdigit()]
    return solutions


def extract_challenges_info(r):
    paths = extract_paths(r)
    statements = extract_statements(r)
    names = extract_names(r)
    validations_percentages = extract_validations_percentages(r)
    validations_nbs = extract_validations_nbs(r)
    difficulties = extract_difficulties(r)
    values = extract_values(r)
    authors = extract_authors(r)
    notes = extract_notes(r)
    solutions_nbs = extract_solutions_nbs(r)

    # TODO: verify that every lists have same lengths
    response = [{
        'path': path.strip(),
        'statement': unescape(statement).strip(),
        'name': unescape(name).strip(),
        'validations_percentage': validations_percentage,
        'validations_nb': validations_nb,
        'value': value,
        'difficulty': unescape(difficulty),
        'author': author,
        'solutions_nb': solutions_nb,
        'note': note,
    }
        for path, statement, name, validations_percentage, validations_nb, value, difficulty, author, solutions_nb, note
        in zip(paths, statements, names, validations_percentages, validations_nbs, values, difficulties, authors,
               solutions_nbs, notes)
    ]
    return response
