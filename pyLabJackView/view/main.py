"""Defines the mainView"""

from . import *

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class MainWindow(Window):
    """"""

    def __init__(self, parent, controller):
        super(MainWindow, self).__init__(parent, controller)
        self._current_view = None

    def setup(self):
        self.configure_grid(self)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        if not self.has_view("main"):
            # add view
            v = MainView(self, self.controller)
            self.add_view("main", v)
            v.setup()

    def show(self):
        self.show_view()

    def show_view(self, name="main"):
        super(MainWindow, self).show_view(name)


class MainView(View):
    """"""

    def __init__(self, parent, window):
        super(MainView, self).__init__(parent, window)

    @property
    def controller(self):
        """

        :rtype: pyLabJackView.controller.main.MainController
        """
        return super(MainView, self).controller

    def setup(self):
        self.configure_grid(self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        # label
        label = ttk.Label(self, text="This is the show page", font=self.FONT_LARGE)
        label.grid(row=0, column=0, columnspan=2)
        # button for add_plot
        button = ttk.Button(
            self, text="Show add_plot", command=self.controller.show_plot
        )
        button.grid(row=1, column=0)
        # button for add_plot
        button = ttk.Button(
            self, text="Show labjack", command=self.controller.show_labjack
        )
        button.grid(row=1, column=2)
