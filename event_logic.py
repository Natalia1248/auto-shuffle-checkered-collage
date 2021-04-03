from copy import deepcopy
from tkinter import filedialog
import tkinter as tk
from functools import wraps

import PIL

from config import *
from pilalgs import test2, to_red , crop, shuffle_alg, shuffle_2


def nofirst(f):
    @wraps(f)
    def inn(event=None):
        if not first: f(event)
    return inn

#NOT FOR RESIZES
def imtrans(funct):
    def inn(event=None):
        global current
        if first: return

        rectid= c.create_rectangle(0,0,
                                   history[current].size[0],
                                   history[current].size[1],
                                   fill='green', stipple='gray25')
        c.update()
        buff= deepcopy(history[current])

        c.delete('all')

        if current<history_size-1:
            history[current+1]=funct(buff)
            for i in range(current+2, history_size, 1):
                history[i]=None
            current+=1
        else:
            history.popleft()
            history.append(funct(buff))
        
        c.update_image(history[current])
        
    
        print(len(c.find_all()))
        
    return inn

def cleans(funct):
    @wraps(funct)
    def inn(event=None):
        cleanup()
        funct()
    return inn

@nofirst
@cleans
@imtrans
def function1(buffed):
    return test2(buffed, c)

@nofirst
@cleans
@imtrans
def function2(buffed):
    return to_red(buffed, c)

@nofirst
@cleans
@imtrans
def restart(buffed):
    return Image.open(imagepath)

@nofirst
@cleans
@imtrans
def cropimage(buffed):
    xtrim=buffed.size[0]%c.cellw
    ytrim=buffed.size[1]%c.cellh
    cropped= buffed.crop((0,0,
                          buffed.size[0]-xtrim,
                          buffed.size[1]-ytrim)
        )
    return cropped

@nofirst
@cleans
@imtrans
def crop_even(buffed):
    if(buffed.size[0]%c.cellw)%2==0:
        xtrim=(buffed.size[0]%c.cellw)/2
        addx=0
    else:
        xtrim=(buffed.size[0]%c.cellw)//2
        addx=1
    if(buffed.size[1]%c.cellh)%2==0:
        ytrim=(buffed.size[1]%c.cellh)/2
        addy=0
    else:
        ytrim=(buffed.size[1]%c.cellw)//2
        addy=1
    cropped= buffed.crop((xtrim,ytrim,
                          buffed.size[0]-xtrim-addx,
                          buffed.size[1]-ytrim-addy)
        )
    c['scrollregion']=(0,0, cropped.size[0], cropped.size[1])
    return cropped

@nofirst
def undo(event=None):
    global current, history, c
    if current>0:
        current-=1
    c.create_grid(history[current], c.cellw, c.cellh)

@nofirst   
def redo(event=None):
    global current, history, c
    if current<history_size and history[current+1]!=None:
        current+=1
    c.create_grid(history[current], c.cellw, c.cellh)

@nofirst 
@imtrans
def original(buffed):
    orig=Image.open(imagepath)
    for i in range(c.gheight):
        for j in range(c.gwidth):
            if c.retrieve(j,i)==1:
                box=(j*c.cellw,i*c.cellh,j*c.cellw+c.cellw,i*c.cellh+c.cellh)
                buffed.paste(orig.crop(box), box)
    return buffed



writing=0
@nofirst
def canvas_click(event):
    global writing
    c.delete(c.cover)
    c.cover=0
    c.stain_select()
    x=int(c.canvasx(event.x)//c.cellw)
    y=int(c.canvasy(event.y)//c.cellh)

    
    if x>c.width or y>c.height or x<0 or y<0: return
    if c.retrieve(x,y)==0:
        c.write_select(x,y,1)
        writing=1
        
    else:
        c.write_select(x,y,0)
        writing=0
    
@nofirst  
def canvas_drag(event):
    global writing
    c.delete(c.cover)
    c.cover=0
    c.stain_select()
    x=int(c.canvasx(event.x)//c.cellw)
    y=int(c.canvasy(event.y)//c.cellh)
    if x>c.image.size[0] or y>c.image.size[1] or x<0 or y<0: return
    
    c.write_select(x,y,writing)

@nofirst
def clear(event):
    
    rectid= c.create_rectangle(0,0,
                                   history[current].size[0],
                                   history[current].size[1],
                                   fill='green', stipple='gray25'
                               )
    c.unselect_all()
    c.cover=0
    c.delete(rectid)
    

@nofirst
def selal(event):
    
    rectid= c.create_rectangle(0,0,
                                   history[current].size[0],
                                   history[current].size[1],
                                   fill='green', stipple='gray25'
                               )
    
    c.select_all()

    c.delete(rectid)
    print(len(c.find_all()))

aux=1
@nofirst
def width_slide(event):
    global intermediate, aux
    if c.cover!=0: 
                selal()
    if checked and (aux==1 or aux==2):
        hval.set(wval.get())
        hstr.set(str(wval.get()))
        c.resize_grid(wval.get(), hval.get())
        if aux==2: aux=3
    else: aux
        
    c.resize_grid(wval.get(), c.cellh)
    wstr.set(str(event))

@nofirst
def height_slide(event):
    global intermediate, aux
    if c.cover!=0: 
                selal()
    if checked and (aux==1 or aux==3):
        wval.set(hval.get())
        wstr.set(str(hval.get()))
        c.resize_grid(wval.get(), hval.get())
        if aux==3: aux=2
    else: aux=1
        
    c.resize_grid(c.cellw, hval.get())
    hstr.set(str(event))

@nofirst
def entpress(event):
    if not (int(wstr.get())==1 or int(hstr.get())==1):
        
        if int(wstr.get())!=wval.get():
            print('cover: ', c.cover)
            wval.set(int(wstr.get()))
            if checked:
                hval.set(int(wstr.get()))
                hstr.set(wstr.get())
        elif int(hstr.get())!=hval.get():
            hval.set(int(hstr.get()))
            if checked:
                wval.set(int(hstr.get()))
                wstr.set(hstr.get())
        c.resize_grid(wval.get(), hval.get())
        if c.cover!=0: 
                selal()
    
checked=False
@nofirst
def check(event=None):
    global checked, aux
    checked=not checked
    if checked:
        lesser=min(hval.get(), wval.get())
        hval.set(lesser)
        wval.set(lesser)
        wstr.set(lesser)
        hstr.set(lesser)
        #aux=2
    c.resize_grid(hval.get(),wval.get())

@nofirst
def saves(event=None):
    extensions=[('Png','*.png'),
                ('Jpg','*.jpg'),
                ('Gif','*.gif'),
                ('type your own and see if it happens to be supported','*')]
    try:
        fileobj=filedialog.asksaveasfile(defaultextension=extensions,filetypes=extensions)
        if fileobj.name!=None: history[current].save(fileobj.name)
    except: pass


@nofirst
def cleanup(event=None):
    global effects_frm, did
    if effects_frm != None: effects_frm.destroy()
    did=False
    
height_sldr=0
width_sldr=0
def openim(event=None):
    global imagepath, current, first, height_sldr, width_sldr, aux
    aux=1
    
    try:
        fileobj=filedialog.askopenfile()
        imagepath=fileobj.name
        im=Image.open(fileobj.name)
    except: return
    
    c['scrollregion']=(0,0, im.size[0], im.size[1])
    c.myupdate(im)
    hlen=2*im.size[1]//3
    if hlen>650:   hlen=650
    
    if height_sldr != 0: height_sldr.destroy()
    if width_sldr != 0: width_sldr.destroy()
    
    height_sldr=tk.Scale(master=s_frm,from_=2,to=im.size[1],length=hlen,command=height_slide,label='CELL HEIGHT',width=10,variable=hval)
    height_sldr.grid(row=0,column=1)
    height_sldr.set(50)

    wlen=2*im.size[0]//3
    if wlen>650: wlen=650
    width_sldr=tk.Scale(master=s_frm,from_=2,to=im.size[0],length=wlen,command=width_slide,label='CELL WIDTH',width=10,variable=wval)
    width_sldr.grid(row=0,column=0)
    width_sldr.set(50)
    if first:
        c.create_grid(im, 50, 50)
        first=False
    else: c.create_grid(im, c.cellw, c.cellh)
    if current==0:
        history[current]=im
    elif current<history_size-1 and current!=0:
        history[current+1]=im
        for i in range(current+2, history_size, 1):
            history[i]=None
        current+=1
    else:
        history.popleft()
        history.append(im)


effects_frm=None
did=False

@nofirst
@cleans
def shuffle(event=None):
    global effects_frm, did 
    @imtrans
    def com(buff):
        try:
            var=int(entry.get())
        except:
            var=0
        return shuffle_alg(buff, c, var)
    if not did:
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

@nofirst
@cleans
def shuffle2(event=None):
    global effects_frm, did 
    @imtrans
    def com(buff):
        try:
            var=int(entry.get())

        except:
            var=0
        return shuffle_2(buff, c, var)
    if not did:
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

show_lines=False
@nofirst
def lines(event):
    global show_lines
    
    if not show_lines:
        c.show_outline=True
    else:
        c.show_outline=False
    c.update()
    show_lines=not show_lines

@cleans
@imtrans
def swapb(buff):
    cell1=0
    cell2=0
    for i in range(c.gwidth):
        for j in range(c.gheight):
            if cell1==0 and c.retrieve(i,j)==1:
                cell1=(i,j)
            elif cell2==0 and c.retrieve(i,j)==1:
                cell2=(i,j)
                break
    if cell1==0 or cell2==0: cell1=cell2=(0,0)
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
        
    


                
