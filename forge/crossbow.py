# Ashes: Hard Reset: the crossbow (pickup XBWPA, in hand XBOW*), forge cube version.
# From the pictures: a steel-framed crossbow with wooden rails along the stock, wide recurve limbs wrapped in black
# and white, pulley cams with cables at their tips, a string, a bolt with yellow fletching and a steel broadhead, a
# scope-like rail sight and a pistol grip.
import math

from _common import Model, fp, BLACK, STEEL, STEEL_HI, DARK, WOOD, WOOD_DK, SCREW, mul

LIMB_W = (210, 208, 200)
FLETCH = (230, 200, 40)
Z_RAIL = 12.0
LIMB_X = 150                           # where the limbs meet the front of the stock
SPAN = 46                              # half the limbs' width (to each cam)


def limb_point(t, side):
    """Along a limb from the riser (t=0) to its cam (t=1): sweeps out, then curls forward at the tip."""
    y = side * (6 + t * (SPAN - 6))
    x = LIMB_X - 14 * t + 12 * max(0.0, t - 0.75) ** 2 * 16
    return x, y


def build():
    m = Model("ashes_crossbow")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (60, 0, 0)
    # the stock: a steel frame with wooden side rails
    m.cprism([(0, -6), (0, 10), (6, 13), (150, 13), (156, 10), (156, 6), (60, 4), (40, 0), (10, -8)], 7.0,
             fp.metal(STEEL), bevel=1.5, edge=0.5)
    for y in (3.5, -5.0):
        m.box(40, 140, y, y + 1.5, 6, 11, fp.wood(WOOD, WOOD_DK), size=0.5)
    m.part = 'rail'
    m.cbox(30, 156, 2.0, 13, 14, fp.metal(DARK), size=0.5)                                     # the bolt groove
    m.cbox(30, 156, 0.75, 13.5, 14, None, size=0.25, carve=True)
    m.part = 'grip'
    m.cprism([(58, 4), (50, 4), (44, -14), (42, -22), (52, -24), (56, -14), (64, 2)], 7.0, fp.metal(BLACK),
             bevel=1.5, edge=0.5)
    m.part = 'guard'
    fp.guard(m, 60, 76, -6, 4, fp.metal(STEEL))
    fp.trigger(m, 66, 4, fp.metal(DARK), length=5)
    m.part = 'body'
    m.cbox(-2, 0, 8.0, -7, 11, fp.metal(DARK), size=0.5)
    m.part = 'riser'
    # the riser and the two limbs, wrapped black and white, with cams at their tips
    m.cbox(LIMB_X - 6, LIMB_X + 6, 14.0, 6, 16, fp.metal(BLACK), bevel=1.5, edge=0.5)
    for side in (-1, 1):
        m.part = 'limbs'
        for i in range(90):
            t = i / 89
            x, y = limb_point(t, side)
            col = LIMB_W if int(t * 18) % 2 else (30, 30, 34)
            m.box(x - 1.5, x + 1.5, y - 1.0, y + 1.0, Z_RAIL - 1.5, Z_RAIL + 1.5, col, size=0.5, keep=True)
        cx, cy = limb_point(1.0, side)
        m.cyl(Z_RAIL - 3, Z_RAIL + 3, cx, cy, 3.5, fp.metal(STEEL_HI), axis='z', edge=0.25)
        m.cyl(Z_RAIL - 4, Z_RAIL + 4, cx, cy, 1.0, fp.metal(DARK), axis='z', edge=0.25)
        m.part = 'string'
        # the string from the cam back to the latch, and a cable crossing to the other limb
        for i in range(120):
            t = i / 119
            x = cx + (96 - cx) * t
            y = cy * (1 - t)
            m.box(x - 0.125, x + 0.125, y - 0.125, y + 0.125, Z_RAIL + 1.5, Z_RAIL + 1.75, (30, 28, 26), size=0.25)
    m.part = 'body'
    m.cbox(92, 100, 6.0, 13, 16, fp.metal(STEEL_HI), size=0.5, edge=0.25)                     # the latch
    # the bolt: shaft, yellow fletching at the back, broadhead in front of the riser
    m.part = 'bolt'
    m.cyl(96, 176, 0, Z_RAIL + 2.5, 0.6, (60, 60, 64), edge=0.25)
    for z0, z1, y0, y1 in ((Z_RAIL + 3, Z_RAIL + 5.5, -0.25, 0.25), (Z_RAIL + 2, Z_RAIL + 3, 0.5, 2.5),
                           (Z_RAIL + 2, Z_RAIL + 3, -2.5, -0.5)):
        m.box(98, 110, y0, y1, z0, z1, FLETCH, size=0.25)
    m.cprism([(176, Z_RAIL + 0.5), (176, Z_RAIL + 4.5), (184, Z_RAIL + 2.5)], 3.0, fp.metal(STEEL_HI), size=0.25)
    m.part = 'body'
    m.part = 'scope'
    # a rail sight on top
    m.cbox(70, 96, 4.0, 14, 16, fp.metal(BLACK), size=0.5)
    m.cyl(72, 94, 0, 19, 2.5, fp.metal(BLACK), edge=0.25)
    m.cyl(71.5, 72, 0, 19, 1.8, (60, 90, 110), size=0.25, edge=0.25)
    for side in ('+y', '-y'):
        for x in (20, 46, 120, 140):
            m.screw(x, 4, side, SCREW, kind='hex')
        m.groove([(10, 2), (150, 8)], side, depth=1, dark=0.5)
    m.wear_edges(0.4, (220, 220, 224))
    m.scratches('+y', (0, 150, 0, 12), 14, 201)
    m.crack(100, 9, '+y', 8, 202, heading=0.0)
    m.grime(0.15, 203)
    return m
