"""The .45 revolver, Meshy 2026-11-27, in the cube look. A forge design (m2_kit.py).
Measured: cylinder x 30-46, y -6..5, z -25..-34 (centre y -0.5 z -29.5, radius 6) under the top strap; Meshy's barrel is
a thin tube (bore y -0.5 z -24.5) from the frame to the muzzle at 88.2; the wooden grip x 0-24 below z -34.
- The bore is cut through the whole barrel (round, quarter cubes).
- On a reload the cylinder swings out to the LEFT on its crane (a hinge along the barrel under the cylinder's left
  side), stays out while the rounds go in, and swings home; the trigger moves on every shot.
"""
from m2_anim import Rig
from m2_kit import bore, cut_scratches, flashes, load, set_part

NAME = "m2_revolver"
FILE = "revolver"
LENGTH_M = 0.30                          # a 6 inch .45 (S&W 625 class)
BORE = (-0.5, -24.5, 1.6, 46.5, 88.2)
CYL = (29.5, 46.5, -35.0, -24.5)         # x0, x1, z0, z1
CRANE = (38.0, 3.0, -35.0)               # the crane's pivot (forge x, y, z): along the barrel, left of and under it
SWING = -75.0                            # degrees on the barrel axis: negative swings the cylinder to the gun's left
TRIGGER = (33, 39, -1.5, 1.5, -48, -39)
GRIP = (0, 24, -72, -34)

CLASSES = {"ep1": ("Revolver.txt", ["revolver"]), "afterglow": ("Revolver.txt", ["revolver"])}
RIG = Rig(open_hinge={"cylinder": (SWING, CRANE, 1)}, trigger="trigger", trigger_back=1.0, kick=0.8,
          flashes=["flash_a", "flash_b"])


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    bore(m, BORE[3], BORE[4], BORE[0], BORE[1], BORE[2])
    x0, x1, z0, z1 = CYL
    set_part(m, lambda x, y, z: x0 <= x < x1 and z0 <= z < z1, "cylinder")
    a0, a1, b0, b1, c0, c1 = TRIGGER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "trigger")
    set_part(m, lambda x, y, z: GRIP[0] <= x < GRIP[1] and GRIP[2] <= z < GRIP[3], "grip")
    cut_scratches(m, 31, 14, parts={"body", "cylinder", "grip"})
    flashes(m, BORE[4], BORE[1], BORE[0], scale=0.5, names=("flash_a", "flash_b"))
    return m
