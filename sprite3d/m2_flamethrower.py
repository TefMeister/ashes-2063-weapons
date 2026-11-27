"""The Master Blaster flamethrower, Meshy 2026-11-27, in the cube look. A forge design (m2_kit.py).
Measured: the vented nozzle x 225-279 (Meshy made it hollow: y -1.5, z -40.5); two tubes along the top (z -30 and
the fuel tube z -44.5); the copper tank underneath x 95-210; the wooden stock and wrist behind the trigger (x 70-86).
- The nozzle is bored right through, so you look into a dark pipe.
- The flame comes out of the nozzle on the firing frames (the kit's three flashes, a little bigger); the trigger moves.
All three episodes."""
from m2_anim import Rig
from m2_kit import bore, cut_scratches, flashes, load, set_part

NAME = "m2_flamethrower"
FILE = "flamethrower"
LENGTH_M = 0.95
NOZZLE = (-1.5, -40.5, 3.2, 222, 279.4)
TRIGGER = (70, 86, -2, 2, -60, -47)
GRIP = (48, 80, -64, -36)

CLASSES = {"ep1": ("MBlaster.txt", ["NapalmGun"]), "afterglow": ("MBlaster.txt", ["NapalmGun"]),
           "hardreset": ("MBlaster.txt", ["NapalmGun"])}
RIG = Rig(trigger="trigger", trigger_back=1.5, kick=0.3)


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    bore(m, NOZZLE[3], NOZZLE[4], NOZZLE[0], NOZZLE[1], NOZZLE[2])
    a0, a1, b0, b1, c0, c1 = TRIGGER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "trigger")
    set_part(m, lambda x, y, z: GRIP[0] <= x < GRIP[1] and GRIP[2] <= z < GRIP[3], "grip")
    cut_scratches(m, 71, 26, parts={"body", "grip"})
    flashes(m, NOZZLE[4], NOZZLE[1], NOZZLE[0], scale=0.9)
    return m
