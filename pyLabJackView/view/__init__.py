from .. import tk


class Window(object, tk.Frame):
    """A window can contain one or more views"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self._frames = {}
        self._controller = controller

    @property
    def frames(self):
        return self._frames

    def get_frame(self, name):
        if not self.has_frame(name):
            KeyError("No frame registered under: {}".format(name))
        return self.frames[name]

    def has_frame(self, name):
        return name in self.frames

    def add_frame(self, name, frame):
        if self.has_frame(name):
            KeyError("Already registered a frame under: {}".format(name))
        self.frames[name] = frame

    def remove_frame(self, name):
        if not self.has_frame(name):
            KeyError("No frame registered under: {}".format(name))
        self.frames.pop(name)

    def configure(self):
        raise NotImplementedError


class View(tk.Frame):
    """A view is a frame inside a window"""

    def __init__(self, parent, window):
        super(View, self).__init__(parent)
        self._window = window