from PIL import Image
from random import randint


def to_red(image, grid_canvas):
    cellw = grid_canvas.cellw
    cellh = grid_canvas.cellh

    for i, j in grid_canvas.selection.all_positions():
        x = i * cellw
        y = j * cellh
        box = (x, y, x + cellw, y + cellh)
        image.paste(make_red(image.crop(box)), box)
    return image


def to_red_checkers(image, grid_canvas):
    cellw = grid_canvas.cellw
    cellh = grid_canvas.cellh
    for i in range(
        grid_canvas.selection.get_left_boundary(), grid_canvas.selection.get_right_boundary() + 1
    ):
        for j in range(
            grid_canvas.selection.get_top_boundary(), grid_canvas.selection.get_bottom_boundary() + 1
        ):
            if grid_canvas.selection.position_id(i, j) != None:
                x = i * cellw
                y = j * cellh
                box = (x, y, x + cellw, y + cellh)
                # one is even and the other is not
                if (i % 2 == 0 and j % 2 != 0) or (i % 2 != 0 and j % 2 == 0):
                    image.paste(make_red(image.crop(box)), box)
    return image


def crop(image):
    return image.crop((0, 0, 600, 400))


def make_red(image):
    imageR = image.getchannel(0)
    imageN = imageR.point(lambda i: False)
    return Image.merge(image.mode, [imageR, imageN, imageN])


def to_shuffle_paste(image, grid_canvas, var):
    cellw = grid_canvas.cellw
    cellh = grid_canvas.cellh
    selected_cells = {}
    for x in range(
        grid_canvas.selection.get_left_boundary(), grid_canvas.selection.get_right_boundary() + 1
    ):
        for y in range(
            grid_canvas.selection.get_top_boundary(), grid_canvas.selection.get_bottom_boundary() + 1
        ):
            if grid_canvas.selection.position_id(x, y) is not None:
                selected_cells[(x, y)] = image.crop(
                    (x * cellw, y * cellh, x * cellw + cellw, y * cellh + cellh)
                )

    for pos in selected_cells.keys():
        x = pos[0]
        y = pos[1]
        n1 = randint(-var, var)
        n2 = randint(-var, var)
        image.paste(selected_cells[pos], ((x + n1) * cellw, (y + n2) * cellh))
    return image


def to_shuffle_swap(image, grid_canvas, var):
    cwidth = grid_canvas.cellw
    cheight = grid_canvas.cellh

    for x in range(
        grid_canvas.selection.get_left_boundary(),
        grid_canvas.selection.get_right_boundary() + 1,
    ):
        for y in range(
            grid_canvas.selection.get_top_boundary(),
            grid_canvas.selection.get_bottom_boundary() + 1,
        ):
            if grid_canvas.selection.position_id(x, y) is not None:
                c = 0
                while c < 3:
                    xfound = randint(x - var, x + var)
                    yfound = randint(y - var, y + var)

                    if grid_canvas.selection.position_id(xfound, yfound) is not None:
                        break

                    c += 1

                if c < 3:
                    ibox = (
                        x * cwidth,
                        y * cheight,
                        (x + 1) * cwidth,
                        (y + 1) * cheight,
                    )
                    guybox = (
                        xfound * cwidth,
                        yfound * cheight,
                        (xfound + 1) * cwidth,
                        (yfound + 1) * cheight,
                    )
                    image = swap(image, ibox, guybox)

    return image


def swap(image, box1, box2):
    buff = image.crop(box1)
    image.paste(image.crop(box2), box1)
    image.paste(buff, box2)
    return image
