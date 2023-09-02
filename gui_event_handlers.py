from tkinter import filedialog
import tkinter as tk
from PIL import Image

from config import c, window
from effects import to_red_checkers, to_red, shuffle_alg, shuffle_alg2

EFFECT_INPUT_NAME = "effect_input"


@c.not_first
@c.canvas_effect_handler
def function1(img, grid_canvas):
    return to_red_checkers(img, grid_canvas)


@c.not_first
@c.canvas_effect_handler
def function2(img, grid_canvas):
    return to_red(img, grid_canvas)


@c.not_first
@c.canvas_effect_handler
def restart(img, grid_canvas):
    return grid_canvas.history.get_first_ever_item()


@c.not_first
@c.canvas_effect_handler
def crop_even(img, grid_canvas):
    if (img.size[0] % grid_canvas.cellw) % 2 == 0:
        xtrim = (img.size[0] % grid_canvas.cellw) / 2
        addx = 0
    else:
        xtrim = (img.size[0] % grid_canvas.cellw) // 2
        addx = 1
    if (img.size[1] % c.cellh) % 2 == 0:
        ytrim = (img.size[1] % grid_canvas.cellh) / 2
        addy = 0
    else:
        ytrim = (img.size[1] % grid_canvas.cellw) // 2
        addy = 1
    cropped = img.crop(
        (xtrim, ytrim, img.size[0] - xtrim - addx, img.size[1] - ytrim - addy)
    )
    return cropped


@c.not_first
@c.canvas_effect_handler
def swapb(buff, grid_canvas):
    cell1, cell2 = grid_canvas.selection.first_two_selected()

    third = buff.crop(
        (
            cell1[0] * grid_canvas.cellw,
            cell1[1] * grid_canvas.cellh,
            cell1[0] * grid_canvas.cellw + grid_canvas.cellw,
            cell1[1] * grid_canvas.cellh + grid_canvas.cellh,
        )
    )
    buff.paste(
        buff.crop(
            (
                cell2[0] * grid_canvas.cellw,
                cell2[1] * grid_canvas.cellh,
                cell2[0] * grid_canvas.cellw + grid_canvas.cellw,
                cell2[1] * grid_canvas.cellh + grid_canvas.cellh,
            )
        ),
        (
            cell1[0] * grid_canvas.cellw,
            cell1[1] * grid_canvas.cellh,
            cell1[0] * grid_canvas.cellw + grid_canvas.cellw,
            cell1[1] * grid_canvas.cellh + grid_canvas.cellh,
        ),
    )
    buff.paste(
        third,
        (
            cell2[0] * grid_canvas.cellw,
            cell2[1] * grid_canvas.cellh,
            cell2[0] * grid_canvas.cellw + grid_canvas.cellw,
            cell2[1] * grid_canvas.cellh + grid_canvas.cellh,
        ),
    )
    return buff


@c.not_first
@c.canvas_effect_handler
def original(img, grid_canvas):
    orig = grid_canvas.history.get_first_ever_item()

    for x, y in grid_canvas.selection.all_positions():
        box = (
            x * grid_canvas.cellw,
            y * grid_canvas.cellh,
            x * grid_canvas.cellw + grid_canvas.cellw,
            y * grid_canvas.cellh + grid_canvas.cellh,
        )
        img.paste(orig.crop(box), box)

    return img


def draw_effects_frm(canvas_frm):
    effects_frm = tk.Frame(master=canvas_frm, name=EFFECT_INPUT_NAME)
    effects_frm["bg"] = "purple"
    effects_frm.pack()
    entry = tk.Entry(master=effects_frm)
    entry.pack(padx=5, pady=5)

    def window_click(event=None):
        if "effect_input" not in str(event.widget):
            effects_frm.destroy()

    window.bind(
        "<Button-1>", window_click
    )  # No need to unbind, next bind will overwrite

    return effects_frm, entry


def shuffle_pasting(parent_effects_frm):
    @c.not_first
    def handle_shuffle(event=None):
        effects_frm, entry = draw_effects_frm(parent_effects_frm)

        @c.canvas_effect_handler
        def com(buff, grid_canvas):
            return shuffle_alg(buff, grid_canvas, int(entry.get()))

        button = tk.Button(master=effects_frm, command=com, text="Go!")
        button.pack(anchor="center")

    return handle_shuffle


def shuffle_swapping(parent_effects_frm):
    @c.not_first
    def handle_shuffle(event=None):
        effects_frm, entry = draw_effects_frm(parent_effects_frm)

        @c.canvas_effect_handler
        def com(buff, grid_canvas):
            return shuffle_alg2(buff, grid_canvas, int(entry.get()))

        button = tk.Button(master=effects_frm, command=com, text="Go!")
        button.pack(anchor="center")

    return handle_shuffle


@c.not_first
def undo(event=None):
    c.history.undo()
    c.update_image(c.history.current())


@c.not_first
def redo(event=None):
    c.history.redo()
    c.update_image(c.history.current())


def width_slide(event):
    c.set_cell_size(int(event), c.cellh)


def height_slide(event):
    c.set_cell_size(c.cellw, int(event))


def entpress(width_entry, height_entry):
    @c.not_first
    def handle_entpress(event):
        c.set_cell_size(int(width_entry.get()), int(height_entry.get()))

    return handle_entpress


@c.not_first
def check(event=None):
    c.toggle_square_cells()


def lines_checkbox():
    c.toggle_lines()


@c.not_first
def saves(event=None):
    extensions = [
        ("Png", "*.png"),
        ("Jpg", "*.jpg"),
        ("Gif", "*.gif"),
        ("type your own and see if it happens to be supported", "*"),
    ]
    try:
        fileobj = filedialog.asksaveasfile(
            defaultextension=extensions, filetypes=extensions
        )
        if fileobj.name != None:
            c.history.current().save(fileobj.name)
    except Exception as e:
        print(e)


def openim(on_openim):
    def handle_openim(event=None):

        fileobj = filedialog.askopenfile()
        im = Image.open(fileobj.name)

        c.update_image(im)
        c.history.push(im)
        on_openim(im)


    return handle_openim
