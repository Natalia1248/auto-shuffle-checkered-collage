from tkinter import Canvas
from copy import deepcopy
from PIL import ImageTk, Image
from selection import Selection
from history import History


class GridCanvas(Canvas):
    def __init__(self, master=None, **kw):
        self.show_outline = False
        self.line_ids = []

        # variable to communicate info between select_clicked and select_dragged, to avoid glitchy dragging
        self.selecting = False

        # cell width, cell height
        self.cellw = 50
        self.cellh = 50

        self.image = None
        self.zoom = 0.5

        self.selection = Selection()

        self.history = History(30)

        Canvas.__init__(self, master=master, **kw)

    def update_image(self, image):
        self.image = deepcopy(image)

        self.delete("all")

        width, height = map(lambda x: int(x * self.zoom), image.size)

        self.display_image = self.image.resize(
            (width, height), Image.Resampling.LANCZOS
        )

        self["scrollregion"] = (0, 0, width, height)
        self.config(width=width, height=height)

        self.__tkimage = ImageTk.PhotoImage(image=self.display_image)
        self.create_image(0, 0, image=self.__tkimage, anchor="nw", state="normal")
        self._remake_grid()

    def unselect_all(self):
        for id in self.selection.all_ids():
            self.delete(id)
        self.selection.remove_all()

    def select_all(self):
        width, height = self.display_image.size

        for i in range(0, width, self.display_cellw):
            for j in range(0, height, self.display_cellh):
                self._select_cell(i, j)

    def handle_click(self, event):
        if not self.image:
            return

        i, j = self._location_to_grid_position(event.x, event.y)

        if not self.selection.position_id(i, j):
            self.selecting = True
            self._select_cell(i, j)
        else:
            self.selecting = False
            self._unselect_cell(i, j)

    def handle_drag(self, event):
        if not self.image:
            return

        i, j = self._location_to_grid_position(event.x, event.y)

        if self.selecting:
            self._select_cell(i, j)
        else:
            self._unselect_cell(i, j)

    def set_cell_size(self, cellw, cellh):

        self.display_cellw = int(cellw * self.zoom)
        self.display_cellh = int(cellh * self.zoom)

        self.cellw = int(self.display_cellw // self.zoom)
        self.cellh = int(self.display_cellh // self.zoom)

        self._remake_grid()

    def canvas_effect_handler(self, func):
        def handler(_event=None):
            self.create_rectangle(
                0,
                0,
                self.history.current().size[0],
                self.history.current().size[1],
                fill="green",
                stipple="gray25",
            )
            new_image = func(deepcopy(self.history.current()), self)
            self.delete("all")
            self.history.push(new_image)
            self.update_image(new_image)
            self._remake_grid()

        return handler

    def not_first(self, func):
        def inner(event=None):
            if self.image:
                func(event)

        return inner

    def toggle_lines(self):
        self.show_outline = not self.show_outline
        self._remake_grid()

    def _location_to_grid_position(self, x, y):
        i = int(self.canvasx(x) // self.display_cellw)
        j = int(self.canvasy(y) // self.display_cellh)
        return (i, j)

    def _select_cell(self, i, j):
        if not self.selection.position_id(i, j):
            self.selection.put_cell(i, j, self._make_orange_cell(i, j))

    def _unselect_cell(self, i, j):
        cell_id = self.selection.position_id(i, j)
        if cell_id:
            self.delete(cell_id)
        self.selection.remove_cell(i, j)

    def _remake_grid(self):
        for id in self.line_ids:
            self.delete(id)
        self.line_ids = []

        if self.show_outline:
            width, height = self.display_image.size

            for i in range(0, width, self.display_cellw):
                self.line_ids.append(self.create_line(i, 0, i, height))
            for j in range(0, height, self.display_cellh):
                self.line_ids.append(self.create_line(0, j, width, j))

        for i, j in self.selection.all_positions():
            self.delete(self.selection.position_id(i, j))

        for i, j in self.selection.all_positions():
            self.selection.put_cell(i, j, self._make_orange_cell(i, j))

    def _make_orange_cell(self, x, y):
        return self.create_rectangle(
            x * self.display_cellw,
            y * self.display_cellh,
            x * self.display_cellw + self.display_cellw,
            y * self.display_cellh + self.display_cellh,
            fill="orange",
            outline="",
            stipple="gray50",
        )
