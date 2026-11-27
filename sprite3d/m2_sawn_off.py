"""The sawed-off shotgun, Meshy 2026-11-27, in the cube look. A forge design (m2_kit.py).
Measured: two barrels side by side, x 56-141, bores (Meshy made them hollow near the muzzle) at y -6.5 and 4.5, z -25;
the action ends at x 55; the wooden fore-end under the barrels x 75-125; grip x 0-30 below z -30.
- Both barrels bored right through, round, from the breech to the muzzle.
- A break action: on a reload the barrels and fore-end tip down on a hinge under the breech, stay open while the
  shells go in and close again; the triggers move on each shot.
"""
from m2_anim import Rig
from m2_kit import bore, cut_scratches, flashes, load, set_part

NAME = "m2_sawn_off"
FILE = "sawn off shotgun"
LENGTH_M = 0.48
BORES = [(-6.5, -25.0), (4.5, -25.0)]
BORE_R, BREECH_X, MUZZLE_X = 3.0, 55.5, 141.2
HINGE = (55.0, 0.0, -36.0)
OPEN_DEG = -38.0                         # nose down
TRIGGER = (37, 48, -2.5, 2.5, -46, -37)
GRIP = (0, 32, -66, -30)

CLASSES = {"ep1": ("Sawedoff.txt", ["SawedOff"]), "afterglow": ("Sawedoff.txt", ["SawedOff"])}
RIG = Rig(open_hinge={"barrels": (OPEN_DEG, HINGE, 0)}, trigger="trigger", trigger_back=1.0, kick=1.2,
          flashes=["flash_a", "flash_b"])


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    for y, z in BORES:
        bore(m, BREECH_X, MUZZLE_X, y, z, BORE_R)
    set_part(m, lambda x, y, z: x >= BREECH_X, "barrels")
    a0, a1, b0, b1, c0, c1 = TRIGGER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "trigger")
    set_part(m, lambda x, y, z: GRIP[0] <= x < GRIP[1] and GRIP[2] <= z < GRIP[3], "grip")
    cut_scratches(m, 51, 16, parts={"body", "barrels", "grip"})
    # one flash per barrel: the right barrel's on its own (flash_a), the left's (flash_b)
    flashes(m, MUZZLE_X, BORES[0][1], BORES[0][0], scale=0.65, names=("flash_a",))
    flashes(m, MUZZLE_X, BORES[1][1], BORES[1][0], scale=0.65, names=("flash_b",), first=1)
    return m
