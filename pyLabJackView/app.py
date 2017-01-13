"""Module managing starting and stopping the application"""

from pyLabJackView import tk
from controller.main import MainController


class LabJackViewApp(object, tk.Tk):
    """The app is the starting stub"""
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._controllers = {}

    @property
    def controllers(self):
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

    def remove_window(self, name):
        if not self.has_window(name):
            raise KeyError("No controller registered under: {}".format(name))
        self.windows.pop(name)

    def configure(self):
        c = MainController(self)
        self.add_controller("main", c)
        c.configure()
        c.show()

    def start(self):
        """Start the application"""
        self.configure()
        self.mainloop()


if __name__ == "__main__":
    app = LabJackViewApp()
    app.start()