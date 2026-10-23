# Ashes: Hard Reset: the lever-action shotgun (pickup GRZPA in Hard Reset, in hand G?IZ*), forge cube version.
# From the pictures: an 1887-style lever gun: bright orange wood fore-end and short stock, a silver-blue receiver
# with a big lever loop under it, a long barrel over a magazine tube, a bead at the muzzle.
from _common import Model, fp, BLACK, STEEL, STEEL_HI, DARK, WOOD_DK, BRASS, SCREW, mul

ORANGE_WOOD = (200, 110, 40)
BLUE_STEEL = (108, 116, 132)
Z_BARREL, Z_TUBE = 12.0, 5.0
RECEIVER = [(40, -3), (40, 15), (46, 17), (88, 17), (90, 14), (90, -3)]
STOCK = [(0, -14), (0, 10), (4, 12), (42, 14), (42, 0), (30, -4), (6, -14)]
FOREEND = (98, 160, 0, 10, 9.0)


def build():
    m = Model("ashes_lever_shotgun")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (60, 0, 0)
    m.cprism(RECEIVER, 9.0, fp.metal(BLUE_STEEL), bevel=1.5, edge=0.5)
    m.box(56, 80, -5, -3, 9, 15, None, size=0.25, carve=True)                               # loading gate
    m.box(56, 80, -3, -2.5, 9, 15, fp.metal(DARK), size=0.5)
    m.part = 'hammer'
    m.cprism([(48, 15), (44, 20), (47, 21), (52, 17)], 2.5, fp.metal(STEEL_HI), size=0.5, edge=0.25)   # hammer
    m.part = 'stock'
    m.cprism(STOCK, 9.0, fp.wood(ORANGE_WOOD, WOOD_DK), bevel=2.5, edge=0.5)
    m.cbox(-2, 0, 9.5, -15, 11, fp.metal(DARK), size=0.5)
    m.part = 'barrel'
    fp.barrel(m, 90, 240, Z_BARREL, 2.6, fp.metal(BLACK), bore=1.6)
    m.part = 'tube'
    m.cyl(90, 226, 0, Z_TUBE, 2.3, fp.metal(BLACK), edge=0.25)
    m.cyl(226, 228, 0, Z_TUBE, 1.8, fp.metal(STEEL), edge=0.25)
    m.cbox(220, 224, 5.0, Z_TUBE - 2, Z_BARREL + 2, fp.metal(BLUE_STEEL), bevel=1.0, edge=0.25)
    m.part = 'sight'
    m.ball(237, 0, Z_BARREL + 3, 0.75, BRASS, edge=0.25)
    m.part = 'foreend'
    ux0, ux1, uz0, uz1, uw = FOREEND
    m.cbox(ux0, ux1, uw, uz0, uz1, fp.wood(ORANGE_WOOD, WOOD_DK), bevel=2.0, bevel_x=1.0, edge=0.5)
    # the lever: a big loop under the receiver
    m.part = 'lever'

    def loop(x, y, z):
        if abs(y) > 1.0:
            return False
        cx, cz = 62, -10
        d = ((x - cx) / 16) ** 2 + ((z - cz) / 8) ** 2
        din = ((x - cx) / 13.5) ** 2 + ((z - cz) / 5.5) ** 2
        return d <= 1.0 and (din > 1.0 or z > -3.5) and z <= -3.0 + 0.01
    m.fill(loop, (46, 78, -1, 1, -18, -3), fp.metal(STEEL_HI), 0.5, 0.25)
    m.part = 'body'
    fp.trigger(m, 58, -3, fp.metal(DARK), length=5)
    for side in ('+y', '-y'):
        for x, z in ((46, 4), (84, 4), (84, 12), (62, 0)):
            m.screw(x, z, side, SCREW, kind='slot')
        m.groove([(42, 8), (88, 8)], side, depth=1, dark=0.5)
        m.decal([".###.", "#...#", "#.#.#", "#...#", ".###."], 64, 14, side, (190, 196, 210), mode='carve')
        for x in range(ux0 + 6, ux1 - 4, 4):
            m.groove([(x, uz0 + 1.5), (x, uz1 - 1.5)], side, depth=1, dark=0.55)
    m.wear_edges(0.45, (220, 224, 232))
    m.scratches('+y', (40, 90, -2, 16), 14, 171)
    m.crack(20, 0, '+y', 14, 172, heading=0.3)
    m.crack(130, 5, '-y', 10, 173, heading=3.1)
    m.grime(0.2, 174)
    return m
