"""Controller for interacting with a labjack"""

from pyLabJackView.model.labjack import LabJackModel
from pyLabJackView.view.labjack import LabjackPlotView
from pyLabJackView.view.main import MainWindow
from plot import PlotController

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class LabJackController(PlotController):
    """A controller for """

    def __init__(self, app, window=None, model=None):
        if model is None:
            model = LabJackModel()
        super(LabJackController, self).__init__(app, window=window, model=model)

    def setup(self, window=None):
        if window is None:
            window = self._window
        if window is None:
            self._window = MainWindow(self.application, self)
        self.window.setup()
        # now add
        if not self.window.has_view("labjack"):
            v = LabjackPlotView(self.window, self)
            self.window.add_view("labjack", v)
            v.setup()

    def show(self):
        self.window.show_view('labjack')
        self._update_state = True
        self.window.after(self.update_interval, self.update)

    def update(self):
        if self.update_state:
            # data = self.model.update()[:]
            # now re-plot
            # v = self.window.get_view("labjack")
            # """:type: pyLabJackView.view.plot.PlotView"""
            # v.plot.plot(data[0], data[1], clear=True)
            self.window.after(self.update_interval * 1000, self.update)

    def close(self):
        self._update_state = False
        if self.window.has_view("labjack"):
            self.window.remove_view("labjack")
        # clean up
