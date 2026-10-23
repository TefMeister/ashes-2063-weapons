# Ashes Afterglow (episode 2): the Military Rifle, an AR-15 (pickup M16PA / AR15A, in hand AR15*), forge cube
# version. From the pictures: a black rifle with a carry handle and its rear sight drum, a triangle front sight, a
# birdcage flash hider, a brown wooden handguard and stock, a straight magazine, and a pale rope sling slung under it.
import math

from _common import Model, fp, BLACK, STEEL, STEEL_HI, DARK, WOOD, WOOD_DK, BRASS, SCREW, mul

WOOD_RED = (128, 66, 34)
ROPE = (168, 150, 112)
Z_BORE = 12.0
UPPER = (60, 128, 9, 20, 8.0)
LOWER = [(58, 9), (58, 2), (70, -2), (110, -2), (124, 2), (128, 9)]
STOCK = [(0, -12), (0, 14), (6, 15), (58, 18), (58, 6), (40, 2), (6, -12)]
GRIP = [(80, 0), (72, 0), (64, -14), (62, -22), (72, -24), (76, -14), (86, -2)]
HANDGUARD = (128, 188, 5.0)
BARREL = (128, 256, 1.6, 0.9)
MAG = [(98, 0), (97, -28), (110, -30), (113, -2)]


def build():
    m = Model("ashes_military_rifle")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (72, 0, 0)
    blk = fp.metal(BLACK)
    ux0, ux1, uz0, uz1, uw = UPPER
    m.cbox(ux0, ux1, uw, uz0, uz1, blk, bevel=1.0, edge=0.5)
    m.part = 'lower'
    m.cprism(LOWER, uw - 0.5, blk, bevel=1.0, edge=0.5)
    m.part = 'body'
    m.box(92, 112, -uw / 2 - 0.5, -uw / 2 + 1.5, 12, 17, None, size=0.25, carve=True)       # ejection port
    m.cyl(96, 102, -2.5, 14.5, 1.0, BRASS, size=0.25, edge=0.25)
    m.cyl(84, 90, -uw / 2 - 2.5, 16, 1.6, blk, axis='x', edge=0.25)                         # forward assist
    m.part = 'handle'
    # carry handle with the rear sight drum at its back
    m.cbox(66, 120, 3.5, uz1 + 5, uz1 + 8, blk, bevel=0.5, edge=0.25)
    for x0 in (66, 112):
        m.cprism([(x0, uz1), (x0, uz1 + 8), (x0 + 8, uz1 + 8), (x0 + 8, uz1)], 3.5, blk, size=0.5, edge=0.25)
    m.cbox(68, 74, 2.5, uz1 + 8, uz1 + 11, blk, size=0.5, edge=0.25)
    m.cyl(69, 73, 0, uz1 + 10, 0.6, None, axis='x', edge=0.25, carve=True)
    m.cyl(-3, 3, 76, uz1 + 6, 1.8, blk, axis='y', edge=0.25)
    m.part = 'stock'
    # stock and grip: brown wood, butt plate
    wood = fp.wood(WOOD_RED, WOOD_DK)
    m.cprism(STOCK, 8.5, wood, bevel=2.0, edge=0.5)
    m.cbox(-2, 0, 9.0, -13, 15, fp.metal(DARK), size=0.5)
    m.part = 'grip'
    m.cprism(GRIP, 7.5, fp.metal(BLACK), bevel=1.5, edge=0.5)
    m.part = 'handguard'
    # handguard: round, wooden, ribbed lengthwise
    hx0, hx1, hr = HANDGUARD
    m.cyl(hx0, hx1, 0, Z_BORE, hr, wood, edge=0.5)
    m.cyl(hx0, hx0 + 3, 0, Z_BORE, hr + 0.75, blk, edge=0.25)
    m.cyl(hx1 - 2, hx1, 0, Z_BORE, hr + 0.5, blk, edge=0.25)
    for side in ('+y', '-y'):                                       # its lengthwise ribs
        for z in (Z_BORE - 2.5, Z_BORE, Z_BORE + 2.5):
            m.groove([(hx0 + 4, z), (hx1 - 3, z)], side, depth=1, dark=0.5)
    m.part = 'barrel'
    # barrel, triangle front sight, birdcage flash hider
    bx0, bx1, br, bore = BARREL
    fp.barrel(m, bx0, bx1, Z_BORE, br, blk, bore=bore)
    m.part = 'sight'
    m.cprism([(192, Z_BORE - 3), (200, Z_BORE - 3), (200, Z_BORE + 4), (197, uz1 + 11), (195, uz1 + 11),
              (192, Z_BORE + 4)], 3.0, blk, size=0.5, edge=0.25)
    m.box(195, 197, -0.25, 0.25, uz1 + 11, uz1 + 13, STEEL_HI, size=0.25)
    m.part = 'barrel'
    m.cyl(bx1 - 10, bx1, 0, Z_BORE, 2.2, fp.metal(DARK), edge=0.25)
    for k in range(6):
        a = k * math.pi / 3
        m.cyl(bx1 - 8, bx1 - 1, math.cos(a) * 2.0, Z_BORE + math.sin(a) * 2.0, 0.6, None, edge=0.25, carve=True)
    m.part = 'mag'
    m.cprism(MAG, 7.0, fp.metal(mul(BLACK, 1.1)), bevel=1.0, edge=0.5)
    m.part = 'body'
    m.part = 'guard'
    fp.guard(m, 78, 98, -6, -1, blk)
    fp.trigger(m, 86, 0, fp.metal(STEEL_HI), length=5)
    m.part = 'sling'
    # the rope sling: from the stock's bottom to the front, hanging in a slack curve under the gun
    for i in range(160):
        t = i / 159
        x = 4 + t * 180
        z = -12 + t * 22 - math.sin(t * math.pi) * 12
        m.ball(x, -4.5, z, 0.9, ROPE if (i // 3) % 2 else mul(ROPE, 0.8), edge=0.25)
    for side in ('+y', '-y'):
        m.screw(64, 4, side, SCREW, kind='rivet')
        m.screw(118, 4, side, SCREW, kind='rivet')
        m.screw(26, 4, side, SCREW, kind='slot')
        m.groove([(ux0, uz0 + 0.5), (ux1, uz0 + 0.5)], side, depth=1, dark=0.45)
        m.decal(["####.###.###", "#....#.#.#..", "###..###.#..", "#....#.#.#..", "####.#.#.###"], 62, 6, side,
                (210, 200, 180), mode='paint')                              # SAFE / FIRE markings
    m.wear_edges(0.4, (190, 186, 180))
    m.scratches('+y', (ux0, ux1, -2, uz1), 14, 131)
    m.crack(30, 6, '+y', 14, 132, heading=0.2)
    m.grime(0.22, 133)
    return m
