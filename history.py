class History:
    def __init__(self, size):
        self._items = []
        self._current_pos = -1
        self._maxsize = size
        self.first_ever_item = None

    def push(self, item):
        if self.first_ever_item is None:
            self.first_ever_item = item

        if self._current_pos < self._maxsize - 1:
            del self._items[self._current_pos + 1 :]
            self._current_pos += 1

        else:
            self._items.pop(0)
        self._items.append(item)

    def undo(self):
        if self._current_pos > -1:
            self._current_pos -= 1

    def redo(self):
        if self._current_pos < len(self._items) - 1:
            self._current_pos += 1

    def current(self):
        if self._current_pos == -1:
            return self._items[0]
        else:
            return self._items[self._current_pos]

