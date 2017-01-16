from . import Model


class LabJackModel(Model):
    """Stores data collected from a labjack"""

    def __init__(self):
        super(LabJackModel, self).__init__()

    def reset(self):
        with self.lock:
            self._data = {}

    def update(self):
        """Updates the data"""
        pass

