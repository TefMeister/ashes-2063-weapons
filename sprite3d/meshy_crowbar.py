"""The Meshy crowbar in the smudge-cube look, round 1 (2026-11-16, Developer PC). A forge design (meshy_kit.py).

Tefa, with the Meshy model and a clean reference picture: "because of the image crowbar angle, meshy kept putting the
slit on both ends in the wrong spot ... that is a crowbar at an angle, not a 2d side view and the slits have to be cut
into the ends, not the ends have like 2 ends". Meshy read the V-slot seen at an angle as two tips one above the other.
A real crowbar end is ONE flat blade with a V-slot cut through it, splitting the tip into two prongs side by side (seen
from the side, one tip). So, at the crowbar's length (sharp_crowbar.py: about 206 cubes, 0.70 m):
- the straight (chisel) end: Meshy's lower prong (splayed down) removed, the gap above it closed into the bar, the
  upper prong (bent up, as in the picture) kept as the blade;
- the hook end: the gap between its two stacked tips closed into one tip;
- both blades get a V-slot from the top, through their whole thickness, widest at the tip.
Axes: x from the chisel end (0) to the hook (206), y across, z up; the hook's tip points back toward -x.
    python blender-cubekit/forge_make.py <out> <out> meshy_crowbar.py
"""
import os

from meshy_kit import Meshy, fill_between

GLB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meshy", "crowbar_meshy_2026-11-15.glb")
NAME = "meshy_crowbar"
GUN_LENGTH_M = 0.70              # the cube crowbar's length (sharp_crowbar.L 176 + the hook: about 206 cubes)
# in main cubes, measured off the converted crowbar (side view, 2026-11-16)
BAR_BOTTOM_Z = -53               # the bar's underside at the chisel end (cells -53 and up are bar)
LOWER_PRONG = (0, 22)            # x where Meshy's lower prong hangs under the bar: removed
CHISEL_GAP = (0, 14, -55, -49)   # the gap between Meshy's two chisel prongs (x0, x1, z0, z1): closed up
HOOK_TIP = (165, 192, -33, -16)  # the hook's tip (x0, x1, z0, z1): its two stacked tips closed into one
GAP = 4                          # how wide a gap between Meshy's doubled tips is closed
# the V-slots: (tip x, which way the blade runs from its tip (+1 along x, -1 back), length, half width at the tip,
# z range); y centre 0
SLOTS = [(0.0, +1, 16.0, 3.0, (-60, -40)),          # the chisel end
         (169.0, +1, 14.0, 2.75, (-33, -16))]        # the hook end: its tip at x 169, the blade running on to +x


def build():
    g = Meshy(GLB, GUN_LENGTH_M)
    m = g.model(NAME)
    lo, hi = g.lo, g.hi
    # the chisel end: the gap between the prongs closed first (it needs the lower prong to close against), then
    # Meshy's lower prong off
    x0, x1, z0, z1 = CHISEL_GAP
    fill_between(m, (x0, x1, int(lo.y) - 1, int(hi.y) + 2, max(z0, BAR_BOTTOM_Z), z1), axis=2, max_gap=GAP)
    m.box(LOWER_PRONG[0] - 2, LOWER_PRONG[1], lo.y - 2, hi.y + 2, lo.z - 2, BAR_BOTTOM_Z, None, size=0.25, carve=True)
    # the hook end: its two tips into one
    x0, x1, z0, z1 = HOOK_TIP
    for axis in (2, 0, 2):
        fill_between(m, (x0, x1, int(lo.y) - 1, int(hi.y) + 2, z0, z1), axis=axis, max_gap=GAP)
    # the V-slots, cut from the top through the blade
    for tip, way, length, half, (za, zb) in SLOTS:
        def slot(x, y, z, tip=tip, way=way, length=length, half=half, za=za, zb=zb):
            t = (x - tip) * way
            return 0 <= t < length and za <= z < zb and abs(y) < half * (1.0 - t / length)
        xa, xb = sorted((tip - 2 * way, tip + way * (length + 1)))
        m.carve(slot, (xa, xb, -half - 1, half + 1, za, zb), size=0.25)
    return m
