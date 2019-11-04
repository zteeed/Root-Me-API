import json
from typing import Dict

from pytest import fixture

from worker.parser import category


@fixture
def category_page_html() -> bytes:
    with open('fixtures/fr_category.html', 'rb') as f:
        return f.read()


@fixture
def category_app_system_html() -> bytes:
    with open('fixtures/fr_category_app_system.html', 'rb') as f:
        return f.read()


@fixture
def category_app_system_result() -> Dict:
    with open('fixtures/fr_category_app_system.json', 'r') as f:
        return json.loads(f.read())


@fixture
def category_cracking_html() -> bytes:
    with open('fixtures/fr_category_cracking.html', 'rb') as f:
        return f.read()


@fixture
def category_cracking_result() -> Dict:
    with open('fixtures/fr_category_cracking.json', 'r') as f:
        return json.loads(f.read())


def test_extract_categories(category_page_html: bytes):
    want = {'App-Script', 'App-Systeme', 'Cracking', 'Cryptanalyse', 'Forensic', 'Programmation',
            'Realiste', 'Reseau', 'Steganographie', 'Web-Client', 'Web-Serveur'}

    actual = category.extract_categories(category_page_html)
    assert set(actual) == want


class TestExtractCategoryInfo:
    def test_app_system(self, category_app_system_html: bytes, category_app_system_result: Dict):
        actual = category.extract_category_info(category_app_system_html, 'App-Systeme')
        assert actual == category_app_system_result

    def test_cracking(self, category_cracking_html: bytes, category_cracking_result: Dict):
        actual = category.extract_category_info(category_cracking_html, 'Cracking')
        assert actual == category_cracking_result
