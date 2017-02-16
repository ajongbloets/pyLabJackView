
from . import Controller
from pyLabJackView.controller.plot import PlotController
from pyLabJackView.controller.labjack import LabJackController
from pyLabJackView.view.main import MainWindow

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class MainController(Controller):

    def __init__(self, app, window=None, model=None):
        super(MainController, self).__init__(app, window=window, model=model)
        self._plot = None

    def _prepare(self, window=None):
        if window is None:
            window = MainWindow(self.application, self)
        self._window = window
        self.window.prepare()
        return self

    def _show(self):
        """What show we do to show the window"""
        self.window.show()
        self.show_labjack()

    def _close(self):
        self.window.remove_view("main")
        self.window.close()

    def load_plot_view(self):
        """Creates a add_plot view if necessary.

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
            c.prepare()
        return self.application.has_controller("labjack")

    def hide_main(self):
        if self.window.has_view("main"):
            self.window.hide_view("main")

    def show_main(self):
        self.hide_labjack()
        self.window.show_view("main")

    def hide_labjack(self):
        if self.window.has_view("labjack"):
            self.window.hide_view("labjack")

    def show_labjack(self):
        self.hide_main()
        self.hide_plot()
        self.load_labjack_view()
        self.application.get_controller("labjack").show()

    def hide_plot(self):
        if self.window.has_view("plot"):
            self.window.hide_view("plot")

    def show_plot(self):
        self.hide_main()
        self.hide_labjack()
        self.load_plot_view()
        self.application.get_controller("plot").show()
