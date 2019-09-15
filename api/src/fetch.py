

async def get_data(redis_app, key):
    data = await redis_app.get(key)
    return data
