from graphics import *

def grid2window(coord, cell_size):
    i, j = coord
    return (i * cell_size, j * cell_size)

def index2coord(): # for the images
    pass

def load_tile(img_name, cell_size):
    charge_image(img_name)
    modifie_taille_image(img_name,cell_size, cell_size)

def int_rect(rect):
    x,y,w,h = rect
    return (int(x), int(y), w, h)

def sign(x):
    if x == 0:
        return 0
    return x // abs(x)