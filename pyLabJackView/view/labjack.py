"""Module with view showing labjack measurements"""

from plot import *

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class LabjackPlotView(PlotView):

    REFRESH_RATES = {
        "50 msec": 0.05,
        "100 msec": 0.1,
        "200 msec": 0.2,
        "500 msec": 0.5,
        "1 sec": 1,
        "2 sec": 2,
        "5 sec": 5,
        "10 sec": 10,
        "15 sec": 15,
        "30 sec": 30,
        "1 min": 60,
        "5 min": 300,
        "10 min": 600,
        "30 min": 1800,
        "1 hour": 3600,
    }  # in seconds per update

    def __init__(self, parent, controller):
        super(LabjackPlotView, self).__init__(parent, controller)
        self._plot = None
        self._picker_value = tk.StringVar()

    @property
    def controller(self):
        """ Returns the

        :return:
        :rtype: pyLabJackView.controller.labjack.LabJackController
        """
        return self._controller

    @property
    def plot(self):
        """Returns the plot object loaded in this view

        :rtype: pyLabJackView.view.plot.PlotFrame
        """
        return self._plot

    def setup(self):
        self.grid(row=0, column=0, sticky="nsew")
        # add widgets
        # refresh rate
        label = ttk.Label(self, text="Refresh rate:")
        label.pack(pady=10, padx=10)
        self.rate_picker = ttk.Combobox(
            self, state="readonly",
            textvariable=self._picker_value
        )
        self.rate_picker.bind("<<ComboboxSelected>>", self.update_rate)
        self.rate_picker.pack()
        self.setup_plot()

    def setup_plot(self):
        self._plot = PlotFrame(self, self.controller)
        self.plot.setup()
        # self.plot.plot([0, 1, 2, 3, 4], [1, 2, 4, 8, 16])

    def update_rate(self, event):
        v = self.rate_picker.get()
        rate = self.REFRESH_RATES.get(v, 1)
        self.controller.update_interval = rate
