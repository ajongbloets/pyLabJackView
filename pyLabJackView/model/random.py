
from . import Model
from numpy.random import normal


class RandomValueModel(Model):
    """Generates random data"""

    def __init__(self, mean=0, std=1):
        super(RandomValueModel, self).__init__()
        self._mean = mean
        self._std = std
        self.reset()

    def reset(self):
        self._data = []

    def generate(self):
        return normal(self.get_mean(), self.get_std())

    def update(self):
        v = self.generate()
        with self.lock:
            self._data.append(v)
        return self.data

    def get_mean(self):
        return self._mean

    def get_std(self):
        return self._std


class RandomXYModel(RandomValueModel):
    """Generates x,y tuples with random y data"""

    def __init__(self, mean=0, std=1):
        """Generates random tuples of x,y, with x increasing

        :param mean:
        :type mean:
        :param std: The Standard deviation of
        :type std:
        """
        super(RandomXYModel, self).__init__(mean=mean, std=std)

    @property
    def data(self):
        """Returns a copy of the data contained in the model

        Use ._data for internal setting of the data in the model
        Or use methods that do this in a thread safe way

        :return:
        :rtype: tuple[list[float | int], list[float, int]]
        """
        with self.lock:
            data = self._data[:]
        return data

    def reset(self):
        with self.lock:
            self._data = ([], [])

    def generate(self):
        x = self._last_x() + 1
        y = super(RandomXYModel, self).generate()
        return x, y

    def update(self):
        x, y = self.generate()
        self.add_xy(x, y)
        return self.data

    def add_xy(self, x, y):
        with self.lock:
            self._data[0].append(x)
            self._data[1].append(y)

    def _last_x(self):
        x = 0
        with self.lock:
            if len(self.data[0]) > 0:
                x = self.data[0][-1]
        return x