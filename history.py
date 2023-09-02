class History:
    def __init__(self, size):
        self.items = []
        self.current_pos = -1
        self.maxsize = size
        self.first = None

    def push(self, item):
        if not self.first:
            self.first = item

        if self.current_pos < self.maxsize - 1:
            del self.items[self.current_pos + 1 :]
            self.current_pos += 1

        else:
            self.items.pop(0)
        self.items.append(item)
    
    def get_first_ever_item(self):
        return self.first

    def undo(self):
        if self.current_pos > -1:
            self.current_pos -= 1

    def redo(self):
        if self.current_pos < len(self.items) - 1:
            self.current_pos += 1

    # not to be called on an empty history
    def current(self):
        if self.current_pos == -1:
            return self.items[0]
        else:
            return self.items[self.current_pos]

