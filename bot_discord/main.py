#!/usr/bin/python3

import asyncio, sys
import discord
from discord.ext import commands

from bot.colors import grey, red, green, yellow, blue, purple, cyan
from bot.constants import token

import bot.manage.json_data as jd
from bot.manage.discord_data import get_channel


class RootMeBot():


    def __init__(self):
        """ Discord Bot to catch RootMe events made by zTeeed """
        self.bot = commands.Bot(command_prefix = '!')
        self.channel = None
        self.lock = False


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
