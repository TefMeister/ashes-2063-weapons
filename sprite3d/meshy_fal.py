"""The Meshy FAL in the smudge-cube look, round 1 (2026-11-16, Developer PC). A forge design (meshy_kit.py).

Tefa, with the Meshy model: "FAL needs the bullet eject opening on the right side and racking knob, but i'm unsure
which side that goes on to". Meshy made both sides of the receiver alike, with neither. On a real FAL the ejection
port is on the right and the cocking handle on the LEFT, at the front of the receiver (racked with the left hand while
the right stays on the grip). So, at the FAL's length (the side picture FWEPA0 spans 73 of its 88 pixels at
FAL_LENGTH_M):
- the ejection port: cut into the right wall above the front of the magazine, a dark pocket with the bolt (blocky
  steel, its own part "bolt") showing at its back;
- the cocking handle: a stem and knob standing out of the left wall at the receiver's front (its own part
  "charging_handle"), with the slot it runs back along cut into the wall behind it.
Slits closed on both sides filled; the wood keeps Meshy's grain.
    python blender-cubekit/forge_make.py <out> <out> meshy_fal.py
"""
import os

from forge import mul
from meshy_kit import Meshy, fill_between, set_part
from sharp_settings import FAL_LENGTH_M, FAL_PIC_W
from smudge_kit import blocky_steel

GLB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meshy", "fal_meshy_2026-11-15.glb")
NAME = "meshy_fal"
GUN_LENGTH_M = FAL_LENGTH_M * 73 / FAL_PIC_W      # 1.33 m, butt to muzzle
SLIT_GAP = 3
# in main cubes, measured off the converted FAL (side map and sections, 2026-11-16); the gun's right is -y
PORT = (162, 190, -65, -59)      # the ejection port (x0, x1, z0, z1): about a cartridge long, above the magazine front
PORT_Y = (-11, -3)               # cut from outside the right wall (y -9) in to here
POCKET_DARK = 0.35
BOLT_Y = (-4, -2)                # the bolt's side, the pocket's back wall
BOLT_BLOCK = 3.0
HANDLE_X, HANDLE_Z = 206.0, -61.5    # the cocking handle's stem: at the receiver's front, upper half
WALL_LEFT_Y = 8.0                # the receiver's left wall there
STEM_R, STEM_LEN = 1.3, 6.0      # the stem out of the wall
KNOB_R, KNOB_LEN = 2.6, 3.0      # the knob on its end
SLOT_LEN, SLOT_H, SLOT_DEPTH = 30.0, 2.0, 2.0    # the slot the handle runs back along (its stroke)
HANDLE_COL = (52, 54, 58)


def build():
    g = Meshy(GLB, GUN_LENGTH_M)
    m = g.model(NAME)
    box = (int(g.lo.x) - 1, int(g.hi.x) + 2, int(g.lo.y) - 1, int(g.hi.y) + 2, int(g.lo.z) - 1, int(g.hi.z) + 2)
    for axis in (1, 2):
        fill_between(m, box, axis=axis, max_gap=SLIT_GAP)

    # the ejection port on the right: a pocket, its rim and back darkened, the bolt at its back
    x0, x1, z0, z1 = PORT
    m.box(x0, x1, PORT_Y[0], PORT_Y[1], z0, z1, None, size=1.0, carve=True)
    set_part(m, lambda x, y, z: x0 - 1 <= x < x1 + 1 and z0 - 1 <= z < z1 + 1 and y < PORT_Y[1] + 1, "body",
             recolour=lambda x, y, z: mul(g.col(x, y, z), POCKET_DARK))
    m.part = "bolt"
    m.box(x0, x1, BOLT_Y[0], BOLT_Y[1], z0, z1, blocky_steel(BOLT_BLOCK), size=1.0)

    # the cocking handle on the left: the slot behind it first, then the stem and knob
    m.box(HANDLE_X - SLOT_LEN, HANDLE_X + 1.0, WALL_LEFT_Y - SLOT_DEPTH, WALL_LEFT_Y + 2.0,
          HANDLE_Z - SLOT_H / 2, HANDLE_Z + SLOT_H / 2, None, size=0.5, carve=True)
    m.part = "charging_handle"
    y0 = WALL_LEFT_Y - SLOT_DEPTH
    m.cyl(y0, y0 + STEM_LEN + SLOT_DEPTH, HANDLE_X, HANDLE_Z, STEM_R, HANDLE_COL, axis='y', size=0.25, edge=0.25)
    m.cyl(y0 + STEM_LEN + SLOT_DEPTH, y0 + STEM_LEN + SLOT_DEPTH + KNOB_LEN, HANDLE_X, HANDLE_Z, KNOB_R,
          mul(HANDLE_COL, 1.15), axis='y', size=0.25, edge=0.25)
    return m
