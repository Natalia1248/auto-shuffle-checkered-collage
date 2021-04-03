from PIL import Image
from matrix import matrix
from random import randint

def to_red(image, matrix):
    cellw= matrix.cellw
    cellh= matrix.cellh

    for i in range(matrix.width):
        for j in range(matrix.height):
            
            if matrix.retrieve(i,j)==1:
                x=i*cellw
                y=j*cellh
                box=(x, y, x+cellw, y+cellh)
                image.paste(make_red(image.crop(box)), box)
    return image

def test2(image, matrix):
    counter=0

    cellw= matrix.cellw
    cellh= matrix.cellh

    for i in range(matrix.width):
        for j in range(matrix.height):
            
            if matrix.retrieve(i,j)==1:
                x=i*cellw
                y=j*cellh
                box=(x, y, x+cellw, y+cellh)
                if counter%2==0:
                    image.paste( make_red( image.crop(box) ), box )
            
            counter+=1
            
        if (matrix.height%2)==0: counter+=1
            
    return image

def crop(image):
    
    return image.crop((0,0, 600, 400))

def grey_select2(image, matrix):
    cellw= matrix.cellw
    cellh= matrix.cellh

    for i in range(matrix.width):
        for j in range(matrix.height):
            
            if matrix.retrieve(i,j)==1:
                x=i*cellw
                y=j*cellh
                box=(x, y, x+cellw, y+cellh)
                image.paste(image.crop(box).convert(mode='L'), box)
    return image

def stain_all(image, matrix):
    cellw= matrix.cellw
    cellh= matrix.cellh

    for i in range(matrix.width):
        for j in range(matrix.height):
            
            if matrix.retrieve(i,j)!=1:
                x=i*cellw
                y=j*cellh
                box=(x, y, x+cellw, y+cellh)
                image.paste(stain_orange(image.crop(box)), box)
    return image
def select_stain(image, matrix):
    cellw= matrix.cellw
    cellh= matrix.cellh

    for i in range(matrix.width):
        for j in range(matrix.height):
            
            if matrix.retrieve(i,j)==1:
                x=i*cellw
                y=j*cellh
                box=(x, y, x+cellw, y+cellh)
                image.paste(stain_orange(image.crop(box)), box)
    return image


def make_red(image):
    imageR=image.getchannel(0)
    imageN=imageR.point(lambda i: False and 0)
    return Image.merge(image.mode,[imageR,imageN,imageN] )

def make_grey(image):
    imageR=image.getchannel(2)
    imageN=imageR.point(lambda i: False and 0)
    return Image.merge(image.mode,[imageR,imageR,imageR] )
def stain_orange(image):
    image=image.convert(mode='L')
    imageR=image.getchannel(0)
    imageG=imageR.point(prop)
    imageB=imageR.point(lambda i: False and 0)
    
    return Image.merge('RGB', [imageR, imageG, imageB])
def prop(pixel):
    return pixel*(128/255)

def shuffle_alg(image, mtrx, var):
    cellw=mtrx.cellw
    cellh=mtrx.cellh
    buff=matrix(image.size[0]//cellw, image.size[1]//cellh)
    
    for j in range(buff.width):
        for i in range(buff.height):
            if mtrx.retrieve(j,i) == 1:
                buff.write(j,i,
                           image.crop((
                               j*cellw, i*cellh,
                               j*cellw+cellw, i*cellh+cellh
                               ))
                           )
    for j in range(buff.width):
        for i in range(buff.height):
            if buff.retrieve(j,i)!=0:
                n1=randint(-var, var)
                n2=randint(-var, var)
                image.paste(buff.retrieve(j,i),
                            ((j+n1)*cellw,
                             (i+n2)*cellh
                             )
                            )
    return image

def shuffle_2(image, mtrx, var):
    cwidth=mtrx.cellw
    cheight=mtrx.cellh

    for j in range(mtrx.gwidth-1):
        for i in range(mtrx.gheight-1):
            if mtrx.retrieve(j,i)==1:
                c=0
                while True:
                    xguy=randint(abs(j-var),j+var)
                    yguy=randint(abs(i-var), i+var)
                    if mtrx.retrieve(xguy,yguy)==1 and (xguy+1)*cwidth<=image.size[0] and (yguy+1)*cheight<=image.size[1]: break
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
        

    
    

        
