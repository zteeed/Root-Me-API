import json
from tornado.web import RequestHandler

from api.constants import VERSION, AUTHORS, GITHUB_ACCOUNTS
from api.routes import routes
from src.fetch import get_data


class RedirectHandler(RequestHandler):

    def initialize(self, url):
        self.url = url

    def get(self):
        self.redirect(self.url, status=302)


class InfoHandler(RequestHandler):
    info = dict(title="Root-Me-API", authors=AUTHORS, follow_us=GITHUB_ACCOUNTS, routes=routes)

    def get(self):
        """List of routes for this API."""
        self.write(InfoHandler.info)


class RootMeStaticHandler(RequestHandler):

    def initialize(self, key):
        self.key = key

    async def get(self):
        """Construct and send a JSON response with appropriate status code."""
        data = await get_data(self.application.redis, self.key)
        if data is None:
            self.write_error(status_code=404)
        else:
            data = dict(body=json.loads(data))
            self.write(data)


class RootMeDynamicHandler(RequestHandler):

    def initialize(self, key):
        self.key = key

    async def get(self, url_argument):
        """Construct and send a JSON response with appropriate status code."""
        data = await get_data(self.application.redis, self.key.format(url_argument))
        if data is None:
            self.write_error(status_code=404)
        else:
            data = dict(body=json.loads(data))
            self.write(data)


pattern = '([\\w-]+)'
handlers = [
    ('/', RedirectHandler, {'url': f'/{VERSION}'}),
    (f'/{VERSION}', InfoHandler),
    (f'/{VERSION}/categories', RootMeStaticHandler, {'key': 'categories'}),
    (f'/{VERSION}/category/{pattern}', RootMeDynamicHandler, {'key': 'categories.{}'}),
    (f'/{VERSION}/challenges', RootMeStaticHandler, {'key': 'challenges'}),
    (f'/{VERSION}/{pattern}/profile', RootMeDynamicHandler, {'key': '{}.profile'}),
    (f'/{VERSION}/{pattern}/contributions', RootMeDynamicHandler, {'key': '{}.contributions'}),
    (f'/{VERSION}/{pattern}/contributions/challenges', RootMeDynamicHandler, {'key': '{}.contributions.challenges'}),
    (f'/{VERSION}/{pattern}/contributions/solutions', RootMeDynamicHandler, {'key': '{}.contributions.solutions'}),
    (f'/{VERSION}/{pattern}/details', RootMeDynamicHandler, {'key': '{}.details'}),
    (f'/{VERSION}/{pattern}/ctf', RootMeDynamicHandler, {'key': '{}.ctfs'}),
    (f'/{VERSION}/{pattern}/stats', RootMeDynamicHandler, {'key': '{}.stats'})
]
