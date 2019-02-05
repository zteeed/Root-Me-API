#!/usr/bin/python3

import asyncio, sys
import discord
from discord.ext import commands

from bot.colors import grey, red, green, yellow, blue, purple, cyan
from bot.constants import token

import bot.manage.json_data as jd
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
            await self.bot.send_message(self.channel, part)
        self.lock = False
        return


    async def cron(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed:
            if not self.lock and self.channel is not None:
                green('RootMeBot open')
            else:
                red('RootMeBot locked')
            await asyncio.sleep(1)


    def catch(self):
        @self.bot.event
        async def on_ready():
            self.channel = get_channel(self.bot)
            if self.channel is None:
                red('{} is not a valid channel name'.format(bot_channel))
                red('Please update the channel name used by the bot '
                    'in ./bot/constants.py')
                sys.exit(0)
            if jd.default() is None:
                red('Can\'t connect to API, please update URL in '
                    './bot/constants.py')
                sys.exit(0)
            green('RootMeBot is coming !')
            if not jd.is_first():
                tosend = 'Auto Reboot'
                await self.bot.send_message(self.channel, tosend)
            else:
                tosend = ('Hello, it seems that it\'s the first time you are ' 
                          'using my services, you might use `!help` to know '
                          'more about my features.')
                jd.launched()
                await self.bot.send_message(self.channel, tosend)

        
        @self.bot.command(description = 'add a user to team into database') 
        async def add_user(*args):
            """ <username> """
            self.lock = True

            if len(args) != 1:
                await self.interrupt('```ERROR, use: !add_user <username>```')
                return

            tosend = disp.display_add_user(self.bot, args[0])
            await self.interrupt(tosend)


        @self.bot.command(description = 'remove a user from team in database') 
        async def remove_user(*args):
            """ <username> """
            self.lock = True

            if len(args) != 1:
                await self.interrupt('```ERROR, use: !remove_user <username>```')
                return

            tosend = disp.display_remove_user(self.bot, args[0])
            await self.interrupt(tosend)


        @self.bot.command(description = 'show list of users from team') 
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
