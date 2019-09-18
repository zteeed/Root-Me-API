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


async def interrupt(self, message, embed_color=None, embed_name=None):
    parts = show.display_parts(message)
    for part in parts:

        display(part)
        if embed_color is None or embed_name is None:
            await self.bot.send_message(self.channel, part)
        else:
            embed = discord.Embed(color=embed_color)
            embed.add_field(name=embed_name, value=part, inline=False)
            await self.channel.send(embed=embed)


def check(self):
    if self.channel is None:
        red(f'{bot_channel} is not a valid channel name')
        red('Please update the channel name used by the bot '
            'in ./bot/constants.py')
        sys.exit(0)

    if sd.default() is None:
        red('Can\'t connect to API, please update URL in '
            './bot/constants.py')
        sys.exit(0)


async def ready(self):
    check(self)
    green('RootMeBot is coming !')

    if not sd.is_first():
        tosend = 'Hello back !'
    else:
        sd.launched()
        tosend = ('Hello, it seems that it\'s the first time you are '
                  'using my services.\nYou might use `!help` to know '
                  'more about my features.')

    embed_color, embed_name = 0x000000, "RootMe Bot"
    await interrupt(self, tosend, embed_color=embed_color, embed_name=embed_name)


async def add_user(self, context):
    args = get_command_args(context)

    if len(args) != 1:
        tosend = 'Use !add_user <username>'
        await interrupt(self, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend = show.display_add_user(self.bot, args[0])
    await interrupt(self, tosend, embed_color=0x16B841, embed_name="Add user")


async def remove_user(self, context):
    args = get_command_args(context)

    if len(args) != 1:
        tosend = 'Use !remove_user <username>'
        await interrupt(self, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend = show.display_remove_user(self.bot, args[0])
    await interrupt(self, tosend, embed_color=0xD81D32, embed_name="Remove user")


async def scoreboard(self):
    tosend = show.display_scoreboard()
    await interrupt(self, tosend, embed_color=0x4200d4, embed_name="Scoreboard")


async def categories(self):
    tosend = show.display_categories()
    await interrupt(self, tosend, embed_color=0xB315A8, embed_name="Categories")


async def category(self, context):
    args = get_command_args(context)

    if len(args) != 1:
        tosend = 'Use !category <category>'
        await interrupt(self, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend = show.display_category(args[0])
    embed_name = f"Category {args[0]}"
    await interrupt(self, tosend, embed_color=0xB315A8, embed_name=embed_name)


async def who_solved(self, context):
    challenge = ' '.join(context.message.content.strip().split(' ')[1:])
    challenge_selected = unescape(challenge.strip())
    if not challenge_selected:
        tosend = 'Use !who_solved <challenge>'
        await interrupt(self, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend = show.display_who_solved(self.bot, challenge_selected)
    embed_name = f"Who solved {challenge_selected} ?"
    await interrupt(self, tosend, embed_color=0x29C1C5, embed_name=embed_name)


async def display_by_blocks_duration(self, tosend_list, color, duration_msg=''):
    for block in tosend_list:
        red(block)
        tosend = block['msg']

        if block['user'] is None:
            embed_name = f"Challenges solved {duration_msg}"
            tosend = tosend_list[0]['msg']
            await interrupt(self, tosend, embed_color=color, embed_name=embed_name)
            return

        if tosend:
            embed_name = f"Challenges solved by {block['user']} {duration_msg}"
            await interrupt(self, tosend, embed_color=color, embed_name=embed_name)


async def duration(self, context, duration_command='today', duration_msg='since last 24h'):
    args = get_command_args(context)

    if len(args) > 1:
        tosend = f'Use !{duration_command} (<username>)'
        await interrupt(self, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    if duration_command == 'week':
        tosend_list = show.display_week(self.bot, args)
    elif duration_command == 'today':
        tosend_list = show.display_today(self.bot, args)
    else:
        return
    await display_by_blocks_duration(self, tosend_list, 0x00C7FF, duration_msg=duration_msg)


async def week(self, context):
    await duration(self, context, duration_command='week', duration_msg='last week')


async def today(self, context):
    await duration(self, context, duration_command='today', duration_msg='since last 24h')


async def display_by_blocks_diff(self, tosend_list, color):
    for block in tosend_list:
        if block['msg']:
            embed_name = f"Challenges solved by {block['user']} "
            await interrupt(self, block['msg'], embed_color=color, embed_name=embed_name, keep_locking=True)


async def diff(self, context):
    args = get_command_args(context)

    if len(args) != 2:
        tosend = 'Use !diff <username1> <username2>'
        await interrupt(self, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    pseudo1, pseudo2 = args[0], args[1]
    tosend_list = show.display_diff(self.bot, pseudo1, pseudo2)
    await display_by_blocks_diff(self, tosend_list, 0xFF00FF)


async def diff_with(self, context):
    args = get_command_args(context)

    if len(args) != 1:
        tosend = 'Use !diff_with <username>'
        await interrupt(self, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    pseudo = args[0]
    tosend_list = show.display_diff_with(self.bot, pseudo)
    await display_by_blocks_diff(self, tosend_list, 0xFF00FF)


async def flush(self, context):
    embed_color, embed_name = 0xD81948, 'FLUSH'
    tosend = f'{context.author} just launched !flush command.'
    await interrupt(self, tosend, embed_color=embed_color, embed_name=embed_name)
    tosend = await show.display_flush(self.channel, context)
    await interrupt(self, tosend, embed_color=embed_color, embed_name=embed_name)


async def cron(self):
    name, tosend_cron = show.display_cron(self.bot)
    if tosend_cron is not None:
        await interrupt(self, tosend_cron, embed_color=0xFFCC00, embed_name=name)
