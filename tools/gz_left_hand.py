# The free LEFT hand for Ashes 2063 VR, rebuilt the way the weapon hands are (2026-10-19, Tefa: "now knowing how the left
# hand looks, can you try to get the left hand to follow left motion controller with one handed weapons ... don't change
# the side where the thumb is"). No Blender: plain Python.
#   python tools/gz_left_hand.py <out folder>
#
# The hand is the approved fingerless glove (ashes gloves/blender, 2026-09-23) in the Ashes shotgun's approved pistol-grip
# pose (vs_hands.py: R_CURLS, R_THUMB, placed by r_axes on its grip), i.e. exactly the right hand Tefa has worn on the
# guns. That right hand is then mirrored across the controller's left/right into a TRUE left hand, and nothing else:
# no roll, no turn. A left hand holds its controller as the mirror of how the right holds the right one (thumb on top,
# back of the hand facing out), while both controllers share the same axes, so the mirror is the whole change.
# (The mirror that went wrong in September was applied to a hand that was already a left one; this one starts right.)
# Drawn by the lantern's route (FollowOffhand, OffhandAngle/Pitch/Roll; engine/README.md): MD3 x forward, y right, z up,
# 34 units a metre, origin = the middle of the closed hand, where the controller's handle is.
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
GLOVES = os.path.join("D:" + os.sep, "MEGA transfer", "Game Files", "ashes-2063-weapons", "3D blender", "ashes gloves",
                      "blender")
sys.path.insert(0, GLOVES)
from gl_pose import build, place          # noqa: E402
from gl_settings import COL, SHADE, VOXEL_M   # noqa: E402

exec(open(os.path.join(REPO, "kit", "gz_md3.py")).read())
MAX_SURFACE_VERTS = 60000
UNITS_PER_M = 34
NAME = "cube_left_hand"

# the Ashes shotgun's right hand on its grip (vs_hands.py, vs_settings GRIP): front 16 at the top, top -1, rake 0.38,
# half width 5
R_CURLS = {"middle": (45, 55, 60), "ring": (45, 55, 60), "pinky": (40, 50, 50), "index": (10, 35, 30)}
R_THUMB = [(12, 5, 80), (10, -30, 20)]
FRONT, TOP, RAKE, HALF = 16, -1, 0.38, 5
RX0, RY0, RZ0 = FRONT - 27, -(HALF + 1) - 4, TOP - 12

hand = build("right", R_CURLS, R_THUMB)
right = {}
for k in ("hand", "thumb", "tip"):
    right.update(place(hand[k], lambda xh, yh, zh: (yh + RX0, -zh + RY0, -xh + RZ0),
                       shear=lambda x, y, z: (x - round(max(0, TOP - z) * RAKE), y, z)))
left = {(x, -y, z): c for (x, y, z), c in right.items()}          # the mirror: a true left hand
xs, zs = [c[0] for c in left], [c[2] for c in left]
cx, cz = (min(xs) + max(xs) + 1) / 2.0, (min(zs) + max(zs) + 1) / 2.0
print(f"{NAME}: {len(left)} cubes, fist centre x {cx:.1f} z {cz:.1f} (cubes)")

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
        pts = [(((x + a) - cx) * S, -((y + b) - 0.5) * S, ((z + c) - cz) * S) for a, b, c in quad]
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
