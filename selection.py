from collections import OrderedDict

class Selection:
    def __init__(self):
        #box of cells that limit the selection
        self.top=0
        self.bottom=0
        self.left=0
        self.right=0

        self.orange_ids=OrderedDict()
        self.cellw=0
        self.cellh=0

    def put_cell(self, x, y, id):
        self.orange_ids[(x,y)]=id
        if x<self.left:
            self.left=x
        if x>self.right:
            self.right=x
        if y>self.bottom:
            self.bottom=y
        if y<self.top:
            self.top=y

    def remove_cell(self, x, y):
        if (x,y) in self.orange_ids.keys():
            self.orange_ids.pop((x,y))
    
    def orange_id(self, x, y):
        if (x,y) in self.orange_ids.keys():
            return self.orange_ids[(x,y)]
        else:
            return None
    def all_ids(self):
        return self.orange_ids.values()

    def all_positions(self):
        return self.orange_ids.keys()
    
    def length(self):
        return len(self.orange_ids)
    
    def first_two_selected(self):
        if len(self.orange_ids)>=2:
            locs=list(self.orange_ids.keys())
            return (locs[0], locs[1])
        else:
            return (0,0)

    def modify_cell(self, x, y, value):
        self.orange_ids[(x,y)]=value
    
    def remove_all(self):
        self.orange_ids.clear()