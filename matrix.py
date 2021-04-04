class Matrix:

    def __init__(self, width, height, fill=0):

        self.width=width
        self.height=height

        self.mat=[[fill for y in range(self.height)] for x in range(self.width)]


    def retrieve(self, x, y):
        return self.mat[x][y]

    def write(self, x, y, thing):
        self.mat[x][y]=thing
        
            
    

