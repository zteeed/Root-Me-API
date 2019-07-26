import sys
from html import unescape

import discord

import bot.display.show as show
import bot.manage.started_data as sd
from bot.colors import green, red, yellow
from bot.constants import bot_channel


def display(part):
    lines = part.split('\n')
    for line in lines:
        yellow(line)


async def interrupt(self, message, **kwargs):
    parts = show.display_parts(message)
    for part in parts:

        display(part)
        if 'embed_color' not in kwargs or 'embed_name' not in kwargs:
            await self.bot.send_message(self.channel, part)
        else:
            embed_color, embed_name = kwargs['embed_color'], kwargs['embed_name']
            embed = discord.Embed(color=embed_color)
            embed.add_field(name=embed_name, value=part, inline=False)
            await self.bot.send_message(self.channel, embed=embed)

    self.lock = False
    return


def check(self):
    if self.channel is None:
        red('{} is not a valid channel name'.format(bot_channel))
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


async def add_user(self, args):
    self.lock = True

    if len(args) != 1:
        tosend = 'Use !add_user <username>'
        await interrupt(self, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend = show.display_add_user(self.bot, args[0])
    await interrupt(self, tosend, embed_color=0x16B841, embed_name="Add user")


async def remove_user(self, args):
    self.lock = True

    if len(args) != 1:
        tosend = 'Use !remove_user <username>'
        await interrupt(self, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend = show.display_remove_user(self.bot, args[0])
    await interrupt(self, tosend, embed_color=0xD81D32, embed_name="Remove user")


async def scoreboard(self):
    self.lock = True
    tosend = show.display_scoreboard()
    await interrupt(self, tosend, embed_color=0x4200d4, embed_name="Scoreboard")


async def categories(self):
    self.lock = True
    tosend = show.display_categories()
    await interrupt(self, tosend, embed_color=0xB315A8, embed_name="Categories")


async def category(self, args):
    self.lock = True

    if len(args) != 1:
        tosend = 'Use !category <category>'
        await interrupt(self, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend = show.display_category(args[0])
    embed_name = "Category {}".format(args[0])
    await interrupt(self, tosend, embed_color=0xB315A8, embed_name=embed_name)


async def who_solved(self, ctx):
    self.lock = True

    challenge = ' '.join(ctx.message.content.strip().split(' ')[1:])
    challenge_selected = unescape(challenge.strip())
    if not challenge_selected:
        tosend = 'Use !who_solved <challenge>'
        await interrupt(self, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend = show.display_who_solved(challenge_selected)
    embed_name = "Who solved {} ?".format(challenge_selected)
    await interrupt(self, tosend, embed_color=0x29C1C5, embed_name=embed_name)


async def display_by_blocks_duration(self, tosend_list, color, **kwargs):
    for block in tosend_list:
        red(block)
        tosend = block['msg']

        if block['user'] is None:
            embed_name = "Challenges solved {}".format(kwargs['duration_msg'])
            tosend = tosend_list[0]['msg']
            await interrupt(self, tosend, embed_color=color, embed_name=embed_name)
            return

        if tosend:
            embed_name = ("Challenges solved by {} "
                          "{}".format(block['user'], kwargs['duration_msg']))
            await interrupt(self, tosend, embed_color=color, embed_name=embed_name)


async def duration(self, args, **kwargs):
    self.lock = True

    if len(args) > 1:
        tosend = 'Use !{} (<username>)'.format(kwargs['duration_command'])
        await interrupt(self, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    if kwargs['duration_command'] == 'week':
        tosend_list = show.display_week(args)
    elif kwargs['duration_command'] == 'today':
        tosend_list = show.display_today(args)
    else:
        return
    await display_by_blocks_duration(self, tosend_list, 0x00C7FF, **kwargs)


async def week(self, args):
    await duration(self, args, duration_command='week', duration_msg='last week')


async def today(self, args):
    await duration(self, args, duration_command='today', duration_msg='since last 24h')


async def display_by_blocks_diff(self, tosend_list, color, **kwargs):
    for block in tosend_list:
        if block['msg']:
            embed_name = "Challenges solved by {} ".format(block['user'])
            await interrupt(self, block['msg'], embed_color=color, embed_name=embed_name)


async def diff(self, args):
    self.lock = True

    if len(args) != 2:
        tosend = 'Use !diff <username1> <username2>'
        await interrupt(self, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend_list = show.display_diff(args[0], args[1])
    await display_by_blocks_diff(self, tosend_list, 0xFF00FF)


async def diff_with(self, args):
    self.lock = True

    if len(args) != 1:
        tosend = 'Use !diff_with <username>'
        await interrupt(self, tosend, embed_color=0xD81948, embed_name="ERROR")
        return

    tosend_list = show.display_diff_with(args[0])
    await display_by_blocks_diff(self, tosend_list, 0xFF00FF)


async def flush(self):
    self.lock = True

    tosend = await show.display_flush(self.bot, self.channel)
    embed_color, embed_name = 0xB315A8, 'Flushing channel'
    await interrupt(self, tosend, embed_color=embed_color, embed_name=embed_name)


async def cron(self):
    self.lock = True
    name, tosend_cron = show.display_cron()
    if tosend_cron is not None:
        await interrupt(self, tosend_cron, embed_color=0xFFCC00, embed_name=name)
    self.lock = False
