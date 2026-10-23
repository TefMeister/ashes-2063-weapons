# Ashes: Hard Reset: the hunter shotgun (pickup HNSPA, in hand HNSN*), forge cube version.
# From the pictures: a long side-by-side hunting double, black barrels with a thin gold line along the rib, an
# engraved silver action with a top lever, a full red-brown wooden stock with a fore-end, the barrels breaking open
# to show brass shell heads.
from _common import Model, fp, BLACK, STEEL, STEEL_HI, DARK, BRASS, SCREW, mul

RED_WOOD = (128, 62, 40)
RED_WOOD_DK = (70, 30, 18)
SILVER = (168, 168, 164)
GOLD = (210, 170, 70)
Z_BORE = 12.0
GAP = 2.8
STOCK = [(0, -16), (0, 12), (4, 14), (52, 12), (66, 10), (66, 2), (48, -2), (28, -6), (6, -16)]
ACTION = [(64, -1), (64, 16), (92, 16), (92, 4), (86, -1)]
FOREEND = [(92, 2), (92, 9), (150, 9), (154, 6), (150, 3), (96, 1)]


def build():
    m = Model("ashes_hunter_shotgun")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (72, 0, 0)
    m.part = 'stock'
    m.cprism(STOCK, 9.0, fp.wood(RED_WOOD, RED_WOOD_DK), bevel=2.5, edge=0.5)
    m.cbox(-2, 0, 9.5, -17, 13, fp.metal(DARK), size=0.5)
    m.part = 'body'
    m.cprism(ACTION, 11.0, fp.metal(SILVER), bevel=1.5, edge=0.5)
    m.part = 'barrels'
    for y in (-GAP, GAP):
        fp.barrel(m, 92, 262, Z_BORE, 2.8, fp.metal(BLACK), bore=1.9, yc=y)
    m.cbox(92, 261, 1.5, Z_BORE + 1.5, Z_BORE + 3.0, fp.metal(BLACK), size=0.5)
    m.box(92, 260, -0.25, 0.25, Z_BORE + 3.0, Z_BORE + 3.25, GOLD, size=0.25)                  # the gold line
    m.ball(258, 0, Z_BORE + 3.75, 0.6, BRASS, edge=0.25)
    m.part = 'foreend'
    m.cprism(FOREEND, 9.5, fp.wood(RED_WOOD, RED_WOOD_DK), bevel=2.0, edge=0.5)
    m.part = 'body'
    m.part = 'lever'
    m.box(70, 82, -2, 2, 16, 17, fp.metal(STEEL_HI), size=0.5, edge=0.25)                       # top lever
    m.box(78, 84, -4, -1, 16, 17, fp.metal(STEEL_HI), size=0.5, edge=0.25)
    m.part = 'guard'
    fp.guard(m, 66, 84, -8, -1, fp.metal(SILVER))
    fp.trigger(m, 72, -1, fp.metal(DARK), length=5)
    fp.trigger(m, 77, -1, fp.metal(DARK), length=5)
    # the engraving: scrolls and a gold-inlaid bird on each side plate, carved with the smallest cubes
    scroll = ["..####..", ".#....#.", "#..##..#", "#.#..#.#", "#..#...#", ".#....#.", "..####.."]
    bird = ["....##....", "...####...", "#..####..#", "##########", ".########.", "...#..#..."]
    for side in ('+y', '-y'):
        m.decal(scroll, 66, 14, side, mul(SILVER, 0.5), mode='carve')
        m.decal(scroll, 82, 8, side, mul(SILVER, 0.5), mode='carve')
        m.decal(bird, 72, 8, side, GOLD, mode='paint')
        m.screw(68, 2, side, SCREW, kind='slot')
        m.screw(88, 2, side, SCREW, kind='slot')
        m.groove([(65, 6), (91, 6)], side, depth=1, dark=0.5)
        fp.checker(m, (44, 64, -2, 10), side, RED_WOOD, RED_WOOD_DK)
    m.wear_edges(0.4, (230, 220, 200))
    m.scratches('+y', (92, 250, Z_BORE - 2, Z_BORE + 2), 14, 181)
    m.crack(20, -2, '+y', 16, 182, heading=0.25)
    m.grime(0.2, 183)
    return m
