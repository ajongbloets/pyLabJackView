"""Model class"""


class Model:

    def __init__(self, controller):
        self._controller = controller

    @property
    def controller(self):
        return self._controller