
from plot import PlotController
from . import Controller
from pyLabJackView.view.main import MainWindow


class MainController(Controller):

    def __init__(self, app):
        super(MainController, self).__init__(app)

    def setup(self):
        w = MainWindow(self.application, self)
        self._window = w
        w.setup()

    def show(self):
        self.window.show()

    def close(self):
        self.window.close()

    def goto_plot(self):
        p = PlotController(self.application)
        p.setup(self.window)
        p.show()
