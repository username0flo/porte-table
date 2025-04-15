import math

# vector implementation: (x,y)

GRAVITY = 9.8

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
    return (x / magintude, y / magintude)

def point_in_rect(point, rect):
    x,y = point
    rx,ry,rw,rh = rect
    return x >= rx and x <= rx+rw and y >= ry and y <= ry+rh

def has_intersection(r1,r2):
    x,y,w,h= r1
    return point_in_rect((x,y),r2) or point_in_rect((x+w, y), r2) or point_in_rect((x, y + h),r2) or point_in_rect((x + w, y + h),r2)

