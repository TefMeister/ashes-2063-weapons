"""The Meshy shotgun in the smudge-cube look, round 1 (2026-11-15, Developer PC). A forge design (meshy_kit.py).

Tefa, with the Meshy model: "it came out with a lot of flaws, but to be honest it looks better than what we did between
ourselves. can you turn it into the blocky look that the latest shotgun looks like, but keep the shape and fill in the
hole in the receiver and have the shell eject on right side only". So: the Meshy gun in cubes at round 12's length;
its receiver (a hollow box with a window right through it and a shell port on both sides) filled solid, except the
right-hand port, which stays open as Meshy made it. One part for now; the moving parts come next.
    python blender-cubekit/forge_make.py <out> <out> meshy_cube_pump.py
"""
import os

from meshy_kit import Meshy, fill_box

GLB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meshy", "ashes_shotgun_meshy_2026-11-15.glb")
NAME = "meshy_cube_pump"
GUN_LENGTH_M = 1.0166            # round 12's length, butt to muzzle
# the receiver, in main cubes, measured off the converted gun (meshy_kit.side_map / section)
REC = (45, 170, -12, 11, -57, -22)   # behind the rear slope to the barrel, wall to wall, the bottom rail to the top
REC_TOP_ROWS = (-9, 8)           # its top two rows are narrower (the rounded top edge)
CLEAN_X1, CLEAN_SHIFT = 125, 60  # new wall takes its colour from a clean bit of side wall behind the port
CLEAN_Z = (-36, -26)
PORT = (128, 166, -38, -23)      # the right-hand shell port (x0, x1, z0, z1), kept open from the right wall ...
PORT_Y_MID = -3                  # ... to just right of the middle (so the left-hand port closes)


def build():
    g = Meshy(GLB, GUN_LENGTH_M)
    m = g.model(NAME)
    x0, x1, y0, y1, z0, z1 = REC

    def wall_col(x, y, z):
        xs = x if x < CLEAN_X1 else x - CLEAN_SHIFT
        return g.col(xs, y1 if y >= 0 else y0, min(CLEAN_Z[1], max(CLEAN_Z[0], z)))

    def port(x, y, z):
        return PORT[0] <= x < PORT[1] and PORT[2] <= z < PORT[3] and y < PORT_Y_MID

    fill_box(m, REC, wall_col, keep_open=port, rows=lambda z: REC_TOP_ROWS if z >= z1 - 2 else (y0, y1))
    return m
