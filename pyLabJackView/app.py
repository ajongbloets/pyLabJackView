"""Module managing starting and stopping the application"""

from julesTk.app import Application
from controller.labjack import LabJackController


class LabJackViewApp(Application):
    """The app is the starting stub"""

    def __init__(self, *args, **kwargs):
        super(LabJackViewApp, self).__init__(*args, **kwargs)

    def _prepare(self):
        self.wm_title("pyLabJackView")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.resizable(True, False)
        c = LabJackController(self)
        self.add_controller("main", c)
        c.prepare()

    def _start(self):
        self.get_controller("main").start()

if __name__ == "__main__":
    app = LabJackViewApp()
    app.run()
