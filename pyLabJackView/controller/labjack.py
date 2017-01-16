"""Controller for interacting with a labjack"""

from pyLabJackView.model import labjack
from plot import PlotController
from threading import Thread, Event
import time

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class LabJackController(PlotController):
    """A controller for """

    def __init__(self, app, window=None, model=None):
        if model is None:
            model = labjack.LabJackModel()
        super(LabJackController, self).__init__(app, window=window, model=model)

    def show(self):
        pass

    def show_labjack_plot(self):
        pass

    @PlotController.thread_safe
    def update(self):
        pass

    def update_labjack_plot(self):
        pass

    def close(self):
        pass

    def close_labjack_plot(self):
        pass


class LabJackControllerThread(LabJackController, Thread):

    def __init__(self, app, window=None, model=None):
        super(LabJackControllerThread, self).__init__(app, window=window, model=model)
        self._interval = 1  # in seconds
        self._exit = Event()  # signals whether the thread should stop
        self._update = Event()   # signals whether the thread should update

    @property
    def interval(self):
        with self.lock:
            result = self._interval
        return result

    def run(self):
        # start of thread
        self.execute()

    def execute(self):
        if not self._exit.isSet():
            with self.lock:
                self.update()
        if not self._exit.isSet():
            i = self.interval
            self.window.after(i, self.execute)
