import json

from pytest import fixture

from worker.parser import category


@fixture
def category_page_html():
    with open('fixtures/fr_category.html', 'r') as f:
        return f.read()


@fixture
def category_app_system_html():
    with open('fixtures/fr_category_app_system.html', 'r') as f:
        return f.read()


@fixture
def category_app_system_result():
    with open('fixtures/fr_category_app_system.json', 'r') as f:
        return json.loads(f.read())


@fixture
def category_cracking_html():
    with open('fixtures/fr_category_cracking.html', 'r') as f:
        return f.read()


@fixture
def category_cracking_result():
    with open('fixtures/fr_category_cracking.json', 'r') as f:
        return json.loads(f.read())


def test_extract_categories(category_page_html: str):
    want = {'App-Script', 'App-Systeme', 'Cracking', 'Cryptanalyse', 'Forensic', 'Programmation',
            'Realiste', 'Reseau', 'Steganographie', 'Web-Client', 'Web-Serveur'}

    actual = category.extract_categories(category_page_html)
    assert set(actual) == want


class TestExtractCategoryInfo:
    def test_app_system(self, category_app_system_html: str, category_app_system_result: dict):
        actual = category.extract_category_info(category_app_system_html, 'App-Systeme')
        assert actual == category_app_system_result

    def test_cracking(self, category_cracking_html: str, category_cracking_result: dict):
        actual = category.extract_category_info(category_cracking_html, 'Cracking')
        assert actual == category_cracking_result
