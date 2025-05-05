from graphics import *
from utils import *
from physics import *
from time import sleep


#input 
def get_input():
    arrows = get_fleches()
    mouse = last_clic()
    return (arrows, mouse)


def move_player(player, map, event, gravity, delta_t):
    # don't work because when we move left we are in colision with the floor because of gravity so we backtracking to a stable position that is the initial position
    arrows, click = event
    prect, pvect, jump = player

    ax, ay = arrows
    x,y = pvect
    if ay == 0:
        pvect = (ax * PLAYER_SPEED * delta_t, y)
    elif ay == 1 and not(jump):
        jump = 1
        pvect = (0.0,JUMP * delta_t)
    grav_vect = (0.0, gravity * delta_t)
    pvect = vect_sum(pvect, grav_vect)

    x,y = pvect
    temp = (x,0.0)
    prect = move_rect(prect, temp)
    has_colision = False
    opposite = (-sign(x),0)
    while colision(map, int_rect(prect), CELL_SIZE):
        has_colision = True
        prect = move_rect(prect, opposite)
    if(has_colision):
        pvect = (0.0,y)
    
    temp = (0.0, y)
    prect = move_rect(prect,temp)
    has_colision = False
    opposite = (0,-sign(y))
    while colision(map, int_rect(prect), CELL_SIZE):
        has_colision = True
        prect = move_rect(prect, opposite)
    if(has_colision):
        jump = 0
        pvect = (x,0.0)

    return (int_rect(prect),pvect, jump)

def apply_colision(rect, vect):
    return_code = False
    normalized = normalize(vect)
    oposite = opposite_vect(normalized)
    
    while colision(map, int_rect(rect), CELL_SIZE):
        return_code = True
        rect = move_rect(rect, oposite)
    return (return_code, rect)

def position_in_window(rect):
    x,y,w,h = rect
    if x < 0:
        x = 0
    elif x + w >= WINDOW_W:
        x = WINDOW_W - w

    if y < 0:
        y = 0
    elif y + h >= WINDOW_H:
        y = WINDOW_H - h
    
    return (x,y,w,h)


def setup_portal(event, player, map, portals):
    arrows, mouse = event
    if mouse is None:
        return
    prect, pvect, jump = player
    playerx, playery, w, h = prect

    x, y = mouse
    vectx, vecty = normalize((x - playerx, y - playery))
    rect_window = (0, 0, WINDOW_W, WINDOW_H)
    rect = (playerx, playery, 0, 0)
    while not(colision(map, rect, CELL_SIZE)):
        if not(has_intersection(rect, rect_window)):
            portals[0] = None
            return
        rect = move_rect(rect, (vectx, vecty))

    rx, ry, rw, rh = rect
    ryt = ry - vecty

    portals[0] = ((rx, ry), couleur(0,47,173), colision(map, (rx, ryt, rw, rh), CELL_SIZE))
def draw_game(map, portals, player, img_player):
    remplir_fenetre(couleur(40, 93, 164))
    for coord in map:
        affiche_image(map[coord], grid2window(coord,CELL_SIZE))
    if img_player != None:
        rect, vector, jump = player
        x, y, w, h = rect
        affiche_image(img_player, (x, y))
    for p in portals:
        if not(p is None):
            portal_coord, color, vertical = p
            x, y = portal_coord
            affiche_rectangle_plein(portal_coord, (x + int(not(vertical)) * 17 + 3, y + vertical * 17 + 3), color)
    affiche_tout()

def wait(nom_chrono, fps):
    tmps = lire_chrono(nom_chrono)
    delta_t = 1000/fps
    ret = tmps/1000
    if(tmps < delta_t):
        ret = 1/fps
        sleep((delta_t - tmps)/1000)
    init_chrono(nom_chrono)
    return ret



#init

portals = [None, None] # for one blue portal inside : ((120, 80), "bleu", 1) 1 or 0 for if it's vertical or horizontal
# with h = 3 and w = 20 for horizontal and h = 20 and w = 3 for vertical

WINDOW_W, WINDOW_H = 800, 600
init_fenetre(WINDOW_W, WINDOW_H,"porte table")

NB_CELL_W = WINDOW_W // 20
NB_CELL_H = WINDOW_H // 20

CELL_SIZE = WINDOW_W // NB_CELL_W # or : WINDOW_H // NB_CELL_H

PLAYER_SPEED = 200
JUMP = 400

player_size = 32
player = (rect(0,50,player_size,player_size), vector(0.0,0.0),1)
img_player = "images/player.png"
charge_image(img_player)
modifie_taille_image(img_player,player_size, player_size)


affiche_auto_off()
# map: a dict of key = coordinates (i,j) and value = a bloc type
HERBE = "images/herbe.png"
PIERRE  = "images/pierres.png"
load_tile(HERBE, CELL_SIZE)
load_tile(PIERRE, CELL_SIZE)
map = {}
for i in range(NB_CELL_W):
    map[(i,0)] = HERBE

for j in range(7):
    map[(10,10+j)] = HERBE

FPS = 60
delta_t = 1/FPS

lance_chrono("temps")

#main

while(pas_echap()):
    event = get_input()
    setup_portal(event, player, map, portals)
    player = move_player(player, map, event, GRAVITY, delta_t)
    draw_game(map, portals, player, img_player)
    delta_t = wait("temps", FPS)
