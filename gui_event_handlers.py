from tkinter import filedialog
import tkinter as tk

from config import *
from effects import to_red_checkers, to_red, shuffle_alg, shuffle_alg2

aux = 1

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
    return Image.open(imagepath)


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
    orig = Image.open(imagepath)

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
    global aux

    if square_checked and (aux == 1 or aux == 2):
        hval.set(wval.get())
        hstr.set(str(wval.get()))
        if aux == 2:
            aux = 3

    c.set_cell_size(wval.get(), hval.get())
    wstr.set(str(event))


def height_slide(event):
    global aux

    if square_checked and (aux == 1 or aux == 3):
        wval.set(hval.get())
        wstr.set(str(hval.get()))
        c.cell_size(wval.get(), hval.get())
        if aux == 3:
            aux = 2
    else:
        aux = 1

    c.set_cell_size(wval.get(), hval.get())
    hstr.set(str(event))


@c.not_first
def entpress(event):
    if not (int(wstr.get()) == 1 or int(hstr.get()) == 1):
        if int(wstr.get()) != wval.get():
            wval.set(int(wstr.get()))
            if square_checked:
                hval.set(int(wstr.get()))
                hstr.set(wstr.get())
        elif int(hstr.get()) != hval.get():
            hval.set(int(hstr.get()))
            if square_checked:
                wval.set(int(hstr.get()))
                wstr.set(hstr.get())
        c.set_cell_size(wval.get(), hval.get())


square_checked = False


@c.not_first
def check(event=None):
    global square_checked

    square_checked = not square_checked
    if square_checked:
        lesser = min(hval.get(), wval.get())
        hval.set(lesser)
        wval.set(lesser)
        wstr.set(lesser)
        hstr.set(lesser)
    c.set_cell_size(hval.get(), wval.get())


show_lines = False


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


def openim(width_sldr, height_sldr):
    def handle_openim(event=None):
        global imagepath, aux
        aux = 1

        try:
            fileobj = filedialog.askopenfile()
            imagepath = fileobj.name
            im = Image.open(fileobj.name)
        except:
            return

        c.update_image(im)

        width_sldr.config(to=im.size[0])
        height_sldr.config(to=im.size[1])

        c.history.push(im)  # TODO: canvas itself should push to history

    return handle_openim
