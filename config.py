from grid_canvas import GridCanvas
import tkinter as tk
from tkinter import filedialog
from PIL import Image

imagepath = ""

window = tk.Tk()

c = GridCanvas()

wstr = tk.StringVar()
wval = tk.IntVar()
hstr = tk.StringVar()
hval = tk.IntVar()
