from matrix import matrix
from tkinter import Canvas
from copy import deepcopy
from PIL import Image, ImageTk


class grid_canvas(matrix, Canvas):

    def __init__(self, master=None, cnf={}, **kw):
        self.mymaster=master
        self.show_outline=False
        self.outlined=[0,0]
        self.n=0
        self.cover=0

        Canvas.__init__(self, master=master, cnf={}, **kw)

    def myupdate(self,image):
        self.lastid=None
        self.delete(self.lastid)
        self.config(width=image.size[0], height=image.size[1])
        image.convert(mode='1')
        self.tkimage=ImageTk.PhotoImage(image=image)
        self.lastid=self.create_image(
                          0,0,
                          image=self.tkimage,
                          anchor='nw',
                          state='normal'
                          )
        self.orange_ids= matrix(image.size[0], image.size[1])
        self.update()
        
    def create_grid(self, image, cellw, cellh):
        self.cellw=cellw
        self.cellh=cellh
        self.gwidth=(image.size[0]//cellw)+1
        self.gheight=(image.size[1]//cellh)+1
        self['scrollregion']=(0,0,image.size[0],image.size[1])
        super().__init__(
            image.size[0],
            image.size[1],
            )
        self.new_oranges=matrix(image.size[0],image.size[1])
        for j in range(self.gwidth):
            for i in range(self.gheight):
                if j<self.new_oranges.width and i<self.new_oranges.height:
                    self.new_oranges.write(j,i, self.orange_ids.retrieve(j,i))
                    if self.orange_ids.retrieve(j,i)!=0:self.write(j,i,1)
        self.orange_ids=self.new_oranges
                    
        self.update_image(image)

    def update_image(self, img):
        """update image with same size"""
        self.image=deepcopy(img)
        self.myupdate(self.image)
        self.stain_select()
        self.update()
        
    def unselect_all(self):
        self.delete('all')
        for i in range(self.gwidth):
            for j in range(self.gheight):
                #print(i)
                self.write_select(i,j, 0)
        self.myupdate(self.image)
        
            
    def select_all(self):
        self.delete('all')
        for i in range(self.gwidth):
            for j in range(self.gheight):
                self.write(i,j,1)
        self.myupdate(self.image)
        self.cover=self.create_rectangle(0,0, self.image.size[0], self.image.size[1], fill='orange', outline='', stipple='gray50')
        

    def write_select(self, x,y, value):
        if value==1:
            self.delete( self.orange_ids.retrieve(x,y) )
            self.orange_ids.write(x,y,
                                  self.create_rectangle(x*self.cellw, y*self.cellh,
                                                     x*self.cellw+self.cellw, y*self.cellh+self.cellh,
                                                     fill='orange',
                                                     outline='',
                                                     stipple='gray50')
                                  )
            
        elif value==0:
            self.delete( self.orange_ids.retrieve(x,y) )
            self.orange_ids.write(x,y,0)
        self.write(x,y, value)
        
    def stain_select(self):
        if self.cover!=0: 
            self.cover=self.create_rectangle(0,0, self.image.size[0], self.image.size[1], fill='orange', outline='', stipple='gray50')
            return
        for x in range(self.gwidth):
            for y in range(self.gheight):
                
                    value=self.retrieve(x,y)
                    
                    if value==1:
                        self.delete( self.orange_ids.retrieve(x,y) )
                        self.orange_ids.write(x,y,
                                              self.create_rectangle(x*self.cellw, y*self.cellh,
                                              x*self.cellw+self.cellw, y*self.cellh+self.cellh,
                                              fill='orange',
                                              outline='',
                                              stipple='gray50') )
        
                    elif value==0:
                        self.delete( self.orange_ids.retrieve(x,y) )
                        self.orange_ids.write(x,y,0)

    def resize_grid(self, cellw, cellh):
        self.cellw=cellw
        self.cellh=cellh

        for j in range(self.gwidth):
            for i in range(self.gheight):
                self.delete( self.orange_ids.retrieve(j,i) )
                self.orange_ids.write(j,i,0)
                
        self.gwidth=(self.image.size[0]//cellw)+1
        self.gheight=(self.image.size[1]//cellh)+1

        self.stain_select()
        self.update()

    def update(self):
        for i in range(self.n):
                self.delete(self.outlined[i])
        if self.show_outline:
            self.n=0
            self.outs=[]
            for x in range(self.gwidth):
                for y in range(self.gheight):
                    self.outs.append(self.create_rectangle(x*self.cellw, y*self.cellh,
                                              x*self.cellw+self.cellw, y*self.cellh+self.cellh,
                                              fill='',
                                              outline='black',
                                              ))
                    self.n+=1
            self.outlined=self.outs
            
            

        Canvas.update(self)
