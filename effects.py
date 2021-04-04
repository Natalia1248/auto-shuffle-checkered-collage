from PIL import Image
from matrix import Matrix
from random import randint

def to_red(image, c):
    cellw= c.cellw
    cellh= c.cellh

    for i, j in c.selection.all_positions():
            x=i*cellw
            y=j*cellh
            box=(x, y, x+cellw, y+cellh)
            image.paste(make_red(image.crop(box)), box)
    return image

def to_red_checkers(image, c):
    cellw= c.cellw
    cellh= c.cellh
    for i in range(c.selection.left, c.selection.right+1):
        for j in range(c.selection.top, c.selection.bottom+1):
            
            if c.selection.orange_id(i, j) != None :
                x=i*cellw
                y=j*cellh
                box=(x, y, x+cellw, y+cellh)
                #one is even and the other is not
                if (i%2==0 and j%2!=0) or (i%2!=0 and j%2==0):
                    image.paste( make_red( image.crop(box) ), box )
    return image

def crop(image):
    return image.crop((0,0, 600, 400))

def make_red(image):
    imageR=image.getchannel(0)
    imageN=imageR.point(lambda i: False)
    return Image.merge(image.mode,[imageR,imageN,imageN] )


def shuffle_alg(image, c, var):
    cellw=c.cellw
    cellh=c.cellh
    selected_cells={}
    
    for i in range(c.selection.left, c.selection.right+1):
        for j in range(c.selection.top, c.selection.bottom+1):
            if c.selection.orange_id(i,j) != None:
                selected_cells[(i,j)]=image.crop((j*cellw,
                                i*cellh,
                                j*cellw+cellw, i*cellh+cellh
                                ))
    
    for pos in selected_cells.keys():
        x=pos[0]
        y=pos[1]
        n1=randint(-var, var)
        n2=randint(-var, var)
        image.paste(selected_cells[pos],
            ((x+n1)*cellw,
            (y+n2)*cellh)
            )
    return image

def shuffle_alg2(image, canvgrid, var):
    cwidth=canvgrid.cellw
    cheight=canvgrid.cellh

    for i in range(canvgrid.selection.left, canvgrid.selection.right+1):
        for j in range(canvgrid.selection.top, canvgrid.selection.bottom+1):
            if canvgrid.selection.orange_id(i,j) != None:
                c=0
                while True:
                    xguy=randint(abs(j-var),j+var)
                    yguy=randint(abs(i-var), i+var)
                    if (canvgrid.selection.orange_id(xguy, yguy) != None and
                    (xguy+1)*cwidth<=image.size[0] and
                    (yguy+1)*cheight<=image.size[1]):
                        break
                    c+=1
                    if c>3:
                        xguy, yguy= j,i
                        break
                ibox=(j*cwidth,i*cheight, (j+1)*cwidth,(i+1)*cheight,)
                guybox=(xguy*cwidth,yguy*cheight, (xguy+1)*cwidth,(yguy+1)*cheight,)
                image=swap(image,ibox, guybox)
                
    return image

def swap(image, box1, box2):
    buff=image.crop(box1)
    image.paste(image.crop(box2),box1)
    image.paste(buff, box2)
    return image
        

    
    

        
