from bot.colors import red, yellow

async def flush(bot, selected_channel):
    for server in bot.servers:
        channels = server.channels
        for channel in server.channels:
            if str(selected_channel) != str(channel):
                continue
            async for m in bot.logs_from(channel):
                try:
                    if m.embeds and 'fields' in m.embeds[0].keys():
                        title = m.embeds[0]['fields'][0]['name']
                        if 'New challenge solved by' not in title:
                            await bot.delete_message(m)
                    else:
                        await bot.delete_message(m)
                except Exception as exception:
                    red(exception)
                    return False
    return True
