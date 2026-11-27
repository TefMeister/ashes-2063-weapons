"""The crowbar, Meshy 2026-11-27, in the cube look. A forge design (m2_kit.py). Meshy laid it on a slant (the straight
shaft falls about 27 degrees from the chisel end to the hook); it is turned level first, so the shaft runs along the
controller. Held near the chisel end, the hook forward (as the earlier Meshy crowbar). Nothing on it moves; in VR the
swing is the player's own, so it has no kick either. All three episodes."""
from m2_anim import Rig
from m2_kit import cut_scratches, load, set_part

NAME = "m2_crowbar"
FILE = "crowbar"
LENGTH_M = 0.75
TILT = -26.6                             # nose up: lifts the hook end so the shaft is level
GRIP_X = (14, 50)

CLASSES = {"ep1": ("Crowbar.txt", ["Crowbar"]), "afterglow": ("Crowbar.txt", ["Crowbar"]),
           "hardreset": ("Crowbar.txt", ["Crowbar"])}
RIG = Rig(trigger=None, flashes=[], kick=0.0)


def build():
    g, m = load(NAME, FILE, LENGTH_M, tilt_deg=TILT)
    set_part(m, lambda x, y, z: GRIP_X[0] <= x < GRIP_X[1], "grip")
    cut_scratches(m, 41, 18, sides=("+y", "-y", "+z", "-z"))
    return m
