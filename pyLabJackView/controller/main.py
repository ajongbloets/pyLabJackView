
from julesTk.controller import Controller
from pyLabJackView.controller.plot import PlotController
from pyLabJackView.controller.labjack import LabJackController
from pyLabJackView.view.main import MainViewSet

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class MainController(Controller):

    def __init__(self, app, view=None, model=None):
        super(MainController, self).__init__(app, view=view, model=model)
        self._plot = None

    @property
    def view(self):
        """The view of this controller

        :rtype: pyLabJackView.view.main.MainViewSet
        """
        return super(MainController, self).view

    def setup(self, view=None):
        if view is None:
            view = MainViewSet(self.application, self)
        self._view = view
        self.view.setup()

    def start(self):
        """What show we do to show the view"""
        self.view.show()
        self.show_labjack()

    def stop(self):
        self.view.remove_view("main")
        self.view.close()

    def load_plot_view(self):
        """Creates a add_plot view if necessary.

        :return:
        :rtype: pyLabJackView.view.plot.PlotView
        """
        if not self.application.has_controller("plot"):
            c = PlotController(self.application).setup()
            self.application.add_controller("plot", c)
            self.view.add_view("plot", c.view)
        return self.application.has_controller("plot")

    def load_labjack_view(self):
        if not self.application.has_controller("labjack"):
            c = LabJackController(self.application).setup()
            self.application.add_controller("labjack", c)
            self.view.add_view("labjack", c.view)
        return self.application.has_controller("labjack")

    def hide_main(self):
        if self.view.has_view("main"):
            self.view.hide_view("main")

    def show_main(self):
        self.hide_labjack()
        self.view.show_view("main")

    def hide_labjack(self):
        if self.view.has_view("labjack"):
            self.view.hide_view("labjack")

    def show_labjack(self):
        self.hide_main()
        self.hide_plot()
        self.load_labjack_view()
        self.application.get_controller("labjack").start()

    def hide_plot(self):
        if self.view.has_view("plot"):
            self.view.hide_view("plot")

    def show_plot(self):
        self.hide_main()
        self.hide_labjack()
        self.load_plot_view()
        self.application.get_controller("plot").start()
