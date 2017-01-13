"""Define a basic controller"""


class Controller(object):

    def __init__(self, app):
        self._app = app
        self._window = None

    def __del__(self):
        pass

    def configure(self):
        """Configures the controller (set-up model, window)"""
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    @property
    def application(self):
        return self._app

    @property
    def window(self):
        return self._window