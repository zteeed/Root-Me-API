import json
from tornado.web import RequestHandler

from api.constants import VERSION, AUTHORS, GITHUB_ACCOUNTS
from api.routes import routes


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
        data = await self.application.redis.get(self.key)
        data = dict(body=json.loads(data))
        self.write(data)


class RootMeDynamicHandler(RequestHandler):

    def initialize(self, key):
        self.key = key

    def format(self, url_argument):
        if 'categories' in self.key:
            self.key = f'{self.key}.{self.url_argument}'
        else:  # url_argument is an username
            self.key = f'{url_argument}.{self.key}'

    async def get(self, url_argument):
        """Construct and send a JSON response with appropriate status code."""
        self.format(url_argument)
        data = await self.application.redis.get(self.key)
        if data is None:
            self.write_error(status_code=404)
        else:
            data = dict(body=json.loads(data))
            self.write(data)


handlers = [
    ('/', RedirectHandler, {'url': f'/{VERSION}'}),
    (f'/{VERSION}', InfoHandler),
    (f'/{VERSION}/categories', RootMeStaticHandler, {'key': 'categories'}),
    (f'/{VERSION}/category/([\\w-]+)', RootMeDynamicHandler, {'key': 'categories'}),
    (f'/{VERSION}/challenges', RootMeStaticHandler, {'key': 'challenges'}),
    (f'/{VERSION}/([\\w-]+)/profile', RootMeDynamicHandler, {'key': 'profile'}),
    (f'/{VERSION}/([\\w-]+)/contributions', RootMeDynamicHandler, {'key': 'contributions'}),
    (f'/{VERSION}/([\\w-]+)/contributions/challenges', RootMeDynamicHandler, {'key': 'contributions.challenges'}),
    (f'/{VERSION}/([\\w-]+)/contributions/solutions', RootMeDynamicHandler, {'key': 'contributions.solutions'}),
    (f'/{VERSION}/([\\w-]+)/details', RootMeDynamicHandler, {'key': 'details'}),
    (f'/{VERSION}/([\\w-]+)/ctf', RootMeDynamicHandler, {'key': 'ctfs'}),
    (f'/{VERSION}/([\\w-]+)/stats', RootMeDynamicHandler, {'key': 'stats'})
]
