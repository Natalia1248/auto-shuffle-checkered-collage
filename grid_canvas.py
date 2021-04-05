from selection import Selection
from tkinter import Canvas
from copy import deepcopy
from PIL import Image, ImageTk


class GridCanvas(Canvas):

    def __init__(self, master=None, cnf={}, **kw):
        self.show_outline=False
        self.line_ids=[]
        
        #variable to communicate info between select_clicked and select_dragged, to avoid glitchy dragging
        self.writing=0

        #cell width, cell height
        self.cellw=50
        self.cellh=50
        self.image_tkinter_id=None
        self.selection=Selection()

        Canvas.__init__(self, master=master, cnf={}, **kw)
        

    def update_image(self, image):
        #takes an image, and replaces the previous image on display with it

        #contemplate shrinking
        

        #grid width, grid height
        if image.size[0]%self.cellw!=0:
            self.gwidth=(image.size[0]//self.cellw)+1
        else:
            self.gwidth=(image.size[0]//self.cellw)
        if image.size[0]%self.cellw!=0:
            self.gheight=(image.size[1]//self.cellh)+1
        else:
            self.gheight=(image.size[1]//self.cellh)

        self['scrollregion']=(0,0,image.size[0],image.size[1])
        self.image=deepcopy(image)
        self.delete(self.image_tkinter_id)
        self.config(width=image.size[0], height=image.size[1])
        image.convert(mode='1')
        self.tkimage=ImageTk.PhotoImage(image=image)
        self.delete('all')
        self.image_tkinter_id=self.create_image(
                          0,0,
                          image=self.tkimage,
                          anchor='nw',
                          state='normal'
                          )
        self.update()
        
    def unselect_all(self):
        for id in self.selection.all_ids():
            self.delete(id)
        self.selection.remove_all()

    def select_all(self):
        for i in range(self.gwidth):
            for j in range(self.gheight):
                if self.selection.orange_id(i,j)==None:
                    self.selection.put_cell(i, j, self.make_orange_rect(i, j))
    
    def select_clicked(self, x,y):
        cellid=self.selection.orange_id(x,y)
        
        if cellid == None:
            self.writing=1
            self.selection.put_cell(x,y,self.make_orange_rect(x,y))
            
        else:
            self.writing=0
            self.delete( self.selection.orange_id(x,y) )
            self.selection.remove_cell(x,y)

    def select_dragged(self, x, y):
        cellid=self.selection.orange_id(x,y)

        if self.writing==1 and cellid==None:
            self.selection.put_cell(x,y, self.make_orange_rect(x,y))
                                  
        elif self.writing==0:
            self.delete( self.selection.orange_id(x,y) )
            self.selection.remove_cell(x,y)
    
    def remake_orange_rectangles(self):
        new_selection=Selection()
        for x,y in self.selection.all_positions():
            self.delete(self.selection.orange_id(x,y))
            new_selection.put_cell(x, y, self.make_orange_rect(x,y))
        self.selection=new_selection
                    

    def cell_size(self, cellw, cellh):
        self.cellw=cellw
        self.cellh=cellh

        self.gwidth=(self.image.size[0]//cellw)+1
        self.gheight=(self.image.size[1]//cellh)+1
    

    def update_grid_lines(self):
        for id in self.line_ids:
            self.delete(id)
        self.line_ids=[]

        if(self.show_outline):
            width=self.image.size[0]
            height=self.image.size[1]

            for i in range(0, width, self.cellw):
                self.line_ids.append(
                    self.create_line(i, 0, i, height)
                )
            for j in range(0, height, self.cellh):
                self.line_ids.append(
                    self.create_line(0, j, width, j)
                )
        
    def make_orange_rect(self, x, y):
        return self.create_rectangle(x*self.cellw, y*self.cellh,
                                                x*self.cellw+self.cellw, y*self.cellh+self.cellh,
                                                fill='orange',
                                                outline='',
                                                stipple='gray50')



