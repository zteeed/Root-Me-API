from html import unescape
from typing import Dict, List, Optional

import discord
from discord.channel import TextChannel
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from discord.guild import Guild

import bot.display.show as show
from bot.colors import green, red, yellow
from bot.constants import bot_channel, PROJECT_INFORMATION
from bot.database.manager import DatabaseManager
from bot.manage.discord_data import get_command_args


def display(part: str) -> None:
    lines = part.split('\n')
    for line in lines:
        yellow(line)


async def interrupt(channel: TextChannel, message: str, embed_color: Optional[int] = None,
                    embed_name: Optional[str] = None) -> None:
    if str(channel) != bot_channel or not message:
        return
    parts = show.display_parts(message)
    for part in parts:
        display(part)
        if embed_color is None or embed_name is None:
            await channel.send(part)
        else:
            embed = discord.Embed(color=embed_color)
            embed.add_field(name=embed_name, value=part, inline=False)
            embed.set_footer(text=PROJECT_INFORMATION['footer'])
            await channel.send(embed=embed)


async def info(context: Context) -> None:
    title = PROJECT_INFORMATION['title']
    tosend = PROJECT_INFORMATION['content']
    await interrupt(context.message.channel, tosend, embed_color=0xF4900C, embed_name=title)


async def lang(db: DatabaseManager, context: Context) -> None:
    args = get_command_args(context)

    if len(args) != 1:
        tosend = f'Use {context.bot.command_prefix}{context.command} {context.command.help.strip()}'
        await interrupt(context.message.channel, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend, response = await show.display_lang_check(db, context.guild.id, context.bot, args[0])
    await interrupt(context.message.channel, tosend, embed_color=0x16B841, embed_name="Update lang")
    if response:
        tosend = await show.display_lang(db, context.guild.id, context.bot, args[0])
        await interrupt(context.message.channel, tosend, embed_color=0x16B841, embed_name="Update lang")


async def add_user(db: DatabaseManager, context: Context) -> None:
    args = get_command_args(context)

    if len(args) != 1:
        tosend = f'Use {context.bot.command_prefix}{context.command} {context.command.help.strip()}'
        await interrupt(context.message.channel, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend = await show.display_add_user(db, context.guild.id, context.bot, args[0])
    await interrupt(context.message.channel, tosend, embed_color=0x16B841, embed_name="Add user")


async def remove_user(db: DatabaseManager, context: Context) -> None:
    args = get_command_args(context)

    if len(args) != 1:
        tosend = f'Use {context.bot.command_prefix}{context.command} {context.command.help.strip()}'
        await interrupt(context.message.channel, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend = await show.display_remove_user(db, context.guild.id, context.bot, args[0])
    await interrupt(context.message.channel, tosend, embed_color=0xD81D32, embed_name="Remove user")


async def scoreboard(db: DatabaseManager, context: Context) -> None:
    users = await db.select_users(context.guild.id)
    if not users:
        tosend = f'No users in team, you might add some with ' \
            f'{context.bot.command_prefix}{context.command} {context.command.help.strip()}'
    else:
        tosend = await show.display_scoreboard(db, context.guild.id)
    await interrupt(context.message.channel, tosend, embed_color=0x4200d4, embed_name="Scoreboard")


async def categories(db: DatabaseManager, context: Context) -> None:
    lang = await db.get_server_language(context.guild.id)
    tosend = await show.display_categories(lang)
    await interrupt(context.message.channel, tosend, embed_color=0xB315A8, embed_name="Categories")


async def category(db: DatabaseManager, context: Context) -> None:
    lang = await db.get_server_language(context.guild.id)
    args = get_command_args(context)

    if len(args) != 1:
        tosend = f'Use {context.bot.command_prefix}{context.command} {context.command.help.strip()}'
        await interrupt(context.message.channel, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend = await show.display_category(lang, args[0])
    embed_name = f"Category {args[0]}"
    await interrupt(context.message.channel, tosend, embed_color=0xB315A8, embed_name=embed_name)


async def who_solved(db: DatabaseManager, context: Context) -> None:
    challenge = ' '.join(context.message.content.strip().split(' ')[1:])
    challenge_selected = unescape(challenge.strip())
    if not challenge_selected:
        tosend = f'Use {context.bot.command_prefix}{context.command} {context.command.help.strip()}'
        await interrupt(context.message.channel, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend = await show.display_who_solved(db, context.guild.id, challenge_selected)
    embed_name = f"Who solved {challenge_selected} ?"
    await interrupt(context.message.channel, tosend, embed_color=0x29C1C5, embed_name=embed_name)


async def remain(db: DatabaseManager, context: Context) -> None:
    args = get_command_args(context)
    if len(args) < 1 or len(args) > 2:
        tosend = f'Use {context.bot.command_prefix}{context.command} {context.command.help.strip()}'
        await interrupt(context.message.channel, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    username = args[0]
    if len(args) == 1:
        embed_name = f"Challenges remaining for {username}"
        tosend = await show.display_remain(db, context.guild.id, context.bot, username)
    else:
        category = args[1]
        embed_name = f"Challenges remaining in {category} for {username}"
        tosend = await show.display_remain(db, context.guild.id, context.bot, username, category=category)

    await interrupt(context.message.channel, tosend, embed_color=0x29C1C5, embed_name=embed_name)


async def display_by_blocks_duration(context: Context, tosend_list: List[str], color: int, duration_msg: str = '') \
        -> None:
    for block in tosend_list:
        red(block)
        tosend = block['msg']

        if block['user'] is None:
            embed_name = f"Challenges solved {duration_msg}"
            tosend = tosend_list[0]['msg']
            await interrupt(context.message.channel, tosend, embed_color=color, embed_name=embed_name)
            return

        if tosend:
            embed_name = f"Challenges solved by {block['user']} {duration_msg}"
            await interrupt(context.message.channel, tosend, embed_color=color, embed_name=embed_name)


async def duration(db: DatabaseManager, context: Context, duration_command: str = 'today',
                   duration_msg: str = 'since last 24h') -> None:
    args = get_command_args(context)

    if len(args) > 1:
        tosend = f'Use !{duration_command} (<username>)'
        await interrupt(context.message.channel, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    if duration_command == 'week':
        tosend_list = await show.display_week(db, context, args)
    elif duration_command == 'today':
        tosend_list = await show.display_today(db, context, args)
    else:
        return
    await display_by_blocks_duration(context, tosend_list, 0x00C7FF, duration_msg=duration_msg)


async def week(db: DatabaseManager, context: Context) -> None:
    await duration(db, context, duration_command='week', duration_msg='last week')


async def today(db: DatabaseManager, context: Context) -> None:
    await duration(db, context, duration_command='today', duration_msg='since last 24h')


async def display_by_blocks_diff(channel: TextChannel, tosend_list: List[Dict[str, str]], color: int) -> None:
    for block in tosend_list:
        if block['msg']:
            embed_name = f"Challenges solved by {block['user']} "
            await interrupt(channel, block['msg'], embed_color=color, embed_name=embed_name)


async def diff(db: DatabaseManager, context: Context) -> None:
    args = get_command_args(context)

    if len(args) != 2:
        tosend = f'Use {context.bot.command_prefix}{context.command} {context.command.help.strip()}'
        await interrupt(context.message.channel, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    pseudo1, pseudo2 = args[0], args[1]
    tosend_list = await show.display_diff(db, context.guild.id, context.bot, pseudo1, pseudo2)
    await display_by_blocks_diff(context.message.channel, tosend_list, 0xFF00FF)


async def diff_with(db: DatabaseManager, context: Context) -> None:
    args = get_command_args(context)

    if len(args) != 1:
        tosend = f'Use {context.bot.command_prefix}{context.command} {context.command.help.strip()}'
        await interrupt(context.message.channel, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    pseudo = args[0]
    tosend_list = await show.display_diff_with(db, context.guild.id, context.bot, pseudo)
    await display_by_blocks_diff(context.message.channel, tosend_list, 0xFF00FF)


async def flush(context: Context) -> None:
    embed_color, embed_name = 0xD81948, 'FLUSH'
    tosend = f'{context.author} just launched {context.bot.command_prefix}{context.command} command.'
    await interrupt(context.message.channel, tosend, embed_color=embed_color, embed_name=embed_name)
    tosend = await show.display_flush(context.message.channel, context)
    await interrupt(context.message.channel, tosend, embed_color=embed_color, embed_name=embed_name)


async def reset_database(db: DatabaseManager, context: Context) -> None:
    if context.message.author != context.guild.owner:
        tosend = f'You need to be the server owner to launch {context.bot.command_prefix}{context.command} command.'
    else:
        tosend = await show.display_reset_database(db, context.guild.id, context.bot)
    await interrupt(context.message.channel, tosend, embed_color=0x16B841, embed_name="Reset Database")


async def check_new_server(channel: TextChannel, server: Guild, db: DatabaseManager, command_prefix: str) -> None:
    if await db.is_server_registered(server.id):
        return
    green(f'RootMeBot is coming on {server.name} discord server !')
    await db.register_server(server.id)
    tosend = f"Hello, it seems that it's the first time you are using my services.\nYou might use " \
        f"`{command_prefix}help` to know more about my features."
    embed_color, embed_name = 0x000000, "RootMe Bot"
    await interrupt(channel, tosend, embed_color=embed_color, embed_name=embed_name)


async def cron(channel: TextChannel, server: Guild, db: DatabaseManager, bot: Bot) -> None:
    await check_new_server(channel, server, db, bot.command_prefix)
    name, tosend_cron = await show.display_cron(server.id, db)
    if tosend_cron is not None:
        await interrupt(channel, tosend_cron, embed_color=0xFFCC00, embed_name=name)
