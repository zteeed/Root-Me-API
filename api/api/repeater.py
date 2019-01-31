from threading import Event, Thread

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
