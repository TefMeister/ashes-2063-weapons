# Ashes: Hard Reset: the Thumper, an M79-style grenade launcher (pickup M79PA, in hand THMP*), forge cube version.
# From the pictures: one fat, short, grey-black barrel that breaks open, a ladder sight on top, a brown wooden
# fore-end under the barrel and a wooden stock with a rubber pad, a steel loop guard.
from _common import Model, fp, BLACK, STEEL, STEEL_HI, DARK, WOOD, WOOD_DK, BRASS, SCREW, mul

GUNMETAL = (82, 84, 96)
WOOD_BR = (122, 78, 44)
Z_BORE = 12.0
STOCK = [(0, -12), (0, 12), (4, 14), (50, 12), (60, 10), (60, 2), (40, -2), (20, -6), (6, -12)]
RECEIVER = [(58, -1), (58, 18), (82, 18), (82, 2), (76, -1)]


def build():
    m = Model("ashes_thumper")
    m.pivot = (64, 0, 0)
    m.cprism(STOCK, 10.0, fp.wood(WOOD_BR, WOOD_DK), bevel=2.5, edge=0.5)
    m.cbox(-3, 0, 10.5, -13, 13, (34, 30, 28), size=0.5)                                    # rubber pad
    m.cprism(RECEIVER, 11.0, fp.metal(GUNMETAL), bevel=1.5, edge=0.5)
    m.part = 'barrel'
    m.cyl(82, 170, 0, Z_BORE, 6.5, fp.metal(GUNMETAL), edge=0.5)
    m.cyl(160, 171, 0, Z_BORE, 7.0, fp.metal(mul(GUNMETAL, 0.8)), edge=0.25)
    m.cyl(164, 172, 0, Z_BORE, 5.0, None, edge=0.25, carve=True)
    m.cyl(163, 164, 0, Z_BORE, 5.0, (30, 30, 32), size=0.25, edge=0.25)
    for x in range(96, 156, 10):                                                           # flats milled along it
        for side in ('+y', '-y'):
            m.groove([(x, Z_BORE - 1), (x + 6, Z_BORE - 1)], side, depth=2, width=8, dark=0.75)
    m.cbox(96, 156, 10.0, 1, 7, fp.wood(WOOD_BR, WOOD_DK), bevel=2.0, edge=0.5)              # fore-end
    m.cbox(150, 154, 3.0, Z_BORE + 6, Z_BORE + 10, fp.metal(BLACK), size=0.5)               # front sight
    m.part = 'body'
    # the ladder sight, folded up
    m.cbox(74, 80, 6.0, 18, 20, fp.metal(BLACK), size=0.5)
    for y in (-2.5, 2.0):
        m.box(76, 78, y, y + 0.5, 20, 30, fp.metal(BLACK), size=0.25)
    for z in range(21, 30, 2):
        m.box(76, 78, -2.5, 2.5, z, z + 0.25, fp.metal(STEEL_HI), size=0.25)
    m.part = 'lever'
    m.box(66, 76, -2, 2, 18, 19.5, fp.metal(STEEL_HI), size=0.5, edge=0.25)                  # top latch
    m.part = 'body'
    fp.guard(m, 60, 80, -9, -1, fp.metal(STEEL))
    fp.trigger(m, 68, -1, fp.metal(DARK), length=6)
    for side in ('+y', '-y'):
        m.screw(62, 8, side, SCREW, kind='slot')
        m.screw(78, 8, side, SCREW, kind='slot')
        m.screw(100, 4, side, SCREW, kind='slot')
        m.screw(150, 4, side, SCREW, kind='slot')
        m.decal(["#...#.###.###", "##.##...#.#.#", "#.#.#..#..###", "#...#.#.....#", "#...#.#...###"], 108,
                Z_BORE + 4, side, (210, 200, 160), mode='paint')
    m.wear_edges(0.45, (200, 200, 210))
    m.scratches('+y', (82, 160, Z_BORE - 5, Z_BORE + 5), 14, 211)
    m.crack(24, 2, '+y', 14, 212, heading=0.3)
    m.grime(0.22, 213)
    return m
