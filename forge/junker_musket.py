# Ashes 2063: the Junker Musket (pickup MKTPA, in hand Musket*), forge cube version.
# From the pictures: a long home-made rifle: an orange-brown wooden stock and fore-end bound with brass bands and coils
# of copper wire, a red cloth wrap at the wrist, a steel action with a bolt handle, a fat black scope with white
# markings on top, and a muzzle cap with slots.
import math

from _common import Model, fp, BLACK, STEEL, STEEL_HI, DARK, WOOD, WOOD_DK, BRASS, SCREW, COPPER, RED_SHELL, mul

Z_BORE = 12.0
STOCK = [(0, -12), (0, 12), (8, 14), (40, 12), (70, 9), (70, 2), (44, -2), (24, -6), (8, -14)]
ACTION = (66, 108, 3, 17, 8.0)
FOREEND = [(108, 4), (108, 13), (176, 12.5), (180, 9), (176, 5), (112, 3)]
BARREL = (106, 232, 2.3, 1.2)
SCOPE = (74, 128, 4.3)                 # x0, x1, radius; its axis above the action


def build():
    m = Model("ashes_junker_musket")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (76, 0, 0)
    wood = fp.wood(WOOD, WOOD_DK)
    m.part = 'stock'
    m.cprism(STOCK, 9.0, wood, bevel=2.5, edge=0.5)
    m.cbox(-2, 0.5, 9.5, -13, 13, fp.metal(BLACK), size=0.5)                            # iron butt plate
    m.recolour(lambda x, y, z: 46 < x < 60, lambda x, y, z: mul(RED_SHELL, 0.85 + 0.15 * ((int(x) + int(z)) % 2)))
    for x in (47, 52, 57):                                                             # the wrap's folds
        for side in ('+y', '-y'):
            m.groove([(x, -3), (x + 2, 12)], side, depth=1, dark=0.6)
    m.part = 'body'
    ax0, ax1, az0, az1, aw = ACTION
    m.cbox(ax0, ax1, aw, az0, az1, fp.metal(STEEL), bevel=1.0, edge=0.5)
    m.box(80, 96, -aw / 2 - 0.5, -aw / 2 + 1.5, 10, 15, None, size=0.25, carve=True)  # loading port, right
    m.part = 'bolt'
    m.cyl(-aw / 2 - 6, -aw / 2, 92, 14, 0.9, fp.metal(STEEL_HI), axis='y', edge=0.25)
    m.ball(92, -aw / 2 - 6.5, 14, 1.8, fp.metal(STEEL_HI), edge=0.25)
    m.part = 'body'
    m.part = 'foreend'
    m.cprism(FOREEND, 9.0, wood, bevel=2.0, edge=0.5)
    m.part = 'barrel'
    bx0, bx1, br, bore = BARREL
    fp.barrel(m, bx0, bx1, Z_BORE, br, fp.metal(BLACK), bore=bore)
    m.cyl(bx1 - 10, bx1, 0, Z_BORE, 3.0, fp.metal(STEEL), edge=0.25)                   # slotted muzzle cap
    for x in (bx1 - 8, bx1 - 5):
        for side in ('+y', '-y', '+z'):
            m.groove([(x, Z_BORE - 1) if side != '+z' else (x, -1), (x + 1.5, Z_BORE + 1) if side != '+z' else
                      (x + 1.5, 1)], side, depth=2, width=2, dark=0.2)
    m.part = 'bands'
    # brass bands and copper wire coils holding wood and barrel together
    for x in (114, 150, 172):
        m.cyl(x, x + 3, 0, 8.5, 5.4, fp.metal(BRASS), edge=0.25)
    for x0 in (124, 186):
        for k in range(10):
            m.cyl(x0 + k * 1.0, x0 + k * 1.0 + 0.5, 0, Z_BORE if x0 > 180 else 8.5, 3.1 if x0 > 180 else 5.6,
                  fp.metal(COPPER if k % 2 == 0 else mul(COPPER, 0.7)), size=0.25, edge=0.25)
    m.part = 'guard'
    # trigger guard, a loop, and the trigger
    fp.guard(m, 66, 86, -6, az0, fp.metal(BRASS))
    fp.trigger(m, 75, az0, fp.metal(STEEL_HI), length=6)
    m.part = 'scope'
    # the scope: rings, a fat tube, an eyepiece with a rubber cup, white markings
    sx0, sx1, sr = SCOPE
    zs = az1 + 6
    for x in (82, 112):
        m.cbox(x, x + 3, 5.0, az1, zs, fp.metal(BLACK), size=0.5)
        m.cyl(x - 0.5, x + 3.5, 0, zs, sr + 0.5, fp.metal(BLACK), edge=0.25)
    m.cyl(sx0, sx1, 0, zs, sr - 1.0, fp.metal(BLACK), edge=0.25)
    m.cyl(sx0, sx0 + 10, 0, zs, sr, fp.metal(mul(BLACK, 0.7)), edge=0.25)
    m.cyl(sx1 - 12, sx1, 0, zs, sr + 0.8, fp.metal(BLACK), edge=0.25)
    m.cyl(sx0 - 0.5, sx0 + 1, 0, zs, sr - 1.5, (40, 70, 90), size=0.25, edge=0.25)
    m.cyl(sx1 - 1, sx1 + 0.5, 0, zs, sr - 0.5, (70, 110, 130), size=0.25, edge=0.25)
    m.cyl(-sr - 1.5, sr + 1.5, 97, zs, 1.4, fp.metal(BLACK), axis='y', edge=0.25)        # windage knobs
    m.cyl(zs, zs + sr + 1.5, 97, 0, 1.4, fp.metal(BLACK), axis='z', edge=0.25)
    for side in ('+y', '-y'):
        m.decal(["#.#.#.#", ".......", "#######"], 100, zs + 1.5, side, (220, 220, 210), mode='paint')
        m.screw(70, 8, side, SCREW, kind='slot')
        m.screw(104, 8, side, SCREW, kind='slot')
        m.screw(20, 2, side, (176, 136, 60), kind='rivet')
        m.groove([(ax0 + 2, 6), (ax1 - 2, 6)], side, depth=1, dark=0.5)
    m.wear_edges(0.4, (210, 190, 150))
    m.scratches('+y', (ax0, ax1, az0, az1), 12, 101)
    m.crack(24, 2, '+y', 16, 102, heading=0.3)
    m.crack(140, 9, '-y', 12, 103, heading=3.0)
    m.grime(0.25, 104)
    return m
