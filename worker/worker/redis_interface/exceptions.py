class RootMeException(BaseException):
    def __init__(self, error):
        self.err_code = error
