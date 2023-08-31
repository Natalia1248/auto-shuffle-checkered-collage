from collections import OrderedDict


class Selection:
    def __init__(self):
        self.__selection = OrderedDict()

    def put_cell(self, x, y, id):
        self.__selection[(x, y)] = id

    def remove_cell(self, x, y):
        if (x, y) in self.__selection:
            self.__selection.pop((x, y))

    def position_id(self, x, y):
        if (x, y) in self.__selection:
            return self.__selection[(x, y)]
        else:
            return None

    def all_ids(self):
        return self.__selection.values()

    def all_positions(self):
        return self.__selection.keys()

    def first_two_selected(self):
        if len(self.__selection) >= 2:
            locs = list(self.__selection.keys())
            return (locs[0], locs[1])
        else:
            return ((0, 0), (0, 0))

    def remove_all(self):
        self.__selection.clear()

    def get_left_boundary(self):
        return min(map(lambda pos: pos[0], self.__selection.keys()))

    def get_right_boundary(self):
        return max(map(lambda pos: pos[0], self.__selection.keys()))

    def get_top_boundary(self):
        return min(map(lambda pos: pos[1], self.__selection.keys()))

    def get_bottom_boundary(self):
        return max(map(lambda pos: pos[1], self.__selection.keys()))
