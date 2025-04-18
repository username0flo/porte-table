from graphics import *
from physics import *


#input 

def get_input():
    arrows = get_fleches()
    mouse = last_clic()
    return (arrows, mouse)


def move_player():
    pass


def setup_portal():
    pass

def draw_game(map, portals, player, img_player):
    for coord in map:
        affiche_image(map[coord], grid2window(coord))
    if img_player != None:
        load_tile(img_player)
        rect, vector = player
        x, y, w, h = rect
        affiche_image(img_player, (x, y))
    if portals != None:
        for p in portals:
            portal_coord, color, vertical = p
            x, y = portal_coord
            affiche_rectangle_plein(portal_coord, (x + int(not(vertical)) * 17 + 3, y + vertical * 17 + 3), color)

def grid2window(i,j):
    return (i * CELL_SIZE, j * CELL_SIZE)

def index2coord(): # for the images
    pass

def load_tile(img_name):
    charge_image(img_name)
    modifie_taille_image(img_name,CELL_SIZE, CELL_SIZE)

#init
player = (rect(0,0,10,10), vector(0.0,0.0))
img_player = "image/player.png"
portals = [] # for one blue portal inside : ((120, 80), "bleu", 1) 1 or 0 for if it's vertical or horizontal
# with h = 3 and w = 20 for horizontal and h = 20 and w = 3 for vertical

WINDOW_W, WINDOW_H = 800, 600
init_fenetre(WINDOW_W, WINDOW_H,"porte table")

NB_CELL_W = WINDOW_W // 20
NB_CELL_H = WINDOW_H // 20

CELL_SIZE = WINDOW_W // NB_CELL_W # or : WINDOW_H // NB_CELL_H


affiche_auto_off()
# map: a dict of key = coordinates (i,j) and value = a bloc type
map = {}

#main

while(pas_echap()):
    event = get_input()
    setup_portal()
    move_player()
    draw_game()
