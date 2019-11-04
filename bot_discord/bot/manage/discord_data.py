from typing import Any, List, Optional

from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.utils import get


def get_emoji(bot: Bot, emoji: str) -> Optional[Any]:
    return get(bot.emojis, name=emoji)


def get_command_args(context: Context) -> List[str]:
    return context.message.content.strip().split()[1:]
