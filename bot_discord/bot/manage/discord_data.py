from typing import Any, List, Optional

from discord.channel import TextChannel
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.utils import get

from bot.constants import bot_channel


def get_channel(bot: Bot) -> Optional[TextChannel]:
    for server in bot.guilds:
        for channel in server.channels:
            if str(channel) == bot_channel:
                return channel
    return None


def get_emoji(bot: Bot, emoji: str) -> Optional[Any]:
    return get(bot.emojis, name=emoji)


def get_command_args(context: Context) -> List[str]:
    return context.message.content.strip().split()[1:]
