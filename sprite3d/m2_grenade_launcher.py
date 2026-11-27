"""The Thumper grenade launcher (an M79-style break-open launcher), Hard Reset, Meshy 2026-11-27, in the cube look. A
forge design (m2_kit.py). Measured: the fat barrel x 103-214.7 (y -0.5, z -62.5, outer radius 6.5) with the ladder sight
on it; the receiver x 85-103; its hinge under the barrel's breech (x 103, z -76); trigger x 95-100; pistol grip x
72-92 below z -78.
- The barrel is bored 40 mm wide, from the breech to the muzzle.
- On a reload the barrel (sight and fore-end with it) tips down on its hinge, stays open while the grenade goes in
  and shuts; the trigger moves on the shot.
"""
from m2_anim import Rig
from m2_kit import bore, cut_scratches, flashes, load, set_part

NAME = "m2_grenade_launcher"
FILE = "grenade launcher"
LENGTH_M = 0.73
BORE = (-0.5, -62.5, 5.0, 103.5, 214.7)
BREECH_X = 103.0
HINGE = (103.0, 0.0, -76.0)
OPEN_DEG = -40.0
TRIGGER = (93, 102, -1.5, 1.5, -86, -75)
GRIP = (70, 94, -108, -78)

CLASSES = {"hardreset": ("Thumper.txt", ["Thumper"])}
RIG = Rig(open_hinge={"barrels": (OPEN_DEG, HINGE, 0)}, trigger="trigger", trigger_back=1.2, kick=1.5,
          flashes=["flash_a", "flash_b"])


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    bore(m, BORE[3], BORE[4], BORE[0], BORE[1], BORE[2])
    set_part(m, lambda x, y, z: x >= BREECH_X, "barrels")
    a0, a1, b0, b1, c0, c1 = TRIGGER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "trigger")
    set_part(m, lambda x, y, z: GRIP[0] <= x < GRIP[1] and GRIP[2] <= z < GRIP[3], "grip")
    cut_scratches(m, 191, 22, parts={"body", "barrels", "grip"})
    flashes(m, BORE[4], BORE[1], BORE[0], scale=0.9, names=("flash_a", "flash_b"))
    return m
