from copy import deepcopy
from PIL import ImageTk, Image
from selection import Selection
from history import History

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600


class GridCanvas:
    def __init__(self):
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

        self.canvas = None

        self.cell_dims_listeners = []

        self.get_square_cells = False

    def update_image(self, image):
        self.image = deepcopy(image)

        self.canvas.delete("all")

        self.zoom = CANVAS_WIDTH / image.size[0]

        width, height = map(lambda x: round(x * self.zoom), image.size)

        self.display_image = self.image.resize(
            (width, height), Image.Resampling.LANCZOS
        )

        self.canvas["scrollregion"] = (0, 0, width, height)
        self.canvas.config(width=CANVAS_WIDTH, height=min(CANVAS_HEIGHT, height))

        self.__tkimage = ImageTk.PhotoImage(image=self.display_image)
        self.canvas.create_image(
            0, 0, image=self.__tkimage, anchor="nw", state="normal"
        )
        self._remake_grid()

    def unselect_all(self):
        for id in self.selection.all_ids():
            self.canvas.delete(id)
        self.selection.remove_all()

    def select_all(self):
        width, height = self.display_image.size

        for i in range(width // round(self.cellw * self.zoom) + 2):
            for j in range(height // round(self.cellh * self.zoom) + 2):
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
        if self.get_square_cells:
            size = (cellw + cellh) // 2
            self.cellw = self.cellh = size
        else:
            self.cellw = cellw
            self.cellh = cellh
        self._notify_cell_dim_change()
        self._remake_grid()

    def canvas_effect_handler(self, func):
        def handler(_event=None):
            self.canvas.create_rectangle(
                0,
                0,
                self.history.current().size[0],
                self.history.current().size[1],
                fill="green",
                stipple="gray25",
            )
            new_image = func(deepcopy(self.history.current()), self)
            self.canvas.delete("all")
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

    def toggle_square_cells(self):
        self.get_square_cells = not self.get_square_cells
        if self.get_square_cells:
            size = (self.cellw + self.cellh) // 2
            self.cellw = self.cellh = size
            self._notify_cell_dim_change()
            self._remake_grid()

    def cell_dim_subscribe(self, callback):
        self.cell_dims_listeners.append(callback)

    def _location_to_grid_position(self, x, y):
        i = round(self.canvas.canvasx(x) // (self.cellw * self.zoom))
        j = round(self.canvas.canvasy(y) // (self.cellh * self.zoom))
        return (i, j)

    def _notify_cell_dim_change(self):
        for fn in self.cell_dims_listeners:
            fn(self.cellw, self.cellh)

    def _select_cell(self, i, j):
        if not self.selection.position_id(i, j):
            self.selection.put_cell(i, j, self._make_orange_cell(i, j))

    def _unselect_cell(self, i, j):
        cell_id = self.selection.position_id(i, j)
        if cell_id:
            self.canvas.delete(cell_id)
        self.selection.remove_cell(i, j)

    def _remake_grid(self):
        for id in self.line_ids:
            self.canvas.delete(id)
        self.line_ids = []

        if self.show_outline:
            width, height = self.image.size

            for a in range(0, width, self.cellw):
                x = a * self.zoom
                self.line_ids.append(self.canvas.create_line(x, 0, x, height))
            for b in range(0, height, self.cellh):
                y = b * self.zoom
                self.line_ids.append(self.canvas.create_line(0, y, width, y))

        for i, j in self.selection.all_positions():
            self.canvas.delete(self.selection.position_id(i, j))

        for i, j in self.selection.all_positions():
            self.selection.put_cell(i, j, self._make_orange_cell(i, j))

    def _make_orange_cell(self, x, y):
        return self.canvas.create_rectangle(
            round(x * self.cellw * self.zoom),
            round(y * self.cellh * self.zoom),
            round((x + 1) * self.cellw * self.zoom),
            round((y + 1) * self.cellh * self.zoom),
            fill="orange",
            outline="",
            stipple="gray50",
        )
