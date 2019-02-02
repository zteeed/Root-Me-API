from multiprocessing.pool import ThreadPool

from api.app import app
from api.constants import URL
from api.http_interface import session
from api.http_interface.exceptions import RootMeException
from api.parser.category import extract_categories, extract_category_logo, extract_category_description, \
    extract_category_prereq, extract_challenges_info
from api.parser.exceptions import RootMeParsingError


def retrieve_category_info(category):
    r = session.get(URL + 'fr/Challenges/{}/'.format(category))
    if r.status_code != 200:
        raise RootMeException(r.status_code)

    logo = extract_category_logo(r.text)
    desc1, desc2 = extract_category_description(r.text)
    prereq = extract_category_prereq(r.text)
    challenges = extract_challenges_info(r.text)

    app.logger.info('Fetched category page "{}"'.format(category))

    return [{
        'name': category,
        'logo': logo,
        'description1': desc1,
        'description2': desc2,
        'prerequisites': prereq,
        'challenges': challenges,
        'challenges_nb': len(challenges),
    }]


def get_all_challenges():
    try:
        r = session.get(URL + 'fr/Challenges/')
        if r.status_code != 200:
            raise RootMeException(r.status_code)

        categories = extract_categories(r.text)

        with ThreadPool(len(categories)) as tp:
            response = tp.map(retrieve_category_info, categories)

        return response

    except RootMeException as e:
        app.logger.exception("Root-me did not respond 200")
        return "RootMe responded {}".format(e.err_code), 502

    except RootMeParsingError:
        app.logger.exception("Parsing error")
        raise
