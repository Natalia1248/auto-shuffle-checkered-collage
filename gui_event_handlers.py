from copy import deepcopy
from tkinter import filedialog
import tkinter as tk
from history import History


import PIL

from config import *
from effects import to_red_checkers, to_red, crop, shuffle_alg, shuffle_alg2


history=History(30)

got_started=False
effects_frm=None
height_sldr=None
width_sldr=None
aux=1

def pushes_new_image(func):
    def inn(event=None):

        rectid= c.create_rectangle(0,0,
                                   history.current().size[0],
                                   history.current().size[1],
                                   fill='green', stipple='gray25')
        c.update()
        new_image=func(deepcopy(history.current()))
        c.delete('all')
        history.push(new_image)

        c.update_image(new_image)
        c.remake_orange_rectangles()
        c.update_grid_lines()
        
    return inn

def cleans_up(func):
    def inn(event=None):
        cleanup()
        func(event)
    return inn

def not_first(func):
    def inner(event=None):
        if got_started:
            func(event)
    return inner

def cleanup(event=None):
    global effects_frm
    if effects_frm != None:
        effects_frm.destroy()
        #the previous frame will be garbage collected
        effects_frm=None

@not_first
@cleans_up
@pushes_new_image
def function1(img):
    return to_red_checkers(img, c)

@not_first
@cleans_up
@pushes_new_image
def function2(img):
    return to_red(img, c)

@not_first
@cleans_up
@pushes_new_image
def restart(img):
    return Image.open(imagepath)

@not_first
@cleans_up
@pushes_new_image
def crop_even(img):
    if(img.size[0]%c.cellw)%2==0:
        xtrim=(img.size[0]%c.cellw)/2
        addx=0
    else:
        xtrim=(img.size[0]%c.cellw)//2
        addx=1
    if(img.size[1]%c.cellh)%2==0:
        ytrim=(img.size[1]%c.cellh)/2
        addy=0
    else:
        ytrim=(img.size[1]%c.cellw)//2
        addy=1
    cropped= img.crop((xtrim,ytrim,
                          img.size[0]-xtrim-addx,
                          img.size[1]-ytrim-addy)
        )
    return cropped

@not_first
@pushes_new_image
def original(img):
    orig=Image.open(imagepath)
                
    for x,y in c.selection.all_positions():
        box=(x*c.cellw,y*c.cellh,x*c.cellw+c.cellw,y*c.cellh+c.cellh)
        img.paste(orig.crop(box), box)

    return img

@not_first
@cleans_up
def shuffle(event=None):
    global effects_frm 
    @pushes_new_image
    def com(buff):
        try:
            var=int(entry.get())
        except:
            var=0
        return shuffle_alg(buff, c, var)
    if effects_frm==None:
        effects_frm=tk.Frame(master=window)
        effects_frm['bg']='purple'
        effects_frm.grid(row=3, column=3, sticky='w', pady=10)
        button=tk.Button(master=effects_frm,
                         command=com,
                         text='Go!')
        entry=tk.Entry(master=effects_frm)
        entry.pack()
    
        button.pack(anchor='center')

@not_first
@cleans_up
def shuffle2(event=None):
    global effects_frm, did 
    @pushes_new_image
    def com(buff):
        try:
            var=int(entry.get())

        except:
            var=0
        return shuffle_alg2(buff, c, var)
    if effects_frm==None:
        effects_frm=tk.Frame(master=window)
        effects_frm['bg']='purple'
        effects_frm.grid(row=3, column=3, sticky='w', pady=10)
        button=tk.Button(master=effects_frm,
                         command=com,
                         text='Go!')
        entry=tk.Entry(master=effects_frm)
        entry.pack()
    
        button.pack(anchor='center')
        did=True

@not_first
@cleans_up
@pushes_new_image
def swapb(buff):
    
    cell1, cell2 = c.selection.first_two_selected()

    third=buff.crop((cell1[0]*c.cellw,cell1[1]*c.cellh,
                     cell1[0]*c.cellw+c.cellw,cell1[1]*c.cellh+c.cellh))
    buff.paste(buff.crop((cell2[0]*c.cellw,cell2[1]*c.cellh,
                          cell2[0]*c.cellw+c.cellw,cell2[1]*c.cellh+c.cellh)),
               (cell1[0]*c.cellw,cell1[1]*c.cellh
                ,cell1[0]*c.cellw+c.cellw,cell1[1]*c.cellh+c.cellh)) 
    buff.paste(third,
               (cell2[0]*c.cellw,cell2[1]*c.cellh,
                cell2[0]*c.cellw+c.cellw,cell2[1]*c.cellh+c.cellh))
    return buff

@not_first
def canvas_click(event):
    x=int(c.canvasx(event.x)//c.cellw)
    y=int(c.canvasy(event.y)//c.cellh)
    if x>c.image.size[0] or y>c.image.size[1] or x<0 or y<0:
        return
    c.select_clicked(x,y)

@not_first
def canvas_drag(event):
    x=int(c.canvasx(event.x)//c.cellw)
    y=int(c.canvasy(event.y)//c.cellh)
    if x>c.image.size[0] or y>c.image.size[1] or x<0 or y<0:
        return
    c.select_dragged(x,y)

@not_first
def undo(event=None):
    history.undo()
    c.update_image(history.current())
    c.remake_orange_rectangles()
    c.update_grid_lines()

@not_first
def redo(event=None):
    history.redo()
    c.update_image(history.current())
    c.remake_orange_rectangles()
    c.update_grid_lines()

def width_slide(event):
    global aux
    
    if square_checked and (aux==1 or aux==2):
        hval.set(wval.get())
        hstr.set(str(wval.get()))
        c.cell_size(wval.get(), hval.get())
        if aux==2: aux=3
    else: aux
        
    c.cell_size(wval.get(), c.cellh)
    wstr.set(str(event))
    c.remake_orange_rectangles()
    c.update_grid_lines()

def height_slide(event):
    global aux
    
    if square_checked and (aux==1 or aux==3):
        wval.set(hval.get())
        wstr.set(str(hval.get()))
        c.cell_size(wval.get(), hval.get())
        if aux==3: aux=2
    else: aux=1
        
    c.cell_size(c.cellw, hval.get())
    hstr.set(str(event))
    c.remake_orange_rectangles()
    c.update_grid_lines()

@not_first
def entpress(event):
    if not (int(wstr.get())==1 or int(hstr.get())==1):
        
        if int(wstr.get())!=wval.get():
            wval.set(int(wstr.get()))
            if square_checked:
                hval.set(int(wstr.get()))
                hstr.set(wstr.get())
        elif int(hstr.get())!=hval.get():
            hval.set(int(hstr.get()))
            if square_checked:
                wval.set(int(hstr.get()))
                wstr.set(hstr.get())
        c.cell_size(wval.get(), hval.get())
        c.update_grid_lines()
        c.remake_orange_rectangles()
    
square_checked=False
def check(event=None):
    global square_checked
    if c.image_tkinter_id!=None:
        square_checked=not square_checked
        if square_checked:
            lesser=min(hval.get(), wval.get())
            hval.set(lesser)
            wval.set(lesser)
            wstr.set(lesser)
            hstr.set(lesser)
        c.cell_size(hval.get(),wval.get())
        c.update_grid_lines()

show_lines=False
def lines_checkbox():
    global show_lines
    c.show_outline= not show_lines
    show_lines=not show_lines
    c.update_grid_lines()

@not_first
def saves(event=None):
    extensions=[('Png','*.png'),
                ('Jpg','*.jpg'),
                ('Gif','*.gif'),
                ('type your own and see if it happens to be supported','*')]
    try:
        fileobj=filedialog.asksaveasfile(defaultextension=extensions,filetypes=extensions)
        if fileobj.name!=None: history.current().save(fileobj.name)
    except Exception as e:
        print(e)
    
def openim(event=None):
    global imagepath, height_sldr, width_sldr, aux, got_started
    aux=1
    
    try:
        fileobj=filedialog.askopenfile()
        imagepath=fileobj.name
        im=Image.open(fileobj.name)
    except: 
        return

    c.update_image(im)

    hlen=2*im.size[1]//3
    if hlen>650:   hlen=650
    
    if height_sldr != None: height_sldr.destroy()
    if width_sldr != None: width_sldr.destroy()
    
    height_sldr=tk.Scale(master=s_frm,from_=2,to=im.size[1],length=hlen,command=height_slide,label='CELL HEIGHT',width=10,variable=hval)
    height_sldr.grid(row=0,column=1)
    height_sldr.set(50)

    wlen=2*im.size[0]//3
    if wlen>650: wlen=650
    width_sldr=tk.Scale(master=s_frm,from_=2,to=im.size[0],length=wlen,command=width_slide,label='CELL WIDTH',width=10,variable=wval)
    width_sldr.grid(row=0,column=0)
    width_sldr.set(50)
        
    history.push(im)

    got_started=True





        
    


                
