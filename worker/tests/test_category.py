from pytest import fixture

from tests.fixtures.fr_category_app_system_chall_info import APP_SYSTEM_INFO
from worker.parser import category


@fixture
def category_page_html():
    with open('fixtures/fr_category.html', 'r') as f:
        return f.read()


@fixture
def category_app_systeme_html():
    with open('fixtures/fr_category_app_systeme.html', 'r') as f:
        return f.read()


@fixture
def category_cracking_html():
    with open('fixtures/fr_category_cracking.html', 'r') as f:
        return f.read()


def test_extract_categories(category_page_html: str):
    want = {'App-Script', 'App-Systeme', 'Cracking', 'Cryptanalyse', 'Forensic', 'Programmation',
            'Realiste', 'Reseau', 'Steganographie', 'Web-Client', 'Web-Serveur'}

    actual = category.extract_categories(category_page_html)
    assert set(actual) == want


def test_extract_category_logo(category_app_systeme_html: str):
    actual = category.extract_category_logo(category_app_systeme_html)
    assert actual == 'local/cache-vignettes/L32xH32/rubon203-3ac88.png?1563879002'


class TestExtractCategoryDescription:
    def test_with_secondary_description(self, category_app_systeme_html: str):
        actual = category.extract_category_description(category_app_systeme_html)
        want = (
            "Cette série d'épreuve vous confronte aux vulnérabilités applicatives principalement liées aux erreurs de "
            "programmation aboutissant à des corruptions de zones mémoire.",
            'Les identifiants de connexion sont fournis pour les différents challenges. Le but est d’obtenir des '
            'droits supplémentaires en exploitant des faiblesses de programmes et ainsi obtenir un mot de passe '
            'permettant de valider chaque épreuve sur le portail.'
        )
        assert actual == want

    def test_without_secondary_description(self, category_cracking_html: str):
        actual = category.extract_category_description(category_cracking_html)
        want = ('Ces challenges permettent de comprendre le sens du terme « langage compilé '
                '». Ce sont des fichiers binaires à décortiquer pour aller chercher les '
                'instructions bas niveau permettant de répondre au problème posé.',
                ''
                )
        assert actual == want


def test_extract_category_prereq(category_app_systeme_html: str):
    actual = category.extract_category_prereq(category_app_systeme_html)
    assert actual == []


def test_extract_challenges_info(category_app_systeme_html: str):
    actual = category.extract_challenges_info(category_app_systeme_html)
    assert actual == APP_SYSTEM_INFO
