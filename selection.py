from collections import OrderedDict


class Selection:
    def __init__(self):
        # box of cells that limit the selection
        self.top = 0
        self.bottom = 0
        self.left = 0
        self.right = 0

        self.orange_ids = OrderedDict()
        self.cellw = 0
        self.cellh = 0

    def put_cell(self, x, y, id):
        self.orange_ids[(x, y)] = id
        if x < self.left:
            self.left = x
        if x > self.right:
            self.right = x
        if y > self.bottom:
            self.bottom = y
        if y < self.top:
            self.top = y

    def remove_cell(self, x, y):
        if (x, y) in self.orange_ids.keys():
            self.orange_ids.pop((x, y))

            # update selection box, inneficient if we wanna delete a lot of cells in bulk.
            # note: create specialized methods for that if final usage requires
            if len(self.orange_ids) > 0:
                xpositions = list(map(lambda k: k[0], self.orange_ids.keys()))
                ypositions = list(map(lambda k: k[1], self.orange_ids.keys()))

                minx = min(xpositions)
                maxx = max(xpositions)
                miny = min(ypositions)
                maxy = max(ypositions)

                if maxx < self.right:
                    self.right = maxx
                if minx > self.left:
                    self.left = minx
                if maxy < self.bottom:
                    self.bottom = maxy
                if miny > self.top:
                    self.top = miny

    def position_id(self, x, y):
        if (x, y) in self.orange_ids.keys():
            return self.orange_ids[(x, y)]
        else:
            return None

    def all_ids(self):
        return self.orange_ids.values()

    def all_positions(self):
        return self.orange_ids.keys()

    def length(self):
        return len(self.orange_ids)

    def first_two_selected(self):
        if len(self.orange_ids) >= 2:
            locs = list(self.orange_ids.keys())
            return (locs[0], locs[1])
        else:
            return ((0, 0), (0, 0))

    def modify_cell(self, x, y, value):
        self.orange_ids[(x, y)] = value

    def remove_all(self):
        self.orange_ids.clear()

    def max_x(self):
        xpositions = list(map(lambda k: k[0], self.orange_ids.keys()))
        return max(xpositions)

    def max_y(self):
        ypositions = list(map(lambda k: k[1], self.orange_ids.keys()))
        return max(ypositions)
