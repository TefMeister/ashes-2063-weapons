"""The pipe bomb, Meshy 2026-11-27, in the cube look. A forge design (m2_kit.py). A taped pipe with end caps, a wire
and a detonator box on top; nothing on it moves; held round its middle. All three episodes."""
from m2_anim import Rig
from m2_kit import cut_scratches, load, set_part

NAME = "m2_pipe_bomb"
FILE = "pipe bomb"
LENGTH_M = 0.28
GRIP_X = (28, 56)

CLASSES = {"ep1": ("pipebomb.txt", ["pipebomb"]), "afterglow": ("pipebomb.txt", ["pipebomb"]),
           "hardreset": ("pipebomb.txt", ["pipebomb"])}
RIG = Rig(trigger=None, flashes=[], kick=0.0)


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    set_part(m, lambda x, y, z: GRIP_X[0] <= x < GRIP_X[1], "grip")
    cut_scratches(m, 111, 14, sides=("+y", "-y", "+z", "-z"))
    return m
