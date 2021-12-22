from R_Tree_To_compile.build.R_Tree import R_Tree, Rect
import pygame as pg
import random
import colorsys

def draw_tree(t: R_Tree,screen):
    s = t.to_string()

    ls = s.split('\n')[:-1]
    nodes = [{"level": int(i.split()[0]), "rect": [float(i.split()[1].replace('((', '').replace(',', '')), float(
        i.split()[2].replace('(', '').replace(')', '').replace(',', '')),
                                                   float(i.split()[3].replace('(', '').replace(',', '')), float(
            i.split()[4].replace('(', '').replace(')', '').replace(',', ''))]} for i in ls]
    l = max(10, nodes[-1]['level'])
    max_level = nodes[-1]['level']
    nodes = sorted(nodes, key=lambda a: a['level'])
    indent = 0
    border = 1
    for node in nodes:
        pg.draw.rect(screen, [j * 255 for j in colorsys.hsv_to_rgb((max_level - node['level']) / (l * 1.1), 1, 1)], (
            node['rect'][0] + node['level'] * indent + border, node['rect'][1] + node['level'] * indent + border,
            node['rect'][2] - node['rect'][0] - node['level'] * 2 * indent - border * 2,
            node['rect'][3] - node['rect'][1] - node['level'] * 2 * indent - border * 2), border_radius=4)
    for node in nodes:
        pg.draw.rect(screen, (0, 0, 0),
                     (node['rect'][0] + node['level'] * indent, node['rect'][1] + node['level'] * indent,
                      node['rect'][2] - node['rect'][0] - node['level'] * 2 * indent,
                      node['rect'][3] - node['rect'][1] - node['level'] * 2 * indent), border, border_radius=4)


def insert(t, ps, pf):
    t.insert(Rect(min(ps[0], pf[0]), min(ps[1], pf[1]), max(ps[0], pf[0]), max(ps[1], pf[1])))


def search(t, ps, pf):
    res = t.search(Rect(min(ps[0], pf[0]), min(ps[1], pf[1]), max(ps[0], pf[0]), max(ps[1], pf[1])))
    return list(map(str, res))


def draw_serched_nodes(nodes,screen):
    rects = [[float(i.split()[0].replace('((', '').replace(',', '')),
              float(i.split()[1].replace('(', '').replace(')', '').replace(',', '')),
              float(i.split()[2].replace('(', '').replace(',', '')),
              float(i.split()[3].replace('(', '').replace(')', '').replace(',', ''))] for i in nodes]
    for r in rects:
        pg.draw.rect(screen, (150, 0, 200), [r[0], r[1], r[2] - r[0], r[3] - r[1]], 5, border_radius=4)


def print_text(srch, font,screen):
    if srch:
        textsurface = font.render('search', False, (30, 0, 0))
    else:
        textsurface = font.render('insert', False, (30, 0, 0))
    screen.blit(textsurface, (0, 0))