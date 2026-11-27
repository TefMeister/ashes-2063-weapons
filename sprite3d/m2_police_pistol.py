"""The police pistol (Meshy made an S&W 1911-style), Hard Reset, Meshy 2026-11-27, in the cube look. A forge design
(m2_kit.py). Measured: slide x 4-55.9 above z -26.5, 5 cubes wide (y -3..1); the wooden grip x 2-22 below z -27; the
magazine's base x 3-12 at z -54; trigger x 22-27. The plain pistol and its hollow-point twin (the same gun with other
ammunition, PolicePistolHP); the suppressed and upgraded builds are later work.
- The barrel is bored from the chamber to the muzzle.
- The slide goes back on every shot; the magazine drops out on a reload and a fresh one comes up; the trigger moves.
"""
from m2_anim import Rig
from m2_kit import bore, cut_scratches, flashes, load, set_part

NAME = "m2_police_pistol"
FILE = "police handhun"
LENGTH_M = 0.19
BORE = (-1.0, -22.0, 1.2, 28, 55.9)
SLIDE_Z, SLIDE_X0 = -26.5, 4.0
TRIGGER = (21, 28, -2, 1, -34, -26.5)
GRIP = (0, 24, -55, -27)
MAG_COLUMN = (5, 16, -2.5, 0.5, -56, -30)
MAG_PLATE_Z = -52.5

CLASSES = {"hardreset": ("PolicePistol.txt", ["PolicePistol", "PolicePistolHP"])}
RIG = Rig(recoil={"slide": 7}, mags={"mag": 25}, trigger="trigger", trigger_back=1.0, kick=0.6,
          flashes=["flash_a", "flash_b"])


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    bore(m, BORE[3], BORE[4], BORE[0], BORE[1], BORE[2])
    set_part(m, lambda x, y, z: x > SLIDE_X0 and z > SLIDE_Z, "slide")
    a0, a1, b0, b1, c0, c1 = TRIGGER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "trigger")
    set_part(m, lambda x, y, z: GRIP[0] <= x < GRIP[1] and GRIP[2] <= z < GRIP[3], "grip")
    a0, a1, b0, b1, c0, c1 = MAG_COLUMN
    set_part(m, lambda x, y, z: (a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1) or (z < MAG_PLATE_Z and x < 16),
             "mag")
    cut_scratches(m, 141, 10, parts={"body", "slide", "grip"})
    flashes(m, BORE[4], BORE[1], BORE[0], scale=0.4, names=("flash_a", "flash_b"))
    return m
