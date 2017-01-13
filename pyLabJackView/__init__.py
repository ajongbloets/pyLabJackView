
try:
    import tkinter as tk
    # try python 2
except ImportError:
    print "Could not import Tkinter"
    # maybe python 3?
    import Tkinter as tk