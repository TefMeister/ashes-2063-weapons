# Ashes: Hard Reset: the police pistol, an S&W 5906 (pickup 590PA, in hand 5906*), forge cube version.
# From the pictures: a bright stainless slide with fine rear serrations, a rounded trigger guard, a maroon wrap-around
# grip, a bobbed hammer and a slide-mounted safety lever.
from _common import Model, fp, STEEL, STEEL_HI, DARK, BRASS, SCREW, mul

STAINLESS = (176, 178, 182)
STAINLESS_DK = (120, 122, 128)
MAROON = (110, 44, 48)
MAROON_DK = (66, 24, 28)
Z_BORE = 9.0
SLIDE = (0, 60, 4, 15, 7.5)
FRAME = [(4, 4), (56, 4), (56, 1), (36, 0), (20, 0), (12, -4), (6, -4)]
GRIP = [(16, 2), (2, 2), (-6, -20), (-5, -27), (8, -27), (11, -20), (19, -2)]


def build():
    m = Model("ashes_police_pistol")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (6, 0, 0)
    m.part = 'slide'
    sx0, sx1, sz0, sz1, sw = SLIDE
    m.cbox(sx0, sx1, sw, sz0, sz1, fp.metal(STAINLESS, 0.05), bevel=2.0, bevel_x=0.5, edge=0.5)
    m.cyl(sx1 - 1, sx1 + 1, 0, Z_BORE, 1.9, fp.metal(STAINLESS_DK), edge=0.25)
    m.cyl(sx1, sx1 + 1.5, 0, Z_BORE, 1.0, None, edge=0.25, carve=True)
    m.box(32, 46, -sw / 2 - 0.5, 1.0, 11, sz1 + 0.5, None, size=0.25, carve=True)           # ejection port
    m.box(32, 46, -1.5, 1.5, 10, 13, fp.metal(STEEL), size=0.5)
    for side in ('+y', '-y'):
        for i in range(10):
            m.groove([(2 + i, sz0 + 2), (2 + i, sz1 - 2)], side, depth=1, dark=0.45)          # serrations
    for y in (sw / 2, -sw / 2 - 1):                                                             # safety levers
        m.box(5, 11, y, y + 1, 11.5, 13.5, fp.metal(STEEL_HI), size=0.5, edge=0.25)
    fp.sight_post(m, sx1 - 4, sz1, 1.5, fp.metal(DARK), w=1.25, dot=(235, 235, 228))
    fp.rear_sight(m, 2, sz1, 1.5, fp.metal(DARK), w=4.5, notch=1.5, dots=(235, 235, 228))
    m.part = 'body'
    m.cprism(FRAME, 7.0, fp.metal(STAINLESS_DK), bevel=1.0, edge=0.5)
    m.cprism([(-1, 9), (-4, 10), (-4, 13), (0, 13), (2, 10)], 3.0, fp.metal(STAINLESS_DK), size=0.5, edge=0.25)
    m.part = 'guard'
    fp.guard(m, 20, 38, -8, 0, fp.metal(STAINLESS_DK))
    fp.trigger(m, 28, 0, fp.metal(DARK), length=5.5)
    m.part = 'grip'
    m.cprism(GRIP, 8.0, fp.metal(MAROON, 0.08), bevel=2.0, edge=0.5)
    for side in ('+y', '-y'):
        fp.checker(m, (-5, 12, -24, -4), side, MAROON, MAROON_DK)
        m.screw(5, -12, side, SCREW, kind='slot')
        m.groove([(0, sz0 + 0.5), (sx1, sz0 + 0.5)], side, depth=1, dark=0.45)
        m.screw(42, 2.5, side, SCREW, kind='rivet')
    m.part = 'mag'
    m.cbox(-5, 8, 6.5, -28, -26, fp.metal(DARK), size=0.5)
    m.decal(["###.###.###.###", "#...#.#.#.#.#..", "###.###.#.#.###", "..#...#.#.#.#.#", "###.###.###.###"],
            20, 13, '+y', mul(STAINLESS, 0.55), mode='carve')                                  # "5906"
    m.wear_edges(0.35, (230, 230, 232))
    m.scratches('+y', (0, 58, 4, 15), 12, 161)
    m.scratches('-y', (0, 58, 4, 15), 12, 162)
    m.crack(4, -16, '+y', 7, 163, heading=1.2)
    return m
