"""The Meshy Stun Ram in the smudge-cube look, round 1 (2026-11-15, Developer PC). A forge design (meshy_kit.py).

Tefa, with the Meshy model of their stun ram concept (a chainsaw body with a ram head in front): "that is the next
one". Round 1: the Meshy model in the kit's mixed cubes at a chainsaw's length, one part, to see what needs filling.
    python blender-cubekit/forge_make.py <out> <out> meshy_stun_ram.py
"""
import os

from meshy_kit import Meshy, fill_between

GLB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meshy", "stun_ram_meshy_2026-11-15.glb")
NAME = "meshy_stun_ram"
GUN_LENGTH_M = 0.85              # about a real chainsaw, back handle to the ram's face; Meshy's own is 1.9 m
SLITS = (0, 250, -40, 40, -101, -16)   # the whole thing: slits closed on both sides, up to SLIT_GAP wide, are filled
SLIT_GAP = 3                     # (a recess open to the outside has no wall on that side, so it stays)


def build():
    m = Meshy(GLB, GUN_LENGTH_M).model(NAME)
    for axis in (1, 2):
        fill_between(m, SLITS, axis=axis, max_gap=SLIT_GAP)
    return m
