# Ashes 2063: the crow-bar (pickup CBARA, in hand PUNG*), forge cube version.
# From the pictures: a long hex bar, dark steel with old red paint worn off along the middle and smeared with blood,
# a hooked goose-neck with a split claw at one end and a flat, slightly bent chisel at the other.
import math

from _common import Model, fp, STEEL, STEEL_HI, DARK, mul, mix, hash01

BAR_STEEL = (84, 86, 92)
RED_PAINT = (184, 32, 28)
RED_DK = (92, 16, 14)
LENGTH = 200                           # the straight part, cubes (68 cm)
R = 1.9                                # bar radius
HOOK_R = 14.0                          # radius the goose-neck bends round


def bar_paint(x, y, z):
    """Red paint over most of the bar, worn back to steel towards the ends and in streaks."""
    wear = hash01(int(x // 2), int(z * 2), 7) * 0.45 + (0.6 if x < 30 or x > 175 else 0.0)
    if wear > 0.55:
        return mul(BAR_STEEL, 1.0 + 0.1 * hash01(int(x), int(z), 8))
    return mix(RED_PAINT, RED_DK, hash01(int(x // 3), int(y * 2), int(z * 2), 9))


def build():
    m = Model("ashes_crowbar")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (60, 0, 0)
    # the straight bar, hex-ish: a round bar with two flats
    m.cyl(0, LENGTH, 0, 0, R, bar_paint, edge=0.25)
    m.box(0, LENGTH, -R, R, R - 0.5, R + 0.5, None, size=0.25, carve=True)
    m.box(0, LENGTH, -R, R, -R - 0.5, -R + 0.5, None, size=0.25, carve=True)
    m.part = 'hook'
    # the goose-neck: the bar bends up and back round a circle at the front
    cx, cz = LENGTH, HOOK_R
    for i in range(70):
        a = -math.pi / 2 + i * (math.pi * 1.05) / 70
        x, z = cx + math.cos(a) * HOOK_R, cz + math.sin(a) * HOOK_R
        m.ball(x, 0, z, R, fp.metal(BAR_STEEL), edge=0.25)
    m.part = 'claw'
    # the split claw at the end of the hook, pointing back
    end = (cx + math.cos(math.pi * 0.55) * HOOK_R, cz + math.sin(math.pi * 0.55) * HOOK_R)
    m.prism([(end[0], end[1] - 2), (end[0] - 12, end[1] - 4), (end[0] - 14, end[1] - 2.5),
             (end[0] - 12, end[1] + 0.5), (end[0], end[1] + 2)], -2.0, 2.0, fp.metal(BAR_STEEL), size=0.5, edge=0.25)
    m.box(end[0] - 15, end[0] - 5, -0.5, 0.5, end[1] - 5, end[1] + 2, None, size=0.25, carve=True)   # the split
    m.part = 'chisel'
    # the flat chisel at the back, bent a little down
    m.prism([(0, -R), (-14, -4), (-16, -3), (-14, -1.5), (0, R)], -2.5, 2.5, fp.metal(BAR_STEEL), size=0.5,
            edge=0.25)
    m.recolour(lambda x, y, z: x < -11, fp.metal(STEEL_HI))                   # the sharpened edge, bright
    # blood smears, darker than the paint, and nicks in the bar
    for side in ('+y', '-y', '+z'):
        m.crack(100, 0, side, 10, 61 if side == '+y' else 62, heading=0.0, dark=0.5)
    m.recolour(lambda x, y, z: hash01(int(x // 2), int(z), 63) > 0.8 and 60 < x < 160,
               lambda x, y, z: mix((70, 10, 8), (40, 6, 5), hash01(int(x), 64)))
    m.scratches('+y', (20, 190, -2, 2), 16, 65, length=(3, 10))
    m.scratches('-y', (20, 190, -2, 2), 16, 66, length=(3, 10))
    m.wear_edges(0.35, (170, 170, 176))
    return m
