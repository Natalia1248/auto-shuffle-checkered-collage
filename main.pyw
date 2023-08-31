import tkinter as tk

from config import *
from gui_event_handlers import *

window.grid_columnconfigure(0, weight=1, minsize=15)
window.grid_columnconfigure(1, weight=1)
window.grid_columnconfigure(2, weight=15, minsize=100)
window.grid_columnconfigure(3, weight=1, minsize=610)
window.grid_rowconfigure(1, weight=1, minsize=15)
window.grid_rowconfigure(2, weight=1)
window.grid_rowconfigure(3, weight=1)
window.bind("<Button-1>", generic_click)

c.canvas = tk.Canvas(master=window)


l_frm.grid(row=0, column=1, pady=3, sticky="w")


r_frm.grid(row=0, column=3)


test_btn = tk.Button(master=r_frm, command=function1, text="red checkers")
test_btn.configure(
    bg=rb_color, fg="white", activebackground=ra_color, activeforeground="white"
)
test_btn.pack(side="right", ipadx=10)

test_btn2 = tk.Button(master=r_frm, command=function2, text="make red")
test_btn2.pack(side="right", ipadx=10)
test_btn2.configure(
    bg=rb_color, fg="white", activebackground=ra_color, activeforeground="white"
)

shuffle2_btn = tk.Button(master=r_frm, command=shuffle2, text="shuffle\nswapping")
shuffle2_btn.pack(side="right")
shuffle2_btn.configure(
    bg=rb_color, fg="white", activebackground=ra_color, activeforeground="white"
)

shfl_btn = tk.Button(master=r_frm, command=shuffle, text="shuffle\npasting")
shfl_btn.pack(side="right")
shfl_btn.configure(
    bg=rb_color, fg="white", activebackground=ra_color, activeforeground="white"
)

or_btn = tk.Button(master=r_frm, command=original, text="replace with original cells")
or_btn.pack(side="right")
or_btn.configure(
    bg=rb_color, fg="white", activebackground=ra_color, activeforeground="white"
)

swap_btn = tk.Button(
    master=r_frm, command=swapb, text="swap two cells\n(swaps the first two selected)"
)
swap_btn.pack(side="right")
swap_btn.configure(
    bg=rb_color, fg="white", activebackground=ra_color, activeforeground="white"
)


##########
save_btn = tk.Button(master=l_frm, command=saves, text="save\nimage")
save_btn.pack(side="left")
save_btn.configure(bg=lb_color, activebackground=la_color)

open_btn = tk.Button(master=l_frm, command=openim, text="load image")
open_btn.pack(side="left")
open_btn.configure(bg=lb_color, activebackground=la_color)

restart_btn = tk.Button(master=l_frm, command=restart, text="reset image")
restart_btn.configure(bg=lb_color, activebackground=la_color)
restart_btn.pack(side="left")

crope_btn = tk.Button(master=l_frm, command=crop_even, text="crop evenly to grid size")
crope_btn.pack(side="left")
crope_btn.configure(bg=lb_color, activebackground=la_color)

undo_btn = tk.Button(master=l_frm, command=undo, text="undo\n[Ctr+z]")
undo_btn.pack(side="left")
undo_btn.configure(bg=lb_color, activebackground=la_color)

redo_btn = tk.Button(master=l_frm, command=redo, text="redo\n[Ctr+Shift+z]")
redo_btn.pack(side="left")
redo_btn.configure(bg=lb_color, activebackground=la_color)

######
vscrollbar = tk.Scrollbar(master=window)
vscrollbar.config(command=c.canvas.yview)
vscrollbar.grid(row=3, column=0, sticky="ens", pady=15)

hscrollbar = tk.Scrollbar(master=window)
hscrollbar.config(
    command=c.canvas.xview,
    orient="horizontal",
)
hscrollbar.grid(row=1, column=1, sticky="wse")

c.canvas.config(yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
c.canvas.outline = ""
c.canvas.grid(row=3, column=1, sticky="n")
c.canvas.create_text(200, 100, text="Load an image please", font=("Helvetica", 24))


wentry = tk.Entry(s_frm, textvariable=wstr, width=4)
wentry.grid(row=1, column=0)
wstr.set(50)
hentry = tk.Entry(s_frm, textvariable=hstr, width=4)
hentry.grid(row=1, column=1, padx=10)
hstr.set(50)
other = 0

chk_btn = tk.Checkbutton(s_frm, text="get square cells", command=check, variable=other)
chk_btn.grid(row=2, column=0)


g_btn = tk.Checkbutton(window, text="show grid", command=lines_checkbox)
g_btn.grid(row=1, column=2, padx=10, sticky="sw")

c.canvas.bind("<B1-Motion>", c.handle_drag)
c.canvas.bind("<Button-1>", c.handle_click)

window.bind("<Escape>", lambda event: c.unselect_all())
window.bind("<Control-a>", lambda event: c.select_all())
window.bind("<Control-z>", undo)
window.bind("<Control-Shift-Key-Z>", redo)
window.bind("<Return>", entpress)

window.mainloop()
