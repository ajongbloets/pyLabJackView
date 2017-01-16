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

    def _setup_figure(self, size, dpi=100):
        if not isinstance(size, tuple) and not len(size) == 2:
            raise ValueError("Invalid value for size (need tuple of length 2)")
        f = Figure(figsize=size, dpi=dpi)
        self._figure = f

    def _setup_canvas(self):
        if not isinstance(self.figure, Figure):
            raise ValueError("Invalid figure object")
        self._canvas = FigureCanvasTkAgg(self.figure, self.parent)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self._setup_toolbar()

    def _setup_toolbar(self):
        self._toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    @property
    def figure(self):
        """Returns the current plot figure of this Frame

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
    def toolbar(self):
        return self._toolbar

    def setup(self, size=None, dpi=100):
        if size is None:
            size = (5, 5)
        self._setup_figure(size, dpi)
        self._setup_canvas()

    def plot(self, x, y, subplot=None, clear=False, **kwargs):
        """Plots the data """
        if clear:
            self.figure.clear()
        if subplot is None:
            subplot = self.figure.add_subplot(111)
        subplot.plot(x, y)
        self.canvas.draw()
        return subplot


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
        self.grid(row=0, column=0, sticky="nsew")
        # add widgets
        label = ttk.Label(self, text="Nice cool graph below", font=self.FONT_LARGE)
        label.pack(pady=10, padx=10)
        self.setup_plot()

    def setup_plot(self):
        self._plot = PlotFrame(self, self.controller)
        self.plot.setup()
        # self.plot.plot([0, 1, 2, 3, 4], [1, 2, 4, 8, 16])
