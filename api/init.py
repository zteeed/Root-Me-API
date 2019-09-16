import aioredis

from api.constants import REDIS_STREAM_USERS, REDIS_STREAM_CHALLENGES, CONSUMER_GROUP_NAME


async def create_cg(redis_app, stream, group_name, latest_id='$', mkstream=False):
    #  aioredis==1.2.0 install via pip does not support mkstream option on xgroup_create (see github repository)
    args = [b'CREATE', stream, group_name, latest_id]
    if mkstream:
        args.append(b'MKSTREAM')
    await redis_app.execute(b'XGROUP', *args)


async def create_cgs(redis_app):
    for stream in [REDIS_STREAM_CHALLENGES, REDIS_STREAM_USERS]:
        try:
            await create_cg(redis_app, stream, CONSUMER_GROUP_NAME, mkstream=True)
        except aioredis.errors.ReplyError as exception:
            if 'BUSYGROUP Consumer Group name already exists' == str(exception):
                pass
            else:
                raise exception
