"""The Military Rifle (an AR-15 with a carry handle and a vertical foregrip), Afterglow, Meshy 2026-11-27, in the cube
look. A forge design (m2_kit.py). Measured: muzzle at 291 (Meshy hollow there: y -0.5, z -45.5); receiver right wall at
y -6 (x 80-125); magazine x 103-130 below z -60; trigger x 92-97; pistol grip x 60-80.
- The barrel is bored from the receiver to the muzzle.
- The bolt (the right side of the receiver over the port) runs back on every shot; the magazine drops out on a reload
  and a fresh one comes up; the trigger moves.
"""
from m2_anim import Rig
from m2_kit import bore, cut_scratches, flashes, load, set_part

NAME = "m2_military_rifle"
FILE = "military rifle"
LENGTH_M = 0.99
BORE = (-0.5, -45.5, 1.3, 200, 291.2)
BOLT = (93, 121, -20, -3.5, -52, -40)
TRIGGER = (89, 99, -2, 2, -64, -53)
GRIP = (58, 82, -88, -54)
MAG = (100, 133, -115, -60)

CLASSES = {"afterglow": ("Ar15.txt", ["M16"])}
RIG = Rig(recoil={"bolt": 9}, mags={"mag": 36}, trigger="trigger", trigger_back=1.2, kick=1.0)


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    bore(m, BORE[3], BORE[4], BORE[0], BORE[1], BORE[2])
    a0, a1, b0, b1, c0, c1 = BOLT
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "bolt")
    a0, a1, b0, b1, c0, c1 = TRIGGER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "trigger")
    set_part(m, lambda x, y, z: GRIP[0] <= x < GRIP[1] and GRIP[2] <= z < GRIP[3], "grip")
    set_part(m, lambda x, y, z: MAG[0] <= x < MAG[1] and MAG[2] <= z < MAG[3], "mag")
    cut_scratches(m, 121, 28, parts={"body", "grip", "mag"})
    flashes(m, BORE[4], BORE[1], BORE[0], scale=0.8)
    return m
