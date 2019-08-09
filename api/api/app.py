import aioredis
import tornado

from api.constants import REDIS_HOST, REDIS_PORT
from api.handlers import handlers


class Application(tornado.web.Application):
    def __init__(self):
        # Prepare IOLoop class to run instances on asyncio
        tornado.ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOMainLoop')
        super().__init__(handlers, debug=True)

    def init_with_loop(self, loop):
        self.redis = loop.run_until_complete(
            aioredis.create_redis_pool((REDIS_HOST, REDIS_PORT), minsize=5, maxsize=25, loop=loop)
        )
