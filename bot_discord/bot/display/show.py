from html import unescape
import bot.manage.json_data as jd
from bot.constants import emoji1, emoji2, emoji3, emoji4, emoji5
from bot.display.update import add_emoji


def display_parts(message):
    message = message.split('\n')
    tosend = ''
    stored = []
    for part in message:
        if len(tosend + part + '\n') >= 2000:
            stored.append(tosend)
            tosend = ''
        tosend += part + '\n'
    stored.append(tosend)
    return stored


def display_add_user(bot, name):
    """ Check if user exist in RootMe """
    if not jd.user_rootme_exists(name):
        tosend = 'RootMe profile for {} can\'t be established'.format(name)
        return add_emoji(bot, 'RootMe profile for {} '
              'can\'t be established'.format(name), emoji3)

    """ Add user to data.json """
    if jd.user_json_exists(name):
        return add_emoji(bot, 'User {} already '
              'exists in team'.format(name), emoji5)
    else:
        jd.create_user(name)
        return add_emoji(bot, 'User {} successfully '
               'added in team'.format(name), emoji2)


def display_remove_user(bot, name):
    """ Remove user from data.json """
    if not jd.user_json_exists(name):
        return add_emoji(bot, 'User {} was not in team'.format(name), emoji5)
    else:
        jd.delete_user(name)
        return add_emoji(bot, 'User {} successfully removed '
               'from team'.format(name),  emoji2)


def display_scoreboard(users):
    tosend = ''
    scores = jd.get_scores(users)
    for rank, d in enumerate(scores):
        user, score = d['name'], d['score']
        tosend += '-{}: {} --> Score = {} \n'.format(1+rank, user, score)
    return tosend


def display_categories():
    tosend = ''
    for c in jd.get_categories():
        tosend += '- {} ({} challenges) \n'.format(c['name'], c['challenges_nb'])
    return tosend


def display_category(category):
    c = jd.get_category(category)

    if c is None:
        tosend = 'Category {} does not exists.'.format(category)
        return tosend

    tosend = ''
    for chall in c[0]['challenges']:
        tosend += ('- {} ({} points / {}% of success / difficulty: {}) '
        '\n'.format(unescape(chall['name']), chall['value'],
                    chall['validations_percentage'], 
                    unescape(chall['difficulty'])))
    return tosend


