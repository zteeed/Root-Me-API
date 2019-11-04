from functools import wraps

import bot.api.fetch as json_data


def update_challenges(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        result = json_data.get_categories()
        if result is not None:
            self.bot.rootme_challenges = result
        return f(*args, **kwargs)

    return wrapper


def stop_if_args_none(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if len(args) == 0 or None in args:
            return
        return f(*args, **kwargs)

    return wrapper
