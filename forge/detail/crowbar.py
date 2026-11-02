# Ashes 2063: the crow-bar, DETAILED (2026-11-02). A tool, no hands on it: the body rig's hands dock onto the bar.
#
# Game look (in-hand PUNG*, pickup CBARA / CROWA): a long dark bar with old red paint worn off along it and smeared
# with blood, a hooked goose-neck with a split claw at one end, a flat bent chisel at the other.
# Real-life detail (refs/crowbar.md; crowbar and wrecking bar pictures): a true hex bar, a V nail slot in the claw with
# bevelled tips, a flattened, slightly bent and sharpened chisel, forging marks where the bar was hammered out, a
# maker's stamp on one flat.
# Wasteland layer: two grip wraps where the hands go (cloth and black tape), a paracord loop at the chisel end, red
# paint chipped back to steel, blood, rust pits, nicks along the edges.
import math

from _common import Model, fp, wl, STEEL, STEEL_HI, DARK, mul, mix, hash01

BAR_STEEL = (84, 86, 92)
RED_PAINT = (132, 28, 24)
RED_DK = (70, 14, 12)
LENGTH = 200.0
R = 1.9
HOOK_R = 14.0


def bar_paint(x, y, z):
    wear = hash01(int(x // 2), int(z * 2), 7) * 0.6 + (0.6 if x < 30 or x > 175 else 0.0)
    if wear > 0.55:
        return mul(BAR_STEEL, 1.0 + 0.1 * hash01(int(x), int(z), 8))
    return mix(RED_PAINT, RED_DK, hash01(int(x // 3), int(y * 2), int(z * 2), 9))


def hex_in(y, z, r):
    c, s = 0.5, math.sqrt(3) / 2
    return max(abs(z), abs(z * c + y * s), abs(z * c - y * s)) <= r


def build():
    m = Model("ashes_crowbar_detail")
    m.pivot = (60, 0, 0)

    m.part = 'bar'
    m.fill(lambda x, y, z: 0 <= x <= LENGTH and hex_in(y, z, R), (0, LENGTH, -R - 1, R + 1, -R - 1, R + 1), bar_paint,
           0.25)
    m.decal(["###.###.###.###.##.", "#...#.#.#.#.#...#.#", "##..#.#.###.#.#.#.#", "#...#.#.#.#.#.#.#.#",
             "#...###.#.#.###.##."], 140, R - 0.25, '+y', None, mode='carve')            # "FORGED"
    m.part = 'hook'
    cx, cz = LENGTH, HOOK_R
    for i in range(140):
        a = -math.pi / 2 + i * (math.pi * 1.05) / 140
        x, z = cx + math.cos(a) * HOOK_R, cz + math.sin(a) * HOOK_R
        m.ball(x, 0, z, R, fp.metal(BAR_STEEL), size=0.25, edge=0.25)
    m.part = 'claw'
    end = (cx + math.cos(math.pi * 0.55) * HOOK_R, cz + math.sin(math.pi * 0.55) * HOOK_R)
    m.prism([(end[0], end[1] - 2), (end[0] - 12, end[1] - 4), (end[0] - 14, end[1] - 3.0),
             (end[0] - 12, end[1] + 0.5), (end[0], end[1] + 2)], -2.0, 2.0, fp.metal(BAR_STEEL), size=0.25,
            edge=0.25)
    m.prism([(end[0] - 4, end[1] - 0.5), (end[0] - 15, end[1] - 2.0), (end[0] - 15, end[1] + 1.0)], -0.6, 0.6, None,
            size=0.25, carve=True)                                                          # the V nail slot
    m.recolour(lambda x, y, z: x < end[0] - 12.5 and z > end[1] - 5, fp.metal(STEEL_HI))    # bright worn tips
    m.part = 'chisel'
    m.prism([(0, -R), (-14, -4), (-16, -3.25), (-14, -1.75), (0, R)], -2.5, 2.5, fp.metal(BAR_STEEL), size=0.25,
            edge=0.25)
    m.recolour(lambda x, y, z: x < -12.5, fp.metal(STEEL_HI))
    for k in range(6):                                                                    # forging hammer marks
        x = -3 - k * 1.8
        m.paint_line([(x, -2.5), (x - 0.5, -1.0)], '+y', lambda c: mul(c, 0.7))

    m.part = 'grip_wraps'
    wl.cloth(m, 'x', 40.0, 62.0, (39, 63, -3.5, 3.5, -3.5, 3.5), col=wl.CLOTH_KHAKI, seed=1001, part='grip',
             layers=2, tail=(41.0, 0.0, -3.0, 4.0, 1.0))
    wl.tape(m, 'x', 110.0, 124.0, (109, 125, -3.5, 3.5, -3.5, 3.5), col=wl.DUCT_BLACK, seed=1002, part='grip_wraps')
    m.part = 'loop'
    for i in range(48):
        a = i / 48 * math.tau
        m.put(-8.0 + math.cos(a) * 3.0, -0.25, -6.0 + math.sin(a) * 3.0, wl.PARACORD if i % 4 else
              mul(wl.PARACORD, 0.7), 0.25, 'loop')

    for side in ('+y', '-y', '+z'):
        m.crack(100, 0, side, 8, 1003 if side == '+y' else 1004, heading=0.0, dark=0.5)
    m.recolour(lambda x, y, z: hash01(int(x // 1.5), int(z * 2), 1005) * hash01(int(x // 5), 1006) > 0.55
               and 60 < x < 160, lambda x, y, z: mix((70, 10, 8), (40, 6, 5), hash01(int(x), 1007)))   # blood
    for side in ('+y', '-y'):
        wl.chips(m, side, (20, 190, -1.5, 1.5), 14, 1008 if side == '+y' else 1009, under=mul(STEEL, 1.1))
        wl.wear_lines(m, side, (20, 190, -1.5, 1.5), 8, 1010 if side == '+y' else 1011)
    wl.rust(m, (-17, LENGTH + HOOK_R + 3, -4, 4, -6, 2 * HOOK_R + 3), amount=0.2, seed=1012, pits=0.05)
    wl.cavity(m)
    m.wear_edges(0.15, (170, 170, 176))
    m.grime(0.15, 1013)
    wl.simplify(m)
    return m
