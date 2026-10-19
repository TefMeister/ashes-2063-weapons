# Ashes: Hard Reset: the bowling ball (pickup BOBLA, in hand BOWLBL*), forge cube version.
# From the pictures: a glossy dark-blue marbled ball, three finger holes, "300" engraved under them, chips and scuffs.
import math

from _common import Model, fp, mul, mix, hash01

BLUE = (40, 62, 118)
BLUE_LIGHT = (96, 130, 190)
BLUE_DARK = (22, 32, 66)
R = 32.0                               # radius in cubes: a 21.8 cm ball


def marble(x, y, z):
    """Swirled marble: bands of light and dark blue wandering round the ball."""
    w = math.sin((x * 0.11 + math.sin(y * 0.09 + z * 0.05) * 2.2 + z * 0.04) * 2.0)
    n = hash01(int(x // 2), int(y // 2), int(z // 2), 221) * 0.25
    if w > 0.72:
        return mix(BLUE, BLUE_LIGHT, (w - 0.72) * 3.0 + n)
    if w < -0.6:
        return mix(BLUE, BLUE_DARK, (-w - 0.6) * 2.0 + n)
    return mul(BLUE, 0.95 + n * 0.4)


def build():
    m = Model("ashes_bowling_ball")
    m.pivot = (0, 0, 0)
    m.ball(0, 0, 0, R, marble, edge=0.5)
    # the three finger holes on top (thumb further back), each with a darker inside
    for hx, hy, r in ((-10, 0, 3.6), (6, -5, 3.0), (6, 5, 3.0)):
        m.cyl(R - 14, R + 2, hx, hy, r, None, axis='z', edge=0.25, carve=True)
        m.cyl(R - 15, R - 14, hx, hy, r, (8, 10, 18), axis='z', size=0.25, edge=0.25)
    # a bright glint on the gloss
    m.recolour(lambda x, y, z: (x + 14) ** 2 + (y - 12) ** 2 < 30 and z > 0, mix(BLUE_LIGHT, (255, 255, 255), 0.5))
    m.decal(["###.###.###", "..#.#.#.#.#", "###.#.#.#.#", "..#.#.#.#.#", "###.###.###"], 13, 6, '+z', BLUE_DARK,
            dot=2, mode='carve')
    for seed in (231, 232, 233, 234):
        a = hash01(seed, 1) * math.tau
        m.crack(math.cos(a) * 18, math.sin(a) * 18, '+z', 7, seed, dark=0.6)
    for i, side in enumerate(('+y', '-y', '+x')):
        m.scratches(side, (-20, 20, -20, 20), 10, 240 + i, lighten=1.3)
    return m
