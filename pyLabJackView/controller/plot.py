from . import Controller
from pyLabJackView.view.main import MainWindow
from pyLabJackView.view.plot import PlotView
from threading import Thread, Timer, Event
import time

__author__ = "Joeri Jongbloets <joer@jongbloets.net>"


class PlotController(Controller):

    def __init__(self, app, window=None, model=None):
        super(PlotController, self).__init__(app, window=window, model=model)

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

    def close(self):
        if self.window.has_view("plot"):
            self.window.get_view("plot").destroy()
            self.window.remove_view("plot")
        # clean up


class PlotControllerThread(PlotController, Thread):
    """This controller runs from a separate thread"""

    def __init__(self, app, window=None, model=None):
        super(PlotControllerThread, self).__init__(app, window=window, model=model)
        self._window = window
        self._interval = 1  # in seconds
        self._timer = None
        self._exit = Event()
        self._exited = Event()

    @property
    def interval(self):
        with self.lock:
            v = self._interval
        return v

    @interval.setter
    def interval(self, v):
        if 0 <= v <= 1800:
            with self.lock:
                self._interval = v

    def update(self):
        if not self._exit.isSet():
            with self.lock:
                data = self.model.update()[:]
                # now re-plot
                v = self.window.get_view("plot")
                """:type: pyLabJackView.view.plot.PlotView"""
                v.plot.plot(data[0], data[1], clear=True)
            self.window.update_idletasks()
            with self.lock:
                i = self._interval
            self.window.after(i * 1000, self.update)
        else:
            self._exited.set()

    def run(self):
        self._exit.clear()
        self.update()

    def close(self):
        self._exited.clear()
        self._exit.set()
        self._exited.wait()
