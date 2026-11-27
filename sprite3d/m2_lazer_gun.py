"""The Lazer Gun (a light-gun style pistol), Afterglow, Meshy 2026-11-27, in the cube look. A forge design (m2_kit.py).
Measured: the box barrel x 0-58.8, z -17..-27 (its middle z -22); the grip x 3-22 below z -27; a small trigger under
the barrel's back at x 19-25.
- A hole bored into the barrel's end, so the muzzle is an open pipe.
- The trigger moves. No fire flash: it shoots a laser, and the game draws its own beam.
"""
from m2_anim import Rig
from m2_kit import bore, cut_scratches, load, set_part

NAME = "m2_lazer_gun"
FILE = "lazer gun"
LENGTH_M = 0.20
BORE = (0.0, -22.0, 1.6, 42, 58.8)
TRIGGER = (18, 26, -1.5, 1.5, -33, -26.5)
GRIP = (2, 24, -49, -27)

CLASSES = {"afterglow": ("LazerGun.txt", ["Lazergun"])}
RIG = Rig(trigger="trigger", trigger_back=1.0, flashes=[], kick=0.3)


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    bore(m, BORE[3], BORE[4], BORE[0], BORE[1], BORE[2])
    a0, a1, b0, b1, c0, c1 = TRIGGER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "trigger")
    set_part(m, lambda x, y, z: GRIP[0] <= x < GRIP[1] and GRIP[2] <= z < GRIP[3], "grip")
    cut_scratches(m, 131, 8, parts={"body", "grip"})
    return m
