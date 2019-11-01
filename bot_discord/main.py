import asyncio
import sys
from typing import Dict, List

from discord.ext import commands

import bot.display.embed as disp
import bot.api.fetch as json_data
from bot.colors import green, red
from bot.constants import FILENAME, bot_channel, token
from bot.database.manager import DatabaseManager
from bot.wraps import update_challenges


class RootMeBot:

    def __init__(self, rootme_challenges: List[Dict[str, str]], db: DatabaseManager):
        """ Discord Bot to catch RootMe events made by zTeeed """
        self.db = db
        self.bot = commands.Bot(command_prefix='!')
        self.bot.rootme_challenges = rootme_challenges

    async def cron(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            for server in self.bot.guilds:  # loop over servers where bot is currently active
                for channel in server.channels:
                    if str(channel) == bot_channel:  # send data only in the right channel
                        await disp.cron(channel, server, self.db, self.bot)
            await asyncio.sleep(1)

    def catch(self):
        @self.bot.event
        async def on_ready():
            green('RootMeBot is starting !')

        @self.bot.command(description='Add a user to team into database.')
        async def add_user(context: commands.context.Context):
            """ <username> """
            await disp.add_user(self.db, context)

        @self.bot.command(description='Remove a user from team in database.')
        async def remove_user(context: commands.context.Context):
            """ <username> """
            await disp.remove_user(self.db, context)

        @self.bot.command(description='Show list of users from team.')
        async def scoreboard(context: commands.context.Context):
            """ """
            await disp.scoreboard(db, context)

        @self.bot.command(description='Show list of categories.')
        async def categories(context: commands.context.Context):
            """ """
            await disp.categories(context)

        @self.bot.command(description='Show list of challenges from a category.')
        async def category(context: commands.context.Context):
            """ <category> """
            await disp.category(context)

        @self.bot.command(description='Return who solved a specific challenge.')
        async def who_solved(context: commands.context.Context):
            """ <challenge> """
            await disp.who_solved(db, context)

        @self.bot.command(description='Return challenges solved grouped by users for last week.')
        async def week(context: commands.context.Context):
            """ (<username>) """
            await disp.week(db, context)

        @self.bot.command(description='Return challenges solved grouped by users for last day.')
        async def today(context: commands.context.Context):
            """ (<username>) """
            await disp.today(db, context)

        @update_challenges
        @self.bot.command(description='Return difference of solved challenges between two users.')
        async def diff(context: commands.context.Context):
            """ <username1> <username2> """
            await disp.diff(db, context)

        @update_challenges
        @self.bot.command(description='Return difference of solved challenges between a user and all team.')
        async def diff_with(context: commands.context.Context):
            """ <username> """
            await disp.diff_with(db, context)

        @self.bot.command(description='Flush all data from bot channel excepted events')
        async def flush(context: commands.context.Context):
            """ """
            await disp.flush(context)

    def start(self):
        if token == 'token':
            red('Please update your token in ./bot/constants.py')
            sys.exit(0)
        self.catch()
        self.bot.loop.create_task(self.cron())
        self.bot.run(token)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()  # event loop
    future = asyncio.ensure_future(json_data.get_categories())  # tasks to do
    rootme_challenges = loop.run_until_complete(future)  # loop until done
    if rootme_challenges is None:
        red('Cannot fetch RootMe challenges from the API.')
        sys.exit(0)
    db = DatabaseManager(FILENAME)
    bot = RootMeBot(rootme_challenges, db)
    bot.start()
