import asyncio
import sys

import bot.display.embed as disp
from bot.colors import red, green
from bot.constants import token
from bot.manage.discord_data import get_channel
import bot.manage.json_data as json_data
from bot.wraps import update_challenges
from discord.ext import commands


class RootMeBot:

    def __init__(self):
        """ Discord Bot to catch RootMe events made by zTeeed """
        self.bot = commands.Bot(command_prefix='!')
        self.bot.rootme_challenges = None
        self.channel = None
        self.lock = False

    async def cron(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
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

        @self.bot.command(description='Add a user to team into database.')
        async def add_user(context):
            """ <username> """
            await disp.add_user(self, context)

        @self.bot.command(description='Remove a user from team in database.')
        async def remove_user(context):
            """ <username> """
            await disp.remove_user(self, context)

        @self.bot.command(description='Show list of users from team.')
        async def scoreboard(context):
            """ """
            await disp.scoreboard(self)

        @self.bot.command(description='Show list of categories.')
        async def categories(context):
            """ """
            await disp.categories(self)

        @self.bot.command(description='Show list of challenges from a category.')
        async def category(context):
            """ <category> """
            await disp.category(self, context)

        @self.bot.command(description='Return who solved a specific challenge.')
        async def who_solved(context):
            """ <challenge> """
            await disp.who_solved(self, context)

        @self.bot.command(description='Return challenges solved grouped by users for last week.')
        async def week(context):
            """ (<username>) """
            await disp.week(self, context)

        @self.bot.command(description='Return challenges solved grouped by users for last day.')
        async def today(context):
            """ (<username>) """
            await disp.today(self, context)

        @update_challenges
        @self.bot.command(description='Return difference of solved challenges between two users.')
        async def diff(context):
            """ <username1> <username2> """
            await disp.diff(self, context)

        @update_challenges
        @self.bot.command(description='Return difference of solved challenges between a user and all team.')
        async def diff_with(context):
            """ <username> """
            await disp.diff_with(self, context)

        @self.bot.command(description='Flush all data from bot channel excepted events')
        async def flush(context):
            """ """
            await disp.flush(self, context)

    def start(self):
        if token == 'token':
            red('Please update your token in ./bot/constants.py')
            sys.exit(0)
        result = json_data.get_categories()
        if result is None:
            red('Cannot fetch RootMe challenges from the API.')
            sys.exit(0)
        self.bot.rootme_challenges = result
        self.catch()
        self.bot.loop.create_task(self.cron())
        self.bot.run(token)


if __name__ == "__main__":
    bot = RootMeBot()
    bot.start()
