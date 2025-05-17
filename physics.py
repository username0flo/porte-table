import math
from utils import *

# vector implementation: (x,y)

GRAVITY = -9.8

def vector(x,y):
    return (x,y)

def move_rect(rect, vect):
    x,y,w,h = rect
    vx,vy = vect
    return (x + vx, y + vy, w, h)

def rect(x,y,w,h):
    return (x,y,w,h)

def get_magnitude(vect):
    x,y = vect
    return math.sqrt(x**2 + y**2)

def normalize(vect):
    x,y = vect
    magintude = get_magnitude(vect)
    if magintude == 0:
        return (0.0, 0.0)
    return (x / magintude, y / magintude)

def point_in_rect(point, rect):
    x,y = point
    rx,ry,rw,rh = rect
    return x >= rx and x <= rx+rw and y >= ry and y <= ry+rh

def has_intersection(r1,r2):
    x,y,w,h= r1
    return point_in_rect((x,y),r2) or point_in_rect((x+w, y), r2) or point_in_rect((x, y + h),r2) or point_in_rect((x + w, y + h),r2)

def colision(map, rect, cell_size):
    for coord in map:
        x,y = grid2window(coord, cell_size)
        block = (x,y,cell_size,cell_size)
        if has_intersection(rect, block) or has_intersection(block,rect):
            return (x,y)
    return False

def vect_sum(v1, v2):
    x1,y1 = v1
    x2, y2 = v2
    return (x1 + x2, y1 + y2)

def opposite_vect(vect):
    x,y = vect
    return (-x, -y)

def multiplication(vect, number):
    x,y = vect
    return (x * number, y* number)