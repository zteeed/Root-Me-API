from datetime import datetime, timedelta
from html import unescape
from typing import Dict, List, Optional, Tuple, Union

from discord.channel import TextChannel
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context

import bot.manage.channel_data as channel_data
import bot.manage.json_data as json_data
from bot.colors import blue, green, red
from bot.constants import emoji2, emoji3, emoji5, limit_size, medals
from bot.display.update import add_emoji
from bot.wraps import stop_if_args_none


def display_parts(message: str) -> List[str]:
    message = message.split('\n')
    tosend = ''
    stored = []
    for part in message:
        if len(tosend + part + '\n') >= limit_size:
            stored.append(tosend)
            tosend = ''
        tosend += part + '\n'
    stored.append(tosend)
    return stored


def display_add_user(bot: Bot, name: str) -> str:
    """ Check if user exist in RootMe """
    if not json_data.user_rootme_exists(name):
        tosend = f'RootMe profile for {name} can\'t be established'
        return add_emoji(bot, f'RootMe profile for {name} can\'t be established', emoji3)

    """ Add user to data.json """
    if json_data.user_json_exists(name):
        return add_emoji(bot, f'User {name} already exists in team', emoji5)
    else:
        json_data.create_user(name)
        return add_emoji(bot, f'User {name} successfully added in team', emoji2)


def display_remove_user(bot: Bot, name: str) -> str:
    """ Remove user from data.json """
    if not json_data.user_json_exists(name):
        return add_emoji(bot, f'User {name} was not in team', emoji5)
    else:
        json_data.delete_user(name)
        return add_emoji(bot, f'User {name} successfully removed from team', emoji2)


def display_scoreboard() -> str:
    tosend = ''
    users = json_data.select_users()
    if not users:
        return '```No users in team, you might add some with !add_user <username>```'
    scores = json_data.get_scores(users)
    for rank, d in enumerate(scores):
        user, score = d['name'], d['score']
        if rank < len(medals):
            tosend += f'{medals[rank]} {user} --> Score = {score} \n'
        else:
            tosend += f' • • • {user} --> Score = {score} \n'

    return tosend


def display_categories() -> str:
    tosend = ''
    for c in json_data.get_categories():
        tosend += f' • {c["name"]} ({c["challenges_nb"]} challenges) \n'
    return tosend


def display_category(category: str) -> str:
    c = json_data.get_category(category)

    if c is None:
        tosend = f'Category {category} does not exists.'
        return tosend

    tosend = ''
    for chall in c[0]['challenges']:
        tosend += f' • {unescape(chall["name"])} ({chall["value"]} points / {chall["validations_percentage"]} of \
success / difficulty: {unescape(chall["difficulty"])}) \n'
    return tosend


def find_challenge(bot: Bot, challenge_selected: str) -> Optional[Dict[str, Union[str, int, List[str]]]]:
    for category in bot.rootme_challenges:
        challenges = category['challenges']
        for challenge in challenges:
            if challenge['name'] == challenge_selected:
                return challenge
    return None


def user_has_solved(challenge_selected: str, solved_challenges: List[Dict[str, Union[str, int]]]) -> bool:
    test = [c['name'] == challenge_selected for c in solved_challenges]
    return True in test


def display_who_solved(bot: Bot, challenge_selected: str) -> str:
    challenge_found = find_challenge(bot, challenge_selected)

    if challenge_found is None:
        return f'Challenge {challenge_selected} does not exists.'

    tosend = ''
    users = json_data.select_users()
    #  TODO: async requests to the API
    scores = json_data.get_scores(users)
    for d in scores:
        user, score = d['name'], d['score']
        solved_challenges = json_data.get_solved_challenges(user)
        if solved_challenges is None:
            return None
        if user_has_solved(challenge_selected, solved_challenges):
            tosend += f' • {user}\n'
    if not tosend:
        tosend = f'Nobody solves {challenge_selected}.'
    return tosend


def display_duration(context: Context, args: Tuple[str], delay: timedelta) -> List[Dict[str, Optional[str]]]:
    if len(args) == 1:
        if not json_data.user_json_exists(args[0]):
            tosend = f'User {args[0]} is not in team.\nYou might add it with ' \
                f'{context.bot.command_prefix}{context.command} {context.command.help.strip()}'
            tosend_list = [{'user': args[0], 'msg': tosend}]
            return tosend_list
        else:
            users = [args[0]]
    else:
        users = json_data.select_users()

    scores = json_data.get_scores(users)
    #  categories = json_data.get_categories()
    pattern = '%Y-%m-%d %H:%M:%S'
    tosend_list = []

    for d in scores:
        tosend = ''
        user, score = d['name'], d['score']
        now = datetime.now()
        challs_selected = []

        for chall in json_data.get_solved_challenges(user):
            date = datetime.strptime(chall['date'], pattern)
            diff = now - date
            if diff < delay:
                challs_selected.append(chall)

        challs_selected.reverse()
        for chall in challs_selected:
            value = find_challenge(context.bot, chall['name'])['value']
            tosend += f' • {chall["name"]} ({value} points) - {chall["date"]}\n'
        tosend_list.append({'user': user, 'msg': tosend})

    test = [item['msg'] == '' for item in tosend_list]
    if len(users) == 1 and False not in test:
        tosend = f'No challenges solved by {user} :frowning:'
        tosend_list = [{'user': None, 'msg': tosend}]
    elif False not in test:
        tosend = 'No challenges solved by anyone :frowning:'
        tosend_list = [{'user': None, 'msg': tosend}]

    return tosend_list


def display_week(context: Context, args: Tuple[str]) -> List[Dict[str, Optional[str]]]:
    return display_duration(context, args, timedelta(weeks=1))


def display_today(context: Context, args: Tuple[str]) -> List[Dict[str, Optional[str]]]:
    return display_duration(context, args, timedelta(days=1))


@stop_if_args_none
def display_diff_one_side(bot: Bot, user_diff: List[Dict[str, Union[str, int]]]) -> str:
    tosend = ''
    for c in user_diff:
        value = find_challenge(bot, c['name'])['value']
        tosend += f' • {c["name"]} ({value} points)\n'
    return tosend


def display_diff(bot: Bot, user1: str, user2: str) -> List[Dict[str, Optional[str]]]:
    if not json_data.user_json_exists(user1):
        tosend = f'User {user1} is not in team.'
        tosend_list = [{'user': user1, 'msg': tosend}]
        return tosend_list
    if not json_data.user_json_exists(user2):
        tosend = f'User {user2} is not in team.'
        tosend_list = [{'user': user2, 'msg': tosend}]
        return tosend_list

    solved_user1 = json_data.get_solved_challenges(user1)
    solved_user2 = json_data.get_solved_challenges(user2)

    user1_diff, user2_diff = json_data.get_diff(solved_user1, solved_user2)
    tosend_list = []

    tosend = display_diff_one_side(bot, user1_diff)
    tosend_list.append({'user': user1, 'msg': tosend})
    tosend = display_diff_one_side(bot, user2_diff)
    tosend_list.append({'user': user2, 'msg': tosend})

    return tosend_list


def display_diff_with(bot: Bot, selected_user: str):
    if not json_data.user_json_exists(selected_user):
        tosend = f'User {selected_user} is not in team.'
        tosend_list = [{'user': selected_user, 'msg': tosend}]
        return tosend_list

    tosend_list = []
    users = json_data.select_users()
    solved_user_select = json_data.get_solved_challenges(selected_user)
    for user in users:
        # TODO: make async requests on get_solved_challenges(user) to reduce delay
        solved_user = json_data.get_solved_challenges(user)
        user_diff, user_diff_select = json_data.get_diff(solved_user, solved_user_select)
        if user_diff:
            tosend = display_diff_one_side(bot, user_diff)
            tosend_list.append({'user': user, 'msg': tosend})
    return tosend_list


async def display_flush(channel: TextChannel, context: Context) -> str:
    result = await channel_data.flush(channel)
    if channel is None or not result:
        return 'An error occurs while trying to flush channel data.'
    return f'Data from channel has been flushed successfully by {context.author}.'


def next_challenge_solved(solved_user: List[Dict[str, Union[str, int]]], challenge_name: str) \
        -> Optional[Dict[str, Union[str, int]]]:
    if len(solved_user) == 1:
        return solved_user[-1]
    for key, chall in enumerate(solved_user[:-1]):
        if chall['name'] == challenge_name:
            return solved_user[1 + key]
    return None


def display_cron(bot: Bot) -> Tuple[Optional[str], Optional[str]]:
    users = json_data.select_users()
    for user in users:
        last = json_data.last_solved(user)
        solved_user = json_data.get_solved_challenges(user)
        if not solved_user or solved_user[-1]['name'] == last:
            continue
        blue(solved_user[-1]['name'] + "  |  " + last + "\n")
        next_chall = next_challenge_solved(solved_user, last)
        if next_chall is None:
            red(f'Error with {user} user --> last chall: {last}\n')
            continue
        name = f'New challenge solved by {user}'
        c = find_challenge(bot, next_chall['name'])
        green(f'{user} --> {c["name"]}')
        tosend = f' • {c["name"]} ({c["value"]} points)'
        tosend += f'\n • Difficulty: {c["difficulty"]}'
        tosend += f'\n • Date: {next_chall["date"]}'
        tosend += f'\n • New score: {next_chall["score_at_date"]}'
        json_data.update_user_last(user, c['name'])
        return name, tosend
    return None, None
