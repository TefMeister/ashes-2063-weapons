# Ashes 2063: the 9mm Autoloader (pickup GLPPA / GLPSA, in hand Glock*), forge cube version.
# From the pictures: a grey service pistol smeared all over with dried blood, a slide with angled grip serrations, a
# squared trigger guard, a big ejection port, white three-dot sights.
from _common import Model, fp, STEEL, DARK, BRASS, SCREW, mul, mix, hash01

SLIDE_GREY = (138, 136, 132)
FRAME_GREY = (96, 94, 94)
BLOOD = (96, 22, 18)
BLOOD_DK = (58, 14, 12)
DOT = (235, 235, 228)
Z_BORE = 9.0
SLIDE = (0, 58, 4, 15, 8.0)            # x0, x1, z0, z1, width
FRAME = [(2, 4), (52, 4), (52, 1), (40, 0), (22, 0), (14, -4), (6, -4)]
GRIP = [(14, 2), (2, 2), (-6, -20), (-6, -27), (7, -27), (10, -20), (17, -2)]


def blood(m, seed):
    """Dried blood: dark red smears over everything, mottled."""
    def f(x, y, z):
        h = hash01(int(x // 3), int(z // 3), int(y > 0), seed)
        h2 = hash01(int(x // 1.5), int(z // 1.5), seed + 1)
        return h * 0.75 + h2 * 0.35 > 0.86
    m.recolour(f, lambda x, y, z: mix(BLOOD, BLOOD_DK, hash01(int(x), int(z), seed + 2)))


def build():
    m = Model("ashes_handgun")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (6, 0, 0)
    sx0, sx1, sz0, sz1, sw = SLIDE
    m.part = 'slide'
    m.cbox(sx0, sx1, sw, sz0, sz1, fp.metal(SLIDE_GREY), bevel=1.5, bevel_x=0.5, edge=0.5)
    m.cbox(sx1 - 0.5, sx1, 3.0, Z_BORE - 1.5, Z_BORE + 1.5, None, size=0.25, carve=True)
    m.cyl(sx1 - 1, sx1 + 0.5, 0, Z_BORE, 1.0, DARK, size=0.25, edge=0.25)
    # ejection port on the right with the barrel hood showing, brass inside
    m.box(30, 44, -sw / 2 - 0.5, 1.0, 11, sz1 + 0.5, None, size=0.25, carve=True)
    m.box(30, 44, -1.5, 1.5, 10, 13, fp.metal(STEEL), size=0.5)
    m.cyl(33, 38, -1.0, 12.5, 1.1, BRASS, size=0.25, edge=0.25)
    for side in ('+y', '-y'):                                       # angled serrations at the back of the slide
        for i in range(7):
            x = 3 + i * 1.5
            m.groove([(x, sz0 + 2), (x + 2, sz1 - 1.5)], side, depth=2, dark=0.45)
    fp.sight_post(m, sx1 - 4, sz1, 2.0, fp.metal(DARK), w=1.25, dot=DOT)
    fp.rear_sight(m, 2, sz1, 2.0, fp.metal(DARK), w=4.5, notch=1.5, dots=DOT)
    m.part = 'body'
    # frame with an accessory rail, squared guard, trigger
    m.cprism(FRAME, 7.0, fp.metal(FRAME_GREY), bevel=1.0, edge=0.5)
    for x in range(40, 52, 3):
        m.box(x, x + 1, -3.5, 3.5, 1, 2, None, size=0.25, carve=True)

    def guard_in(x, y, z):
        return abs(y) < 1.0 and 18 <= x <= 36 and -8 <= z <= 0 and not (19.5 < x < 34.5 and -6.5 < z)
    m.part = 'guard'
    m.fill(guard_in, (18, 36, -1, 1, -8, 0), fp.metal(FRAME_GREY), 0.5)
    fp.trigger(m, 26, 0, fp.metal(DARK), length=5.0, curve=1.5)
    m.part = 'grip'
    # grip, stippled by hand on both sides
    m.cprism(GRIP, 7.5, fp.metal(FRAME_GREY), bevel=1.5, edge=0.5)
    for side in ('+y', '-y'):
        for i in range(60):
            a = -2 + 10 * hash01(i, 1, 31)
            b = -24 + 20 * hash01(i, 2, 31)
            m.groove([(a + (b + 24) * 0.25, b), (a + (b + 24) * 0.25 + 0.3, b)], side, depth=1, dark=0.7)
        m.screw(20, 2.5, side, SCREW, kind='rivet')
        m.screw(44, 2.5, side, SCREW, kind='rivet')
        m.groove([(0, sz0 + 0.5), (sx1, sz0 + 0.5)], side, depth=1, dark=0.4)                 # slide / frame line
    m.part = 'mag'
    m.cbox(-6, 7, 6.0, -27, -25, fp.metal(DARK), size=0.5)                                     # magazine base
    m.decal(["###.###", "#.#.#.#", "###.###", "..#...#", "###.###"], 46, 13, '+y', mul(SLIDE_GREY, 0.5), mode='carve')
    m.wear_edges(0.5, (186, 184, 180))
    blood(m, 41)
    m.scratches('+y', (0, 56, 4, 15), 10, 42)
    m.scratches('-y', (0, 56, 4, 15), 10, 43)
    m.crack(4, -14, '-y', 8, 44, heading=1.3)
    return m
