"""The crowbar in sharp cubes (2026-11-04, home PC). A forge design: forge_make.py builds it.

Tefa, after the sharp sawn-off: "please carry on with all the rest in this style". Same look (sharp_kit.py), but the
crowbar has no side pickup picture (it is the weapon you start with); it follows the game's in-hand picture
(Graphics/crowbar/PUNGA.png): a red-painted octagonal bar worn to bare steel in patches, a gooseneck hook with a forked
claw at the front, a flattened chisel end at the back. 2026-11-05, Tefa: "the crowbar needs to look and bend more like
the one from half life series, also the bend needs to bend outwards away from the player": the classic red crowbar's
open J-hook and slightly bent chisel end (our own build of that common shape), the hook curling down, away.
No moving parts: its swings move the whole crowbar, which in VR is the player's own hand (Tefa, 2026-11-04: "all the
rest has to stay still"). Built straight in main cubes, x forward, z up.
"""
import math

from forge import hash01, mix
from sharp_kit import BRIGHT_METAL, GUNMETAL, SURF, finish, noise, start

NAME = "sharp_crowbar"
RED = [(110, 22, 18), (152, 32, 24), (186, 50, 36)]
R = 3.0                     # the bar's half thickness (main cubes)
L = 176.0                   # straight bar, from the chisel end to where the hook starts
HOOK_R = 11.0               # the hook's bend radius, to the bar's middle
HOOK_DEG = 130              # how far it turns
CLAW = 16.0                 # the straight claw after the bend
GRIP_X = (22.0, 58.0)       # where the hand holds it (the paint worn most there)
BEND = -1                   # the hook curls down: away from the player (Tefa, 2026-11-05), not up and back


def octagon(dy, dz, r=R):
    return abs(dy) < r and abs(dz) < r and abs(dy) + abs(dz) < r * 1.45


def paint(x, y, z):
    """Red paint, worn to bare steel in small patches, most where the hand holds it, a little grime."""
    worn = 0.62 if GRIP_X[0] <= x < GRIP_X[1] else 0.74
    if noise(x, y * 2.5, z * 2.5, 31, 3.0) > worn:
        return mix(GUNMETAL[2], BRIGHT_METAL, 0.3 + 0.2 * hash01(int(x * 2), int(y * 2), int(z * 2), 3))
    t = hash01(int(x * 2), int(y * 2), int(z * 2), 5)
    return RED[0] if t < 0.08 else RED[1] if t < 0.92 else RED[2]


def sweep(m, part, path, col, radius):
    """A bar along a list of (x, z, r) points: an octagon `r` thick round each, in half and whole cubes."""
    m.part = part
    for (ax, az, ar), (bx, bz, br) in zip(path, path[1:]):
        n = max(1, int(math.hypot(bx - ax, bz - az) / 0.5))
        for k in range(n + 1):
            t = k / n
            cx, cz, r = ax + (bx - ax) * t, az + (bz - az) * t, ar + (br - ar) * t
            w = radius(cx, cz, r)
            m.fill(lambda x, y, z, cx=cx, cz=cz, r=r, w=w: abs(y) < w and octagon(0.0, math.hypot(x - cx, z - cz), r),
                   (cx - r - 1, cx + r + 1, -w - 1, w + 1, cz - r - 1, cz + r + 1), col, size=SURF, keep=True)


def build():
    m = start(NAME)

    # --- the straight bar; "grip" is the stretch the hand holds (the exporter centres the hand on it)
    m.part = "shaft"
    m.fill(lambda x, y, z: 12.0 <= x < L and octagon(y, z) and not GRIP_X[0] <= x < GRIP_X[1],
           (12, L, -R - 1, R + 1, -R - 1, R + 1), paint, size=1.0, edge=SURF)
    m.part = "grip"
    m.fill(lambda x, y, z: GRIP_X[0] <= x < GRIP_X[1] and octagon(y, z),
           (GRIP_X[0], GRIP_X[1], -R - 1, R + 1, -R - 1, R + 1), paint, size=1.0, edge=SURF)

    # --- the hook: an open bend, then a straight claw that flattens and widens, split down the middle at the tip
    path = []
    for d in range(0, HOOK_DEG + 1, 4):
        a = math.radians(d)
        path.append((L + HOOK_R * math.sin(a), BEND * HOOK_R * (1 - math.cos(a)), R))
    a = math.radians(HOOK_DEG)
    ex, ez = path[-1][0], path[-1][1]
    dx, dz = math.cos(a), BEND * math.sin(a)                              # the direction the bend ends in
    for k in range(1, 9):
        t = k / 8
        path.append((ex + dx * CLAW * t, ez + dz * CLAW * t, R * (1.0 - 0.55 * t)))
    sweep(m, "hook", path, paint, lambda cx, cz, r: R + (R - r) * 0.9)
    tx, tz = ex + dx * CLAW, ez + dz * CLAW
    m.fill(lambda x, y, z: abs(y) < 0.75 and math.hypot(x - (tx - dx * 3), z - (tz - dz * 3)) < 3.5,
           (tx - 8, tx + 8, -1.5, 1.5, tz - 8, tz + 8), None, size=SURF, carve=True)

    # --- the chisel end at the back: bent the other way a little, flattened and widened, its edge worn bright
    cpath = [(12.0 - k * 1.5, -BEND * (k * 1.5) ** 2 * 0.035, R * (1.0 - 0.6 * k / 8)) for k in range(9)]
    sweep(m, "chisel", cpath, paint, lambda cx, cz, r: R + (R - r) * 1.2)

    finish(m, ["shaft", "hook", "chisel", "grip"], [])
    return m
