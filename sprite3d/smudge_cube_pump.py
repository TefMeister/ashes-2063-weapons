"""The smudge-cube shotgun (2026-11-07, home PC). A forge design: forge_make.py builds it.

Tefa, 2026-11-07: "i really liked the smudged low res pixelated look from when we tried the 3d sprite look, but it was
too flat ... can you use the smudged look, but a bit less 'smudgy', but give the gun its shape by using cubes, so that
the underlying picture and colours will stay the same, it just gets the 3d pixelated look? ... the normal shotgun, not
the sawn off." And: "please save all the model we create don't overwrite them".

The sister of sprite_cube_pump.py (same outline, parts, thicknesses and round cross-sections from the game's side
pickup picture GRZPA0, 60 x 21, read at run time and never stored here), with three changes:
- Surfaces in HALF cubes (1.7 mm), as Tefa asked on 2026-11-04 ("the cubes are too small ... one measure bigger").
- Less smudge: each cube's colour is part the nearest picture pixel and part the smooth (bicubic) read that made the
  smudge (SMUDGE below; 0 = hard pixels as the sharp guns, 1 = the full smudge of the cube sprite shotgun).
- Only the picture: no added wear, scratches, grime or straps, and a light cube wobble, so the game's own colours stay.
  The barrel is hollow (a round bore), the one carved detail.
"""
import math
import os
import zipfile

import bpy

import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "blender-cubekit")))
import forge  # noqa: E402
from forge import Model, mix  # noqa: E402

GAME_PK3S = (r"C:/NonSteam/Ashes 2063 VR/Resources/Ashes2063Enriched2_23.pk3",
             r"D:/ashes2063vr/Ashes 2063 VR/Resources/Ashes2063Enriched2_23.pk3")
SIDE_SPRITE = "Sprites/Weapons/GRZPA0.png"
NAME = "smudge_cube_pump"
GUN_LENGTH_M = 1.0                     # as the sprite-faced one: the 60-pixel picture spans one metre
CUBE_M = 0.0034                        # cube_size.VOXEL_M: one main cube
Q = 4                                  # quarter cells per main cube (the outline grid)
SURF = 0.5                             # surface cube: the half cube
SOLID_ALPHA = 0.5
COLOUR_FINE = 3                        # colour cells per picture pixel (the sprite-faced gun's grid, about 5.6 mm)
SMUDGE = 0.5                           # 0 = nearest pixel (hard), 1 = full bicubic smudge
CUBE_NOISE = 0.02                      # each cube's brightness wobble (forge default 0.06), kept low: the picture rules
BORE = 0.55                            # the bore's radius, share of the barrel's

# part, which picture pixels belong to it (first match wins), thickness in picture pixels, rounding (0..1 of the
# half-thickness: 1 = fully round cross-section) - as sprite_cube_pump.py
PARTS = [
    ("barrel",   lambda x, y: y <= 6 and x >= 31, 1.8, 1.0),
    ("pump",     lambda x, y: 7 <= y <= 9 and 34 <= x <= 51, 3.4, 0.7),
    ("tube",     lambda x, y: y >= 7 and x >= 30, 2.0, 1.0),
    ("receiver", lambda x, y: x >= 12 and y <= 11 and x < 31, 3.0, 0.45),
    ("guard",    lambda x, y: y >= 12 and x >= 12, 1.0, 0.8),
    ("grip",     lambda x, y: x < 12, 2.6, 0.75),
]


def _cubic(t):
    return (((-t + 2) * t - 1) * t / 2, ((3 * t - 5) * t * t + 2) / 2, ((-3 * t + 4) * t + 1) * t / 2,
            (t - 1) * t * t / 2)


def load_side():
    for pk3 in GAME_PK3S:
        if os.path.exists(pk3):
            data = zipfile.ZipFile(pk3).read(SIDE_SPRITE)
            break
    path = os.path.join(bpy.app.tempdir, "GRZPA0.png")
    open(path, "wb").write(data)
    img = bpy.data.images.load(path)
    W, H = img.size
    px = list(img.pixels)
    bpy.data.images.remove(img)
    # top row first, premultiplied, sRGB bytes as stored
    rows = [[(px[((H - 1 - y) * W + x) * 4 + 0], px[((H - 1 - y) * W + x) * 4 + 1],
              px[((H - 1 - y) * W + x) * 4 + 2], px[((H - 1 - y) * W + x) * 4 + 3]) for x in range(W)]
            for y in range(H)]
    return W, H, rows


def build():
    W, H, rows = load_side()
    S = GUN_LENGTH_M / W / CUBE_M                       # main cubes per picture pixel (4.9)

    def sample(u, v):
        """Smooth (bicubic) colour and alpha of the picture at pixel coordinates (u, v), 0..255 and 0..1."""
        u0, v0 = math.floor(u - 0.5), math.floor(v - 0.5)
        wu, wv = _cubic(u - 0.5 - u0), _cubic(v - 0.5 - v0)
        acc = [0.0] * 4
        for j in range(4):
            yy = min(max(v0 - 1 + j, 0), H - 1)
            for i in range(4):
                xx = min(max(u0 - 1 + i, 0), W - 1)
                r, g, b, a = rows[yy][xx]
                w = wu[i] * wv[j]
                acc[0] += w * r * a
                acc[1] += w * g * a
                acc[2] += w * b * a
                acc[3] += w * a
        a = min(max(acc[3], 0.0), 1.0)
        if acc[3] < 1e-4:
            return (0, 0, 0), 0.0
        return tuple(min(max(c / acc[3], 0.0), 1.0) * 255 for c in acc[:3]), a

    # the outline and parts on a quarter-cube grid in the side view (gx along the gun, gz down from the top)
    GX, GZ = int(W * S * Q) + 1, int(H * S * Q) + 1
    names = [p[0] for p in PARTS]
    label = [[-1] * GX for _ in range(GZ)]
    for gz in range(GZ):
        v = (gz + 0.5) / Q / S
        for gx in range(GX):
            u = (gx + 0.5) / Q / S
            if sample(u, v)[1] > SOLID_ALPHA:
                for n, (_, test, _, _) in enumerate(PARTS):
                    if test(min(int(u), W - 1), min(int(v), H - 1)):
                        label[gz][gx] = n
                        break
    # how far each point is inside its own part's outline (two-pass chamfer, in quarter cubes)
    INF = 1e9
    d = [[INF if label[z][x] >= 0 else 0.0 for x in range(GX)] for z in range(GZ)]
    A, B = 1.0, math.sqrt(2.0)

    def relax(z, x, nz, nx, cost):
        if 0 <= nz < GZ and 0 <= nx < GX:
            other = d[nz][nx] + cost if label[nz][nx] == label[z][x] else cost * 0.5
        else:
            other = cost * 0.5
        if other < d[z][x]:
            d[z][x] = other

    for z in range(GZ):
        for x in range(GX):
            if label[z][x] >= 0:
                for nz, nx, c in ((z - 1, x - 1, B), (z - 1, x, A), (z - 1, x + 1, B), (z, x - 1, A)):
                    relax(z, x, nz, nx, c)
    for z in range(GZ - 1, -1, -1):
        for x in range(GX - 1, -1, -1):
            if label[z][x] >= 0:
                for nz, nx, c in ((z + 1, x + 1, B), (z + 1, x, A), (z + 1, x - 1, B), (z, x + 1, A)):
                    relax(z, x, nz, nx, c)

    half = {n: PARTS[i][2] * S / 2 for i, n in enumerate(names)}          # main cubes
    rnd = {n: max(PARTS[i][3] * half[n], 0.5) for i, n in enumerate(names)}

    def cell(x, z):
        gx, gz = int(math.floor(x * Q)), int(math.floor(-z * Q))
        if 0 <= gx < GX and 0 <= gz < GZ:
            return gz, gx
        return None

    def half_width(gz, gx):
        n = names[label[gz][gx]]
        t = min(d[gz][gx] / Q / rnd[n], 1.0)
        return half[n] * math.sqrt(max(0.0, 1.0 - (1.0 - t) ** 2))

    def colour(x, y, z):
        """The picture's colour on the sprite-faced gun's fine grid: part sharp (the nearest picture pixel), part
        smooth (the bicubic read that gave the smudge), SMUDGE of the way to smooth."""
        u = (math.floor(x / S * COLOUR_FINE) + 0.5) / COLOUR_FINE
        v = (math.floor(-z / S * COLOUR_FINE) + 0.5) / COLOUR_FINE
        smooth, _ = sample(u, v)
        r, g, b, a = rows[min(max(int(v), 0), H - 1)][min(max(int(u), 0), W - 1)]
        if a < SOLID_ALPHA:
            return smooth                                   # the outline's edge: only the smooth read has a colour
        return mix((r * 255, g * 255, b * 255), smooth, SMUDGE)

    # the barrel's bore: per column of the side view, the barrel's centre height and radius (quarter cells)
    bi = names.index("barrel")
    bore = {}
    for gx in range(GX):
        zs = [gz for gz in range(GZ) if label[gz][gx] == bi]
        if len(zs) > 2:
            bore[gx] = ((min(zs) + max(zs) + 1) / 2.0, (max(zs) - min(zs) + 1) / 2.0)

    def in_bore(x, y, z):
        c = cell(x, z)
        if c is None or c[1] not in bore:
            return False
        zc, r = bore[c[1]]
        return math.hypot(y * Q, -z * Q - zc) < r * BORE

    forge.NOISE = CUBE_NOISE
    m = Model(NAME)
    L, Hh = W * S, H * S
    for i, n in enumerate(names):
        m.part = n

        def inside(x, y, z, i=i, n=n):
            c = cell(x, z)
            if c is None or label[c[0]][c[1]] != i or abs(y) >= half_width(*c):
                return False
            return not (n == "barrel" and in_bore(x, y, z))

        m.fill(inside, (0, L, -half[n] - 1, half[n] + 1, -Hh, 0), colour, size=1.0, edge=SURF)
    return m
