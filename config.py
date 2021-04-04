from grid_canvas import grid_canvas
import tkinter as tk
from tkinter import filedialog
from collections import deque
from PIL import Image



general_color='#310058'
lb_color='#00D6DC'
la_color='#00999D'
rb_color='#A300D9'
ra_color='#8E00BD'
s_color='#0C01BE'
window=tk.Tk()
window.iconbitmap('icon.ico')
window.title('Checkered collage-o-matic')
window.configure(bg=general_color)

imagepath=""#filedialog.askopenfile().name#"C:\\Users\\Usuario\\OneDrive\\Escritorio\\some python shit\\playin around slash learning\\ImgsStuff\\image.jpg"


wscroll_length=0#2*history[current].size[0]//3
hscroll_length=0
l_frm=tk.Frame(master=window,
               relief=tk.RAISED,
               borderwidth=5,
               background=general_color
               )

r_frm=tk.Frame(master=window,
               relief=tk.RAISED,
               borderwidth=5,
               background=general_color
               )
s_frm=tk.Frame(master=window)
s_frm.grid(row=3, column=3, sticky='e')
s_frm['bg']=s_color

c_frm=tk.Frame(window)
c_frm['bg']=s_color
c_frm.grid(row=1,column=1, padx=5, pady=5)
c=grid_canvas(window,)


#print(c.cellw)

wstr=tk.StringVar()
wval=tk.IntVar()
hstr=tk.StringVar()
hval=tk.IntVar()


