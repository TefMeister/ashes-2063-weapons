# Ashes 2063: the pipe bomb (pickup ROCKA, in hand pipe*), forge cube version.
# From the pictures: a dark steel pipe with threaded end caps, wrapped round the middle in duct tape, a red-labelled
# charge, wires and a black fuse coming out of the top cap, sparks at its tip once lit.
import math

from _common import Model, fp, BLACK, STEEL, STEEL_HI, DARK, SCREW, mul, hash01

PIPE = (122, 124, 128)
TAPE_GREY = (150, 150, 146)
LABEL_RED = (176, 28, 24)


def build():
    m = Model("ashes_pipe_bomb")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (24, 0, 0)
    # the pipe along x, 16 cm, end caps a little wider, hex flats on the caps
    m.cyl(0, 48, 0, 0, 5.0, fp.rusty(PIPE, (110, 60, 30), 0.25), edge=0.5)
    m.part = 'caps'
    for x0, x1 in ((-6, 4), (44, 54)):
        m.cyl(x0, x1, 0, 0, 6.2, fp.metal(mul(PIPE, 0.85)), edge=0.5)
        for side in ('+y', '-y', '+z', '-z'):
            for x in range(int(x0) + 1, int(x1), 2):
                pts = [(x, -2), (x, 2)]
                m.groove(pts, side, depth=1, dark=0.6)
    m.part = 'tape'
    # duct tape round the middle, its loose end lifting
    m.cyl(16, 34, 0, 0, 5.6, fp.metal(TAPE_GREY, 0.12), edge=0.25)
    for x in (20, 26, 31):
        for side in ('+y', '-y', '+z', '-z'):
            m.groove([(x, -3), (x + 1, 3)], side, depth=1, dark=0.75)
    m.box(33, 37, -1, 3, 5, 5.5, TAPE_GREY, size=0.25)
    # a red label with a skull taped on
    m.decal(["..####..", ".######.", "##.##.##", "########", ".#.##.#.", "..####.."], 22, 3, '+y', LABEL_RED,
            dot=2, mode='paint')
    m.part = 'fuse'
    # the fuse: out of the back cap's centre, curling up
    m.cyl(-9, -6, 0, 0, 1.4, fp.metal(STEEL_HI), edge=0.25)
    for i in range(40):
        t = i / 39
        x = -9 - math.sin(t * 2.4) * 8
        z = t * 14
        m.ball(x, math.sin(t * 5) * 1.5, z, 0.7, (30, 30, 30), edge=0.25)
    m.ball(-9 - math.sin(2.4) * 8, math.sin(5) * 1.5, 14.5, 0.9, (255, 170, 60), edge=0.25)    # glowing tip
    m.part = 'wires'
    # two wires taped along it to a little battery pack
    for y in (2.2, 3.2):
        m.box(-4, 40, y, y + 0.5, 5.25, 5.75, (40, 90, 170) if y < 3 else (190, 40, 30), size=0.25)
    m.cbox(4, 14, 6.0, 5, 9, fp.metal((40, 40, 46)), size=0.5)
    m.wear_edges(0.4, (190, 190, 190))
    m.scratches('-y', (0, 48, -4, 4), 10, 121)
    m.grime(0.3, 122)
    return m
