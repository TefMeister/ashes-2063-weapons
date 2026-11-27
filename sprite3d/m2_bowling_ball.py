"""The bowling ball, Hard Reset, Meshy 2026-11-27, in the cube look. A forge design (m2_kit.py). A real ball's size
(21.8 cm); nothing moves; held from its middle (no grip part: the export takes the whole ball's middle)."""
from m2_anim import Rig
from m2_kit import cut_scratches, load

NAME = "m2_bowling_ball"
FILE = "Bowling ball"
LENGTH_M = 0.218

CLASSES = {"hardreset": ("BowlBall.txt", ["BowlBallWeapon"])}
RIG = Rig(trigger=None, flashes=[], kick=0.0)


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    cut_scratches(m, 201, 10, sides=("+y", "-y", "+z", "-z"))
    return m
