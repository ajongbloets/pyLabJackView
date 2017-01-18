from . import Model
from datetime import datetime as dt


class LabJackModel(Model):
    """Stores data collected from a labjack"""

    def __init__(self, connection, resolution=12, gain=2):
        """

        :type connection: pyLabJackView.connection.labjack.LabJackConnection
        """
        super(LabJackModel, self).__init__()
        self._connection = connection
        self._resolution = resolution
        self._gain = gain
        self.reset()

    @property
    def connection(self):
        with self.lock:
            c = self._connection
        return c

    @property
    def channels(self):
        with self.lock:
            c = self._data.keys()
        return c

    @property
    def resolution(self):
        with self.lock:
            resolution = self._resolution
        return resolution

    @resolution.setter
    def resolution(self, v):
        if 0 <= v <= 13:
            with self.lock:
                self._resolution = int(v)

    @property
    def gain(self):
        with self.lock:
            gain = self._gain
        return gain

    @gain.setter
    def gain(self, v):
        if v in [0, 1, 2, 3, 15]:
            with self.lock:
                self._gain = int(v)

    @Model.thread_safe
    def reset(self):
        self._data = {}

    @Model.thread_safe
    def update(self):
        """Updates the data"""
        for ain in self.channels:
            self._data[ain].update()
        return self._data

    @Model.thread_safe
    def get_channels(self):
        return self._data.keys()[:]

    @Model.thread_safe
    def has_channel(self, ain):
        return ain in self._data.keys()

    @Model.thread_safe
    def get_channel(self, ain):
        if not self.has_channel(ain):
            raise KeyError("Unknown AIN value: {}".format(ain))
        return self._data[ain]

    @Model.thread_safe
    def add_channel(self, ain):
        """Creates a new AIN Model and adds this to this model"""
        if not self.has_channel(ain):
            model = LabJackAinModel(self.connection, ain, self.resolution, self.gain)
            self._data[ain] = model
        else:
            model = self._data[ain]
        return model

    @Model.thread_safe
    def remove_channel(self, ain):
        if not self.has_channel(ain):
            raise KeyError("AIN not registered to this model: {}".format(ain))
        self._data.pop(ain)

    @Model.thread_safe
    def add_measurement(self, ain, value, **kwargs):
        v = kwargs.copy()
        v["time"] = dt.now()
        v["value"] = value
        if ain in self._data.keys():
            self._data[ain].append(v)
        else:
            self._data[ain] = [v]

    @Model.thread_safe
    def read_ain(self, ain, resolution=None, gain=None):
        if resolution is None:
            resolution = self.resolution
        if gain is None:
            gain = self.gain
        result = 0.0
        if self.connection.is_connected():
            result = self.connection.measure_ain(ain, resolution=resolution, gain=gain)
        return result


class LabJackAinModel(LabJackModel):
    """Models data collected from one AIN Channel"""

    def __init__(self, connection, ain=0, resolution=12, gain=2):
        super(LabJackAinModel, self).__init__(connection=connection, resolution=resolution, gain=gain)
        self._ain = ain
        self._state = True

    @property
    def ain(self):
        with self.lock:
            ain = self._ain
        return ain

    @property
    def is_active(self):
        with self.lock:
            active = self._state
        return active

    @is_active.setter
    def is_active(self, state):
        with self.lock:
            self._state = state is True

    @LabJackModel.thread_safe
    def reset(self):
        self._data = []

    @LabJackModel.thread_safe
    def add_measurement(self, ain, value, **kwargs):
        v = kwargs.copy()
        v["time"] = dt.now()
        v["value"] = value
        self._data.append(v)

    @LabJackModel.thread_safe
    def update(self):
        kwargs = {"resolution": self.resolution, "gain": self.gain}
        self.add_measurement(
            self.ain, self.read_ain(self.ain, **kwargs), **kwargs
        )
        return self._data[:]

