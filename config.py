try:
    import tkinter as tk
    from tkinter import messagebox
    from tkinter.filedialog import asksaveasfilename
except ImportError:
    import Tkinter as tk
    from Tkinter import messagebox
    from Tkinter.filedialog import asksaveasfilename

import os


class Config:
    def __init__(self):
        pass