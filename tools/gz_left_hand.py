# The free LEFT hand for Ashes 2063 VR. No Blender: plain Python.
#   python tools/gz_left_hand.py <out folder>                      the relaxed hand (Tefa's pick, 2026-10-24)
#   python tools/gz_left_hand.py <out folder> pump [thumb-up]      the shotgun's pump hand, for comparison
#
# ⭐ The game swaps left and right on everything drawn at the off hand: this hand is a world actor (FollowOffhand), not
# a weapon, and a RIGHT hand in the file shows as a LEFT hand in the headset `[verified-live 2026-10-24, n=1]`. Tefa wore
# the pump hand built as a true left hand and saw "still the right hand :D just shaped different" (as with every left
# hand on the controller since September); the same hand mirrored into a right hand: "it's a left hand now! it worked".
# So the file always holds a RIGHT hand.
#
# Relaxed (default): Tefa, 2026-10-24: "make the left hand based on the right hand but with a relaxed hand pose and not
# the finger on the trigger pose". The approved fingerless glove (ashes gloves/blender, 2026-09-23) as a right hand in
# a relaxed pose (RELAXED_CURLS / RELAXED_THUMB: the approved glove's own pose curled a little more, most at the pinky,
# and the thumb closer to the index, as a hand hangs at rest), turned the way the shotgun's right hand
# holds its grip (vs_hands r_axes: fingers forward, thumb on top, back of the hand out) but with no grip and no lean.
# Origin = the middle of the palm, HAND_DOWN_CM above it and HAND_BACK_CM in front of it in the file (see relaxed()).
# Pump: the shotgun's own left hand under the pump with all of Tefa's 2026-09-24 cubes, mirrored into a right hand for
# the swap; `thumb-up` turns it a quarter turn about the pump's line first. Origin = the pump's centre line.
# MD3 axes as the guns (kit/gz_export.py): x forward, y = -gun y, z up; 34 units a metre.
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BLENDER = os.path.join("D:" + os.sep, "MEGA transfer", "Game Files", "ashes-2063-weapons", "3D blender")
sys.path.insert(0, os.path.join(BLENDER, "ashes gloves", "blender"))
sys.path.insert(0, os.path.join(BLENDER, "ashes shotgun", "blender"))
from gl_pose import build as build_hand       # noqa: E402
from gl_settings import COL, SHADE, VOXEL_M, PALM_L   # noqa: E402

exec(open(os.path.join(REPO, "kit", "gz_md3.py")).read())
MAX_SURFACE_VERTS = 60000
UNITS_PER_M = 34
NAME = "cube_left_hand"
PUMP = "pump" in sys.argv[2:]
ROLL_THUMB_UP = "thumb-up" in sys.argv[2:]
# degrees down at each finger's three joints (gl_settings CURL = 14, 26, 16 is the glove's own, nearly straight)
RELAXED_CURLS = {"index": (18, 30, 18), "middle": (22, 36, 22), "ring": (26, 40, 24), "pinky": (30, 44, 26)}
RELAXED_THUMB = [(14, 38, 14), (12, 20, 30)]     # (length, degrees outward, degrees down); gl_settings: 56 out
HAND_DOWN_CM = 3.5                                # Tefa: "sitting ... about 3 - 4 cm too high"
HAND_BACK_CM = 4.0                                # Tefa, 3rd wear: "needs to be pulled back towards the player about 4cm"


def relaxed():
    """A right hand, relaxed, in gun space (x forward, y left, z up), and its origin in cube corners."""
    p = build_hand("right", RELAXED_CURLS, RELAXED_THUMB)
    cells = {}
    for k in ("hand", "thumb", "tip"):
        cells.update(p[k])
    palm = [c for c in cells if 0 <= c[1] < PALM_L]
    o = [(min(c[i] for c in palm) + max(c[i] for c in palm) + 1) / 2.0 for i in range(3)]
    # vs_hands r_axes without its offsets: across the hand -> down, wrist->fingertips -> forward, back of hand -> right
    out = {(yh, -zh - 1, -xh - 1): c for (xh, yh, zh), c in cells.items()}
    ox, oy, oz = o[1], -o[2], -o[0]
    # Tefa wore that (2026-10-24): "the hand is correct, but ... the palm is outwards to the left, not facing the
    # weapon", "about 3 - 4 cm too high". So it is turned half a turn about its own forward line (a turn, so it
    # stays the same hand): the palm faces the weapon and the thumb comes back on top. With the palm out and the
    # fingers forward the thumb must have been underneath, i.e. this actor shows the file's up-down flipped
    # [inferred-static 2026-10-24]; so lowering it in the game means moving it UP in the file.
    out = {(x, -y - 1, -z - 1): c for (x, y, z), c in out.items()}
    # forward/back is not flipped (the fingers point the right way), so pulling it back = moving it back in the file
    return out, (ox + HAND_BACK_CM / 100.0 / VOXEL_M, -oy, -oz - HAND_DOWN_CM / 100.0 / VOXEL_M)


def pump():
    """The shotgun's pump hand mirrored into a right hand, in gun space, and the pump's centre line."""
    from vs_gun import build as build_gun
    from vs_hands import hands
    gun = build_gun()
    on_gun = hands(set().union(*(v for k, v in gun.p.items() if k != "shield")))
    cells = {}
    for part in ("left_hand", "left_thumb"):
        cells.update(on_gun[part])
    pc = gun.p["pump"]
    cy = (min(c[1] for c in pc) + max(c[1] for c in pc) + 1) / 2.0
    cz = (min(c[2] for c in pc) + max(c[2] for c in pc) + 1) / 2.0
    if ROLL_THUMB_UP:              # a quarter turn about x: the gun's left (+y, the thumb) goes up
        cells = {(x, -z - 1, y): c for (x, y, z), c in cells.items()}
        cy, cz = -cz, cy
    cells = {(x, -y - 1, z): c for (x, y, z), c in cells.items()}   # the mirror, for the game's swap
    xs = [c[0] for c in cells]
    return cells, ((min(xs) + max(xs) + 1) / 2.0, -cy, cz)


left, (cx, cy, cz) = pump() if PUMP else relaxed()
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
