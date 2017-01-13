"""A simple view with a plot"""

from . import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


class PlotView(View):
    """Note: inline view!"""

    def __init__(self, parent, window):
        super(PlotView, self).__init__(parent, window)

    def setup(self):
        self.grid(row=0, column=0, sticky="nsew")
        # add widgets
        label = ttk.Label(self, text="Nice cool graph below", font=self.FONT_LARGE)
        label.pack(pady=10, padx=10)
        self.setup_plot()

    def setup_plot(self):
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
