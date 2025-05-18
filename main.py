from graphics import *
from utils import *
from physics import *
from time import sleep


#input 
def get_input():
    arrows = get_fleches()
    mouse = last_clic()
    touche = ""
    if(touche_enfoncee('K_SPACE')):
        touche = " "
    elif(touche_enfoncee('K_RSHIFT')):
        touche = "rshift"
        sleep(0.1)
    return (arrows, mouse, touche)


def new_pos(player,portals, index):
    src_pos, src_col, src_vertical, src_origin = portals[index] # src_portal
    dst_pos, dst_col, dst_vertical, dst_origin = portals[not(index)] #dest portal
    prect, pvect, jmp = player

    vx,vy = pvect   
    dx,dy = dst_pos

    # se sert a drien 
    if not( (src_vertical and dst_vertical) or not(src_vertical or dst_vertical) ): #src_vertical xor dst_vertical
        temp = vy
        vy = vx
        vx = temp
    elif src_origin == dst_origin:
        if(dst_vertical):
            vx *= -1
        else:
            vy *= -1

    
    x,y,w,h = prect
    x = dx
    y = dy

    if(dst_origin):
        if(dst_vertical):
            x-= w+1
        else:
            y -= h+1
    elif(dst_vertical):
        x += 1
    else:
        y += 1
    
    return ((x,y,w,h),(vx,vy),jmp)




def move_player(player, map, portals, event, gravity, delta_t):
    # don't work because when we move left we are in colision with the floor because of gravity so we backtracking to a stable position that is the initial position
    arrows, click, touche = event
    prect, pvect, jump = player

    ax, ay = arrows
    x,y = pvect
    if ay == 0:
        pvect = (ax * PLAYER_SPEED * delta_t, y)
    elif ay == 1 and not(jump):
        pvect = (0.0,JUMP * delta_t)
    grav_vect = (0.0, gravity * delta_t)
    pvect = vect_sum(pvect, grav_vect)
    jump = 1
    portals_is_active = not(portals[0] is None or portals[1] is None)

    x,y = pvect
    temp = (x,0.0)
    prect = move_rect(prect, temp)
    has_colision = False
    opposite = (-sign(x),0)
    while colision(map, int_rect(prect), CELL_SIZE):

        if(portals_is_active):
            for i,portal in enumerate(portals):
                if point_in_rect(portal_center(portal),prect):
                    return new_pos((prect,pvect,1),portals,i)
                
        has_colision = True
        prect = move_rect(prect, opposite)
    if(has_colision):
        pvect = (0.0,y)
    
    temp = (0.0, y)
    prect = move_rect(prect,temp)
    has_colision = False
    opposite = (0,-sign(y))
    while colision(map, int_rect(prect), CELL_SIZE):

        if(portals_is_active):
            for i,portal in enumerate(portals):
                if point_in_rect(portal_center(portal),prect):
                    return new_pos((prect,pvect,1),portals,i)
                
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
    global active_portal
    arrows, mouse, touche = event
    if touche == "rshift":
        active_portal = not(active_portal)
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
            portals[active_portal] = None
            return
        rect = move_rect(rect, (vectx, vecty))
    pos = colision(map, rect, CELL_SIZE)
    x,y = pos
    if(vectx < 0):
        x += CELL_SIZE
    if(vecty < 0):
        y += CELL_SIZE

    rx, ry, rw, rh = rect
    ryt = ry - vecty

    vertical = bool(colision(map, (rx, ryt, rw, rh), CELL_SIZE))
    if(vertical):
        portals[active_portal] = ((int(x), int(y)), PORTALS_COLOR[active_portal], vertical, vectx > 0)
    else:
        portals[active_portal] = ((int(x), int(y)), PORTALS_COLOR[active_portal], vertical, vecty > 0)
    


def draw_game(map, portals, player, img_player, title_screen, end):
    if(title_screen):
        affiche_image(TITLE_SCREEN,(0,0))
    else:
        remplir_fenetre(couleur(40, 93, 164))
        for coord in map:
            affiche_image(map[coord], grid2window(coord,CELL_SIZE))
        affiche_image(END, grid2window(end,CELL_SIZE))
        if img_player != None:
            rect, vector, jump = player
            x, y, w, h = rect
            affiche_image(img_player, (x, y))
        affiche_rectangle_plein((0,WINDOW_H -30),(30,WINDOW_H),PORTALS_COLOR[active_portal])
        for p in portals:
            if not(p is None):
                portal_coord, color, vertical, origin = p
                x, y = portal_coord
                if(origin):
                    affiche_rectangle_plein(portal_coord, (x + int(not(vertical)) * CELL_SIZE + 3* vertical, y + vertical * CELL_SIZE +3* int(not(vertical)) ), color)
                else:
                    affiche_rectangle_plein(portal_coord, (x + int(not(vertical)) * CELL_SIZE - 3* vertical, y + vertical * CELL_SIZE -3* int(not(vertical)) ), color)
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

def portal_center(portal):
    (x,y),color,vertical, origin = portal
    if(vertical):
        y += CELL_SIZE//2
    else:
        x += CELL_SIZE//2
    return (x,y)

def end_game(player, end):
    prect, pvect, jmp = player
    endx, endy = grid2window(end, CELL_SIZE)
    end_rect =  endx, endy, CELL_SIZE, CELL_SIZE
    return has_intersection(prect,end_rect)



#init

portals = [None, None] # for one blue portal inside : ((120, 80), "bleu", 1,0) 1 or 0 for if it's vertical or horizontal
# with h = 3 and w = 20 for horizontal and h = 20 and w = 3 for vertical
active_portal = 0
PORTALS_COLOR = [bleu,orange]

WINDOW_W, WINDOW_H = 800, 600
init_fenetre(WINDOW_W, WINDOW_H,"porte table")

NB_CELL_W = WINDOW_W // 40
NB_CELL_H = WINDOW_H // 40

CELL_SIZE = WINDOW_W // NB_CELL_W # or : WINDOW_H // NB_CELL_H

PLAYER_SPEED = 200
JUMP = 400

player_size = 32
player = (rect(100,50,player_size,player_size), vector(0.0,0.0),1)
img_player = "images/player.png"
charge_image(img_player)
modifie_taille_image(img_player,player_size, player_size)


affiche_auto_off()
# map: a dict of key = coordinates (i,j) and value = a bloc type
HERBE = "images/herbe.png"
PIERRE  = "images/pierres.png"
MARBLE = "images/marble.png"
TITLE_SCREEN = "images/title_screen.png"
load_tile(HERBE, CELL_SIZE)
load_tile(PIERRE, CELL_SIZE)
load_tile(MARBLE, CELL_SIZE)
charge_image(TITLE_SCREEN)
modifie_taille_image(TITLE_SCREEN,WINDOW_W, WINDOW_H)
ttl_scr = True

END = "images/arrivee.png"
load_tile(END, CELL_SIZE)
end_cell = NB_CELL_W -1, 6

map = {}
for i in range(NB_CELL_W):
    map[(i,0)] = MARBLE
    map[(i,NB_CELL_H-1)] = MARBLE
    if i >10:
        map[(i,5)] = MARBLE

for j in range(NB_CELL_H):
    map[(0,j)] = MARBLE
    if(j < 5 or j > 7):
        map[(NB_CELL_W-1,j)] = MARBLE
    if(j > 7):
        map[(10,j)] = MARBLE

FPS = 60
delta_t = 1/FPS

lance_chrono("temps")

#main

while(not(end_game(player,end_cell))):
    event = get_input()
    arrow, mouse, touche = event
    if(touche == " "):
        ttl_scr = False
    if not(ttl_scr):
        setup_portal(event, player, map, portals)
        player = move_player(player, map,portals, event, GRAVITY, delta_t)
    draw_game(map, portals, player, img_player, ttl_scr, end_cell)
    delta_t = wait("temps", FPS)


print("gagné")
attendre_echap()