
from . import Controller
from pyLabJackView.model.random import RandomXYModel
from pyLabJackView.controller.plot import PlotControllerThread
from pyLabJackView.view.main import MainWindow, MainView
from pyLabJackView.view.plot import PlotView

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
        self.window.show()

    def close(self):
        self.window.close()

    def load_main_view(self):
        """Creates a main view if necessary.

        :return:
        :rtype: pyLabJackView.view.main.MainView
        """
        if not self.window.has_view("main"):
            v = MainView(self.window, self)
            self.window.add_view("main", v)
            v.setup()
        return self.window.has_view("main")

    def load_plot_view(self):
        """Creates a plot view if necessary.

        :return:
        :rtype: pyLabJackView.view.plot.PlotView
        """
        if self._plot is None:
            self._plot = PlotControllerThread(self.application, self.window)
            self._plot.model = RandomXYModel(self._plot)
            self._plot.setup()
            self._plot.start()
        if not self.window.has_view("plot"):
            v = PlotView(self.window, self._plot)
            self.window.add_view("plot", v)
            v.setup()
        return self.window.has_view("plot")

    def show_main(self):
        # stop PlotController
        if self._plot is not None:
            self._plot.close()
        self.load_main_view()
        self.window.show_view("main")

    def show_plot(self):
        # load PlotController
        self.load_plot_view()
        self.window.show_view("plot")
