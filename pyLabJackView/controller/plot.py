"""Implement a view with a matplotlib plot"""

from pyLabJackView import PyLabJackViewException
from julesTk.controller import Controller
from pyLabJackView.model.random import RandomXYModel
from pyLabJackView.view.main import MainViewSet
from pyLabJackView.view.plot import LivePlotView

__author__ = "Joeri Jongbloets <joer@jongbloets.net>"


class PlotController(Controller):

    def __init__(self, app, view=None, model=None):
        if model is None:
            model = RandomXYModel()
        super(PlotController, self).__init__(app, view=view, model=model)
        self._update_interval = 1
        self._update_state = False

    @property
    def view(self):
        """

        :rtype: pyLabJackView.view.plot.LivePlotView
        """
        return super(PlotController, self).view

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

    def setup(self, view=None):
        if view is None:
            view = self._view
        if view is None:
            self._view = LivePlotView(self.view, self)
        self.view.setup()
        return self

    def start(self):
        self.view.show()

    def start_update(self):
        self._update_state = True
        self.view.after(self.update_interval, self.update)
        return True

    def stop_update(self):
        self._update_state = False
        self.view.set_status_text("Paused")
        return True

    def update(self):
        if self.update_state:
            self.update_plot()
            self.view.after(self.update_interval * 1000, self.update)

    def update_plot(self):
        data = self.model.update()[:]
        self.view.plot.figure.plot(data[0], data[1], clear=True)

    def reset_plot(self):
        self.model.reset()
        self.update_plot()

    def stop(self):
        self._update_state = False


class PlotControllerException(PyLabJackViewException):

    def __init__(self, msg):
        super(PlotControllerException, self).__init__(msg)