from R_Tree_To_compile.build.R_Tree import R_Tree, Rect
import pygame as pg
import random
import colorsys
from visualisation import *



t = R_Tree()

WIDTH = 1500
HEIGHT = 1000
FPS = 30

pg.init()

pg.font.init()
pg.mixer.init()
myfont = pg.font.SysFont('Comic Sans MS', 50)
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("R-Tree")
clock = pg.time.Clock()

srch = False

running = True

start_pos = 0
srch_res = 0
while running:

    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if pg.mouse.get_pressed()[0]:
                if not start_pos:
                    start_pos = pg.mouse.get_pos()
                else:
                    if srch:
                        srch_res = search(t, start_pos, pg.mouse.get_pos())
                    else:
                        insert(t, start_pos, pg.mouse.get_pos())

                    start_pos = 0

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                if (srch):
                    srch_res = 0
                srch = not srch

    screen.fill((150, 150, 150))
    draw_tree(t,screen)

    if start_pos:
        mp = pg.mouse.get_pos()
        pg.draw.rect(screen, (180, 180, 180, 20) if srch else (180, 0, 0),
                     (min(start_pos[0], mp[0]), min(start_pos[1], mp[1]), abs(start_pos[0] - mp[0]),
                      abs(start_pos[1] - mp[1])), 2 if srch else 0, border_radius=4, )
    if srch_res:
        draw_serched_nodes(srch_res,screen)

    print_text(srch,myfont,screen)

    pg.display.flip()

t.print_tree()