from . import Controller
from pyLabJackView.view.main import MainWindow
from pyLabJackView.view.plot import PlotView


class PlotController(Controller):

    def __init__(self, app):
        super(PlotController, self).__init__(app)

    def setup(self, window=None):
        if window is None:
            window = MainWindow(self.application, self)
        self._window = window
        window.setup()
        # now add
        if not window.has_view("plot"):
            v = PlotView(window, self)
            window.add_view("plot", v)
            v.setup()

    def show(self):
        self.window.show_view('plot')

    def close(self):
        if self.window.has_view("plot"):
            self.window.get_view("plot").destroy()
            self.window.remove_view("plot")
        # clean up