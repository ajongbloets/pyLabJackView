
from . import Connection
import u6

__author__ = "Joeri Jongbloets"


class LabJackConnection(Connection):

    TEMPERATURE_KELVIN = "kelvin"
    TEMPERATURE_CELSIUS = "celsius"

    def __init__(self):
        super(LabJackConnection, self).__init__()
        self._serial_nr = None
        self._local_id = None
        self._auto_connect = False

    @property
    def local_id(self):
        """Thread safe property"""
        with self.lock:
            result = self._local_id
        return result

    @property
    def serial_nr(self):
        with self.lock:
            result = self._serial_nr
        return result

    @property
    def auto_connect(self):
        with self.lock:
            result = self._auto_connect
        return result

    def connect_serial_nr(self, serial_nr=None):
        with self.lock:
            if serial_nr is None:
                serial_nr = self.serial_nr
            result = self._connect(serial_id=serial_nr)
        return result

    def connect_local_id(self, local_id=None):
        with self.lock:
            if local_id is None:
                local_id = self.local_id
            result = self._connect(local_id=local_id)
        return result

    def connect(self, serial_id=None, local_id=None, auto=None):
        """ Connect to the labjack

        :param serial_id:
        :type serial_id:
        :param local_id:
        :type local_id:
        :param auto:
        :type auto:
        :return:
        :rtype:
        """
        result = False
        with self.lock:
            if serial_id is None:
                serial_id = self._serial_nr
            if local_id is None:
                local_id = self._local_id
            if auto is None:
                auto = self._auto_connect
        if serial_id is None and local_id is None:
            auto = True
        if not result and serial_id is not None:
            result = self._connect(serial_id=serial_id, auto=auto)
        if not result and local_id is not None:
            result = self._connect(local_id=local_id, auto=auto)
        if not result and auto:
            result = self._connect(auto=auto)
        return result

    def _connect(self, serial_id=None, local_id=None, auto=False):
        """Intern connect function"""
        result = False
        with self.lock:
            if self.is_connected():
                raise LabJackConnectionException("Disconnect first")
            if None not in (local_id, serial_id):
                raise LabJackConnectionException("Local ID and Serial ID cannot be set at the same time")
            if not self.has_connection():
                self._create_connection()
            try:
                self._connection.open(localId=local_id, serial=serial_id)
                self._connection.getCalibrationData()
                self._connected = True
                result = self.is_connected()
                self.read_info()
            except u6.LabJackException as lje:
                pass
        return result

    def _create_connection(self):
        with self.lock:
            self._connection = u6.U6(autoOpen=False)
        return self.has_connection()

    def disconnect(self):
        with self.lock:
            if self.is_connected():
                self._connection.close()
                self._connected = False
                self._serial_nr = None
                self._local_id = None
        return not self.is_connected()

    def read_info(self):
        """Reads some basic configuration information of the u6"""
        result = {}
        with self.lock:
            if self.is_connected():
                result = self._connection.configU6()
                # update serial number
                self._serial_nr = result.get("SerialNumber", None)
                # update local ID
                self._local_id = result.get("LocalID", None)
        return result

    def measure_ain(self, channel, resolution=12, gain=1, differential=False):
        """Read the voltage from the Analog In"""
        result = 0.0
        with self.lock:
            if self.is_connected():
                try:
                    result = self._connection.getAIN(
                        channel, resolutionIndex=resolution, gainIndex=gain, differential=differential
                    )
                except:
                    pass
        return result

    def measureTemperature(self, units=TEMPERATURE_KELVIN):
        """Measures the internal temperature of the labjack"""
        result = 0.0
        with self.lock:
            if self.is_connected():
                try:
                    result = self._connection.getTemperature()
                    if units == self.TEMPERATURE_CELSIUS:
                        result = self._kelvin_to_celsius(result)
                except Exception as e:
                    pass
        return result

    def set_dio_state(self, ioNum, state=1):
        result = 0.0
        with self.lock:
            if self.is_connected():
                try:
                    result = self._connection.setDIOState(ioNum, state=state)
                except Exception as e:
                    pass
        return result

    def set_do_state(self, ioNum, state=1):
        result = 0.0
        with self.lock:
            if self.is_connected():
                try:
                    self._connection.setDOState(ioNum, state=state)
                    result = True
                except Exception as e:
                    pass
        return result

    def _kelvin_to_celsius(self, kelvin):
        """Transforms kelvin into celsius"""
        return kelvin - 273.15

    def celcius_to_kelvin(self, celsius):
        """Transforms celsius to kelvin"""
        return celsius + 273.15




class LabJackConnectionException(Exception):

    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg
