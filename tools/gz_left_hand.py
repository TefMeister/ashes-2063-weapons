# The free LEFT hand for Ashes 2063 VR (2026-10-24, Tefa: "use the hand that is sitting under the pump handle for the
# free floating left hand"). No Blender: plain Python.
#   python tools/gz_left_hand.py <out folder>
#
# The hand is the shotgun's own left hand under the pump (ashes shotgun/blender/vs_hands.py), every cube Tefa placed
# by hand on 2026-09-24 included, taken off the gun as it is. It was built as a left hand, so it needs no mirror.
# Replaces the 2026-10-19 hand (the shotgun's RIGHT hand mirrored; commit 9287b9b), which was never worn.
# On the pump the palm is up, the thumb runs forward along the pump's left side and the wrist drops back, down and
# out, as a forearm does. ROLL_THUMB_UP turns it a quarter turn about the pump's line (a turn, not a mirror, so it
# stays a left hand): thumb on top, back of the hand out, palm facing in, as a left hand holds its controller; but
# then the wrist rises up and out instead of dropping. Both are built for Tefa to wear and choose (2026-10-24):
#   python tools/gz_left_hand.py <out folder> [thumb-up]
# The hollow where the pump was is where the controller's handle is, so the origin is the pump's centre line.
# Drawn by the lantern's route (FollowOffhand, OffhandAngle/Pitch/Roll; engine/README.md): MD3 x forward, y right, z up,
# 34 units a metre.
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BLENDER = os.path.join("D:" + os.sep, "MEGA transfer", "Game Files", "ashes-2063-weapons", "3D blender")
sys.path.insert(0, os.path.join(BLENDER, "ashes gloves", "blender"))
sys.path.insert(0, os.path.join(BLENDER, "ashes shotgun", "blender"))
from gl_settings import COL, SHADE, VOXEL_M   # noqa: E402
from vs_gun import build as build_gun         # noqa: E402
from vs_hands import hands                    # noqa: E402

exec(open(os.path.join(REPO, "kit", "gz_md3.py")).read())
MAX_SURFACE_VERTS = 60000
UNITS_PER_M = 34
NAME = "cube_left_hand"
ROLL_THUMB_UP = len(sys.argv) > 2 and sys.argv[2] == "thumb-up"

gun = build_gun()
on_gun = hands(set().union(*(v for k, v in gun.p.items() if k != "shield")))
left = {}
for part in ("left_hand", "left_thumb"):
    left.update(on_gun[part])
pump = gun.p["pump"]
# the pump's centre line, in cube corners (gun space: x forward, y left, z up)
cy = (min(c[1] for c in pump) + max(c[1] for c in pump) + 1) / 2.0
cz = (min(c[2] for c in pump) + max(c[2] for c in pump) + 1) / 2.0
if ROLL_THUMB_UP:                  # a quarter turn about x: the gun's left (+y, the thumb) goes up
    left = {(x, -z - 1, y): c for (x, y, z), c in left.items()}
    cy, cz = -cz, cy
xs = [c[0] for c in left]
cx = (min(xs) + max(xs) + 1) / 2.0
print(f"{NAME}: {len(left)} cubes, origin x {cx:.1f} y {cy:.1f} z {cz:.1f} (cubes)")

# every exposed cube face, its corners counter-clockwise from outside in gun space (x forward, y left, z up)
FACES = {
    (1, 0, 0): ((1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)),
    (-1, 0, 0): ((0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0)),
    (0, 1, 0): ((0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0)),
    (0, -1, 0): ((0, 0, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1)),
    (0, 0, 1): ((0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)),
    (0, 0, -1): ((0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0)),
}


def shade(rgb, n):
    f = SHADE.get(n, 1.0) if isinstance(SHADE, dict) else 1.0
    return tuple(max(0, min(255, int(round(v * f)))) for v in rgb)


S = VOXEL_M * UNITS_PER_M
tris_out = []                      # ([three (pos, normal)], colour) in MD3 axes
for (x, y, z), name in left.items():
    rgb = COL[name]
    for n, quad in FACES.items():
        if (x + n[0], y + n[1], z + n[2]) in left:
            continue
        key = shade(rgb, n)
        # gun space -> MD3 (x forward, y RIGHT = -gun y, z up): one flip, so the corner order is reversed (as the guns)
        pts = [(((x + a) - cx) * S, -((y + b) - cy) * S, ((z + c) - cz) * S) for a, b, c in quad]
        nm = (n[0], -n[1], n[2])
        for tri in ((pts[0], pts[2], pts[1]), (pts[0], pts[3], pts[2])):
            tris_out.append(([(p, nm) for p in tri], key))

palette = sorted({k for _, k in tris_out})
side = 1
while side * side < len(palette):
    side *= 2
index = {k: i for i, k in enumerate(palette)}
rows = []
for yy in range(side):
    row = bytearray(b"\x00")
    for xx in range(side):
        i = yy * side + xx
        row += bytes(palette[i]) if i < len(palette) else b"\x00\x00\x00"
    rows.append(bytes(row))


def chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


OUT = os.path.abspath(sys.argv[1])
os.makedirs(OUT, exist_ok=True)
png = NAME + ".png"
with open(os.path.join(OUT, png), "wb") as f:
    f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", side, side, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(b"".join(rows), 9)) + chunk(b"IEND", b""))
verts, uvs = [], []
for tri, key in tris_out:
    i = index[key]
    uv = ((i % side + 0.5) / side, 1.0 - (i // side + 0.5) / side)
    for v in tri:
        verts.append(v)
        uvs.append(uv)
tris = [(j, j + 1, j + 2) for j in range(0, len(uvs), 3)]
nsurf, nv, nt = write_md3(os.path.join(OUT, NAME + ".md3"), NAME, [verts], (tris, uvs),
                         f"models/ashes2063/cubehands/{png}")
print(f"{NAME}: {nt} triangles, {nsurf} surfaces, {len(palette)} colours -> {OUT}")
