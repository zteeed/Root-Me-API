import asyncio
import sys

from discord.ext import commands

import bot.display.embed as disp
from bot.api.fetch import get_categories
from bot.colors import green, red
from bot.constants import LANGS, FILENAME, bot_channel, token
from bot.database.manager import DatabaseManager
from bot.wraps import update_challenges


class RootMeBot:

    def __init__(self, db: DatabaseManager):
        """ Discord Bot to catch RootMe events made by zTeeed """
        self.db = db
        self.bot = commands.Bot(command_prefix='!')

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

        @self.bot.command(description='Show information about the project')
        async def info(context: commands.context.Context):
            """ """
            await disp.info(context)

        @self.bot.command(description='Update language used to fetch data from API.')
        async def lang(context: commands.context.Context):
            """ <lang> """
            await disp.lang(self.db, context)

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
            await disp.scoreboard(self.db, context)

        @self.bot.command(description='Show list of categories.')
        async def categories(context: commands.context.Context):
            """ """
            await disp.categories(self.db, context)

        @self.bot.command(description='Show list of challenges from a category.')
        async def category(context: commands.context.Context):
            """ <category> """
            await disp.category(self.db, context)

        @self.bot.command(description='Return who solved a specific challenge.')
        async def who_solved(context: commands.context.Context):
            """ <challenge> """
            await disp.who_solved(self.db, context)

        @self.bot.command(description='Return the number of challenges remaining for a specific user.')
        async def remain(context: commands.context.Context):
            """ <username> (<category>) """
            await disp.remain(self.db, context)

        @self.bot.command(description='Return challenges solved grouped by users for last week.')
        async def week(context: commands.context.Context):
            """ (<username>) """
            await disp.week(self.db, context)

        @self.bot.command(description='Return challenges solved grouped by users for last day.')
        async def today(context: commands.context.Context):
            """ (<username>) """
            await disp.today(self.db, context)

        @update_challenges
        @self.bot.command(description='Return difference of solved challenges between two users.')
        async def diff(context: commands.context.Context):
            """ <username1> <username2> """
            await disp.diff(self.db, context)

        @update_challenges
        @self.bot.command(description='Return difference of solved challenges between a user and all team.')
        async def diff_with(context: commands.context.Context):
            """ <username> """
            await disp.diff_with(self.db, context)

        @self.bot.command(description='Flush all data from bot channel excepted events')
        async def flush(context: commands.context.Context):
            """ """
            await disp.flush(context)

        @self.bot.command(description='Reset bot database')
        async def reset_database(context: commands.context.Context):
            """ """
            await disp.reset_database(db, context)

    def start(self):
        if token == 'token':
            red('Please update your token in ./bot/constants.py')
            sys.exit(0)
        self.catch()
        self.bot.loop.create_task(self.cron())
        self.bot.run(token)


def init_rootme_challenges():
    rootme_challenges = {}
    for lang in LANGS:
        loop = asyncio.get_event_loop()  # event loop
        future = asyncio.ensure_future(get_categories(lang))  # tasks to do
        challenges = loop.run_until_complete(future)  # loop until done
        rootme_challenges[lang] = challenges
    return rootme_challenges


if __name__ == "__main__":
    rootme_challenges = init_rootme_challenges()
    if rootme_challenges is None:
        red('Cannot fetch RootMe challenges from the API.')
        sys.exit(0)
    db = DatabaseManager(FILENAME, rootme_challenges)
    bot = RootMeBot(db)
    bot.start()
