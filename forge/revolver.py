# Ashes 2063: the .45 revolver (pickup REVPA / PISTA, in hand PISTO*), forge cube version.
# From the pictures: grey steel, a heavy barrel with a full under-lug and a ventilated top rib, a fluted six-shot
# cylinder, a spur hammer, an orange dot on the front sight, an olive-brown wooden grip ending in a red-brown butt.
import math

from _common import Model, fp, STEEL, STEEL_HI, DARK, BRASS, SCREW, mul

STEEL_R = (104, 108, 112)
GRIP_WOOD = (112, 98, 52)              # the pictures' olive-brown grip
GRIP_DK = (70, 58, 28)
BUTT = (104, 44, 28)
Z_BORE = 10.0
FRAME = [(0, 2), (0, 14), (6, 15), (30, 15), (30, 3), (24, 0), (8, -2)]
BARREL = (30, 74, 2.3, 1.2)            # x0, x1, radius, bore
LUG = (30, 70, 4.5, 8.0)               # x0, x1, z0, z1 under the barrel
CYL = (8, 26, 5.6)                     # x0, x1, radius (axis just under the bore line)
GRIP = [(2, 2), (-4, 0), (-12, -16), (-14, -26), (-2, -29), (4, -24), (8, -10), (10, 0)]


def build():
    m = Model("ashes_revolver")
    m.pivot = (4, 0, 0)
    st = fp.metal(STEEL_R)
    m.cprism(FRAME, 7.0, st, bevel=1.0, edge=0.5)
    m.box(0, 32, -2.5, 2.5, 15, 17, fp.metal(mul(STEEL_R, 0.9)), size=0.5, edge=0.25)    # top strap
    # cylinder: fluted, with brass in the chamber mouths at the front
    cx0, cx1, cr = CYL
    cz = Z_BORE - 1.5
    m.part = 'cylinder'
    m.cyl(cx0, cx1, 0, cz, cr, fp.metal(mul(STEEL_R, 1.15)), edge=0.25)
    m.cyl(cx0 - 0.5, cx0, 0, cz, cr, None, size=0.25, edge=0.25, carve=True)          # gaps either side of it
    m.cyl(cx1, cx1 + 0.5, 0, cz, cr, None, size=0.25, edge=0.25, carve=True)
    for k in range(6):
        a = k * math.pi / 3 + math.pi / 6
        m.cyl(cx0 + 3, cx1 - 3, math.cos(a) * (cr + 0.6), cz + math.sin(a) * (cr + 0.6), 1.9, None, edge=0.25,
              carve=True)                                                                  # flutes
        b = a + math.pi / 6
        yc, zc = math.cos(b) * 3.3, cz + math.sin(b) * 3.3
        m.cyl(cx1 - 1.5, cx1 + 0.5, yc, zc, 1.0, None, edge=0.25, carve=True)              # chamber mouths
        m.cyl(cx1 - 2, cx1 - 1.5, yc, zc, 1.0, BRASS, size=0.25, edge=0.25)
    m.part = 'body'
    # barrel with an under-lug and a vented rib
    bx0, bx1, br, bore = BARREL
    fp.barrel(m, bx0, bx1, Z_BORE, br, st, bore=bore)
    lx0, lx1, lz0, lz1 = LUG
    m.cbox(lx0, lx1, 4.0, lz0, lz1, st, bevel=1.0, edge=0.5)
    m.cyl(lx1 - 2, lx1, 0, lz0 + 2.0, 1.5, fp.metal(STEEL_HI), edge=0.25)                 # ejector rod tip
    m.cbox(bx0, bx1 - 1, 2.0, Z_BORE + 2, Z_BORE + 3.5, st, size=0.5, edge=0.25)
    for x in range(int(bx0) + 3, int(bx1) - 3, 4):
        m.box(x, x + 1.5, -1, 1, Z_BORE + 2.5, Z_BORE + 3.5, None, size=0.25, carve=True)  # rib vents
    m.box(bx1 - 4, bx1 - 1, -0.75, 0.75, Z_BORE + 3.5, Z_BORE + 6, fp.metal(STEEL), size=0.25)   # front sight
    m.box(bx1 - 4.25, bx1 - 4, -0.5, 0.5, Z_BORE + 4.75, Z_BORE + 5.5, (255, 140, 30), size=0.25)  # orange dot
    fp.rear_sight(m, 2, 16.5, 1.5, st, w=3.0, notch=1.0)
    # hammer: a spur leaning back, its thumb piece cut in steps
    m.part = 'hammer'
    m.cprism([(-1, 12), (-4, 16), (-6, 16.5), (-5.5, 17.5), (-2, 17), (2, 14), (1, 11)], 2.5, fp.metal(STEEL_HI),
             size=0.5, edge=0.25)
    m.part = 'body'
    for i in range(4):
        m.box(-5.5 + i * 0.75, -5.0 + i * 0.75, -1.25, 1.25, 16.75 - i * 0.25, 17.75 - i * 0.25, None, size=0.25,
              carve=True)
    fp.guard(m, 6, 22, -9, -1, st)
    fp.trigger(m, 15, -1, fp.metal(STEEL_HI), length=6.0)
    # grip: olive-brown wood with a red-brown butt, checkered panels, a medallion screw
    m.cprism(GRIP, 8.0, fp.wood(GRIP_WOOD, GRIP_DK, along='z', ring=2.0), bevel=2.0, edge=0.5)
    m.recolour(lambda x, y, z: z < -24.5, fp.wood(BUTT, mul(BUTT, 0.6), along='z'))
    m.cprism([(-1, 1), (-4, 1), (-6, -4), (2, -4), (4, 1)], 7.5, st, size=0.5, edge=0.25)   # frame tang over the grip
    for side in ('+y', '-y'):
        fp.checker(m, (-10, 5, -22, -6), side, GRIP_WOOD, GRIP_DK)
        m.screw(-2, -14, side, (150, 130, 70), kind='slot')
        m.screw(4, 7, side, SCREW, kind='slot')
        m.screw(22, 6, side, SCREW, kind='cross')
        m.groove([(1, 13), (28, 13)], side, depth=1, dark=0.5)                                 # side plate seam
        m.groove([(28, 3), (28, 13)], side, depth=1, dark=0.5)
    m.decal(["#..#.###.###", "#..#.#...#..", "####.###.###", "...#...#...#", "...#.###.###"], 34, Z_BORE - 1.0,
            '+y', mul(STEEL_R, 0.5), mode='carve')                                              # a ".45"-style stamp
    m.wear_edges(0.45, (190, 192, 196))
    m.scratches('+y', (2, 70, 2, 16), 14, 21)
    m.scratches('-y', (2, 70, 2, 16), 10, 22)
    m.crack(-6, -12, '+y', 9, 23, heading=-1.2)
    m.grime(0.18, 24)
    return m
