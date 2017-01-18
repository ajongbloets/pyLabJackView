"""Implementing basic view objects"""

import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

import ttk
from pyLabJackView import PyLabJackViewException

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class Frame(ttk.Frame, object):

    FONT_FAMILY = "Verdana"
    FONT_SMALL = (FONT_FAMILY, 8)
    FONT_NORMAL = (FONT_FAMILY, 10)
    FONT_LARGE = (FONT_FAMILY, 14)

    @staticmethod
    def configure_grid(w, sticky="nsew", **kwargs):
        w.grid(sticky=sticky, **kwargs)

    @staticmethod
    def configure_column(w, indexes, weight=1):
        if not isinstance(indexes, (tuple, list)):
            indexes = [indexes]
        for index in indexes:
            w.grid_columnconfigure(index, weight)

    @staticmethod
    def configure_row(w, indexes, weight=1):
        if not isinstance(indexes, (tuple, list)):
            indexes = [indexes]
        for index in indexes:
            w.grid_rowconfigure(index, weight)

    def __init__(self, parent, controller):
        """

        :rtype: Tkinter.Frame
        """
        ttk.Frame.__init__(self, parent)
        self._controller = controller
        self._parent = parent

    @property
    def parent(self):
        return self._parent

    @property
    def controller(self):
        """

        :rtype: pyLabJackView.controller.Controller
        """
        return self._controller

    def setup(self):
        raise NotImplementedError

    def close(self):
        pass


class Window(Frame):
    """A window can contain one or more views"""

    def __init__(self, parent, controller):
        super(Window, self).__init__(parent, controller)
        self._views = {}

    @property
    def views(self):
        """

        :rtype: dict[str, pyLabJackView.view.View]
        """
        return self._views

    def get_view(self, name):
        """

        :param name: Name of the view
        :rtype: pyLabJackView.view.View
        """
        if not self.has_view(name):
            KeyError("No view registered under: {}".format(name))
        return self.views[name]

    def has_view(self, name):
        return name in self.views

    def add_view(self, name, frame):
        if self.has_view(name):
            KeyError("Already registered a view under: {}".format(name))
        self.views[name] = frame

    def remove_view(self, name):
        if not self.has_view(name):
            KeyError("No view registered under: {}".format(name))
        self.get_view(name).close()
        self.views.pop(name)

    def show_view(self, name):
        v = self.get_view(name)
        v.show()

    def hide_view(self, name):
        v = self.get_view(name)
        v.grid_remove()

    def setup(self):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    def close(self):
        for v in self.views.values():
            v.close()


class View(Frame):
    """A view is a frame inside a window"""

    def __init__(self, parent, controller):
        super(View, self).__init__(parent, controller)
        self._variables = {}
        self._widgets = {}

    @property
    def variables(self):
        return self._variables

    def has_variable(self, name):
        return name in self.variables.keys()

    def get_variable(self, name):
        if not self.has_variable(name):
            raise KeyError("Unknown variable: {}".format(name))
        return self.variables[name]

    def add_variable(self, name, variable):
        if self.has_variable(name):
            raise KeyError("Already registered a variable as: {}".format(name))
        self.variables[name] = variable
        return variable

    def remove_variable(self, name):
        if not self.has_variable(name):
            raise KeyError("Unknown variable: {}".format(name))
        self.variables.pop(name)
        return not self.has_variable(name)

    @property
    def widgets(self):
        return self._widgets

    def has_widget(self, name):
        return name in self.widgets.keys()

    def get_widget(self, name):
        if not self.has_widget(name):
            raise KeyError("Unknown widget: {}".format(name))
        return self.widgets[name]

    def add_widget(self, name, widget):
        if self.has_widget(name):
            raise KeyError("Already registered a widget as: {}".format(name))
        self.widgets[name] = widget
        return widget

    def remove_widget(self, name):
        if not self.has_widget(name):
            raise KeyError("Unknown widget: {}".format(name))
        self.widgets.pop(name)
        return name not in self.widgets.keys()

    def show(self):
        self.tkraise()

    def setup(self):
        raise NotImplementedError
