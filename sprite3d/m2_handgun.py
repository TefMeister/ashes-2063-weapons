"""The 9mm Autoloader (a Glock), Meshy 2026-11-27, in the cube look. A forge design (m2_kit.py).
Measured: slide x 2.5-54.7 above z -25.3, 7 cubes wide (y -4..2); Meshy's own bore at the muzzle y -0.5 z -21.5;
the grip x 0-18 below z -27, 9 cubes wide.
- The barrel is bored from the chamber to the muzzle.
- The slide goes back on every shot; the magazine (the column inside the grip and its floor plate) drops out on a
  reload and a fresh one comes up; the trigger moves.
"""
from m2_anim import Rig
from m2_kit import bore, cut_scratches, flashes, load, set_part

NAME = "m2_handgun"
FILE = "Handgun"
LENGTH_M = 0.186                         # a Glock 19
OWN = ("GLOK",)                          # the 9mm's own frames (forge_jobs.ASHES_FOREIGN lists them for others)
BORE = (-0.5, -21.5, 1.5, 30, 54.7)      # y, z, radius, from x, to the muzzle
SLIDE_Z, SLIDE_X0 = -25.3, 2.0
TRIGGER = (23, 31, -2, 1, -35, -27)
GRIP = (0, 18, -56, -27)
MAG_COLUMN = (4, 15, -3, 2, -52, -27)
MAG_PLATE_Z, MAG_PLATE_X = -47.5, 17

CLASSES = {"ep1": ("Glock.txt", ["Glock"]), "afterglow": ("Glock.txt", ["Glock"])}
RIG = Rig(recoil={"slide": 7}, mags={"mag": 25}, trigger="trigger", trigger_back=1.0, kick=0.6)


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    bore(m, BORE[3], BORE[4], BORE[0], BORE[1], BORE[2])
    set_part(m, lambda x, y, z: x > SLIDE_X0 and z > SLIDE_Z, "slide")
    a0, a1, b0, b1, c0, c1 = TRIGGER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "trigger")
    set_part(m, lambda x, y, z: GRIP[0] <= x < GRIP[1] and GRIP[2] <= z < GRIP[3], "grip")
    a0, a1, b0, b1, c0, c1 = MAG_COLUMN
    set_part(m, lambda x, y, z: (a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1)
             or (z < MAG_PLATE_Z and x < MAG_PLATE_X), "mag")
    cut_scratches(m, 21, 10, parts={"body", "slide", "grip"})
    flashes(m, BORE[4], BORE[1], BORE[0], scale=0.4)
    return m
