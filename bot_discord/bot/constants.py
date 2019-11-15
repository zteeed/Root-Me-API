bot_channel = 'root-me-news'
emoji1 = 'dab'
emoji2 = 'ok_hand'
emoji3 = 'thinking'
emoji4 = 'thinking'
emoji5 = 'thumbsdown'
limit_size = 1000
medals = [':first_place:', ':second_place:', ':third_place:']
token = 'token'
timeout = 15
URL = 'http://api:3000'
DEFAULT_LANG = 'en'
LANGS = ['en', 'fr', 'de', 'es']
FILENAME = 'data/data.json'
VERSION = '1.2'
GITHUB_REPOSITORY = 'https://github.com/zteeed/Root-Me-API'
ROOTME_WEBSITE = 'https://www.root-me.org'
PROJECT_INFORMATION = {
    'title': 'Project information',
    'content': f'This Discord Bot uses a custom API which sends tasks to several workers.\nEach worker makes requests '
    f'to the [RootMe]({ROOTME_WEBSITE}) website, parses the collected data using the DOM and stores it into '
    f'redis streams.\nGithub repository: [{GITHUB_REPOSITORY}]({GITHUB_REPOSITORY})',
    'footer': f'Root Me Discord Bot v{VERSION}'
}
