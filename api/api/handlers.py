from abc import ABC
import asyncio
import json

import tornado
import tornado.ioloop
import tornado.web
import tornado.gen

from api.constants import VERSION, AUTHORS, GITHUB_ACCOUNTS
from api.routes import routes


class AsyncRequestHandler(tornado.web.RequestHandler, ABC):
    """Base class for request handlers with `asyncio` coroutines support.
    It runs methods on Tornado's ``AsyncIOMainLoop`` instance.
    Subclasses have to implement one of `get_async()`, `post_async()`, etc.
    Asynchronous method should be decorated with `@asyncio.coroutine`.
    Usage example::
        class MyAsyncRequestHandler(AsyncRequestHandler):
            @asyncio.coroutine
            def get_async(self):
                html = yield from self.application.http.get('http://python.org')
                self.write({'html': html})
    You may also just re-define `get()` or `post()` methods and they will be simply run
    synchronously. This may be convinient for draft implementation, i.e. for testing
    new libs or concepts.
    """

    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        """Handle GET request asyncronously, delegates to
        ``self.get_async()`` coroutine.
        """
        yield self._run_method('get', *args, **kwargs)

    @asyncio.coroutine
    def _run_async(self, coroutine, future_, *args, **kwargs):
        """Perform coroutine and set result to ``Future`` object."""

        try:
            result = yield from coroutine(*args, **kwargs)
            future_.set_result(result)
        except Exception as e:
            future_.set_exception(e)
            #  print(traceback.format_exc())

    def _run_method(self, method_, *args, **kwargs):
        """Run ``get_async()`` / ``post_async()`` / etc. coroutine
        wrapping result with ``tornado.concurrent.Future`` for
        compatibility with ``gen.coroutine``.
        """
        coroutine = getattr(self, '%s_async' % method_, None)

        if not coroutine:
            raise tornado.web.HTTPError(405)

        future_ = tornado.concurrent.Future()
        asyncio.create_task(
            self._run_async(coroutine, future_, *args, **kwargs)
        )

        return future_


class RedirectHandler(AsyncRequestHandler, ABC):
    """Only allow GET requests."""
    SUPPORTED_METHODS = ["GET"]

    def initialize(self, url):
        self.url = url

    @asyncio.coroutine
    def get_async(self):
        self.set_status(302)
        self.redirect(self.url)


class InfoHandler(AsyncRequestHandler, ABC):
    """Only allow GET requests."""
    SUPPORTED_METHODS = ["GET"]

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    @asyncio.coroutine
    def get_async(self):
        """List of routes for this API."""
        self.set_status(200)
        #  routes imported from api.routes
        info = dict(title="Root-Me-API", authors=AUTHORS, follow_us=GITHUB_ACCOUNTS, routes=routes)
        self.write(json.dumps(info))


class RootMeStaticHandler(AsyncRequestHandler, ABC):
    """Only allow GET requests."""
    SUPPORTED_METHODS = ["GET"]

    def initialize(self, key):
        self.key = key

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    @asyncio.coroutine
    def get_async(self):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(200)
        data = yield from self.application.redis.get(self.key)
        self.write(data)


class RootMeDynamicHandler(AsyncRequestHandler, ABC):
    """Only allow GET requests."""
    SUPPORTED_METHODS = ["GET"]

    def initialize(self, key):
        if 'categories' in key:
            self.key = key + '.{}'
        else:  # url_argument is an username
            self.key = '{}.' + key

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    @asyncio.coroutine
    def get_async(self, url_argument):
        """Construct and send a JSON response with appropriate status code."""
        self.key = self.key.format(url_argument)
        data = yield from self.application.redis.get(self.key)
        if data is None:
            self.set_status(404)  # raise raise tornado.web.HTTPError ?
        else:
            self.set_status(200)
            self.write(data)


handlers = [
    ('/', RedirectHandler, {'url': f'/{VERSION}'}),
    (f'/{VERSION}', InfoHandler),
    (f'/{VERSION}/categories', RootMeStaticHandler, {'key': 'categories'}),
    (f'/{VERSION}/category/(.*)', RootMeDynamicHandler, {'key': 'categories'}),
    (f'/{VERSION}/challenges', RootMeStaticHandler, {'key': 'challenges'}),
    (f'/{VERSION}/(.*)/profile', RootMeDynamicHandler, {'key': 'profile'}),
    (f'/{VERSION}/(.*)/contributions', RootMeDynamicHandler, {'key': 'contributions'}),
    (f'/{VERSION}/(.*)/contributions/challenges', RootMeDynamicHandler, {'key': 'contributions.challenges'}),
    (f'/{VERSION}/(.*)/contributions/solutions', RootMeDynamicHandler, {'key': 'contributions.solutions'}),
    (f'/{VERSION}/(.*)/details', RootMeDynamicHandler, {'key': 'details'}),
    (f'/{VERSION}/(.*)/ctf', RootMeDynamicHandler, {'key': 'ctfs'}),
    (f'/{VERSION}/(.*)/stats', RootMeDynamicHandler, {'key': 'stats'})
]
