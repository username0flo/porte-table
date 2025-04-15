from graphics import *


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


#main

while(1):
    event = get_input()
    setup_portal()
    move_player()
    draw_game()
