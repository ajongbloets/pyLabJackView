
from . import Connection
import u6

__author__ = "Joeri Jongbloets"


class LabJackConnection(Connection):

    def __init__(self):
        super(LabJackConnection, self).__init__()
        self._serial_nr = None
        self._local_id = None
        self._auto_connect = False

    def connect(self, serial_nr=None, local_id=None, auto=False):
        """ Connect to

        :param serial_nr:
        :type serial_nr:
        :param local_id:
        :type local_id:
        :param auto:
        :type auto:
        :return:
        :rtype:
        """
        with self.lock:
            if serial_nr is None:
                serial_nr = self._serial_nr

    def connect

    def disconnect(self):
        pass
