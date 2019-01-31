from threading import Lock


class CacheUpdater:
    """
    Used to refresh the endpoints of the API.
    """
    def __init__(self, app):
        self._lock = Lock()
        self._forced_update = False
        self.app = app

    def force_update(self, f):
        self._forced_update = True
        self.app.logger.info("Forced updated triggered on {}".format(f))
        f()

    def should_update(self):
        with self._lock:
            if not self._forced_update:
                return False

            self._forced_update = False
            return True
