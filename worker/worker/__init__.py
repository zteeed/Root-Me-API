from structlog import get_logger


class App:

    def __init__(self):
        self.redis = None


app = App()
log = get_logger()
