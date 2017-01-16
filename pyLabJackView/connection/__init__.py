"""Base (thread-safe) connection object"""

from threading import RLock


class Connection(object):
    """A simple connection object"""

    def __init__(self):
        self._lock = RLock()
        self._connection = None
        self._connected = False

    def __del__(self):
        with self.lock:
            if self.is_connected():
                self.disconnect()

    @property
    def lock(self):
        return self._lock

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def _create_connection(self):
        raise NotImplementedError

    def has_connection(self):
        return self._connection is not None

    def is_connected(self):
        """Whether there is a connection object and the connection is open"""
        with self.lock:
            state = self.has_connection() and self._connected
        return state


class Manager(object):
    """A connection manager, for managing a connection in  a thread"""

    _instance = None

    @classmethod
    def load(cls, *args, **kwargs):
        """Returns a Manager instance"""
        if cls._instance is None:
            cls._instance = cls(*args, **kwargs)
        return cls._instance

    def __init__(self):
        self._connections = {}

    def new_connection(self, name):
        pass
