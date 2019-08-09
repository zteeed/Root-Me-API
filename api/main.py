import asyncio
import aioredis

from tornado.web import Application
from tornado.options import define, options

from api.constants import REDIS_HOST, REDIS_PORT
from api.handlers import handlers

if __name__ == '__main__':
    define('port', default=3000, help='port to listen on')
    application = Application(handlers)
    application.listen(options.port)

    loop = asyncio.get_event_loop()
    application.redis = loop.run_until_complete(
        aioredis.create_redis_pool((REDIS_HOST, REDIS_PORT), loop=loop)
    )
    loop.run_forever()
