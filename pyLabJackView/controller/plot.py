from . import Controller
from pyLabJackView.model.random import RandomXYModel
from pyLabJackView.view.main import MainWindow
from pyLabJackView.view.plot import PlotView

__author__ = "Joeri Jongbloets <joer@jongbloets.net>"


class PlotController(Controller):

    def __init__(self, app, window=None, model=None):
        if model is None:
            model = RandomXYModel()
        super(PlotController, self).__init__(app, window=window, model=model)
        self._update_interval = 1
        self._update_state = False

    @property
    def update_interval(self):
        return self._update_interval

    @update_interval.setter
    def update_interval(self, v):
        if 0 <= v <= 300:
            self._update_interval = v

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
            v = PlotView(self.window, self)
            self.window.add_view("plot", v)
            v.setup()

    def show(self):
        self.window.show_view('plot')
        self._update_state = True
        self.window.after(self.update_interval, self.update)

    def update(self):
        if self.update_state:
            data = self.model.update()[:]
            # now re-plot
            v = self.window.get_view("plot")
            """:type: pyLabJackView.view.plot.PlotView"""
            v.plot.plot(data[0], data[1], clear=True)
            self.window.after(self.update_interval * 1000, self.update)

    def close(self):
        self._update_state = False
        if self.window.has_view("plot"):
            self.window.remove_view("plot")
        # clean up
