import tkinter as tk

from config import c, window
from gui_event_handlers import *

general_color = "#310058"
left_btn_a_color = "#00999D"
left_btn_b_color = "#00D6DC"
right_btn_a_color = "#8E00BD"
right_btn_b_color = "#A300D9"
sliders_color = "#0C01BE"


window.iconbitmap("icon.ico")
window.title("Checkered collage-o-matic")
window.configure(bg=general_color)


def draw_effects_frm(r_frm, parent_effects_frm):
    red_checkers_btn = tk.Button(master=r_frm, command=make_red_checkers, text="red checkers".title())
    red_checkers_btn.configure(
        bg=right_btn_b_color, fg="white", activebackground=right_btn_a_color, activeforeground="white"
    )
    red_checkers_btn.grid(row=1, column=3, sticky="nsew")

    red_btn = tk.Button(master=r_frm, command=make_red, text="make red".title())
    red_btn.grid(row=1, column=2, sticky="nsew")
    red_btn.configure(
        bg=right_btn_b_color, fg="white", activebackground=right_btn_a_color, activeforeground="white"
    )

    shuffle_swapping_btn = tk.Button(
        master=r_frm,
        command=shuffle_swapping(parent_effects_frm),
        text="shuffle swapping".title(),
    )
    shuffle_swapping_btn.grid(row=0, column=0, sticky="nsew")
    shuffle_swapping_btn.configure(
        bg=right_btn_b_color, fg="white", activebackground=right_btn_a_color, activeforeground="white"
    )

    shuffle_pasting_btn = tk.Button(
        master=r_frm,
        command=shuffle_pasting(parent_effects_frm),
        text="shuffle pasting".title(),
    )
    shuffle_pasting_btn.grid(row=0, column=1, sticky="nsew")
    shuffle_pasting_btn.configure(
        bg=right_btn_b_color, fg="white", activebackground=right_btn_a_color, activeforeground="white"
    )

    original_cells_btn = tk.Button(
        master=r_frm, command=original, text="replace with original cells".title()
    )
    original_cells_btn.grid(row=0, column=2, sticky="nsew")
    original_cells_btn.configure(
        bg=right_btn_b_color, fg="white", activebackground=right_btn_a_color, activeforeground="white"
    )

    swap_btn = tk.Button(
        master=r_frm,
        command=swap,
        text="swap two cells\n(swaps the first two selected)".title(),
    )
    swap_btn.grid(row=0, column=3, sticky="nsew")
    swap_btn.configure(
        bg=right_btn_b_color, fg="white", activebackground=right_btn_a_color, activeforeground="white"
    )


def draw_file_control_frm(l_frm, on_openim):
    save_btn = tk.Button(master=l_frm, command=saves, text="save\nimage".title())
    save_btn.pack(side="left", fill="both")
    save_btn.configure(bg=left_btn_a_color, activebackground=left_btn_b_color)

    open_btn = tk.Button(
        master=l_frm, command=openim(on_openim), text="load image".title()
    )
    open_btn.pack(side="left", fill="both")
    open_btn.configure(bg=left_btn_a_color, activebackground=left_btn_b_color)

    restart_btn = tk.Button(master=l_frm, command=restart, text="reset image".title())
    restart_btn.configure(bg=left_btn_a_color, activebackground=left_btn_b_color)
    restart_btn.pack(side="left", fill="both")

    crop_even_btn = tk.Button(
        master=l_frm, command=crop_even, text="crop evenly to grid size".title()
    )
    crop_even_btn.pack(side="left", fill="both")
    crop_even_btn.configure(bg=left_btn_a_color, activebackground=left_btn_b_color)

    undo_btn = tk.Button(master=l_frm, command=undo, text="undo\n[Ctr+z]".title())
    undo_btn.pack(side="left", fill="both")
    undo_btn.configure(bg=left_btn_a_color, activebackground=left_btn_b_color)

    redo_btn = tk.Button(master=l_frm, command=redo, text="redo\n[Ctr+Shift+z]".title())
    redo_btn.pack(side="left", fill="both")
    redo_btn.configure(bg=left_btn_a_color, activebackground=left_btn_b_color)


def draw_canvas_frm(canvas_frm):
    c.canvas = tk.Canvas(master=canvas_frm)

    c.canvas.outline = "red"
    c.canvas.pack()
    c.canvas.create_text(
        200, 100, text="Load an image please".title(), font=("Helvetica", 24)
    )


def draw_sliders_frm(sliders_frm):
    sliders_frm["bg"] = sliders_color

    wstr = tk.StringVar(value=50)
    wval = tk.IntVar(value=50)
    hstr = tk.StringVar(value=50)
    hval = tk.IntVar(value=50)

    width_slider = tk.Scale(
        master=sliders_frm,
        from_=2,
        command=width_slide,
        label="CELL WIDTH",
        width=10,
        length=400,
        variable=wval,
        state="disabled",
    )
    width_slider.grid(row=0, column=3)

    height_slider = tk.Scale(
        master=sliders_frm,
        from_=2,
        command=height_slide,
        label="CELL HEIGHT",
        width=10,
        length=400,
        variable=hval,
        state="disabled",
    )
    height_slider.grid(row=0, column=2)

    wentry = tk.Entry(sliders_frm, textvariable=wstr, width=4, state="disabled")
    wentry.grid(row=1, column=3)
    hentry = tk.Entry(sliders_frm, textvariable=hstr, width=4, state="disabled")
    hentry.grid(row=1, column=2)

    c.cell_dim_subscribe(lambda *cell_dims: wstr.set(cell_dims[0]))
    c.cell_dim_subscribe(lambda *cell_dims: hstr.set(cell_dims[1]))
    c.cell_dim_subscribe(lambda *cell_dims: width_slider.set(cell_dims[0]))
    c.cell_dim_subscribe(lambda *cell_dims: height_slider.set(cell_dims[1]))

    buttons_frm = tk.Frame(master=sliders_frm)
    buttons_frm.grid(row=0, column=0, sticky="n")
    grid_btn = tk.Checkbutton(
        buttons_frm, text="show grid".title(), command=lines_checkbox, state="disabled"
    )
    grid_btn.pack(side="top")

    chk_btn = tk.Checkbutton(
        buttons_frm, text="get square cells".title(), command=check, state="disabled"
    )
    chk_btn.pack(side="top")

    for frm in sliders_frm.winfo_children():
        frm.grid_configure(padx=5, pady=5)

    def on_openim(image):
        width_slider.config(to=image.size[0])
        height_slider.config(to=image.size[1])

        width_slider.config(state="normal")
        height_slider.config(state="normal")
        wentry.config(state="normal")
        hentry.config(state="normal")
        chk_btn.config(state="normal")
        grid_btn.config(state="normal")

    return on_openim, buttons_frm, wentry, hentry


l_frm = tk.Frame(
    master=window, relief=tk.RAISED, borderwidth=5, background=general_color
)
sliders_frm = tk.Frame(master=window)
canvas_frm = tk.Frame(master=window)
r_frm = tk.Frame(
    master=window, relief=tk.RAISED, borderwidth=5, background=general_color
)


l_frm.grid(row=0, column=0, sticky="w")
canvas_frm.grid(row=1, column=0)
r_frm.grid(row=0, column=2)
sliders_frm.grid(row=1, column=2, sticky="se")

on_openim, buttons_frm, width_entry, height_entry = draw_sliders_frm(sliders_frm)
draw_file_control_frm(l_frm, on_openim)
draw_canvas_frm(canvas_frm)
draw_effects_frm(r_frm, buttons_frm)

for frm in window.winfo_children():
    frm.grid_configure(padx=10, pady=10)

c.canvas.bind("<B1-Motion>", c.handle_drag)
c.canvas.bind("<Button-1>", c.handle_click)
window.bind("<Escape>", lambda event: c.unselect_all())
window.bind("<Control-a>", lambda event: c.select_all())
window.bind("<Control-z>", undo)
window.bind("<Control-Shift-Key-Z>", redo)
window.bind("<Return>", entpress(width_entry, height_entry))

window.mainloop()
