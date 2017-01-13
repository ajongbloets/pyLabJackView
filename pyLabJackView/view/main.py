"""Defines the mainView"""

from . import Window, View


class MainWindow(Window):
    """"""

    def __init__(self, parent, controller):
        super(MainWindow, self).__init__(parent, controller)

    def configure(self):
        self.pack()

    def show(self):
        self.tkraise()


class MainView(View):

    def __init__(self, parent, window):
        super(MainView, self).__init__(parent, window)
