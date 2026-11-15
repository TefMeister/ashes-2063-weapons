"""The Meshy shotgun in the smudge-cube look (2026-11-15, Developer PC). A forge design (meshy_kit.py).

Round 1, Tefa with the Meshy model: "it came out with a lot of flaws, but to be honest it looks better than what we did
between ourselves. can you turn it into the blocky look that the latest shotgun looks like, but keep the shape and fill
in the hole in the receiver and have the shell eject on right side only". So: the Meshy gun in cubes at round 12's
length; its receiver (a hollow box with a window right through it and a shell port on both sides) filled solid, the
left port closed.

Round 2, Tefa on round 1: "these are actually looking really good. can you now please use different size cubes, that
gave the latest shotgun that you did that not-perfect look, remove the shell from the eject hole and close the guard
please, it needs to open when the pump handle is pulled down". So: the kit's mixed cubes (meshy_kit.Meshy.model); the
right-hand port emptied to a dark pocket (Meshy's shell gone); the shell guard ("bolt", round 12's name for it) a
plate of blocky steel set into the port, two cubes in from the wall, which slides back by the port's length as the pump
comes back (the export job moves both: pump by its stroke, bolt by BOLT_STROKE_M on the same share); the pump its own
part, with the magazine tube's core under it left on the body in the tube's colour.

Round 3, Tefa: "can you make the wooden bits look more wood colour, the look a lot like orange right now, too bright
and need to look like wood ... please be thorough with getting even the smallest specs of orange and change the colour
to this, as best as possible" (with a photo of a brown plank). So on the pump and the grip every orange colour, down to
the faintest fleck, becomes wood grain in the photo's colours (meshy_kit.wood); the metal keeps its rust.
    python blender-cubekit/forge_make.py <out> <out> meshy_cube_pump.py
"""
import math
import os

from forge import mul
from meshy_kit import Meshy, fill_box, set_part, wood
from smudge_kit import blocky_steel

GLB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meshy", "ashes_shotgun_meshy_2026-11-15.glb")
NAME = "meshy_cube_pump"
GUN_LENGTH_M = 1.0166            # round 12's length, butt to muzzle
# the receiver, in main cubes, measured off the converted gun (meshy_kit.side_map / section)
REC = (45, 170, -12, 11, -57, -22)   # behind the rear slope to the barrel, wall to wall, the bottom rail to the top
REC_TOP_ROWS = (-9, 8)           # its top two rows are narrower (the rounded top edge)
CLEAN_X1, CLEAN_SHIFT = 125, 60  # new wall takes its colour from a clean bit of side wall behind the port
CLEAN_Z = (-36, -26)
# the right-hand shell port (x0, x1, z0, z1): emptied from outside the wall to the pocket's back
PORT = (128, 166, -38, -23)
POCKET_BACK_Y = -3               # the pocket's back wall (the gun's right is -y)
POCKET_DARK = 0.35               # the back wall and the pocket's sides darkened, as round 12's port
# the shell guard: a plate in the port, set in from the wall so it slides back inside the receiver's wall
GUARD_Y = (-10, -8)              # two cubes thick
GUARD_BLOCK = 4.0                # main cubes per steel block (smudge_kit.blocky_steel)
# the pump: what sits round the magazine tube from PUMP_X0 to PUMP_X1, below the barrel
TUBE_ZC, TUBE_R = -50.0, 7.6     # the magazine tube's axis (y 0) and radius
PUMP_TOP_Z = -40.0               # above this is the barrel (the pump's own top row is cell -41)
PUMP_X = (187, 267)              # where the gun is wider and deeper than the bare tube (the clamp at 280 is not pump)
TUBE_SAMPLE_X = 180              # the tube's own colour is read from the bare tube here (behind the pump)
GRIP_X1 = 52                     # the wooden grip: everything behind this (into the receiver: only orange changes)


def in_wood(x, y, z):
    return x < GRIP_X1 or (PUMP_X[0] <= x < PUMP_X[1] and z < PUMP_TOP_Z)


def bright_orange(rgb):
    """Meshy's orange itself (its wood paint), not the metal's rust, which is browner and darker."""
    return rgb[0] > 170 and rgb[2] < 90 and rgb[0] - rgb[2] > 110


def tint(x, y, z, rgb):
    """Wood on the pump and grip, every orange tone; anywhere else only Meshy's bright orange specks."""
    return wood(x, y, z, rgb) if in_wood(x, y, z) or bright_orange(rgb) else rgb


def build():
    g = Meshy(GLB, GUN_LENGTH_M)
    g.tint = tint
    m = g.model(NAME)
    x0, x1, y0, y1, z0, z1 = REC

    def wall_col(x, y, z):
        xs = x if x < CLEAN_X1 else x - CLEAN_SHIFT
        return g.col(xs, y1 if y >= 0 else y0, min(CLEAN_Z[1], max(CLEAN_Z[0], z)))

    def in_port(x, y, z):
        return PORT[0] <= x < PORT[1] and PORT[2] <= z < PORT[3]

    # the receiver solid; the right port is left for the pocket below
    fill_box(m, REC, wall_col, keep_open=lambda x, y, z: in_port(x, y, z) and y < POCKET_BACK_Y,
             rows=lambda z: REC_TOP_ROWS if z >= z1 - 2 else (y0, y1))

    # the pocket: everything right of its back wall goes (Meshy's shell with it), the back wall and rim darkened
    m.box(PORT[0], PORT[1], y0 - 2, POCKET_BACK_Y, PORT[2], PORT[3], None, size=1.0, carve=True)
    set_part(m, lambda x, y, z: (PORT[0] - 1 <= x < PORT[1] + 1 and PORT[2] - 1 <= z < PORT[3] + 1
                                 and y < POCKET_BACK_Y + 1),
             "body", recolour=lambda x, y, z: mul(wall_col(x, y, z), POCKET_DARK))

    # the shell guard: blocky steel, filling the port two cubes in from the wall
    m.part = "bolt"
    m.box(PORT[0], PORT[1], GUARD_Y[0], GUARD_Y[1], PORT[2], PORT[3], blocky_steel(GUARD_BLOCK), size=1.0)

    # the pump: every cube outside the tube's radius, below the barrel, where the gun is wider than the tube
    px0, px1 = PUMP_X
    tube_col = {}

    def tube_colour(x, y, z):
        key = (round(y), round(z))
        if key not in tube_col:
            tube_col[key] = g.col(TUBE_SAMPLE_X, y, z)
        return tube_col[key]

    set_part(m, lambda x, y, z: px0 <= x < px1 and z < PUMP_TOP_Z and math.hypot(y, z - TUBE_ZC) >= TUBE_R, "pump")
    set_part(m, lambda x, y, z: px0 <= x < px1 and math.hypot(y, z - TUBE_ZC) < TUBE_R, "body", recolour=tube_colour)
    return m
