
from threading import RLock


class PyLabJackViewException(BaseException):

    def __init__(self, msg=None):
        if msg is None:
            self._msg = ""
        self._msg = msg

    def __str__(self):
        return self._msg


class ThreadSafeObject(object):
    """A class providing infrastructure for creating thread-safe objects"""

    def __init__(self):
        self._lock = RLock()

    @property
    def lock(self):
        """Retrieve the lock of this object"""
        return self._lock

    def thread_safe(f):
        """"""
        def magic(self, *args, **kwargs):
            with self.lock:
                result = f(self, *args, **kwargs)
            return result
        return magic

    thread_safe = staticmethod(thread_safe)
