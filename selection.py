from collections import OrderedDict


class Selection:
    def __init__(self):
        self._selection = OrderedDict()

    def put_cell(self, x, y, id):
        self._selection[(x, y)] = id

    def remove_cell(self, x, y):
        if (x, y) in self._selection:
            self._selection.pop((x, y))

    def position_id(self, x, y):
        return self._selection.get((x, y), None)

    def all_ids(self):
        return self._selection.values()

    def all_positions(self):
        return self._selection.keys()

    def first_two_selected(self):
        if len(self._selection) >= 2:
            locs = list(self._selection.keys())
            return (locs[0], locs[1])
        else:
            return ((0, 0), (0, 0))

    def remove_all(self):
        self._selection.clear()

    def get_left_boundary(self):
        return min(map(lambda pos: pos[0], self._selection.keys()))

    def get_right_boundary(self):
        return max(map(lambda pos: pos[0], self._selection.keys()))

    def get_top_boundary(self):
        return min(map(lambda pos: pos[1], self._selection.keys()))

    def get_bottom_boundary(self):
        return max(map(lambda pos: pos[1], self._selection.keys()))
