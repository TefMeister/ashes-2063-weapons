"""The modular rifle (an M4-style carbine), Hard Reset, Meshy 2026-11-27, in the cube look: its first build (ModRifle1);
the other eight builds are later work. A forge design (m2_kit.py). Measured: muzzle at 247 (Meshy hollow there: y -1,
z -41); receiver right wall at y -6 (x 59-123); magazine x 98-122 below z -60; pistol grip x 55-73; trigger x 85-88.
- The barrel is bored from the receiver to the muzzle.
- The bolt (the right side of the receiver over the port) runs back on every shot; the magazine drops out on a reload
  and a fresh one comes up; the trigger moves.
"""
from m2_anim import Rig
from m2_kit import bore, cut_scratches, flashes, load, set_part

NAME = "m2_modular_rifle"
FILE = "modular rifle"
LENGTH_M = 0.84
BORE = (-1.0, -41.0, 1.3, 180, 247.1)
BOLT = (88, 112, -20, -3.5, -52, -38)
TRIGGER = (82, 93, -2, 2, -64, -53)
GRIP = (52, 77, -90, -56)
MAG = (95, 128, -106, -60)

CLASSES = {"hardreset": ("ModRifle.txt", ["ModRifle1"])}
RIG = Rig(recoil={"bolt": 8}, mags={"mag": 34}, trigger="trigger", trigger_back=1.2, kick=1.0)


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    bore(m, BORE[3], BORE[4], BORE[0], BORE[1], BORE[2])
    a0, a1, b0, b1, c0, c1 = BOLT
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "bolt")
    a0, a1, b0, b1, c0, c1 = TRIGGER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "trigger")
    set_part(m, lambda x, y, z: GRIP[0] <= x < GRIP[1] and GRIP[2] <= z < GRIP[3], "grip")
    set_part(m, lambda x, y, z: MAG[0] <= x < MAG[1] and MAG[2] <= z < MAG[3], "mag")
    cut_scratches(m, 171, 24, parts={"body", "grip", "mag"})
    flashes(m, BORE[4], BORE[1], BORE[0], scale=0.7)
    return m
