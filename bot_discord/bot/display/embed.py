import sys
from html import unescape

import discord

import bot.display.show as show
import bot.manage.started_data as sd
from bot.colors import green, red, yellow
from bot.constants import bot_channel
from bot.manage.discord_data import get_command_args


def display(part):
    lines = part.split('\n')
    for line in lines:
        yellow(line)


async def interrupt(channel, message, embed_color=None, embed_name=None):
    if str(channel) != bot_channel:
        return
    parts = show.display_parts(message)
    for part in parts:
        display(part)
        if embed_color is None or embed_name is None:
            await channel.send(part)
        else:
            embed = discord.Embed(color=embed_color)
            embed.add_field(name=embed_name, value=part, inline=False)
            await channel.send(embed=embed)


def check(channel):
    if channel is None:
        red(f'{bot_channel} is not a valid channel name')
        red('Please update the channel name used by the bot '
            'in ./bot/constants.py')
        sys.exit(0)

    if sd.default() is None:
        red('Can\'t connect to API, please update URL in '
            './bot/constants.py')
        sys.exit(0)


async def ready(channel, command_prefix):
    check(channel)
    green('RootMeBot is coming !')

    if not sd.is_first():
        tosend = 'Hello back !'
    else:
        sd.launched()
        tosend = f"Hello, it seems that it's the first time you are using my services.\nYou might use " \
            f"`{command_prefix}help` to know more about my features."

    embed_color, embed_name = 0x000000, "RootMe Bot"
    await interrupt(channel, tosend, embed_color=embed_color, embed_name=embed_name)


async def add_user(context):
    args = get_command_args(context)

    if len(args) != 1:
        tosend = f'Use {context.bot.command_prefix}{context.command} {context.command.help.strip()}'
        await interrupt(context.message.channel, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend = show.display_add_user(context.bot, args[0])
    await interrupt(context.message.channel, tosend, embed_color=0x16B841, embed_name="Add user")


async def remove_user(context):
    args = get_command_args(context)

    if len(args) != 1:
        tosend = f'Use {context.bot.command_prefix}{context.command} {context.command.help.strip()}'
        await interrupt(context.message.channel, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend = show.display_remove_user(context.bot, args[0])
    await interrupt(context.message.channel, tosend, embed_color=0xD81D32, embed_name="Remove user")


async def scoreboard(context):
    tosend = show.display_scoreboard()
    await interrupt(context.message.channel, tosend, embed_color=0x4200d4, embed_name="Scoreboard")


async def categories(context):
    tosend = show.display_categories()
    await interrupt(context.message.channel, tosend, embed_color=0xB315A8, embed_name="Categories")


async def category(context):
    args = get_command_args(context)

    if len(args) != 1:
        tosend = f'Use {context.bot.command_prefix}{context.command} {context.command.help.strip()}'
        await interrupt(context.message.channel, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend = show.display_category(args[0])
    embed_name = f"Category {args[0]}"
    await interrupt(context.message.channel, tosend, embed_color=0xB315A8, embed_name=embed_name)


async def who_solved(context):
    challenge = ' '.join(context.message.content.strip().split(' ')[1:])
    challenge_selected = unescape(challenge.strip())
    if not challenge_selected:
        tosend = f'Use {context.bot.command_prefix}{context.command} {context.command.help.strip()}'
        await interrupt(context.message.channel, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend = show.display_who_solved(context.bot, challenge_selected)
    embed_name = f"Who solved {challenge_selected} ?"
    await interrupt(context.message.channel, tosend, embed_color=0x29C1C5, embed_name=embed_name)


async def display_by_blocks_duration(context, tosend_list, color, duration_msg=''):
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


async def duration(context, duration_command='today', duration_msg='since last 24h'):
    args = get_command_args(context)

    if len(args) > 1:
        tosend = f'Use !{duration_command} (<username>)'
        await interrupt(context.message.channel, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    if duration_command == 'week':
        tosend_list = show.display_week(context, args)
    elif duration_command == 'today':
        tosend_list = show.display_today(context, args)
    else:
        return
    await display_by_blocks_duration(context, tosend_list, 0x00C7FF, duration_msg=duration_msg)


async def week(context):
    await duration(context, duration_command='week', duration_msg='last week')


async def today(context):
    await duration(context, duration_command='today', duration_msg='since last 24h')


async def display_by_blocks_diff(channel, tosend_list, color):
    for block in tosend_list:
        if block['msg']:
            embed_name = f"Challenges solved by {block['user']} "
            await interrupt(channel, block['msg'], embed_color=color, embed_name=embed_name, keep_locking=True)


async def diff(context):
    args = get_command_args(context)

    if len(args) != 2:
        tosend = f'Use {context.bot.command_prefix}{context.command} {context.command.help.strip()}'
        await interrupt(context.message.channel, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    pseudo1, pseudo2 = args[0], args[1]
    tosend_list = show.display_diff(context.bot, pseudo1, pseudo2)
    await display_by_blocks_diff(context.message.channel, tosend_list, 0xFF00FF)


async def diff_with(context):
    args = get_command_args(context)

    if len(args) != 1:
        tosend = f'Use {context.bot.command_prefix}{context.command} {context.command.help.strip()}'
        await interrupt(context.message.channel, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    pseudo = args[0]
    tosend_list = show.display_diff_with(context.bot, pseudo)
    await display_by_blocks_diff(context.message.channel, tosend_list, 0xFF00FF)


async def flush(context):
    embed_color, embed_name = 0xD81948, 'FLUSH'
    tosend = f'{context.author} just launched {context.bot.command_prefix}{context.command} command.'
    await interrupt(context.message.channel, tosend, embed_color=embed_color, embed_name=embed_name)
    tosend = await show.display_flush(context.message.channel, context)
    await interrupt(context.message.channel, tosend, embed_color=embed_color, embed_name=embed_name)


async def cron(self):
    name, tosend_cron = show.display_cron(self.bot)
    if tosend_cron is not None:
        await interrupt(self, tosend_cron, embed_color=0xFFCC00, embed_name=name)
