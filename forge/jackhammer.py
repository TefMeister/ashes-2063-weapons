# Ashes 2063: the JackHammer (pickup JHAMA, in hand hamm*), forge cube version.
# From the pictures: a petrol-engine gun: a red finned engine block at the back under a white-silver shroud with vent
# slots, a yellow two-character label on a black plate, a black tubular roll cage with a taped carry handle over it,
# a fuel cap, and in front a long black six-barrel drum on a frame.
import math

from _common import Model, fp, BLACK, STEEL, STEEL_HI, DARK, SCREW, mul, mix

ENGINE_RED = (160, 46, 32)
ENGINE_DK = (96, 26, 18)
SHROUD = (196, 194, 188)
LABEL = (200, 170, 40)
GRIP_TAPE = (110, 80, 60)
Z_AXIS = 14.0


def tube_path(m, pts, r, col):
    for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
        n = int(max(abs(x1 - x0), abs(z1 - z0)) * 2) + 1
        for i in range(n + 1):
            t = i / n
            m.ball(x0 + (x1 - x0) * t, 0, z0 + (z1 - z0) * t, r, col, ry=r, edge=0.25)


def build():
    m = Model("ashes_jackhammer")
    m.pivot = (40, 0, 0)
    # engine: a red block with cooling fins cut across it
    m.cbox(0, 52, 22.0, -4, 26, fp.metal(ENGINE_RED), bevel=3.0, bevel_x=1.5, edge=0.5)
    for x in range(3, 50, 3):
        for side in ('+y', '-y'):
            m.groove([(x, -2), (x, 18)], side, depth=3, width=2, dark=0.45)
    m.recolour(lambda x, y, z: z < 2, ENGINE_DK)
    # shroud on top: silver, slotted
    m.cbox(4, 48, 18.0, 20, 30, fp.metal(SHROUD), bevel=2.0, edge=0.5)
    for x in range(10, 44, 5):
        for y in (-6, 2):
            m.groove([(x, y), (x + 3, y)], '+z', depth=2, width=4, dark=0.3)
    # the label plate on the left side, with two yellow characters
    m.box(12, 40, 11, 12, 6, 15, fp.metal(DARK), size=0.5)
    glyph = ["#######", "#.....#", "#######", "#.....#", "#######", "..#.#..", "##...##"]
    m.decal(glyph, 16, 14, '+y', LABEL, dot=2, mode='raise')
    m.decal(glyph, 27, 14, '+y', LABEL, dot=2, mode='raise')
    # roll cage: black tubes over and round the engine, a taped carry handle on top
    tube_path(m, [(-2, -2), (-4, 30), (4, 40), (44, 40), (54, 30), (54, 20)], 1.6, fp.metal(BLACK))
    for y in (-11.5, 11.5):
        for i in range(53):
            m.ball(i, y, -3, 1.4, fp.metal(BLACK), edge=0.25)
    m.cyl(10, 38, 0, 40, 2.4, GRIP_TAPE, edge=0.25)
    for x in range(11, 38, 2):
        m.cyl(x, x + 0.5, 0, 40, 2.6, mul(GRIP_TAPE, 0.6), size=0.25, edge=0.25)
    # fuel cap and starter pull
    m.cyl(30, 34, 0, 0, 2.6, fp.metal(DARK), axis='z', edge=0.25)
    m.cyl(-4, 0, 0, 12, 4.0, fp.metal(BLACK), edge=0.25)
    m.cbox(-6, -4, 6.0, 10, 14, fp.metal((150, 30, 26)), size=0.5)
    # the drum frame and six barrels in front
    m.cbox(52, 66, 14.0, 2, 26, fp.metal(BLACK), bevel=2.0, edge=0.5)
    m.part = 'drum'
    for k in range(6):
        a = k * math.pi / 3
        yc, zc = math.cos(a) * 4.5, Z_AXIS + math.sin(a) * 4.5
        m.cyl(66, 150, yc, zc, 1.7, fp.metal(mul(BLACK, 1.2)), edge=0.25)
        m.cyl(146, 151, yc, zc, 0.9, None, edge=0.25, carve=True)
    for x in (80, 112, 144):
        m.cyl(x, x + 3, 0, Z_AXIS, 7.0, fp.metal(BLACK), edge=0.25)
    m.cyl(66, 150, 0, Z_AXIS, 2.0, fp.metal(STEEL), edge=0.25)
    m.part = 'body'
    # grip under the engine with a throttle trigger
    m.cprism([(36, -4), (30, -10), (28, -26), (38, -28), (42, -14), (48, -4)], 8.0, fp.metal(BLACK), bevel=1.5,
             edge=0.5)
    fp.trigger(m, 46, -4, fp.metal((190, 40, 30)), length=8, curve=1.0)
    for side in ('+y', '-y'):
        for x, z in ((6, 2), (46, 2), (6, 18), (46, 18), (56, 6), (62, 22)):
            m.bolt(x, z, side, SCREW)
    m.decal(["#.#.#", "#.#.#", "#####"], 56, 24, '+y', (220, 180, 40), mode='paint')
    m.wear_edges(0.4, (220, 200, 180))
    m.scratches('+y', (0, 52, -2, 24), 14, 111)
    m.crack(20, 4, '-y', 12, 112, heading=0.6)
    m.grime(0.3, 113, col=(40, 30, 20))
    return m
