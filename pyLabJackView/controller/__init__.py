"""Define a basic controller"""

from pyLabJackView.model import Model
from pyLabJackView import ThreadSafeObject


class Controller(ThreadSafeObject):

    def __init__(self, app, window=None, model=None):
        super(Controller, self).__init__()
        self._app = app
        # handle to the window (main responsible view)
        self._window = window
        # handle to the model
        self._model = model

    def __del__(self):
        self.close()

    def setup(self):
        """Configures the controller (set-up model, window)"""
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    def hide(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    @property
    def application(self):
        """Return reference to the application object

        :rtype: pyLabJackView.app.LabJackViewApp
        """
        return self._app

    @property
    def window(self):
        """Return the window

        :rtype: pyLabJackView.view.Window
        """
        return self._window

    @property
    def model(self):
        """Return the model

        """
        return self._model

    @model.setter
    def model(self, model):
        if not isinstance(model, Model):
            raise ValueError("Invalid model")
        self._model = model
