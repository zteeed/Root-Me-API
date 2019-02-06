#!/usr/bin/python3

import asyncio, sys
import discord
from discord.ext import commands

from bot.colors import grey, red, green, yellow, blue, purple, cyan
from bot.constants import token

import bot.manage.started_data as sd
import bot.display.show as disp
from bot.manage.discord_data import get_channel


class RootMeBot():


    def __init__(self):
        """ Discord Bot to catch RootMe events made by zTeeed """
        self.bot = commands.Bot(command_prefix = '!')
        self.channel = None
        self.lock = False


    async def interrupt(self, message):
        parts = disp.display_parts(message) 
        for part in parts:
            lines = part.split('\n')
            for line in lines:
                yellow(line)
            await self.bot.send_message(self.channel, part)
        self.lock = False
        return


    async def cron(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            if not self.lock and self.channel is not None:
                green('RootMeBot open')
                self.lock = True
                tosend_cron = disp.display_cron()
                if tosend_cron:
                    await self.interrupt(tosend_cron)
                self.lock = False
            else:
                red('RootMeBot locked')
            await asyncio.sleep(5)


    def catch(self):
        @self.bot.event
        async def on_ready():
            self.channel = get_channel(self.bot)
            if self.channel is None:
                red('{} is not a valid channel name'.format(bot_channel))
                red('Please update the channel name used by the bot '
                    'in ./bot/constants.py')
                sys.exit(0)
            if sd.default() is None:
                red('Can\'t connect to API, please update URL in '
                    './bot/constants.py')
                sys.exit(0)
            green('RootMeBot is coming !')
            if not sd.is_first():
                tosend = 'Auto Reboot'
                await self.bot.send_message(self.channel, tosend)
            else:
                tosend = ('Hello, it seems that it\'s the first time you are ' 
                          'using my services, you might use `!help` to know '
                          'more about my features.')
                sd.launched()
                await self.bot.send_message(self.channel, tosend)

        
        @self.bot.command(description = 'Add a user to team into database.') 
        async def add_user(*args):
            """ <username> """
            self.lock = True

            if len(args) != 1:
                await self.interrupt('```ERROR, use: !add_user <username>```')
                return

            tosend = disp.display_add_user(self.bot, args[0])
            await self.interrupt(tosend)


        @self.bot.command(description = 'Remove a user from team in database.') 
        async def remove_user(*args):
            """ <username> """
            self.lock = True

            if len(args) != 1:
                await self.interrupt('```ERROR, use: !remove_user <username>```')
                return

            tosend = disp.display_remove_user(self.bot, args[0])
            await self.interrupt(tosend)


        @self.bot.command(description = 'Show list of users from team.') 
        async def scoreboard():
            """ """
            self.lock = True

            users = jd.select_users()
            if not users:
                await self.interrupt('```No users in team, you might add '
                      'some with !add_user <username>```')
                return

            tosend = disp.display_scoreboard(users)
            await self.interrupt(tosend)



        @self.bot.command(description = 'Show list of categories.') 
        async def categories():
            """ """
            self.lock = True
            tosend = disp.display_categories()
            await self.interrupt(tosend)


        @self.bot.command(description = 'Show list of challenges from a category.') 
        async def category(*args):
            """ <category> """
            self.lock = True

            if len(args) != 1:
                await self.interrupt('```ERROR, use !category <category>```')
                return

            tosend = disp.display_category(args[0])
            await self.interrupt(tosend)


        @self.bot.command(pass_context=True, description = 'Return who solved a specific challenge.') 
        async def who_solved(ctx):
            """ <challenge> """
            self.lock = True

            challenge = ' '.join(ctx.message.content.strip().split(' ')[1:])
            challenge_selected = unescape(challenge.strip())
            if not challenge_selected:
                await self.interrupt('```ERROR, use !who_solved <challenge>```')
                return

            tosend = disp.display_who_solved(challenge_selected)
            await self.interrupt(tosend)


        @self.bot.command(description = 'Return challenges solved grouped by users for last week.') 
        async def week(*args):
            """ (<username>) """
            self.lock = True

            if len(args) > 1:
                await self.interrupt('```ERROR, use !week (<username>)```')
                return

            tosend = disp.display_week(args)
            await self.interrupt(tosend)


        @self.bot.command(description = 'Return challenges solved grouped by users for last day.') 
        async def today(*args):
            """ (<username>) """
            self.lock = True

            if len(args) > 1:
                await self.interrupt('```ERROR, use !today (<username>)```')
                return

            tosend = disp.display_today(args)
            await self.interrupt(tosend)


        @self.bot.command(description = 'Return difference of solved challenges between two users.') 
        async def diff(*args):
            """ <username1> <username2> """
            self.lock = True

            if len(args) != 2:
                await self.interrupt('```ERROR, use !diff <username1> '
                                     '<username2>```')
                return

            tosend = disp.display_diff(args[0], args[1])
            await self.interrupt(tosend)


    def start(self):
        if token == 'token':
            red('Please update your token in ./bot/constants.py')
            sys.exit(0)
        self.catch()
        self.bot.loop.create_task(self.cron())
        self.bot.run(token)


if __name__ == "__main__":
    bot = RootMeBot()
    bot.start()
