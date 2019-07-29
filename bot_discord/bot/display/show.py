from datetime import datetime, timedelta
from html import unescape

import bot.manage.channel_data as cd
import bot.manage.json_data as jd
from bot.colors import blue, green, red
from bot.constants import emoji2, emoji3, emoji5, limit_size, medals
from bot.display.update import add_emoji


def display_parts(message):
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


def display_add_user(bot, name):
    """ Check if user exist in RootMe """
    if not jd.user_rootme_exists(name):
        tosend = f'RootMe profile for {name} can\'t be established'
        return add_emoji(bot, f'RootMe profile for {name} can\'t be established', emoji3)

    """ Add user to data.json """
    if jd.user_json_exists(name):
        return add_emoji(bot, f'User {name} already exists in team', emoji5)
    else:
        jd.create_user(name)
        return add_emoji(bot, f'User {name} successfully added in team', emoji2)


def display_remove_user(bot, name):
    """ Remove user from data.json """
    if not jd.user_json_exists(name):
        return add_emoji(bot, f'User {name} was not in team', emoji5)
    else:
        jd.delete_user(name)
        return add_emoji(bot, f'User {name} successfully removed from team', emoji2)


def display_scoreboard():
    tosend = ''
    users = jd.select_users()
    if not users:
        return '```No users in team, you might add some with !add_user <username>```'
    scores = jd.get_scores(users)
    for rank, d in enumerate(scores):
        user, score = d['name'], d['score']
        if rank < len(medals):
            tosend += f'{medals[rank]} {user} --> Score = {score} \n'
        else:
            tosend += f' • • • {user} --> Score = {score} \n'

    return tosend


def display_categories():
    tosend = ''
    for c in jd.get_categories():
        tosend += f' • {c["name"]} ({c["challenges_nb"]} challenges) \n'
    return tosend


def display_category(category):
    c = jd.get_category(category)

    if c is None:
        tosend = f'Category {category} does not exists.'
        return tosend

    tosend = ''
    for chall in c[0]['challenges']:
        tosend += f' • {unescape(chall["name"])} ({chall["value"]} points / {chall["validations_percentage"]}% of \
success / difficulty: {unescape(chall["difficulty"])}) \n'
    return tosend


def find_challenge(challenge_selected):
    for category in jd.get_categories():
        challenges = category['challenges']
        for challenge in challenges:
            if challenge['name'] == challenge_selected:
                return challenge
    return None


def user_has_solved(challenge_selected, solved_challenges):
    test = [c['name'] == challenge_selected for c in solved_challenges]
    return True in test


def display_who_solved(challenge_selected):
    challenge_found = find_challenge(challenge_selected)

    if challenge_found is None:
        return f'Challenge {challenge_selected} does not exists.'

    tosend = ''
    users = jd.select_users()
    scores = jd.get_scores(users)
    for d in scores:
        user, score = d['name'], d['score']
        solved_challenges = jd.get_solved_challenges(user)
        if solved_challenges is None:
            return None
        if user_has_solved(challenge_selected, solved_challenges):
            tosend += f' • {user}\n'
    if not tosend:
        tosend = f'Nobody solves {challenge_selected}.'
    return tosend


def display_duration(args, delay):
    if len(args) == 1:
        if not jd.user_json_exists(args[0]):
            tosend = f'User {args[0]} is not in team.\nYou might add it with !add_user <username>'
            tosend_list = [{'user': args[0], 'msg': tosend}]
            return tosend_list
        else:
            users = [args[0]]
    else:
        users = jd.select_users()

    scores = jd.get_scores(users)
    categories = jd.get_categories()
    pattern = '%Y-%m-%d %H:%M:%S'
    tosend_list = []

    for d in scores:
        tosend = ''
        user, score = d['name'], d['score']
        now = datetime.now()
        challs_selected = []

        for chall in jd.get_solved_challenges(user):
            date = datetime.strptime(chall['date'], pattern)
            diff = now - date
            if diff < delay:
                challs_selected.append(chall)

        challs_selected.reverse()
        for chall in challs_selected:
            value = find_challenge(chall['name'])['value']
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


def display_week(args):
    return display_duration(args, timedelta(weeks=1))


def display_today(args):
    return display_duration(args, timedelta(days=1))


def display_diff_one_side(user_diff, user):
    if not user_diff:
        return
    tosend = ''
    for c in user_diff:
        value = find_challenge(c['name'])['value']
        tosend += ' • {} ({} points)\n'.format(c['name'], value)
    return tosend


def display_diff(user1, user2):
    if not jd.user_json_exists(user1):
        tosend = 'User {} is not in team.'.format(user1)
        tosend_list = [{'user': user1, 'msg': tosend}]
        return tosend_list
    if not jd.user_json_exists(user2):
        tosend = 'User {} is not in team.'.format(user2)
        tosend_list = [{'user': user2, 'msg': tosend}]
        return tosend_list

    solved_user1 = jd.get_solved_challenges(user1)
    solved_user2 = jd.get_solved_challenges(user2)

    user1_diff, user2_diff = jd.get_diff(solved_user1, solved_user2)
    tosend_list = []

    tosend = display_diff_one_side(user1_diff, user1)
    tosend_list.append({'user': user1, 'msg': tosend})
    tosend = display_diff_one_side(user2_diff, user2)
    tosend_list.append({'user': user2, 'msg': tosend})

    return tosend_list


def display_diff_with(select_user):
    if not jd.user_json_exists(select_user):
        tosend = 'User {} is not in team.'.format(select_user)
        tosend_list = [{'user': select_user, 'msg': tosend}]
        return tosend_list

    tosend_list = []
    users = jd.select_users()
    for user in users:
        solved_user = jd.get_solved_challenges(user)
        solved_user_select = jd.get_solved_challenges(select_user)
        user_diff, user_diff_select = jd.get_diff(solved_user, solved_user_select)
        if user_diff:
            tosend = display_diff_one_side(user_diff, user)
            tosend_list.append({'user': user, 'msg': tosend})
    return tosend_list


async def display_flush(bot, channel):
    result = await cd.flush(bot, channel)
    if channel is None or not result:
        return 'An error occurs while trying to flush channel data.'
    return 'Data from channel has been flushed successfully.'


def next_challenge_solved(solved_user, challenge_name):
    if len(solved_user) == 1:
        return solved_user[-1]
    for key, chall in enumerate(solved_user[:-1]):
        if chall['name'] == challenge_name:
            return solved_user[1 + key]
    return None


def display_cron():
    tosend = ''
    users = jd.select_users()
    for user in users:
        last = jd.last_solved(user)
        solved_user = jd.get_solved_challenges(user)
        if not solved_user or solved_user[-1]['name'] == last:
            continue
        blue(solved_user[-1]['name'] + "  |  " + last + "\n")
        next_chall = next_challenge_solved(solved_user, last)
        if next_chall is None:
            red(f'Error with {user} user --> last chall: {last}\n')
            continue
        c = find_challenge(next_chall['name'])
        jd.update_user_last(user, c['name'])
        name = f'New challenge solved by {user}'
        green(f'{user} --> {c["name"]}')
        tosend = f' • {c["name"]} ({c["value"]} points)'
        tosend += f'\n • Difficulty: {c["difficulty"]}'
        tosend += f'\n • Date: {next_chall["date"]}'
        tosend += f'\n • New score: {next_chall["score_at_date"]}'
        return name, tosend
    return None, None
