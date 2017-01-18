from . import *
from pyLabJackView.model.random import RandomXYModel
from pyLabJackView.view.main import MainWindow
from pyLabJackView.view.plot import PlotView, LivePlotView

__author__ = "Joeri Jongbloets <joer@jongbloets.net>"


class PlotController(Controller):

    def __init__(self, app, window=None, model=None):
        if model is None:
            model = RandomXYModel()
        super(PlotController, self).__init__(app, window=window, model=model)
        self._update_interval = 1
        self._update_state = False

    @property
    def view(self):
        """

        :rtype: pyLabJackView.view.plot.LivePlotView
        """
        if not self.window.has_view("plot"):
            raise PlotControllerException("No plot view defined")
        return self.window.get_view("plot")

    @property
    def update_interval(self):
        return self._update_interval

    @update_interval.setter
    def update_interval(self, v):
        if 0 <= v <= 300:
            self._update_interval = int(v)

    @property
    def update_state(self):
        return self._update_state

    @update_state.setter
    def update_state(self, v):
        self._update_state = v is True

    def setup(self, window=None):
        if window is None:
            window = self._window
        if window is None:
            self._window = MainWindow(self.application, self)
        self.window.setup()
        # now add
        if not self.window.has_view("plot"):
            v = LivePlotView(self.window, self)
            self.window.add_view("plot", v)
            v.setup()

    def show(self):
        self.view.show()

    def start_update(self):
        self._update_state = True
        self.window.after(self.update_interval, self.update)
        return True

    def stop_update(self):
        self._update_state = False
        self.view.set_status_text("Paused")
        return True

    def update(self):
        if self.update_state:
            self.update_plot()
            self.window.after(self.update_interval * 1000, self.update)

    def update_plot(self):
        data = self.model.update()[:]
        self.view.plot.add_plot(data[0], data[1], clear=True)

    def reset_plot(self):
        self.model.reset()
        self.update_plot()

    def close(self):
        self._update_state = False
        if self.window.has_view("plot"):
            self.window.remove_view("plot")
        # clean up


class PlotControllerException(PyLabJackViewException):

    def __init__(self, msg):
        super(PlotControllerException, self).__init__(msg)