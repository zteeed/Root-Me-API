import asyncio

import aioredis
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application

from api.constants import REDIS_HOST, REDIS_PORT
from api.handlers import handlers
from init import create_cgs

if __name__ == '__main__':
    define('port', default=3000, help='port to listen on')
    application = Application(handlers)

    server = HTTPServer(application)
    server.bind(options.port)
    server.start(0)  # forks one process per cpu

    loop = asyncio.get_event_loop()
    application.redis = loop.run_until_complete(
        aioredis.create_redis_pool((REDIS_HOST, REDIS_PORT), loop=loop)
    )
    asyncio.get_event_loop().run_until_complete(create_cgs(application.redis))
    loop.run_forever()
    IOLoop.current().start()
