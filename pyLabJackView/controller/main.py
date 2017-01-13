
from . import Controller
from pyLabJackView.view.main import MainWindow

class MainController(Controller):

    def __init__(self, app):
        super(MainController, self).__init__(app)

    def configure(self):
        w = MainWindow(self.application, self)
        self._window = w

    def show(self):
        self.window.show()