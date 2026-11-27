"""The Machine Pistol (an Ingram MAC with its stock out), Meshy 2026-11-27, in the cube look. A forge design.
Measured: receiver x 12-140 z -26..-55; cocking knob on top x 108-115 above z -26; the threaded muzzle x 140-162
(Meshy made it hollow: y -1, z -39.5); the grip x 60-88 z -55..-88, the magazine sticking out under it to z -157 at the
grip's own width.
- The barrel is bored from inside the receiver to the muzzle.
- The cocking knob runs back with the bolt on every shot (an open-bolt gun); the magazine drops out on a reload and
  a fresh one comes up; the trigger moves.
"""
from m2_anim import Rig
from m2_kit import bore, cut_scratches, flashes, load, set_part

NAME = "m2_machine_pistol"
FILE = "Machine pistol"
LENGTH_M = 0.55
OWN = ("INGG",)
BORE = (-1.0, -39.5, 2.0, 118, 161.8)
KNOB = (106, 116, -26.5, -14)            # x0, x1, z0, z1
TRIGGER = (92, 100, -2, 2, -68, -54)
GRIP = (58, 90, -88, -55)
MAG = (69, 89, -160, -88.5)

CLASSES = {"ep1": ("Ingram.txt", ["Ingram"]), "afterglow": ("Ingram.txt", ["Ingram"])}
RIG = Rig(recoil={"bolt": 12}, mags={"mag": 30}, trigger="trigger", trigger_back=1.2, kick=0.5)


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    bore(m, BORE[3], BORE[4], BORE[0], BORE[1], BORE[2])
    set_part(m, lambda x, y, z: KNOB[0] <= x < KNOB[1] and KNOB[2] <= z < KNOB[3], "bolt")
    a0, a1, b0, b1, c0, c1 = TRIGGER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "trigger")
    set_part(m, lambda x, y, z: GRIP[0] <= x < GRIP[1] and GRIP[2] <= z < GRIP[3], "grip")
    set_part(m, lambda x, y, z: MAG[0] <= x < MAG[1] and MAG[2] <= z < MAG[3], "mag")
    cut_scratches(m, 61, 18, parts={"body", "grip", "mag"})
    flashes(m, BORE[4], BORE[1], BORE[0], scale=0.5)
    return m
