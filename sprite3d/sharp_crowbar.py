"""The crowbar in sharp cubes (2026-11-04, home PC). A forge design: forge_make.py builds it.

Tefa, after the sharp sawn-off: "please carry on with all the rest in this style". Same look (sharp_kit.py), but the
crowbar has no side pickup picture (it is the weapon you start with); it follows the game's in-hand picture
(Graphics/crowbar/PUNGA.png): a red-painted octagonal bar worn to bare steel in patches, a gooseneck hook with a forked
claw at the front, a flattened chisel end at the back, and (ours) black tape wound where the hand holds it.
No moving parts: its swings move the whole crowbar, which in VR is the player's own hand (Tefa, 2026-11-04: "all the
rest has to stay still"). Built straight in main cubes, x forward, z up.
"""
import math

from forge import hash01, mix
from sharp_kit import BRIGHT_METAL, GUNMETAL, SURF, finish, noise, start

NAME = "sharp_crowbar"
RED = [(110, 22, 18), (152, 32, 24), (186, 50, 36)]
TAPE = [(16, 16, 18), (28, 28, 31), (42, 42, 46)]
R = 3.0                     # the bar's half thickness (main cubes)
L = 170.0                   # straight bar, from the chisel end to where the hook starts
HOOK_R = 15.0               # the gooseneck's radius, to the bar's middle
GRIP_X = (22.0, 58.0)       # where the hand holds it, taped


def octagon(dy, dz, r=R):
    return abs(dy) < r and abs(dz) < r and abs(dy) + abs(dz) < r * 1.45


def paint(x, y, z):
    """Red paint, worn to bare steel in patches and on the corners, a little grime."""
    # small patches (a bar this thin turned big patches into rings: a candy cane), only where an edge or a knock
    # would wear it: the noise is read on a finer grid across the bar than along it
    if noise(x, y * 2.5, z * 2.5, 31, 3.0) > 0.74:
        return mix(GUNMETAL[2], BRIGHT_METAL, 0.3 + 0.2 * hash01(int(x * 2), int(y * 2), int(z * 2), 3))
    t = hash01(int(x * 2), int(y * 2), int(z * 2), 5)
    return RED[0] if t < 0.08 else RED[1] if t < 0.92 else RED[2]


def build():
    m = start(NAME)

    # --- the straight bar, the taped grip on it
    m.part = "shaft"
    m.fill(lambda x, y, z: 10.0 <= x < L and octagon(y, z) and not GRIP_X[0] <= x < GRIP_X[1],
           (10, L, -R - 1, R + 1, -R - 1, R + 1), paint, size=1.0, edge=SURF)
    m.part = "grip"

    def tape(x, y, z):
        if int(math.floor((x - GRIP_X[0]) * 2)) % 6 == 0:
            return TAPE[0]                                                  # where each turn overlaps the last
        return TAPE[1 if hash01(int(x * 2), int(y * 2), int(z * 2), 7) < 0.8 else 2]
    m.fill(lambda x, y, z: GRIP_X[0] <= x < GRIP_X[1] and octagon(y, z, R + 0.5),
           (GRIP_X[0], GRIP_X[1], -R - 2, R + 2, -R - 2, R + 2), tape, size=1.0, edge=SURF)

    # --- the chisel end at the back: flattened and widened, bent up a little
    m.part = "chisel"

    def chisel(x, y, z):
        if not (0.0 <= x < 10.0):
            return False
        t = (10.0 - x) / 10.0                                               # 0 at the bar, 1 at the tip
        zc = t * 2.5                                                        # bent up
        return abs(y) < R + t * 1.5 and abs(z - zc) < R * (1.0 - 0.75 * t) + 0.25
    m.fill(chisel, (-1, 11, -R - 3, R + 3, -R - 1, R + 4), paint, size=SURF)
    m.box(-0.5, 2.0, -R - 2, R + 2, 1.5, 3.5, mix(GUNMETAL[2], BRIGHT_METAL, 0.5), size=SURF, keep=False)

    # --- the gooseneck: the bar bends up and back over itself, ending in a forked claw
    m.part = "hook"
    cx, cz = L, HOOK_R
    for d in range(-90, 151, 2):
        a = math.radians(d)
        px_, pz_ = cx + HOOK_R * math.cos(a), cz + HOOK_R * math.sin(a)
        m.fill(lambda x, y, z, px_=px_, pz_=pz_: octagon(y, math.hypot(x - px_, z - pz_)),
               (px_ - R - 1, px_ + R + 1, -R - 1, R + 1, pz_ - R - 1, pz_ + R + 1), paint, size=SURF, keep=True)
    # the claw: the last stretch flattened, with a V cut down its middle
    a = math.radians(150)
    tip = (cx + HOOK_R * math.cos(a), cz + HOOK_R * math.sin(a))
    back = (math.cos(a + math.pi / 2), math.sin(a + math.pi / 2))
    for k in range(10):
        px_, pz_ = tip[0] + back[0] * k * 0.6, tip[1] + back[1] * k * 0.6
        w = R + 0.5 * k / 9
        m.fill(lambda x, y, z, px_=px_, pz_=pz_, w=w: abs(y) < w and math.hypot(x - px_, z - pz_) < R * (1 - k / 14),
               (px_ - R - 1, px_ + R + 1, -w - 1, w + 1, pz_ - R - 1, pz_ + R + 1), paint, size=SURF, keep=True)
    m.fill(lambda x, y, z: abs(y) < 1.0 and math.hypot(x - tip[0] - back[0] * 5, z - tip[1] - back[1] * 5) < 3.5,
           (tip[0] - 8, tip[0] + 8, -1.5, 1.5, tip[1] - 8, tip[1] + 8), None, size=SURF, carve=True)

    finish(m, ["shaft", "hook", "chisel"], [])
    return m
