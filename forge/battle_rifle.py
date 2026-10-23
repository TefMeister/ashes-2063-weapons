# Ashes 2063: the Battle Rifle, an FAL (pickup FICOA / FWEPA, in hand FAL1*), forge cube version.
# From the pictures: light tan wood stock, pistol grip and handguard over a black receiver, a box magazine, a slotted
# flash hider, a tall box sight on top with a round lens, and a red no-entry sticker on its side.
from _common import Model, fp, BLACK, STEEL, STEEL_HI, DARK, BRASS, SCREW, mul

TAN = (176, 116, 62)
TAN_DK = (112, 66, 30)
STICKER = (200, 30, 30)
Z_BORE = 12.0
RECEIVER = (60, 136, 2, 18, 9.0)                  # x0, x1, z0, z1, width
STOCK = [(0, -14), (0, 14), (6, 16), (60, 16), (60, 6), (36, -2), (8, -16)]
GRIP = [(80, 2), (70, 2), (62, -14), (60, -24), (70, -26), (76, -16), (86, 0)]
HANDGUARD = (136, 196, 1.5, 16.5, 10.0)
BARREL = (196, 270, 2.0, 1.0)
MAG = [(110, 2), (108, -24), (124, -26), (128, 2)]


def build():
    m = Model("ashes_battle_rifle")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (72, 0, 0)
    wood = fp.wood(TAN, TAN_DK)
    rx0, rx1, rz0, rz1, rw = RECEIVER
    m.cbox(rx0, rx1, rw, rz0, rz1, fp.metal(BLACK), bevel=1.0, edge=0.5)
    m.cbox(rx0 + 4, rx1 - 8, rw - 3, rz1, rz1 + 1.5, fp.metal(mul(BLACK, 0.85)), size=0.5)     # dust cover
    m.box(96, 120, -rw / 2 - 0.5, -rw / 2 + 1.5, 10, 15, None, size=0.25, carve=True)          # ejection port
    m.cyl(100, 106, -2.5, 12.5, 1.2, BRASS, size=0.25, edge=0.25)
    m.part = 'charge'
    m.box(124, 128, rw / 2, rw / 2 + 3, 12, 14, fp.metal(STEEL_HI), size=0.5, edge=0.25)        # charging handle
    m.part = 'body'
    m.part = 'stock'
    m.cprism(STOCK, 9.0, wood, bevel=2.0, edge=0.5)
    m.cbox(-2, 0, 9.5, -15, 15, fp.metal(DARK), size=0.5)                                      # butt plate
    m.part = 'grip'
    m.cprism(GRIP, 8.0, wood, bevel=2.0, edge=0.5)
    m.part = 'handguard'
    hx0, hx1, hz0, hz1, hw = HANDGUARD
    m.cbox(hx0, hx1, hw, hz0, hz1, wood, bevel=2.5, edge=0.5)
    for x in range(int(hx0) + 8, int(hx1) - 6, 6):                                             # vent holes
        for side in ('+y', '-y'):
            m.groove([(x, 9), (x + 2, 9)], side, depth=3, width=4, dark=0.25)
    m.part = 'barrel'
    bx0, bx1, br, bore = BARREL
    fp.barrel(m, hx0, bx1, Z_BORE, br, fp.metal(BLACK), bore=bore)
    m.cyl(bx1 - 12, bx1, 0, Z_BORE, 2.6, fp.metal(DARK), edge=0.25)                             # flash hider
    for x in range(int(bx1) - 10, int(bx1) - 1, 3):
        for side in ('+y', '-y', '+z', '-z'):
            m.groove([(x, Z_BORE - 1) if side in ('+y', '-y') else (x, -1),
                      (x, Z_BORE + 1) if side in ('+y', '-y') else (x, 1)], side, depth=2, dark=0.2)
    m.cyl(hx1, hx1 + 14, 0, Z_BORE + 5, 1.6, fp.metal(BLACK), edge=0.25)                       # gas tube
    m.part = 'sight'
    m.cbox(bx0 + 30, bx0 + 34, 3.0, Z_BORE, Z_BORE + 10, fp.metal(BLACK), size=0.5)          # front sight
    m.cbox(bx0 + 30, bx0 + 34, 1.0, Z_BORE + 6, Z_BORE + 9, None, size=0.25, carve=True)
    m.box(bx0 + 31, bx0 + 33, -0.25, 0.25, Z_BORE + 6, Z_BORE + 9.5, STEEL_HI, size=0.25)
    m.part = 'mag'
    m.cprism(MAG, 7.5, fp.metal(BLACK), bevel=1.0, edge=0.5)
    for z in (-6, -12, -18):
        for side in ('+y', '-y'):
            m.groove([(110, z), (126, z)], side, depth=1, dark=0.5)
    m.part = 'body'
    m.part = 'guard'
    fp.guard(m, 80, 100, -8, rz0, fp.metal(BLACK))
    fp.trigger(m, 88, rz0, fp.metal(STEEL_HI), length=6)
    m.part = 'sight'
    # the box sight: a tall square tube on top, a lens at each end, a red sticker on its left
    m.cbox(96, 116, 10.0, rz1 + 1.5, rz1 + 15, fp.metal(DARK), bevel=1.0, edge=0.5)
    m.cbox(95, 117, 6.0, rz1 + 4, rz1 + 12, None, size=0.5, carve=True)
    m.cyl(98, 99, 0, rz1 + 8, 3.0, (60, 90, 110), size=0.25, edge=0.25)
    m.cyl(113, 114, 0, rz1 + 8, 3.0, (90, 130, 150), size=0.25, edge=0.25)
    m.box(100, 101, -0.25, 0.25, rz1 + 6.5, rz1 + 9.5, (230, 40, 30), size=0.25)
    m.decal(["..###..", ".#####.", "#######", "#.....#", "#######", ".#####.", "..###.."], 102, rz1 + 12, '+y',
            STICKER, dot=2, mode='paint')
    for side in ('+y', '-y'):
        m.screw(64, 10, side, SCREW, kind='slot')
        m.screw(132, 6, side, SCREW, kind='cross')
        m.screw(140, 12, side, SCREW, kind='slot')
        m.screw(20, 4, side, SCREW, kind='rivet')
        m.groove([(rx0 + 2, 6), (rx1 - 2, 6)], side, depth=1, dark=0.5)
    m.wear_edges(0.4, (200, 190, 170))
    m.scratches('+y', (rx0, rx1, rz0, rz1), 14, 81)
    m.crack(30, 6, '+y', 16, 82, heading=0.2)
    m.crack(160, 10, '-y', 12, 83, heading=3.1)
    m.grime(0.2, 84)
    return m
