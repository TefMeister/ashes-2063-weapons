"""The sprite-faced shotgun again, in cubes (2026-11-03, home PC). A forge design: forge_make.py builds it.

Tefa, after wearing the sprite-faced shotgun: "this simple style is the best fitting for this game by far, but can you
build now the same sort of a gun out of cubes, the really small ones ... it needs rounder edges as it looks too blocky
now compared to the game ... the simple weapons not over done on detail ... wear and tear on it and brown leather
straps on the handle of the gun".

The same shape as build_sprite_shotgun.py: the outline and colours come from the game's side pickup picture (GRZPA0,
60 x 21), read smoothly (sharp bicubic), so the outline steps in quarter cubes (0.85 mm), not in picture pixels. Each
part keeps its thickness from that file, and its cross-section is rounded: the further a point is inside the part's
outline, the closer it comes to the full thickness (an ellipse), so barrel and tube are round and the receiver,
pump and stock have soft edges. The surface is quarter cubes; the inside stays whole cubes.
Picture pixels are read from the game at run time and never stored here.
"""
import math
import os
import zipfile

import bpy

import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "blender-cubekit")))
from forge import Model, mix, hash01  # noqa: E402

GAME_PK3S = (r"C:/NonSteam/Ashes 2063 VR/Resources/Ashes2063Enriched2_23.pk3",
             r"D:/ashes2063vr/Ashes 2063 VR/Resources/Ashes2063Enriched2_23.pk3")
SIDE_SPRITE = "Sprites/Weapons/GRZPA0.png"
NAME = "sprite_cube_pump"
GUN_LENGTH_M = 1.0                     # as the sprite-faced one: the 60-pixel picture spans one metre
CUBE_M = 0.0034                        # cube_size.VOXEL_M: one main cube
Q = 4                                  # quarter cubes per main cube
SOLID_ALPHA = 0.5
# Colours are read once per cell of the sprite-faced shotgun's finer grid (3 per picture pixel, about 5.6 mm), so the
# cubes show the same fine pixels Tefa liked on it, not a smear (the first cube build read them per cube: blurry).
COLOUR_FINE = 3

# part, which picture pixels belong to it (first match wins), thickness in picture pixels, rounding (0..1 of the
# half-thickness: 1 = fully round cross-section) - the parts and thicknesses of build_sprite_shotgun.py
PARTS = [
    ("barrel",   lambda x, y: y <= 6 and x >= 31, 1.8, 1.0),
    ("pump",     lambda x, y: 7 <= y <= 9 and 34 <= x <= 51, 3.4, 0.7),
    ("tube",     lambda x, y: y >= 7 and x >= 30, 2.0, 1.0),
    ("receiver", lambda x, y: x >= 12 and y <= 11 and x < 31, 3.0, 0.45),
    ("guard",    lambda x, y: y >= 12 and x >= 12, 1.0, 0.8),
    ("grip",     lambda x, y: x < 12, 2.6, 0.75),
]

LEATHER = (96, 58, 32)
LEATHER_DK = (58, 34, 18)
STITCH = (156, 128, 88)
STRAPS = 3                             # leather straps round the stock's wrist
STRAP_W = 3.0                          # main cubes wide
STRAP_GAP = 3.5                        # main cubes between straps
STRAP_SLANT = 0.35                     # how much each strap leans (x per z)
STRAP_RAISE = 0.75                     # main cubes it stands proud of the wood
WEAR = 0.35
SCRATCHES = 16
GRIME = 0.18


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
        u = (math.floor(x / S * COLOUR_FINE) + 0.5) / COLOUR_FINE
        v = (math.floor(-z / S * COLOUR_FINE) + 0.5) / COLOUR_FINE
        c, _ = sample(u, v)
        return c

    m = Model(NAME)
    L, Hh = W * S, H * S
    for i, n in enumerate(names):
        m.part = n

        def inside(x, y, z, i=i):
            c = cell(x, z)
            return c is not None and label[c[0]][c[1]] == i and abs(y) < half_width(*c)

        m.fill(inside, (0, L, -half[n] - 1, half[n] + 1, -Hh, 0), colour, size=1.0, edge=0.25)

    # leather straps round the stock's wrist: where the grip is narrowest, top to bottom
    grip = names.index("grip")
    heights = []
    for gx in range(GX):
        zs = [gz for gz in range(GZ) if label[gz][gx] == grip]
        if len(zs) > 4:
            heights.append((len(zs), gx, (min(zs) + max(zs)) / 2))
    if heights:
        # the wrist: the narrowest column in the front half of the stock (the butt is the rear end)
        front = [h for h in heights if h[1] > heights[len(heights) // 2][1]] or heights
        _, wx, wz = min(front)
        x_mid, z_mid = wx / Q, -wz / Q
        m.part = "grip"
        span = STRAPS * STRAP_W + (STRAPS - 1) * STRAP_GAP
        for k in range(STRAPS):
            c0 = x_mid - span / 2 + k * (STRAP_W + STRAP_GAP)

            def band(x, z, c0=c0):
                return 0.0 <= (x - c0) + STRAP_SLANT * (z - z_mid) < STRAP_W

            def strap(x, y, z, band=band):
                c = cell(x, z)
                return (c is not None and label[c[0]][c[1]] == grip and band(x, z)
                        and abs(y) < half_width(*c) + STRAP_RAISE)

            def strap_col(x, y, z, c0=c0):
                a = (x - c0) + STRAP_SLANT * (z - z_mid)
                if a < 0.5 or a > STRAP_W - 0.5:
                    return LEATHER_DK                                       # the cut edges
                if abs(a - STRAP_W / 2) < 0.3 and int(math.floor(z * 2)) % 3 == 0:
                    return STITCH                                           # stitches down the middle
                return mix(LEATHER, LEATHER_DK, 0.35 * hash01(math.floor(x * 4), math.floor(y * 4), math.floor(z * 4)))

            m.fill(strap, (c0 - 8, c0 + STRAP_W + 8, -half["grip"] - 2, half["grip"] + 2, -Hh, 0), strap_col,
                   size=0.25)

    # wear and tear, kept light so the gun stays simple
    def bbox(n):
        i = names.index(n)
        xs = [gx for gz in range(GZ) for gx in range(GX) if label[gz][gx] == i]
        zs = [gz for gz in range(GZ) for gx in range(GX) if label[gz][gx] == i]
        return min(xs) / Q, max(xs) / Q, -max(zs) / Q, -min(zs) / Q

    m.wear_edges(WEAR, (150, 150, 150))
    rx0, rx1, rz0, rz1 = bbox("receiver")
    m.scratches('+y', (rx0 + 2, rx1 - 2, rz0 + 2, rz1 - 2), SCRATCHES, 11)
    m.scratches('-y', (rx0 + 2, rx1 - 2, rz0 + 2, rz1 - 2), SCRATCHES - 4, 12)
    bx0, bx1, bz0, bz1 = bbox("barrel")
    m.scratches('+y', (bx0 + 4, bx1 - 4, bz0, bz1), 6, 13)
    px0, px1, pz0, pz1 = bbox("pump")
    m.crack(px0 + (px1 - px0) * 0.4, (pz0 + pz1) / 2, '+y', 14, 5, heading=0.1)
    gx0, gx1, gz0, gz1 = bbox("grip")
    m.crack(gx0 + 6, (gz0 + gz1) / 2, '-y', 10, 6, heading=2.6)
    m.grime(GRIME, 4)
    return m
