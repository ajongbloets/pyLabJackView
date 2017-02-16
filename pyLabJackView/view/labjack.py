"""Module with view showing labjack measurements"""

from julesTk.view import *
from julesTk.view.plot import PlotFrame
import numpy as np
from datetime import datetime as dt

__author__ = "Joeri Jongbloets <joeri@jongbloets.net>"


class LabJackPlotFrame(PlotFrame):
    """Frame capable of plotting labjack data"""

    def __init__(self, parent):
        super(LabJackPlotFrame, self).__init__(parent)
        self._t_zero = None
        self._lines = {}

    @property
    def t_zero(self):
        """ Returns the time zero of the plot

        :rtype: datetime.datetime
        """
        if self._t_zero is None:
            self._t_zero = dt.now()
        return self._t_zero

    def t_since(self, t_point=None):
        t_zero = self.t_zero
        if t_point is None:
            t_point = dt.now()
        return (t_point - t_zero).total_seconds()

    def clear(self):
        self._lines = {}
        super(LabJackPlotFrame, self).clear()
        self._t_zero = None

    def update_line(self, ain, x, y):
        if not isinstance(x, (tuple, list)):
            x = x,
        if not isinstance(y, (tuple, list)):
            y = y,
        x_new = []
        for v in x:
            if isinstance(v, dt):
                x_new.append(self.t_since(v))
        x = x_new
        del x_new
        if ain in self._lines.keys():
            line = self._lines[ain]
            xlim, ylim = self.add_line_point(line, x, y)
        else:
            xlim, ylim = self.add_line(ain, x, y)
        return xlim, ylim

    def add_line(self, ain, x, y):
        """Adds a new line to the plot"""
        l = self.axes.plot(x, y, label="AIN {}".format(ain))[0]
        self._lines[ain] = l
        return self.axes.get_xlim(), self.axes.get_ylim()

    def add_line_point(self, line, x, y):
        """Adds a new point to an existing line"""
        xdata = np.append(line.get_xdata(), x)
        line.set_xdata(xdata)
        ydata = np.append(line.get_ydata(), y)
        line.set_ydata(ydata)
        return (xdata.min(), xdata.max()), (ydata.min(), ydata.max())


class LabJackView(View):

    GAIN_INDEXES = {
        "x1": 0,
        "x10": 1,
        "x100": 2,
        "x1000": 3,
        "auto": 15,
    }

    REFRESH_RATES = {
        # "50 msec": 0.05,
        # "100 msec": 0.1,
        # "200 msec": 0.2,
        "500 msec": 0.5,
        "1 sec": 1,
        "2 sec": 2,
        "5 sec": 5,
        "10 sec": 10,
        "15 sec": 15,
        "30 sec": 30,
        "1 min": 60,
        #  "5 min": 300,
        #  "10 min": 600,
        #  "30 min": 1800,
        #  "1 hour": 3600,
    }  # in seconds per update

    def __init__(self, parent, controller):
        super(LabJackView, self).__init__(parent, controller)

    @property
    def controller(self):
        """ Returns the

        :return:
        :rtype: pyLabJackView.controller.labjack.LabJackController
        """
        return self._controller

    @property
    def plot(self):
        """Returns the add_plot object loaded in this view

        :rtype: pyLabJackView.view.labjack.LabJackPlotFrame
        """
        return self.get_widget("add_plot")

    @property
    def refresh_rate(self):
        v = self.variables["refresh_rate"].get()
        return self.REFRESH_RATES.get(v, 1)

    @property
    def resolution(self):
        v = self.variables["resolution"].get()
        return int(v)

    @property
    def gain(self):
        v = self.variables["gain"].get()
        return self.GAIN_INDEXES.get(v, 1)

    def set_status_text(self, str):
        self.variables["status"].set(str)

    def _prepare(self):
        self.configure_grid(self)
        # add widgets
        lbj_ports_frame = ttk.Frame(self)
        self.configure_grid(lbj_ports_frame, row=0, column=0)
        self.setup_labjack_ports(parent=lbj_ports_frame)
        lbj_msr_frame = ttk.Frame(self)
        self.configure_grid(lbj_msr_frame, row=1, column=0)
        self.setup_labjack_settings(parent=lbj_msr_frame)
        ctrl_frame = ttk.Frame(self)
        self.configure_grid(ctrl_frame, row=2, column=0)
        self.setup_control(parent=ctrl_frame)
        plt_frame = ttk.Frame(self)
        self.configure_grid(plt_frame, row=3, column=0)
        self.setup_plot(parent=plt_frame)
        # set min size
        min_colsize = self.plot.figure.get_figwidth() * self.plot.figure.dpi
        min_rowsize = self.plot.figure.get_figheight() * self.plot.figure.dpi
        self.grid_columnconfigure(0, weight=1, minsize=min_colsize)
        self.grid_rowconfigure(3, weight=1, minsize=min_rowsize)

    def setup_labjack_settings(self, parent=None):
        if parent is None:
            parent = self
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        # resolution
        lbl = ttk.Label(text="Resolution:")
        v = self.add_variable("resolution", tk.StringVar())
        cob = self.add_widget("resolution", ttk.Combobox(
            parent, state="readonly", textvariable=v
        ))
        cob["values"] = range(13)
        cob.current(12)
        cob.bind("<<ComboboxSelected>>", self.update_resolution)
        cob.grid(row=0, column=0)
        # gain
        v = self.add_variable("gain", tk.StringVar())
        cob = self.add_widget("gain", ttk.Combobox(
            parent, state="readonly", textvariable=v
        ))
        gains = sorted(self.GAIN_INDEXES, key=self.GAIN_INDEXES.get)
        cob["values"] = gains
        cob.current(gains.index("x100"))
        cob.bind("<<ComboboxSelected>>", self.update_gain)
        cob.grid(row=0, column=1)

    def setup_labjack_ports(self, parent=None):
        if parent is None:
            parent = self
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        # add ains
        ain_frm = ttk.Frame(parent)
        self.configure_grid(ain_frm, row=0, column=0)
        lbl = ttk.Label(ain_frm, text="Analog Inputs")
        self.configure_grid(lbl, sticky="n", row=0, column=0)
        for ain in range(14):
            row = ain % 5
            column = ain // 5
            w = self.new_ain_widget(ain, parent=ain_frm)
            self.configure_grid(w, sticky="w", row=row+1, column=column)
        self.configure_column(ain_frm, [0, 1, 2])
        # add mios
        dio_frm = ttk.Frame(parent)
        self.configure_grid(dio_frm, row=0, column=1)
        self.configure_column(dio_frm, [0, 1, 2])
        lbl = ttk.Label(dio_frm, text="Digital I/O")
        self.configure_grid(lbl, sticky="nw", row=0, column=0)
        for dio in range(20):
            row = dio % 5
            column = dio // 5
            w = self.new_dio_widget(dio, parent=dio_frm)
            self.configure_grid(w, sticky="w", row=row+1, column=column)

    def new_ain_widget(self, ain, parent=None):
        if parent is None:
            parent = self
        name = "ain_%s" % ain
        v = self.add_variable(name, tk.IntVar())
        cb = ttk.Checkbutton(
            parent, text=name.upper(), command=lambda: self.toggle_ain(ain),
            variable=v
        )
        return self.add_widget(name, cb)

    def new_dio_widget(self, dio, parent=None):
        if parent is None:
            parent = self
        name = "dio_%s" % dio
        v = self.add_variable(name, tk.IntVar())
        cb = ttk.Checkbutton(
            parent, text=name.upper(), command=lambda: self.toggle_dio(dio),
            variable=v
        )
        return self.add_widget(name, cb)

    def setup_plot(self, parent=None):
        if parent is None:
            parent = self
        self.add_widget("add_plot", LabJackPlotFrame(parent))
        self.plot.setup()
        self.configure_grid(self.plot, row=3, column=0, columnspan=2)
        self.plot.grid_columnconfigure(0, weight=1)
        self.plot.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)

    def setup_control(self, parent=None):
        if parent is None:
            parent = self
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(2, weight=1)
        self.widgets["start"] = ttk.Button(
            parent, text="Record", command=self.start_update,
            state="normal"
        )
        self.widgets["start"].grid(row=0, column=0)
        self.widgets["pause"] = ttk.Button(
            parent, text="Pause", command=self.pause_update,
            state="disabled"
        )
        self.widgets["pause"].grid(row=0, column=1)
        self.widgets["reset"] = ttk.Button(
            parent, text="Reset", command=self.reset_plot,
            state="normal"
        )
        self.widgets["reset"].grid(row=0, column=2)
        v = self.add_variable("status", tk.StringVar())
        status = ttk.Label(
            parent, textvariable=v,
        )
        status.grid(row=1, column=0, columnspan=3)
        # refresh rate
        self.setup_rate(parent)

    def setup_rate(self, parent=None):
        if parent is None:
            parent = self
        label = ttk.Label(parent, text="Refresh rate:")
        label.grid(row=2, column=0)
        v = self.add_variable("refresh_rate", tk.StringVar())
        cob = ttk.Combobox(
            parent, state="readonly", textvariable=v
        )
        self.add_widget("refresh_rate", cob)
        rates = sorted(self.REFRESH_RATES, key=self.REFRESH_RATES.get)
        cob["values"] = rates
        cob.current(rates.index("1 sec"))
        cob.bind("<<ComboboxSelected>>", self.update_rate)
        cob.grid(row=2, column=1)

    def reset_plot(self):
        self.controller.reset_plot()

    def start_update(self):
        if self.controller.start_update():
            self.get_widget("start")["state"] = "disabled"
            self.get_widget("pause")["state"] = "normal"

    def pause_update(self):
        if self.controller.stop_update():
            self.get_widget("pause")["state"] = "disabled"
            self.get_widget("start")["state"] = "normal"

    def update_rate(self, event):
        self.controller.update_interval = self.refresh_rate

    def update_resolution(self, event):
        self.controller.update_resolution(self.resolution)

    def update_gain(self, event):
        self.controller.update_gain(self.gain)

    def toggle_ain(self, ain):
        name = "ain_%s" % ain
        v = self.get_variable(name)
        self.controller.toggle_ain(ain, v.get())

    def toggle_dio(self, dio):
        name = "dio_%s" % dio
        v = self.get_variable(name)
        self.controller.toggle_dio(dio, v.get())
