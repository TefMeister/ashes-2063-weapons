"""The Solar Lantern, Meshy 2026-11-27, in the cube look (no hand). A forge design (m2_kit.py); it goes into the game
by m2_lantern_world.py, in place of the cube lantern of September (the off-hand lantern actors stay, their models
change). Measured (x 0-28.8, axis x 14.4 y -0.5): a carry bar across the top z -17..-21, the top cap z -30..-45, a
round glass drum z -46..-87 (radius 11) with a glowing tube in it (radius about 3.6), the bottom cap z -88..-99.
0.28 m tall, the old lantern's size after Tefa had it made 25% smaller (2026-11-16).
Parts: body (caps, bar, posts), glass (the drum's outer skin, drawn see-through in the game), core (the tube, which
carries the light). Between the tube and the glass is emptied, so the tube shows through the glass."""
import math

from m2_kit import cut_scratches, load, set_part

NAME = "m2_lantern"
FILE = "Lantern"
LENGTH_M = 0.098                         # its width along x; it stands 0.28 m tall
AXIS = (14.4, -0.5)
GLASS_Z = (-87.0, -46.0)
CORE_R = 3.6
GLASS_IN_R = 9.0                         # the glass skin is what lies outside this
HANDLE_Z = -19.0                         # the middle of the carry bar: where the hand holds it

CLASSES = {}                             # not a weapon: m2_lantern_world.py puts it on the off hand


def r_of(x, y):
    return math.hypot(x - AXIS[0], y - AXIS[1])


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    z0, z1 = GLASS_Z
    m.fill(lambda x, y, z: z0 <= z < z1 and CORE_R + 0.3 <= r_of(x, y) < GLASS_IN_R,
           (AXIS[0] - 12, AXIS[0] + 12, AXIS[1] - 12, AXIS[1] + 12, z0, z1), None, size=0.5, carve=True)
    set_part(m, lambda x, y, z: z0 <= z < z1 and r_of(x, y) < CORE_R + 0.3, "core")
    set_part(m, lambda x, y, z: z0 <= z < z1 and r_of(x, y) >= GLASS_IN_R, "glass")
    cut_scratches(m, 211, 10, sides=("+y", "-y", "+x", "-x"), parts={"body"})
    return m
