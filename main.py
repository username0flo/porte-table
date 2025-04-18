from graphics import *
from physics import *


#input 

def get_input():
    arrows = get_fleches()
    mouse = last_clic()
    return (arrows, mouse)


def move_player(player, gravity):
    rect,vect = player
    rect = move_rect(rect,(0.0, gravity))
    rect = move_rect(rect,vect)
    return (rect,vect)

def setup_portal():
    pass

def draw_game(map, portals, player, img_player):
    remplir_fenetre(couleur(40, 93, 164))
    for coord in map:
        affiche_image(map[coord], grid2window(coord))
    if img_player != None:
        #charge_image(img_player)
        rect, vector = player
        x, y, w, h = rect
        affiche_image(img_player, (x, y))
    if portals != None:
        for p in portals:
            portal_coord, color, vertical = p
            x, y = portal_coord
            affiche_rectangle_plein(portal_coord, (x + int(not(vertical)) * 17 + 3, y + vertical * 17 + 3), color)
    affiche_tout()

def grid2window(coord):
    i, j = coord
    return (i * CELL_SIZE, j * CELL_SIZE)

def index2coord(): # for the images
    pass

def load_tile(img_name):
    charge_image(img_name)
    modifie_taille_image(img_name,CELL_SIZE, CELL_SIZE)

#init

portals = [] # for one blue portal inside : ((120, 80), "bleu", 1) 1 or 0 for if it's vertical or horizontal
# with h = 3 and w = 20 for horizontal and h = 20 and w = 3 for vertical

WINDOW_W, WINDOW_H = 800, 600
init_fenetre(WINDOW_W, WINDOW_H,"porte table")

NB_CELL_W = WINDOW_W // 20
NB_CELL_H = WINDOW_H // 20

CELL_SIZE = WINDOW_W // NB_CELL_W # or : WINDOW_H // NB_CELL_H

player = (rect(0,100,10,10), vector(0.0,0.0))
img_player = "images/player.png"
charge_image(img_player)

affiche_auto_off()
# map: a dict of key = coordinates (i,j) and value = a bloc type
HERBE = "images/herbe.png"
load_tile(HERBE)
map = {}
for i in range(NB_CELL_W):
    map[(i,0)] = HERBE

#main

while(pas_echap()):
    event = get_input()
    setup_portal()
    #player = move_player(player, GRAVITY)
    draw_game(map, None, player, img_player)
