"""The crossbow (a black compound crossbow), Hard Reset, Meshy 2026-11-27, in the cube look. A forge design
(m2_kit.py). Measured: stock x 0-90, trigger x 97-104, the rail on top with the white bolt lying on it (x 108-192,
z -44..-51), the limbs and pulleys x 170-185 reaching y +-78, the foot stirrup in front to x 250.
- The bolt leaves on the shot (gone until the reload) and slides forward onto the rail over a reload; the trigger
  moves. The string is a few cubes thin and stays put.
"""
from m2_anim import Rig
from m2_kit import cut_scratches, load, set_part

NAME = "m2_crossbow"
FILE = "crossbow"
LENGTH_M = 0.85
ARROW = (106, 194, -5, 5, -52, -43)
TRIGGER = (95, 106, -1.5, 1.5, -71, -58)
GRIP = (62, 95, -80, -52)

CLASSES = {"hardreset": ("XBOW.txt", ["Xbow"])}
RIG = Rig(spent={"arrow": (-40.0, 0.0, 0.0)}, trigger="trigger", trigger_back=1.2, flashes=[], kick=0.5)


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    a0, a1, b0, b1, c0, c1 = ARROW
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1
             and sum(g.col(x, y, z)) > 330, "arrow")       # the white bolt only, not the black rail under it
    a0, a1, b0, b1, c0, c1 = TRIGGER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "trigger")
    set_part(m, lambda x, y, z: GRIP[0] <= x < GRIP[1] and GRIP[2] <= z < GRIP[3], "grip")
    cut_scratches(m, 181, 22, parts={"body", "grip"})
    return m
