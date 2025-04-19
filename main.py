from graphics import *
from utils import *
from physics import *
from time import sleep


#input 
def get_input():
    arrows = get_fleches()
    mouse = last_clic()
    return (arrows, mouse)


def move_player(player, map, event, gravity):
    # don't work because when we move left we are in colision with the floor because of gravity so we backtracking to a stable position that is the initial position
    arrows, click = event
    prect,pvect = player
    pvect = multiplication(arrows, PLAYER_SPEED)
    grav_vect = (0.0, gravity)
    prect = move_rect(prect, grav_vect)
    prect = move_rect(prect,pvect)
    i_rect = (int(prect[0]), int(prect[1]), prect[2], prect[3])

    normalized = normalize(vect_sum(grav_vect, pvect))
    # normalized = normalize(pvect)
    oposite = opposite_vect(normalized)
    
    while colision(map, i_rect, CELL_SIZE):
        prect = move_rect(prect, oposite)
        i_rect = (int(prect[0]), int(prect[1]), prect[2], prect[3])

    return (i_rect,pvect)

def setup_portal():
    pass

def draw_game(map, portals, player, img_player):
    remplir_fenetre(couleur(40, 93, 164))
    for coord in map:
        affiche_image(map[coord], grid2window(coord,CELL_SIZE))
    if img_player != None:
        rect, vector = player
        x, y, w, h = rect
        affiche_image(img_player, (x, y))
    if portals != None:
        for p in portals:
            portal_coord, color, vertical = p
            x, y = portal_coord
            affiche_rectangle_plein(portal_coord, (x + int(not(vertical)) * 17 + 3, y + vertical * 17 + 3), color)
    affiche_tout()

def wait(nom_chrono, fps):
    tmps = lire_chrono("temps")
    delta_t = 1000/fps
    if(tmps < delta_t):
        sleep((delta_t - tmps)/1000)
    init_chrono("temps")



#init

portals = [] # for one blue portal inside : ((120, 80), "bleu", 1) 1 or 0 for if it's vertical or horizontal
# with h = 3 and w = 20 for horizontal and h = 20 and w = 3 for vertical

WINDOW_W, WINDOW_H = 800, 600
init_fenetre(WINDOW_W, WINDOW_H,"porte table")

NB_CELL_W = WINDOW_W // 20
NB_CELL_H = WINDOW_H // 20

CELL_SIZE = WINDOW_W // NB_CELL_W # or : WINDOW_H // NB_CELL_H

PLAYER_SPEED = 10

player = (rect(0,100,10,10), vector(0.0,0.0))
img_player = "images/player.png"
charge_image(img_player)

affiche_auto_off()
# map: a dict of key = coordinates (i,j) and value = a bloc type
HERBE = "images/herbe.png"
load_tile(HERBE, CELL_SIZE)
map = {}
for i in range(NB_CELL_W):
    map[(i,0)] = HERBE


FPS = 60

lance_chrono("temps")

#main

while(pas_echap()):
    event = get_input()
    setup_portal()
    player = move_player(player, map, event, GRAVITY)
    draw_game(map, None, player, img_player)
    wait("temps", FPS)
