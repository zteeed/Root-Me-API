#!/usr/bin/python3

import asyncio, sys
import discord
from discord.ext import commands

from bot.colors import grey, red, green, yellow, blue, purple, cyan
from bot.constants import token
from bot.manage.discord_data import get_channel
import bot.display.embed as disp


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
                await disp.cron(self)
            else:
                red('RootMeBot locked')
            await asyncio.sleep(5)


    def catch(self):
        @self.bot.event
        async def on_ready():
            self.channel = get_channel(self.bot)
            await disp.ready(self)

        
        @self.bot.command(description = 'Add a user to team into database.') 
        async def add_user(*args):
            """ <username> """
            await disp.add_user(self, args)


        @self.bot.command(description = 'Remove a user from team in database.') 
        async def remove_user(*args):
            """ <username> """
            await disp.remove_user(self, args)


        @self.bot.command(description = 'Show list of users from team.') 
        async def scoreboard():
            """ """
            await disp.scoreboard(self)


        @self.bot.command(description = 'Show list of categories.') 
        async def categories():
            """ """
            await disp.categories(self)


        @self.bot.command(description = 'Show list of challenges from a category.') 
        async def category(*args):
            """ <category> """
            await disp.category(self, args)


        @self.bot.command(pass_context=True, description = 'Return who solved a specific challenge.') 
        async def who_solved(ctx):
            """ <challenge> """
            await disp.who_solved(self, ctx)
        

        @self.bot.command(description = 'Return challenges solved grouped by users for last week.') 
        async def week(*args):
            """ (<username>) """
            await disp.week(self, args)


        @self.bot.command(description = 'Return challenges solved grouped by users for last day.') 
        async def today(*args):
            """ (<username>) """
            await disp.today(self, args)


        @self.bot.command(description = 'Return difference of solved challenges between two users.') 
        async def diff(*args):
            """ <username1> <username2> """
            await disp.diff(self, args)


        @self.bot.command(description = 'Return difference of solved challenges between a user and all team.') 
        async def diff_with(*args):
            """ <username> """
            await disp.diff_with(self, args)


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
