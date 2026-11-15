"""The Meshy Junker Musket in the smudge-cube look, round 1 (2026-11-16, Developer PC). A forge design (meshy_kit.py).

Tefa, with the Meshy model: "let's focus on how they get converted first, as so far the results have been amazing".
Round 1: the Meshy model in the kit's mixed cubes at the musket's length (the game's side picture MKTPA0 spans 64 of
its 69 pixels at MSK_LENGTH_M), slits closed on both sides filled. Its wood keeps Meshy's colours (it has real grain;
the shotgun's was flat orange paint). One part.
    python blender-cubekit/forge_make.py <out> <out> meshy_musket.py
"""
import os

from meshy_kit import Meshy, fill_between
from sharp_settings import MSK_LENGTH_M, MSK_PIC_W

GLB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meshy", "junker_musket_meshy_2026-11-15.glb")
NAME = "meshy_musket"
GUN_LENGTH_M = MSK_LENGTH_M * 64 / MSK_PIC_W     # 1.39 m, butt to muzzle
SLIT_GAP = 3                     # slits closed on both sides, up to this wide, are filled (meshy_kit.fill_between)
# Meshy made the barrel between the scope's front band and the front band an open shell: the converter only caught
# bits of its wall (streaks). That stretch is filled as the round barrel either side of it is (measured 2026-11-16).
BARREL_X = (236, 320)            # the hollow stretch
BARREL_YC, BARREL_ZC, BARREL_R = -3.5, -60.5, 6.8


def build():
    g = Meshy(GLB, GUN_LENGTH_M)
    m = g.model(NAME)
    box = (int(g.lo.x) - 1, int(g.hi.x) + 2, int(g.lo.y) - 1, int(g.hi.y) + 2, int(g.lo.z) - 1, int(g.hi.z) + 2)
    m.cyl(BARREL_X[0], BARREL_X[1], BARREL_YC, BARREL_ZC, BARREL_R, g.col, size=1.0, edge=0.5, keep=True)
    for axis in (1, 2):
        fill_between(m, box, axis=axis, max_gap=SLIT_GAP)
    return m
