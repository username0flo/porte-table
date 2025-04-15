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

def draw_game():
    pass

def grid2window(i,j):
    return (i * CELL_SIZE, j * CELL_SIZE)

def load_tile(img_name):
    charge_image(img_name)
    modifie_taille_image(img_name,CELL_SIZE, CELL_SIZE)

#init
player = (rect(0,0,10,10), vector(0.0,0.0))

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
