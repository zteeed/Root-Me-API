from bot.constants import bot_channel
from discord.utils import get


def get_channel(bot):
    for server in bot.servers:
        for channel in server.channels:
            if str(channel) == bot_channel:
                return channel
    return None


def get_emoji(bot, emoji):
    return get(bot.get_all_emojis(), name=emoji)
