class History:
    def __init__(self, size):
        self.items=[None for i in range(size)]
        self.last_valid=size
        self.current_pos=size
        self.size=size
        
    
    def push(self, item):
        self.items.insert(self.current_pos, item)
        if self.current_pos<self.size:
            self.current_pos+=1
            self.items.pop()
        else:
            self.items.pop(0)
        
        self.last_valid=self.current_pos

    def undo(self):
        if self.current_pos>1:
            self.current_pos-=1
    
    def redo(self):
        if self.current_pos<self.last_valid:
            self.current_pos+=1

    def current(self):
        return self.items[self.current_pos-1]



if __name__=="__main__":
    hist=History(3)
    hist.get_current()
    hist.push(1)
    hist.push(2)
    hist.push(3)
    hist.push(4)
    hist.push(5)
    hist.undo()
    hist.undo()
    hist.push(6)

    print(hist.get_current())
    hist.undo()
    hist.undo()
    hist.undo()

    hist.redo()
    hist.redo()
    hist.redo()

    hist.push(7)
    hist.push(8)
    hist.push(9)
    print(hist.get_current())

