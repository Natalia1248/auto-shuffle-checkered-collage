class matrix:

    def __init__(self, width, height, fill=0):

        self.j=[]
        self.i=[]
        self.width=width
        self.height=height
        for self.y in range(self.height):
            self.j=[]
            for self.x in range(self.width):
                self.j.append(fill)
                
            self.i.append(self.j)


                

    def retrieve(self, x, y):

        return self.i[y][x]

    def write(self, x, y, thing):
        
        self.i[y][x]=thing
        #print(self.i[x][y])

    def print(self):
        
        for self.y in range(self.height):
            
            for self.x in range(self.width-1):
                print(self.i[self.y][self.x], end=" ")
            
            print(self.i[self.y][self.width-1])
            
    








if __name__=="__main__":

    pass
