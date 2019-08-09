from tornado.web import RequestHandler

from api.constants import VERSION, AUTHORS, GITHUB_ACCOUNTS
from api.routes import routes


class RedirectHandler(RequestHandler):

    def initialize(self, url):
        self.url = url

    def get(self):
        self.redirect(self.url, status=302)


class InfoHandler(RequestHandler):

    def get(self):
        """List of routes for this API."""
        self.set_status(200)
        #  routes imported from api.routes
        info = dict(title="Root-Me-API", authors=AUTHORS, follow_us=GITHUB_ACCOUNTS, routes=routes)
        self.write(info)


class RootMeStaticHandler(RequestHandler):

    def initialize(self, key):
        self.key = key

    async def get(self):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(200)
        data = await self.application.redis.get(self.key)
        self.write(data)


class RootMeDynamicHandler(RequestHandler):

    def initialize(self, key):
        if 'categories' in key:
            self.key = key + '.{}'
        else:  # url_argument is an username
            self.key = '{}.' + key

    async def get(self, url_argument):
        """Construct and send a JSON response with appropriate status code."""
        self.key = self.key.format(url_argument)
        data = await self.application.redis.get(self.key)
        if data is None:
            self.write_error(status_code=404)
        else:
            self.set_status(200)
            self.write(data)


handlers = [
    ('/', RedirectHandler, {'url': f'/{VERSION}'}),
    (f'/{VERSION}', InfoHandler),
    (f'/{VERSION}/categories', RootMeStaticHandler, {'key': 'categories'}),
    (f'/{VERSION}/category/[\\w-]+', RootMeDynamicHandler, {'key': 'categories'}),
    (f'/{VERSION}/challenges', RootMeStaticHandler, {'key': 'challenges'}),
    (f'/{VERSION}/[\\w-]+/profile', RootMeDynamicHandler, {'key': 'profile'}),
    (f'/{VERSION}/[\\w-]+/contributions', RootMeDynamicHandler, {'key': 'contributions'}),
    (f'/{VERSION}/[\\w-]+/contributions/challenges', RootMeDynamicHandler, {'key': 'contributions.challenges'}),
    (f'/{VERSION}/[\\w-]+/contributions/solutions', RootMeDynamicHandler, {'key': 'contributions.solutions'}),
    (f'/{VERSION}/[\\w-]+/details', RootMeDynamicHandler, {'key': 'details'}),
    (f'/{VERSION}/[\\w-]+/ctf', RootMeDynamicHandler, {'key': 'ctfs'}),
    (f'/{VERSION}/[\\w-]+/stats', RootMeDynamicHandler, {'key': 'stats'})
]
