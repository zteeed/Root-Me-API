import json
from typing import Dict

from pytest import fixture

from worker.parser import category


@fixture
def category_page_html_fr() -> bytes:
    with open('fixtures/fr_category.html', 'rb') as f:
        return f.read()


@fixture
def category_app_system_html_fr() -> bytes:
    with open('fixtures/fr_category_app_system.html', 'rb') as f:
        return f.read()


@fixture
def category_app_system_result_fr() -> Dict:
    with open('fixtures/fr_category_app_system.json', 'r') as f:
        return json.loads(f.read())


@fixture
def category_cracking_html_fr() -> bytes:
    with open('fixtures/fr_category_cracking.html', 'rb') as f:
        return f.read()


@fixture
def category_cracking_result_fr() -> Dict:
    with open('fixtures/fr_category_cracking.json', 'r') as f:
        return json.loads(f.read())


@fixture
def category_page_html_en() -> bytes:
    with open('fixtures/en_category.html', 'rb') as f:
        return f.read()


@fixture
def category_app_system_html_en() -> bytes:
    with open('fixtures/en_category_app_system.html', 'rb') as f:
        return f.read()


@fixture
def category_app_system_result_en() -> Dict:
    with open('fixtures/en_category_app_system.json', 'r') as f:
        return json.loads(f.read())


@fixture
def category_cracking_html_en() -> bytes:
    with open('fixtures/en_category_cracking.html', 'rb') as f:
        return f.read()


@fixture
def category_cracking_result_en() -> Dict:
    with open('fixtures/en_category_cracking.json', 'r') as f:
        return json.loads(f.read())


@fixture
def category_page_html_de() -> bytes:
    with open('fixtures/de_category.html', 'rb') as f:
        return f.read()


@fixture
def category_app_system_html_de() -> bytes:
    with open('fixtures/de_category_app_system.html', 'rb') as f:
        return f.read()


@fixture
def category_app_system_result_de() -> Dict:
    with open('fixtures/de_category_app_system.json', 'r') as f:
        return json.loads(f.read())


@fixture
def category_cracking_html_de() -> bytes:
    with open('fixtures/de_category_cracking.html', 'rb') as f:
        return f.read()


@fixture
def category_cracking_result_de() -> Dict:
    with open('fixtures/de_category_cracking.json', 'r') as f:
        return json.loads(f.read())


@fixture
def category_page_html_es() -> bytes:
    with open('fixtures/es_category.html', 'rb') as f:
        return f.read()


@fixture
def category_app_system_html_es() -> bytes:
    with open('fixtures/es_category_app_system.html', 'rb') as f:
        return f.read()


@fixture
def category_app_system_result_es() -> Dict:
    with open('fixtures/es_category_app_system.json', 'r') as f:
        return json.loads(f.read())


@fixture
def category_cracking_html_es() -> bytes:
    with open('fixtures/es_category_cracking.html', 'rb') as f:
        return f.read()


@fixture
def category_cracking_result_es() -> Dict:
    with open('fixtures/es_category_cracking.json', 'r') as f:
        return json.loads(f.read())


def test_extract_categories_fr(category_page_html_fr: bytes):
    want = {'App-Script', 'App-Systeme', 'Cracking', 'Cryptanalyse', 'Forensic', 'Programmation',
            'Realiste', 'Reseau', 'Steganographie', 'Web-Client', 'Web-Serveur'}

    actual = category.extract_categories(category_page_html_fr)
    assert set(actual) == want


def test_extract_categories_en(category_page_html_en: bytes):
    want = {"App-Script", "App-System", "Cracking", "Cryptanalysis", "Forensic", "Network", "Programming", "Realist",
            "Steganography", "Web-Client", "Web-Server"}

    actual = category.extract_categories(category_page_html_en)
    assert set(actual) == want


def test_extract_categories_de(category_page_html_de: bytes):
    want = {"App-Script", "App-System", "Cracking", "Forensik", "Kryptoanalyse", "Netzwerk", "Programmierung",
            "Realistisch", "Steganographie", "Web-Client", "Web-Server"}

    actual = category.extract_categories(category_page_html_de)
    assert set(actual) == want


def test_extract_categories_es(category_page_html_es: bytes):
    want = {"App-Script", "App-Sistema", "Cracking", "Criptoanalisis", "Esteganografia", "Forense", "Programacion",
            "Realista", "Redes", "Web-Cliente", "Web-Servidor"}

    actual = category.extract_categories(category_page_html_es)
    assert set(actual) == want


class TestExtractCategoryInfo:
    def test_app_system_fr(self, category_app_system_html_fr: bytes, category_app_system_result_fr: Dict):
        actual = category.extract_category_info(category_app_system_html_fr, 'App-Systeme')
        assert actual == category_app_system_result_fr

    def test_cracking_fr(self, category_cracking_html_fr: bytes, category_cracking_result_fr: Dict):
        actual = category.extract_category_info(category_cracking_html_fr, 'Cracking')
        assert actual == category_cracking_result_fr

    def test_app_system_en(self, category_app_system_html_en: bytes, category_app_system_result_en: Dict):
        actual = category.extract_category_info(category_app_system_html_en, 'App-System')
        assert actual == category_app_system_result_en

    def test_cracking_en(self, category_cracking_html_en: bytes, category_cracking_result_en: Dict):
        actual = category.extract_category_info(category_cracking_html_en, 'Cracking')
        assert actual == category_cracking_result_en

    def test_app_system_de(self, category_app_system_html_de: bytes, category_app_system_result_de: Dict):
        actual = category.extract_category_info(category_app_system_html_de, 'App-System')
        assert actual == category_app_system_result_de

    def test_cracking_de(self, category_cracking_html_de: bytes, category_cracking_result_de: Dict):
        actual = category.extract_category_info(category_cracking_html_de, 'Cracking')
        assert actual == category_cracking_result_de

    def test_app_system_es(self, category_app_system_html_es: bytes, category_app_system_result_es: Dict):
        actual = category.extract_category_info(category_app_system_html_es, 'App-Sistema')
        assert actual == category_app_system_result_es

    def test_cracking_es(self, category_cracking_html_es: bytes, category_cracking_result_es: Dict):
        actual = category.extract_category_info(category_cracking_html_es, 'Cracking')
        assert actual == category_cracking_result_es
