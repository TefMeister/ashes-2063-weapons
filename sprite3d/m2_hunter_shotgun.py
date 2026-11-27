"""The hunter shotgun (a long side-by-side), Hard Reset, Meshy 2026-11-27, in the cube look. A forge design
(m2_kit.py). Measured: two barrels x 118-323, Meshy made them hollow thin tubes (bores y -7.5 and 6, z -26); the
action ends at x 118, its hinge under the breech (z -38); double triggers x 95-113; the wooden wrist x 55-95.
- Both barrels bored through from the breech to the muzzle.
- A break action: on a reload the barrels and fore-end tip down on the hinge, stay open while the shells go in and
  close again; the triggers move on each shot.
"""
from m2_anim import Rig
from m2_kit import bore, cut_scratches, flashes, load, set_part

NAME = "m2_hunter_shotgun"
FILE = "hunter shotgun"
LENGTH_M = 1.10
BORES = [(-7.5, -26.0), (6.0, -26.0)]
BORE_R, BREECH_X, MUZZLE_X = 4.2, 118.5, 323.5
HINGE = (118.0, 0.0, -38.0)
OPEN_DEG = -35.0
TRIGGER = (94, 114, -2.5, 2.5, -57, -40)
GRIP = (52, 96, -62, -30)

CLASSES = {"hardreset": ("HunterShotgun.txt", ["HunterShotgun"])}
RIG = Rig(open_hinge={"barrels": (OPEN_DEG, HINGE, 0)}, trigger="trigger", trigger_back=1.0, kick=1.3,
          flashes=["flash_a", "flash_b"])


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    for y, z in BORES:
        bore(m, BREECH_X, MUZZLE_X, y, z, BORE_R)
    set_part(m, lambda x, y, z: x >= BREECH_X, "barrels")
    a0, a1, b0, b1, c0, c1 = TRIGGER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "trigger")
    set_part(m, lambda x, y, z: GRIP[0] <= x < GRIP[1] and GRIP[2] <= z < GRIP[3], "grip")
    cut_scratches(m, 161, 30, parts={"body", "barrels", "grip"})
    flashes(m, MUZZLE_X, BORES[0][1], BORES[0][0], scale=0.8, names=("flash_a",))
    flashes(m, MUZZLE_X, BORES[1][1], BORES[1][0], scale=0.8, names=("flash_b",), first=1)
    return m
