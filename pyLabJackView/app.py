"""Module managing starting and stopping the application"""

from view import tk
from controller.main import MainController
from threading import RLock


class LabJackViewApp(object, tk.Tk):
    """The app is the starting stub"""

    lock = RLock()

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._controllers = {}

    @property
    def controllers(self):
        """

        :return:
        :rtype: dict[str, pyLabJackView.controller.Controller]
        """
        return self._controllers

    def get_controller(self, name):
        if not self.has_controller(name):
            raise KeyError("No controller registered under: {}".format(name))
        return self.controllers[name]

    def has_controller(self, name):
        return name in self.controllers.keys()

    def add_controller(self, name, controller):
        if self.has_controller(name):
            raise KeyError("Already registered a controller under: {}".format(name))
        self.controllers[name] = controller

    def remove_controller(self, name):
        if not self.has_controller(name):
            raise KeyError("No controller registered under: {}".format(name))
        self.controllers.pop(name)

    def setup(self):
        self.wm_title("pyLabJackView")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.resizable(True, False)
        c = MainController(self)
        self.add_controller("main", c)
        c.setup()
        c.show()

    def start(self):
        """Start the application"""
        with self.lock:
            self.setup()
        # in the main loop we wait, so we do not need a lock
        self.mainloop()
        with self.lock:
            self.quit()

    def quit(self):
        while len(self.controllers) > 0:
            name = self.controllers.keys()[0]
            self.get_controller(name).close()
            self.remove_controller(name)
        tk.Tk.quit(self)


if __name__ == "__main__":
    app = LabJackViewApp()
    app.start()
