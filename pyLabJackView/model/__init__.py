"""Model class"""

from threading import RLock


class Model(object):

    def __init__(self):
        self._data = None
        self._lock = RLock()

    @property
    def data(self):
        return self._data

    @property
    def lock(self):
        return self._lock

    def update(self):
        """Request the model to update it self"""
        raise NotImplementedError
