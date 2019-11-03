import json

from tornado.web import RequestHandler

from api.constants import AUTHORS, GITHUB_ACCOUNTS
from api.routes import routes
from src.fetch import read_from_redis_key


class InfoHandler(RequestHandler):
    info = dict(title="Root-Me-API", authors=AUTHORS, follow_us=GITHUB_ACCOUNTS, routes=routes)

    def get(self):
        """List of routes for this API."""
        self.application.log.info('GET request', handler='InfoHandler')
        self.write(InfoHandler.info)


class RootMeStaticCategoryHandler(RequestHandler):

    def initialize(self, key: str):
        self.key = key

    async def get(self, lang):
        """Construct and send a JSON response with appropriate status code."""
        self.application.log.info('GET request', handler='RootMeStaticCategoryHandler', lang=lang)
        key = self.key.format(lang)
        data = await read_from_redis_key(self.application.log, self.application.redis, key, arg=None,
                                         handler_type='static_category', lang=lang)
        if data is None:
            self.write_error(status_code=404)
        else:
            self.write(json.loads(data))


class RootMeDynamicCategoryHandler(RequestHandler):

    def initialize(self, key: str):
        self.key = key

    async def get(self, lang, category):
        """Construct and send a JSON response with appropriate status code."""
        self.application.log.info('GET request', handler='RootMeDynamicCategoryHandler', category=category, lang=lang)
        key = self.key.format(lang, category)
        data = await read_from_redis_key(self.application.log, self.application.redis, key, arg=category,
                                         handler_type='dynamic_category', lang=lang)

        if data is None:
            self.write_error(status_code=404)
        else:
            self.write(json.loads(data))


class RootMeDynamicUserHandler(RequestHandler):

    def initialize(self, key: str):
        self.key = key

    async def get(self, lang, username):
        """Construct and send a JSON response with appropriate status code."""
        self.application.log.info('GET request', handler='RootMeDynamicUserHandler', username=username, lang=lang)
        key = self.key.format(lang, username)
        data = await read_from_redis_key(self.application.log, self.application.redis, key, arg=username,
                                         handler_type='dynamic_user', lang=lang)

        if data is None:
            self.write_error(status_code=404)
        else:
            self.write(json.loads(data))


#  username_regex = r'([\\w-]+)'
#  username_regex = r'(.*)'  # username may contain unicode characters
username_regex = r'([^\/]+)'  # username may contain unicode characters but do not contain slashes
lang_regex = r'(en|fr|de|es)'
handlers = [
    (f'/', InfoHandler),
    (f"/{lang_regex}/categories", RootMeStaticCategoryHandler, {'key': '{}.categories'}),
    (f'/{lang_regex}/category/{username_regex}', RootMeDynamicCategoryHandler, {'key': '{}.categories.{}'}),
    (f'/{lang_regex}/challenges', RootMeStaticCategoryHandler, {'key': '{}.challenges'}),
    (f'/{lang_regex}/{username_regex}/profile', RootMeDynamicUserHandler, {'key': '{}.{}.profile'}),
    (f'/{lang_regex}/{username_regex}/contributions', RootMeDynamicUserHandler, {'key': '{}.{}.contributions'}),
    (f'/{lang_regex}/{username_regex}/contributions/challenges', RootMeDynamicUserHandler,
     {'key': '{}.{}.contributions.challenges'}),
    (f'/{lang_regex}/{username_regex}/contributions/solutions', RootMeDynamicUserHandler,
     {'key': '{}.{}.contributions.solutions'}),
    (f'/{lang_regex}/{username_regex}/details', RootMeDynamicUserHandler, {'key': '{}.{}.details'}),
    (f'/{lang_regex}/{username_regex}/ctf', RootMeDynamicUserHandler, {'key': '{}.{}.ctfs'}),
    (f'/{lang_regex}/{username_regex}/stats', RootMeDynamicUserHandler, {'key': '{}.{}.stats'})
]
