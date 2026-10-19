# Ashes 2063: the sawed-off shotgun (pickup SAWPA, in hand SAWN*), forge cube version.
# From the pictures: a side-by-side double barrel cut short, a steel action with a top lever, the stock cut down to a
# bulbous wooden pistol grip wrapped in blue cloth and tape, a dented brass-capped butt.
from _common import Model, fp, BLACK, STEEL, STEEL_HI, WOOD, WOOD_DK, TAPE_BLUE, TAPE, BRASS, SCREW, RUST, mul

Z_BORE = 9.0
BARRELS = (40, 128, 2.9, 1.9)          # x0, x1, radius, bore; two of them side by side
GAP = 2.9                              # each barrel's centre off y = 0
ACTION = (18, 42, -1, 14, 11.0)        # x0, x1, z0, z1, width
FOREND = [(42, 2), (42, 6), (80, 6.5), (84, 4), (82, 2), (46, 1)]
GRIP = [(20, 2), (8, 4), (-4, -2), (-14, -12), (-20, -22), (-8, -26), (2, -14), (14, -4), (24, -1)]


def build():
    m = Model("ashes_sawed_off")
    m.pivot = (12, 0, 0)
    bx0, bx1, br, bore = BARRELS
    for y in (-GAP, GAP):
        fp.barrel(m, bx0, bx1, Z_BORE, br, fp.rusty(STEEL, RUST, 0.3), bore=bore, yc=y)
    m.cbox(bx0, bx1 - 1, 2.0, Z_BORE + 1.5, Z_BORE + 3.25, fp.metal(BLACK), size=0.5)        # rib between them
    m.cbox(bx0, bx1 - 3, 3.0, Z_BORE - 3.5, Z_BORE - 2, fp.metal(BLACK), size=0.5)
    for i in range(10):                                            # a ragged hacksaw cut at the muzzle
        y = -GAP - 2.5 + i * 1.1
        z = Z_BORE + (2.2 if i % 3 else -2.7)
        m.box(bx1 - 0.5, bx1, y, y + 0.5, z, z + 0.5, None, size=0.25, carve=True)
    ax0, ax1, az0, az1, aw = ACTION
    m.cbox(ax0, ax1, aw, az0, az1, fp.metal(STEEL), bevel=2.0, bevel_x=1.0, edge=0.5)
    m.part = 'lever'
    m.box(24, 34, -3.5, 1.0, 14, 15.0, fp.metal(STEEL_HI), size=0.5, edge=0.25, bevel_x=0.5)      # top lever, lying flat
    m.part = 'body'
    for y in (-2.5, 2.5):                                          # two hammers
        m.prism([(16, 12), (14, 15), (15.5, 15.5), (19, 13.5)], y - 0.75, y + 0.75, fp.metal(STEEL_HI), size=0.25)
    m.cprism(FOREND, 9.0, fp.wood(WOOD, WOOD_DK), bevel=2.0, edge=0.5)
    # grip: the stock cut down, wrapped in blue cloth with tape turns, a brass cap on the butt
    m.cprism(GRIP, 8.0, fp.wood(WOOD, WOOD_DK, along='z'), bevel=2.0, edge=0.5)
    m.recolour(lambda x, y, z: -16 < z < -2 and x < 14, TAPE_BLUE)
    m.recolour(lambda x, y, z: -10 < z < -7.5 and x < 14, TAPE)
    m.ball(-14, 0, -23, 5.0, fp.metal(BRASS), ry=4.5, rz=4.0, edge=0.25)
    fp.guard(m, 18, 32, -8, -1, fp.metal(STEEL))
    fp.trigger(m, 23, -1, fp.metal(STEEL_HI), length=5)
    fp.trigger(m, 28, -1, fp.metal(STEEL_HI), length=5)
    for side in ('+y', '-y'):
        m.screw(24, 6, side, SCREW, kind='slot')
        m.screw(36, 9, side, SCREW, kind='slot')
        m.screw(36, 2, side, SCREW, kind='cross')
        m.groove([(ax0 + 2, az1 - 3), (ax1 - 2, az1 - 3)], side, depth=1, dark=0.5)
        m.decal(["..#..", ".###.", "#####", ".###.", "..#.."], 26, 11, side, (190, 170, 120), mode='raise')
        for t in (-14, -12, -5, -3):
            m.groove([(-16, t), (14, t + 6)], side, depth=1, dark=0.55)                       # wrap turns
    m.wear_edges(0.4, (180, 176, 168))
    m.scratches('+y', (ax0, ax1, az0, az1), 10, 51)
    m.scratches('+y', (bx0, bx1, Z_BORE - 2, Z_BORE + 3), 10, 52)
    m.crack(60, 4, '+y', 10, 53, heading=0.0)
    m.grime(0.24, 54)
    return m
