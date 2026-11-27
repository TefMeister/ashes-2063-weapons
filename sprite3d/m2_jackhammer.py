"""The JackHammer (Tefa's Stun Ram, Meshy 2026-11-15; the one gun not remade on 2026-11-27), in the new cube look. A
forge design (m2_kit.py). Measured: the chainsaw-style rear handle x 5-55 (the hand on its top bar, the red throttle
under it), the red body x 60-140, the grey ram shaft x 140-172, the black ram head x 172-250.
- The ram head punches forward on the firing frames and comes back (as the 2026-11-16 Stun Ram); the throttle moves.
"""
from m2_anim import Rig
from m2_kit import cut_scratches, load, set_part

NAME = "m2_jackhammer"
FILE = "Jackhammer"
LENGTH_M = 0.85
HEAD_X = 171.5
TRIGGER = (20, 37, -15, 15, -80, -70.5)  # the red throttle plate under the loop's top barGRIP = (8, 56, -71, -54)

CLASSES = {"ep1": ("Hammer.txt", ["JACKHAMMER"]), "afterglow": ("Hammer.txt", ["JACKHAMMER"])}
RIG = Rig(forward={"chisel": 16}, trigger="trigger", trigger_back=1.5, flashes=[], kick=0.4)


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    set_part(m, lambda x, y, z: x >= HEAD_X, "chisel")
    a0, a1, b0, b1, c0, c1 = TRIGGER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "trigger")
    set_part(m, lambda x, y, z: GRIP[0] <= x < GRIP[1] and GRIP[2] <= z < GRIP[3], "grip")
    cut_scratches(m, 101, 26, parts={"body", "chisel", "grip"})
    return m
