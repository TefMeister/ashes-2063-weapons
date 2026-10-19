# Ashes Afterglow (episode 2): the Lazer Gun (pickup LZRGA, in hand LZERP*), forge cube version.
# From the pictures: a sleek, glossy blue-black energy gun: a long rounded top shroud with a raised spine of rivets,
# red light strips along its side (green on the upgraded one), a thin glowing line along the bottom edge, small sight
# ears, a stubby grip and a short emitter at the front.
from _common import Model, fp, STEEL, STEEL_HI, DARK, SCREW, mul

GLOSS = (80, 88, 120)
GLOSS_HI = (150, 160, 204)
GLOW_RED = (236, 44, 40)
GLOW_GREEN = (40, 200, 60)
Z_AXIS = 12.0
SHROUD = [(0, 2), (0, 18), (6, 22), (70, 22), (86, 18), (92, 12), (88, 4), (60, 2)]


def build():
    m = Model("ashes_lazer_gun")
    m.pivot = (18, 0, 0)
    # the shroud: rounded top (prism with a heavy bevel), glossy, a highlight along its crown
    m.cprism(SHROUD, 13.0, fp.metal(GLOSS, 0.04), bevel=4.0, edge=0.25)
    m.recolour(lambda x, y, z: z > 20.5 and abs(y) < 2.5, fp.metal(GLOSS_HI, 0.04))
    m.raised([(8, 0), (70, 0)], '+z', fp.metal(STEEL), height=1, width=2)       # the spine
    for x in range(10, 70, 6):
        m.screw(x, 0.25, '+z', SCREW, kind='rivet')
    # light strips on each side, and the glowing line along the bottom edge
    for side, y in (('+y', 6.5), ('-y', -6.5)):
        for x0, x1 in ((14, 34), (44, 64)):
            m.groove([(x0, 13), (x1, 13)], side, depth=1, width=2, col=GLOW_RED)
        m.groove([(4, 4), (86, 6)], side, depth=1, width=2, col=GLOW_GREEN)
        for x in (36, 52, 68):
            m.groove([(x, 8), (x + 4, 18)], side, depth=1, dark=0.4)             # panel seams
        m.screw(10, 8, side, SCREW, kind='hex')
        m.screw(80, 10, side, SCREW, kind='hex')
    # the emitter: a short barrel with cooling rings and a lens
    m.cyl(90, 108, 0, Z_AXIS, 3.4, fp.metal(DARK), edge=0.25)
    for x in (94, 98, 102):
        m.cyl(x, x + 1.5, 0, Z_AXIS, 4.2, fp.metal(STEEL), edge=0.25)
    m.cyl(107.5, 108.5, 0, Z_AXIS, 2.2, GLOW_RED, size=0.25, edge=0.25)
    # sight ears at the back, a post at the front
    for y in (-4, 2.5):
        m.box(4, 8, y, y + 1.5, 21, 25, fp.metal(DARK), size=0.5)
    m.box(80, 82, -0.75, 0.75, 20, 24, fp.metal(DARK), size=0.5)
    m.box(80.5, 81.5, -0.25, 0.25, 23, 23.75, GLOW_RED, size=0.25)
    # grip and a battery pack in it, trigger
    m.cprism([(26, 3), (18, 3), (12, -18), (22, -20), (28, -8), (34, 2)], 8.0, fp.metal(mul(GLOSS, 0.7)), bevel=2.0,
             edge=0.5)
    m.cbox(12, 24, 8.5, -22, -19, fp.metal(DARK), size=0.5)
    m.box(14, 22, -4.5, -4, -21.5, -19.5, GLOW_GREEN, size=0.25)
    fp.guard(m, 30, 46, -8, 2, fp.metal(mul(GLOSS, 0.8)))
    fp.trigger(m, 38, 2, fp.metal(STEEL_HI), length=6)
    m.wear_edges(0.3, (170, 176, 210))
    m.scratches('+y', (0, 88, 4, 21), 12, 151)
    m.scratches('-y', (0, 88, 4, 21), 10, 152)
    m.crack(24, 16, '+y', 8, 153, heading=0.4)
    return m
