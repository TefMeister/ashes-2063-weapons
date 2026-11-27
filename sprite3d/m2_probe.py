"""Measure a Meshy gun before designing it (2026-11-27): cross-sections in main cubes, as meshy_kit.section.
    blender -b --factory-startup --python m2_probe.py -- <glb file name> <length m> x:<x>[,<x>...] [z0:z1] [y0:y1]
Each section is printed top down, y from the gun's right (-y) on the left to its left (+y)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "..", "blender-cubekit")]
import meshy_kit  # noqa: E402
from m2_kit import glb  # noqa: E402

a = sys.argv[sys.argv.index("--") + 1:]
g = meshy_kit.Meshy(glb(a[0]), float(a[1]))
print("PROBE bounds lo", tuple(round(v, 1) for v in g.lo), "hi", tuple(round(v, 1) for v in g.hi))
xs = [float(v) for v in a[2].split(":")[1].split(",")]
z0, z1 = (int(v) for v in a[3].split(":")) if len(a) > 3 else (int(g.lo.z) - 1, int(g.hi.z) + 1)
y0, y1 = (int(v) for v in a[4].split(":")) if len(a) > 4 else (int(g.lo.y) - 1, int(g.hi.y) + 2)
for x in xs:
    print("PROBE x=%g  (y %d .. %d)" % (x, y0, y1))
    for z in range(z1, z0, -1):
        print("PROBE  z=%4d %s" % (z, "".join("#" if g.inside(x + .5, y + .5, z + .5) else "." for y in range(y0, y1))))
