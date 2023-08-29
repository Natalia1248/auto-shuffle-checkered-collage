class History:
    def __init__(self, size):
        self.items = []
        # the first position of the array is the 0 position
        self.current_pos = -1
        self.maxsize = size

    def push(self, item):
        if self.current_pos < self.maxsize - 1:
            del self.items[self.current_pos + 1 :]
            self.items.append(item)
            self.current_pos += 1

        else:
            self.items.pop(0)
            self.items.append(item)

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


if __name__ == "__main__":
    hist = History(4)

    hist.push(1)
    hist.push(2)
    hist.push(3)
    hist.push(4)
    hist.push(5)

    print(hist.current())

    hist.undo()
    hist.undo()
    hist.push(6)

    print(hist.current())
    hist.undo()
    hist.undo()
    hist.undo()
    hist.undo()
    hist.undo()
    hist.undo()
    hist.undo()

    print(hist.current())

    hist.push(20)

    print(hist.current())

    hist.redo()
    hist.redo()
    hist.redo()

    print(hist.current())

    hist.push(7)
    hist.push(8)
    hist.push(9)
    print(hist.current())
