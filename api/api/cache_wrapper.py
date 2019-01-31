from functools import wraps

from api.app import cache


def cached(**decorator_kwargs):
    updating = [False]

    def should_update():
        return updating[0]

    def cache_decorator(f):
        f = cache.cached(forced_update=should_update, **decorator_kwargs)(f)

        @wraps(f)
        def func_wrapper(*args, cache_refresh=False, **kwargs):
            updating[0] = cache_refresh
            return f(*args, **kwargs)

        return func_wrapper

    return cache_decorator
