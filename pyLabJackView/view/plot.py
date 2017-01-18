"""A simple view with a plot"""

from . import *
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


class PlotFrame(Frame):
    """Only the Plot as a frame object"""

    def __init__(self, parent, controller):
        super(PlotFrame, self).__init__(parent, controller)
        self._figure = None
        self._canvas = None
        self._toolbar = None
        self._legend = None
        self._axes = None

    def _setup_figure(self, size, dpi=100):
        if not isinstance(size, tuple) and not len(size) == 2:
            raise ValueError("Invalid value for size (need tuple of length 2)")
        f = Figure(figsize=size, dpi=dpi)
        self._figure = f

    def _setup_canvas(self):
        if not isinstance(self.figure, Figure):
            raise ValueError("Invalid figure object")
        self._canvas = FigureCanvasTkAgg(self.figure, self)
        self._setup_toolbar()
        self.canvas.show()
        self._canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def _setup_toolbar(self):
        self._toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def _setup_subplot(self):
        self._axes = self.figure.add_subplot(111)

    @property
    def figure(self):
        """Returns the current add_plot figure of this Frame

        :rtype: matplotlib.figure.Figure
        """
        return self._figure

    @property
    def canvas(self):
        """Returns the current canvas of this frame

        :rtype: matplotlib.backends.backend_tkagg.FigureCanvasTkAgg
        """
        return self._canvas

    @property
    def axes(self):
        return self._axes

    @property
    def legend(self):
        return self._legend

    @property
    def toolbar(self):
        return self._toolbar

    def setup(self, size=None, dpi=100):
        if size is None:
            size = (5, 5)
        self._setup_figure(size, dpi)
        self._setup_canvas()
        self._setup_subplot()

    def add_legend(self):
        if self.axes is not None:
            self._legend = self.axes.legend(loc='best')

    def draw(self):
        self.canvas.draw()

    def clear(self):
        self.figure.clear()
        self._setup_subplot()
        self.canvas.draw()


class PlotView(View):
    """Note: inline view!"""

    def __init__(self, parent, controller):
        super(PlotView, self).__init__(parent, controller)
        self._plot = None

    @property
    def plot(self):
        """
        :rtype: pyLabJackView.view.plot.PlotFrame
        """
        return self._plot

    def setup(self):
        self.configure_grid(self)
        # add widgets
        label = ttk.Label(self, text="Nice cool graph below", font=self.FONT_LARGE)
        label.pack(pady=10, padx=10)
        self.setup_plot()

    def setup_plot(self):
        self._plot = PlotFrame(self, self.controller)
        self.plot.setup()
        # self.add_plot.add_plot([0, 1, 2, 3, 4], [1, 2, 4, 8, 16])


class LivePlotView(PlotView):
    """Module with view showing labjack measurements"""

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
        super(LivePlotView, self).__init__(parent, controller)
        self._start_button = None
        self._pause_button = None
        self._reset_button = None
        self._rate_picker = None
        self._refresh_rate = tk.StringVar()
        self._status = tk.StringVar()
        self._plot = None

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

        :rtype: pyLabJackView.view.plot.PlotFrame
        """
        return self._plot

    @property
    def refresh_rate(self):
        v = self._rate_picker.get()
        return self.REFRESH_RATES.get(v, 1)

    def set_status_text(self, str):
        self._status.set(str)

    def setup(self):
        self.grid(row=0, column=0, sticky="nsew")
        # add widgets
        self.setup_control()
        self.setup_plot()

    def setup_plot(self):
        self._plot = PlotFrame(self, self.controller)
        self.plot.setup()
        self.plot.grid(row=3, column=0, columnspan=3)

    def setup_control(self, parent=None):
        if parent is None:
            parent = self
        self._start_button = ttk.Button(
            parent, text="Record", command=self.start_update,
            state="normal"
        )
        self._start_button.grid(row=0, column=0)
        self._pause_button = ttk.Button(
            parent, text="Pause", command=self.pause_update,
            state="disabled"
        )
        self._pause_button.grid(row=0, column=1)
        status = ttk.Label(
            parent, textvariable=self._status,
        )
        self._reset_button = ttk.Button(
            parent, text="Reset", command=self.reset_plot,
            state="disabled"
        )
        self._reset_button.grid(row=0, column=2)
        status.grid(row=1, columnspan=3)
        # refresh rate
        self.setup_rate(parent)

    def setup_rate(self, parent=None):
        if parent is None:
            parent = self
        label = ttk.Label(parent, text="Refresh rate:")
        label.grid(row=2, column=0)
        self._rate_picker = ttk.Combobox(
            parent, state="readonly", textvariable=self._refresh_rate
        )
        self._rate_picker["values"] = self.REFRESH_RATES.keys()
        self._rate_picker.current(self.REFRESH_RATES.keys().index("1 sec"))
        self._rate_picker.bind("<<ComboboxSelected>>", self.update_rate)
        self._rate_picker.grid(row=2, column=1, columnspan=2)

    def reset_plot(self):
        self.controller.reset_plot()

    def start_update(self):
        if self.controller.start_update():
            self._start_button["state"] = "disabled"
            self._pause_button["state"] = "normal"
            self._reset_button["state"] = "normal"

    def pause_update(self):
        if self.controller.stop_update():
            self._pause_button["state"] = "disabled"
            self._start_button["state"] = "normal"

    def update_rate(self, event):
        self.controller.update_interval = self.refresh_rate
