# Ashes: Hard Reset: the modular rifle (pickup MR1PA, in hand REL*/MDRIF*), forge cube version.
# From the pictures: a clean grey modern rifle: a flat-top receiver with a long top rail, a slotted rail handguard,
# a skeleton adjustable stock with a cheek riser, a curved magazine, a box red-dot sight and a folding front sight.
from _common import Model, fp, BLACK, STEEL, STEEL_HI, DARK, BRASS, SCREW, mul

GREY = (112, 116, 122)
GREY_DK = (70, 74, 80)
Z_BORE = 12.0
RECEIVER = (60, 130, 3, 19, 8.0)
STOCK = [(0, -10), (0, 14), (4, 16), (24, 16), (40, 14), (60, 13), (60, 6), (40, 4), (20, -4), (6, -10)]
GRIP = [(80, 2), (72, 2), (64, -14), (62, -22), (72, -24), (76, -14), (86, 0)]
MAG = [(98, 2), (97, -14), (100, -26), (112, -28), (112, -14), (113, 2)]


def build():
    m = Model("ashes_modular_rifle")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (72, 0, 0)
    g = fp.metal(GREY)
    rx0, rx1, rz0, rz1, rw = RECEIVER
    m.cbox(rx0, rx1, rw, rz0, rz1, g, bevel=1.0, edge=0.5)
    m.box(94, 112, -rw / 2 - 0.5, -rw / 2 + 1.5, 11, 16, None, size=0.25, carve=True)
    m.cyl(98, 104, -2.5, 13.5, 1.1, BRASS, size=0.25, edge=0.25)
    m.part = 'rail'
    # the long top rail: slots across it all the way
    m.cbox(rx0 + 2, 200, 5.0, rz1, rz1 + 2, fp.metal(GREY_DK), size=0.5)
    for x in range(rx0 + 4, 199, 3):
        m.box(x, x + 1, -2.5, 2.5, rz1 + 1.25, rz1 + 2, None, size=0.25, carve=True)
    m.part = 'handguard'
    # handguard with long slots, barrel, a muzzle brake
    m.cbox(rx1, 200, 9.0, 4, rz1, g, bevel=1.5, edge=0.5)
    for x in range(rx1 + 6, 194, 12):
        for side in ('+y', '-y'):
            m.groove([(x, 9), (x + 7, 9)], side, depth=3, width=6, dark=0.2)
    m.part = 'barrel'
    fp.barrel(m, 200, 240, Z_BORE, 1.8, fp.metal(BLACK), bore=1.0)
    m.cbox(232, 244, 5.0, Z_BORE - 2.5, Z_BORE + 2.5, fp.metal(DARK), bevel=1.0, edge=0.25)
    for x in (235, 239):
        for side in ('+y', '-y'):
            m.groove([(x, Z_BORE - 1.5), (x, Z_BORE + 1.5)], side, depth=3, width=2, dark=0.15)
    m.part = 'stock'
    # skeleton stock with a cheek riser
    m.cprism(STOCK, 7.0, fp.metal(GREY_DK), bevel=1.5, edge=0.5)
    m.prism([(10, 4), (10, 10), (44, 9), (44, 5)], -4, 4, None, carve=True, size=0.5)
    m.cbox(4, 34, 4.0, 16, 19, fp.metal(BLACK), bevel=1.0, edge=0.25)
    m.cbox(-2, 0, 7.5, -11, 15, fp.metal(BLACK), size=0.5)
    m.part = 'grip'
    m.cprism(GRIP, 7.5, fp.metal(BLACK), bevel=1.5, edge=0.5)
    m.part = 'mag'
    m.cprism(MAG, 7.0, fp.metal(GREY_DK), bevel=1.0, edge=0.5)
    m.part = 'body'
    m.part = 'guard'
    fp.guard(m, 80, 98, -6, rz0, g)
    fp.trigger(m, 88, rz0, fp.metal(STEEL_HI), length=5)
    m.part = 'sight'
    # red-dot box sight, folding front sight
    m.cbox(96, 116, 8.0, rz1 + 2, rz1 + 11, fp.metal(BLACK), bevel=1.0, edge=0.5)
    m.cbox(95, 117, 5.0, rz1 + 4, rz1 + 9, None, size=0.5, carve=True)
    m.box(110, 110.5, -0.25, 0.25, rz1 + 6.25, rz1 + 6.75, (255, 40, 30), size=0.25)
    m.cyl(-4, 4, 104, rz1 + 7, 1.3, fp.metal(DARK), axis='y', edge=0.25)
    m.cbox(192, 196, 3.0, rz1 + 2, rz1 + 9, fp.metal(BLACK), size=0.5)
    m.cbox(192, 196, 1.0, rz1 + 5, rz1 + 8, None, size=0.25, carve=True)
    for side in ('+y', '-y'):
        m.screw(64, 6, side, SCREW, kind='hex')
        m.screw(126, 6, side, SCREW, kind='hex')
        m.screw(40, 10, side, SCREW, kind='hex')
        m.groove([(rx0, rz0 + 4), (rx1, rz0 + 4)], side, depth=1, dark=0.45)
        m.decal(["#...#.###", "##.##.#.#", "#.#.#.##.", "#...#.#.#"], 66, 16, side, (220, 220, 220), mode='paint')
    m.wear_edges(0.4, (200, 204, 210))
    m.scratches('+y', (rx0, 200, 4, rz1), 18, 191)
    m.crack(150, 8, '-y', 10, 192, heading=0.1)
    m.grime(0.15, 193)
    return m
