"""The Battle Rifle (the game's FAL; Meshy made a scoped AR-style rifle), Meshy 2026-11-27, in the cube look. A forge
design (m2_kit.py). Measured: barrel to the muzzle at 294 (Meshy made it hollow at the muzzle: y -0.5, z -56.5); scope
on top x 85-160; receiver x 80-155, its right wall at y -6; magazine x 122-152 below z -70; trigger x 110-117; pistol
grip x 75-108. Episode 1 only (the FAL is not in Afterglow or Hard Reset).
- The barrel is bored from the receiver to the muzzle.
- The bolt (the right side of the receiver over the ejection port) runs back on every shot; the magazine drops out on
  a reload and a fresh one comes up; the trigger moves.
"""
from m2_anim import Rig
from m2_kit import bore, cut_scratches, flashes, load, set_part

NAME = "m2_battle_rifle"
FILE = "Battle Rifle"
LENGTH_M = 1.00
BORE = (-0.5, -56.5, 1.3, 200, 294.1)
BOLT = (120, 142, -20, -3.5, -62, -50)
TRIGGER = (108, 119, -2, 2, -74, -63)
GRIP = (74, 108, -102, -62)
MAG = (120, 156, -125, -70)

CLASSES = {"ep1": ("FAL.txt", ["FAL"])}
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
    cut_scratches(m, 91, 28, parts={"body", "grip", "mag"})
    flashes(m, BORE[4], BORE[1], BORE[0], scale=0.8)
    return m
