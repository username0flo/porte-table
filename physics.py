# vector implementation: (x,y)

GRAVITY = 9.8

def vector(x,y):
    return (x,y)

def move_rect(rect, vect):
    x,y,w,h = rect
    vx,vy = vect
    return (x + int(vx), y + int(vy), w, h)

def rect(x,y,w,h):
    return (x,y,w,h)


