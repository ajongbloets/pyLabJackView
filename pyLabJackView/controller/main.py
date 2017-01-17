
from . import Controller
from pyLabJackView.controller.plot import PlotController
from pyLabJackView.controller.labjack import LabJackController
from pyLabJackView.view.main import MainWindow

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class MainController(Controller):

    def __init__(self, app, window=None, model=None):
        super(MainController, self).__init__(app, window=window, model=model)
        self._plot = None

    def setup(self, window=None):
        if window is None:
            window = MainWindow(self.application, self)
        self._window = window
        self.window.setup()

    def show(self):
        """What show we do to show the window"""
        self.window.show()
        self.show_main()

    def close(self):
        self.window.remove_view("main")
        self.window.close()

    def load_plot_view(self):
        """Creates a plot view if necessary.

        :return:
        :rtype: pyLabJackView.view.plot.PlotView
        """
        if not self.application.has_controller("plot"):
            c = PlotController(self.application, self.window)
            self.application.add_controller("plot", c)
            c.setup()
        return self.application.has_controller("plot")

    def load_labjack_view(self):
        if not self.application.has_controller("labjack"):
            c = LabJackController(self.application, self.window)
            self.application.add_controller("labjack", c)
            c.setup()
        return self.application.has_controller("labjack")

    def show_main(self):
        self.window.show_view("main")

    def show_labjack(self):
        self.load_labjack_view()
        self.application.get_controller("labjack").show()

    def show_plot(self):
        self.load_plot_view()
        self.application.get_controller("plot").show()
