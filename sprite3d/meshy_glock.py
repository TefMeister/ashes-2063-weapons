"""The Meshy Glock in the smudge-cube look, round 1 (2026-11-15, Developer PC). A forge design (meshy_kit.py).

Tefa, with the Meshy model: "please do that one next in the same style as the shotgun ... all that needs to be done is
filling the loose gaps and putting the bullet/shell eject on one side only". So: the Meshy Glock in cubes at the 9mm's
length (sharp_settings: the gun spans 26 of the picture's 34 pixels at GLK_LENGTH_M); the slit between slide and frame
and the pinholes closed (fill_between); the ejection port, which Meshy cut across the whole top of the slide, closed on
the left half so the case leaves to the right. One part for now; the slide, trigger and magazine come next.

Round 2, Tefa: "please try to reduce the amount of rust on the bottom half of the weapon, especially on the grip
handle where the plastic covers are on the sides, they should appear just worn and not covered in rust, and give it the
different cube size treatment as well". So: the kit's mixed cubes; below the slide the orange is mostly taken out
(meshy_kit.derust: a rust fleck becomes a lighter grey scuff), on the grip almost all of it.
    python blender-cubekit/forge_make.py <out> <out> meshy_glock.py
"""
import os

from meshy_kit import Meshy, derust, fill_between, fill_box
from sharp_settings import GLK_LENGTH_M, GLK_PIC_W

GLB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meshy", "ashes_glock19_meshy_2026-11-15.glb")
NAME = "meshy_glock"
GUN_LENGTH_M = GLK_LENGTH_M * 26 / GLK_PIC_W        # 0.237 m, back of the grip to the muzzle
# in main cubes, measured off the converted gun (meshy_kit.side_map / section)
SEAM = (24, 60, -6, 5, -30, -28)     # the slit between slide and frame (z -29) and the cells round it
WALLS = (0, 70, -8, 8, -70, -17)     # the whole gun, for pinholes through a wall
PORT = (26, 38, -23, -19)            # the ejection port on top of the slide (x0, x1, z0, z1)
PORT_ROWS = {-23: (-5, 4), -22: (-5, 4), -21: (-5, 4), -20: (-3, 2)}   # the slide's width in each of those rows
PORT_CLEAN_DX = 15                   # closed port takes the colour of the slide top this far in front of it
FRAME_TOP_Z = -29.0                  # below this is the polymer frame (the slide-to-frame line)
GRIP_X1, GRIP_TOP_Z = 27.0, -34.0    # behind and below this is the grip with its side panels
FRAME_DERUST = 0.8                   # share of the orange taken out on the frame ...
GRIP_DERUST = 0.95                   # ... and on the grip


def tint(x, y, z, rgb):
    if z >= FRAME_TOP_Z:
        return rgb                   # the slide keeps its rust
    return derust(rgb, GRIP_DERUST if (x < GRIP_X1 and z < GRIP_TOP_Z) else FRAME_DERUST)


def build():
    g = Meshy(GLB, GUN_LENGTH_M)
    g.tint = tint
    m = g.model(NAME)
    fill_between(m, SEAM, axis=2, max_gap=1)        # slide to frame
    fill_between(m, WALLS, axis=1, max_gap=2)       # pinholes through the gun's thickness
    x0, x1, z0, z1 = PORT
    fill_box(m, (x0, x1, 0, 8, z0, z1), lambda x, y, z: g.col(x + PORT_CLEAN_DX, y, z),
             rows=lambda z: (0, PORT_ROWS[z][1]))   # the left half of the port closed; the right half stays open
    return m
