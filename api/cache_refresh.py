from functools import wraps
from threading import Event, Thread

from flask_caching import Cache

stop_event = Event()
stop_event.set()


def stop():
    stop_event.set()


def start(func, refresh_rate):
    assert stop_event.is_set()
    stop_event.clear()

    def update_cached_endpoints():
        while True:
            func()
            stop_event.wait(refresh_rate)
            if stop_event.is_set():
                return

    Thread(target=update_cached_endpoints).start()


def cached(cache: Cache, **decorator_kwargs):
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
