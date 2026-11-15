"""The Meshy heavy machine gun cut into its parts, step 1 of the heavy MQ11 (2026-11-16, Developer PC).

Tefa: "this came out all sorts of wrong, but can you take the MQ11 as a reference for it and build the parts into it
so it looks like a heavy model of the submachine gun, parts like the barrel, body, grip, trigger and guard, sights and
the stock (which is way too short and wide) can hopefully still be usable, then for the silenced MQ11 (ingram) we can
use the same suppressor just change the colour a little". Done together, a step at a time. This step: the Meshy model
turned 10 degrees nose-down (Meshy built it tilted), in cubes, each part its own object, so the parts can be picked
and placed on the MQ11 (meshy_mq11.py) next. Sized for now at 0.74 m overall.
    python blender-cubekit/forge_make.py <out> <out> meshy_heavy_parts.py
"""
import os

from meshy_kit import Meshy, fill_between, set_part

GLB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meshy", "heavy_mg_meshy_2026-11-15.glb")
NAME = "meshy_heavy_parts"
LENGTH_M = 0.74
TILT_DEG = 10.0
# the parts, in main cubes of the straightened model (side map, 2026-11-16): name -> test(x, y, z)
PARTS = [
    ("stock", lambda x, y, z: x < 42 and z < -62 or x < 21),
    ("grip", lambda x, y, z: 64 <= x < 104 and z < -63),
    ("trigger_guard", lambda x, y, z: 104 <= x < 150 and z < -62),
    ("rear_sight", lambda x, y, z: 40 <= x < 52 and z > -33),
    ("front_sight", lambda x, y, z: 108 <= x < 124 and z > -31),
    ("shroud", lambda x, y, z: 124 <= x < 173 and z >= -62),
    ("suppressor", lambda x, y, z: x >= 173),
]


def build():
    g = Meshy(GLB, LENGTH_M, tilt_deg=TILT_DEG)
    m = g.model(NAME, part="receiver")
    box = (int(g.lo.x) - 1, int(g.hi.x) + 2, int(g.lo.y) - 1, int(g.hi.y) + 2, int(g.lo.z) - 1, int(g.hi.z) + 2)
    for axis in (1, 2):
        fill_between(m, box, axis=axis, max_gap=3)
    for name, test in PARTS:
        set_part(m, test, name)
    return m
