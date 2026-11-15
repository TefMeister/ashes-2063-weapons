"""The Meshy MQ11 (the machine pistol, stock unfolded) in the smudge-cube look, round 1 (2026-11-16, Developer PC).

Tefa, with the Meshy model: "that one's next please". Meshy gave it a port-shaped recess (one or two cubes deep) on
both sides; on the real gun the ejection port is on the right and the cocking knob on top (Meshy has the knob, in the
right place). So, at a size where the gun without its stock is the game's machine pistol (MPIPA0: 31 of 46 pixels at
ING_LENGTH_M, 0.38 m; with the unfolded stock 0.59 m):
- the right recess deepened into a real port: a dark pocket with the bolt (blocky steel, its own part "bolt") at its
  back;
- the left recess filled flush with the wall, in the wall's colour just behind it;
- slits closed on both sides filled. (Meshy mirrored the left side's lettering; in cubes it is a blur.)
    python blender-cubekit/forge_make.py <out> <out> meshy_mq11.py
"""
import os

from forge import mul
from meshy_kit import Meshy, fill_between, fill_box, set_part
from smudge_kit import blocky_steel

GLB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meshy", "mq11_meshy_2026-11-15.glb")
NAME = "meshy_mq11"
GUN_LENGTH_M = 0.59              # stock end to muzzle; the gun alone (0.637 of it) is the game's 0.38 m machine pistol
SLIT_GAP = 3
# in main cubes, measured off the converted gun (sections at x 92..118, 2026-11-16); the gun's right is -y
RECESS = (95, 118, -36, -27)     # Meshy's port-shaped recess on both sides (x0, x1, z0, z1)
PORT_Y = (-10, -2)               # the right port: cut from outside the wall (y -8) in to here
POCKET_DARK = 0.35
BOLT_Y = (-3, -1)                # the bolt's side at the pocket's back
BOLT_BLOCK = 3.0
LEFT_FILL_Y = (4, 7)             # the left recess (the wall's outside is y +6), filled flush
CLEAN_DX = -20                   # the filling takes the left wall's colour this far behind the recess (plain wall)


def build():
    g = Meshy(GLB, GUN_LENGTH_M)
    m = g.model(NAME)
    box = (int(g.lo.x) - 1, int(g.hi.x) + 2, int(g.lo.y) - 1, int(g.hi.y) + 2, int(g.lo.z) - 1, int(g.hi.z) + 2)
    for axis in (1, 2):
        fill_between(m, box, axis=axis, max_gap=SLIT_GAP)
    x0, x1, z0, z1 = RECESS
    # the left recess filled flush
    def wall(x, y, z):
        """The left wall's own outer cube at that height, further back (reading the texture from inside the wall
        picked up a darker surface)."""
        v = m.at(x0 + CLEAN_DX + 0.5, LEFT_FILL_Y[1] - 0.5, z)
        return tuple(v[0]) if v else g.col(x0 + CLEAN_DX, y, z)
    fill_box(m, (x0, x1, LEFT_FILL_Y[0], LEFT_FILL_Y[1], z0, z1), wall)
    # in cubes the recess is mostly Meshy's dark paint, not depth: its face is repainted in the wall's colour too
    set_part(m, lambda x, y, z: x0 <= x < x1 and z0 <= z < z1 and y >= LEFT_FILL_Y[0] - 2, "body", recolour=wall)
    # the right one a real port: a dark pocket, the bolt at its back
    m.box(x0, x1, PORT_Y[0], PORT_Y[1], z0, z1, None, size=1.0, carve=True)
    set_part(m, lambda x, y, z: x0 - 1 <= x < x1 + 1 and z0 - 1 <= z < z1 + 1 and y < PORT_Y[1] + 1, "body",
             recolour=lambda x, y, z: mul(g.col(x, y, z), POCKET_DARK))
    m.part = "bolt"
    m.box(x0, x1, BOLT_Y[0], BOLT_Y[1], z0, z1, blocky_steel(BOLT_BLOCK), size=1.0)
    return m
