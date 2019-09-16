from api.constants import REDIS_STREAM_CHALLENGES, REDIS_STREAM_USERS


async def get_data(redis_app, key, username=None):
    data = await redis_app.get(key)
    if '.' not in key:  # handler is RootMeStaticHandler
        await redis_app.xadd(REDIS_STREAM_CHALLENGES, {b'update': b"ok"})
    else:  # handler is RootMeDynamicHandler
        await redis_app.xadd(REDIS_STREAM_USERS, {b'username': username.encode()})
    return data
