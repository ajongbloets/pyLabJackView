"""Implementing basic view objects"""
from pyLabJackView import ThreadSafeObject
import sys
if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

import ttk

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class Frame(ttk.Frame, ThreadSafeObject):

    FONT_FAMILY = "Verdana"
    FONT_SMALL = (FONT_FAMILY, 8)
    FONT_NORMAL = (FONT_FAMILY, 10)
    FONT_LARGE = (FONT_FAMILY, 14)

    def __init__(self, parent, controller):
        """

        :rtype: Tkinter.Frame
        """
        ThreadSafeObject.__init__(self)
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

    @ThreadSafeObject.thread_safe
    def close(self):
        self.destroy()


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

    @ThreadSafeObject.thread_safe
    def get_view(self, name):
        """

        :param name: Name of the view
        :rtype: pyLabJackView.view.View
        """
        if not self.has_view(name):
            KeyError("No view registered under: {}".format(name))
        return self.views[name]

    @ThreadSafeObject.thread_safe
    def has_view(self, name):
        return name in self.views

    @ThreadSafeObject.thread_safe
    def add_view(self, name, frame):
        if self.has_view(name):
            KeyError("Already registered a view under: {}".format(name))
        self.views[name] = frame

    @ThreadSafeObject.thread_safe
    def remove_view(self, name):
        if not self.has_view(name):
            KeyError("No view registered under: {}".format(name))
        self.views.pop(name)

    def setup(self):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError

    @ThreadSafeObject.thread_safe
    def show_view(self, name):
        v = self.get_view(name)
        v.tkraise()

    @ThreadSafeObject.thread_safe
    def close(self):
        for v in self.views.values():
            v.close()


class View(Frame):
    """A view is a frame inside a window"""

    def __init__(self, parent, controller):
        super(View, self).__init__(parent, controller)

    def setup(self):
        raise NotImplementedError
