"""The cube shotgun, sharper (2026-11-04, home PC). A forge design: forge_make.py builds it.

Tefa, after wearing the cube sprite shotgun (sprite_cube_pump.py): "the cubes are too small ... use the one measure
bigger cubes and right now the weapon is too blurry and smudgy in VR, but that type of low rez look fits it. can you
make it look sharper but instead of just using paint for gaps and ridges, please use carving and adding cubes. also
the barrel has to be nice and round barrel with a flat end and actually hollow inside. please animate it with all the
game's animations and use the smallest cubes to make the flash when shot is fired."

What changed against the cube sprite shotgun:
- Surfaces step in HALF cubes (1.7 mm), not quarter cubes; the inside stays whole cubes. Quarter cubes are used only
  for the muzzle flash.
- Colours are no longer read smoothly from the game picture (that smear was the blur). Each part has its own small
  palette of flat colours; the game picture only picks WHICH of them a cube gets (nearest picture pixel, no blending),
  so the low-res pixel pattern stays but every edge between colours is sharp.
- Gaps and ridges are geometry: grooves round the pump and the butt pad are cut, the ejection port and loading port
  are cut, the receiver seam is cut, the trim, pins, top rib, barrel band and front bead are added cubes.
- The barrel is a real round tube with a flat muzzle and an empty bore; the magazine tube is round with an end cap.
- Moving parts for the game's animations (make_job_sharp.py maps the frames): the pump and its action bars, the
  trigger, three muzzle flashes, a shell pushed into the loading port and one dropped into the ejection port.
Shape and size follow the game's side pickup picture (GRZPA0, 60 x 21), read at run time and never stored here.
"""
import math
import os
import sys
import zipfile

import bpy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "blender-cubekit")))
import forge  # noqa: E402
from forge import FINE, Model, hash01, mix, mul  # noqa: E402

GAME_PK3S = (r"C:/NonSteam/Ashes 2063 VR/Resources/Ashes2063Enriched2_23.pk3",
             r"D:/ashes2063vr/Ashes 2063 VR/Resources/Ashes2063Enriched2_23.pk3")
SIDE_SPRITE = "Sprites/Weapons/GRZPA0.png"
NAME = "sharp_cube_pump"
GUN_LENGTH_M = 1.0                     # as before: the 60-pixel picture spans one metre (Tefa settled the size at 1.0)
CUBE_M = 0.0034                        # cube_size.VOXEL_M: one main cube
SURF = 0.5                             # surface cube: the half cube (Tefa: "one measure bigger")
FLASH = 0.25                           # the smallest cube, for the flash only
S = GUN_LENGTH_M / 60 / CUBE_M         # main cubes per picture pixel (4.9)


def X(px):
    return px * S


def Z(row):
    return -row * S


# ---------------------------------------------------------------------------------------------- sizes (main cubes)
BARREL_TOP = Z(4.0)
BARREL_R = 5.4                         # 37 mm across
BORE_R = 3.0                           # 20 mm bore (a 12 gauge is 18.5)
BARREL_ZC = BARREL_TOP - BARREL_R
BARREL_X0, MUZZLE_X = X(30.5), X(57.0)
TUBE_R, TUBE_ZC = 3.8, -43.0
TUBE_X0, TUBE_X1 = X(30.5), X(56.2)
CAP_R, CAP_LEN = 4.3, 2.5
REC_X0, REC_X1 = X(12.0), X(31.0)
REC_TOP, REC_BOT = Z(4.0), Z(11.9)
REC_W, REC_ROUND = 14.0, 2.0
PORT_X0, PORT_LEN, PORT_DEPTH = X(25.0), 3 * S, 4.0   # as long as the pump stroke (make_job.PUMP_STROKE_PX = 3)
SHELL2_OUT = 6.0                       # main cubes from the receiver's right side to the ejection-port shell's axis
PUMP_X0, PUMP_X1 = X(33.6), X(51.4)
PUMP_TOP, PUMP_BOT = Z(6.9), Z(11.6)
PUMP_W, PUMP_ROUND = 16.0, 6.5
PUMP_GROOVE_W, PUMP_GROOVE_STEP, PUMP_GROOVE_DEPTH, PUMP_GROOVE_MARGIN = 2.0, 6.0, 1.0, 7.0
STOCK_W_WRIST, STOCK_W_BUTT, STOCK_ROUND = 11.0, 13.5, 4.0
PAD_LEN = 2.5                          # rubber butt pad
STRAPS, STRAP_W, STRAP_GAP, STRAP_SLANT, STRAP_RAISE = 3, 4.0, 3.0, 0.35, 0.5
GUARD_X0, GUARD_X1, GUARD_BOT, GUARD_W, GUARD_BAR = X(14.6), X(21.4), Z(13.6), 4.0, 2.5

# ---------------------------------------------------------------------------------------------- palettes (sRGB)
GUNMETAL = [(40, 42, 48), (58, 60, 67), (82, 84, 91)]
BLUED = [(36, 38, 46), (52, 55, 64), (76, 79, 88)]
BRIGHT_METAL = (142, 142, 146)
BORE = (14, 14, 16)
RUST = [(78, 52, 34), (102, 66, 40)]
RUST_SCALE = 10.0                      # main cubes: rust in a few big patches, not specks
CUBE_NOISE = 0.03                      # each cube's brightness wobble (forge default 0.06: busy, reads as noise in VR)
PUMP_WOOD = [(84, 46, 22), (122, 72, 34), (156, 96, 46)]
STOCK_WOOD = [(70, 40, 20), (102, 60, 30), (134, 82, 42)]
RUBBER = (34, 30, 28)
LEATHER, LEATHER_DK, STITCH = (78, 46, 24), (48, 28, 14), (150, 122, 84)
BRASS = (196, 160, 78)
HULL = [(132, 26, 22), (170, 38, 30)]
FLASH_COLS = [(255, 252, 226), (255, 222, 104), (250, 150, 44), (222, 86, 26)]


# ---------------------------------------------------------------------------------------------- the game picture
def load_side():
    data = None
    for pk3 in GAME_PK3S:
        if os.path.exists(pk3):
            data = zipfile.ZipFile(pk3).read(SIDE_SPRITE)
            break
    assert data, "the game's pk3 was not found"
    path = os.path.join(bpy.app.tempdir, "GRZPA0.png")
    open(path, "wb").write(data)
    img = bpy.data.images.load(path)
    W, H = img.size
    px = list(img.pixels)
    bpy.data.images.remove(img)
    return W, H, [[(px[((H - 1 - y) * W + x) * 4], px[((H - 1 - y) * W + x) * 4 + 1],
                    px[((H - 1 - y) * W + x) * 4 + 2], px[((H - 1 - y) * W + x) * 4 + 3]) for x in range(W)]
                  for y in range(H)]


class Picture:
    """Nearest-pixel brightness of the game picture, and per-part thresholds that split a part's pixels in three."""

    def __init__(self):
        self.W, self.H, self.rows = load_side()

    def lum(self, x, z):
        u, v = int(math.floor(x / S)), int(math.floor(-z / S))
        if not (0 <= u < self.W and 0 <= v < self.H):
            return None
        r, g, b, a = self.rows[v][u]
        return None if a < 0.5 else (r + g + b) / 3

    def thresholds(self, x0, x1, r0, r1):
        ls = sorted(l for v in range(r0, r1 + 1) for u in range(x0, x1 + 1)
                    for (r, g, b, a) in [self.rows[v][u]] if a >= 0.5 for l in [(r + g + b) / 3])
        if not ls:
            return (0.33, 0.66)
        return ls[len(ls) // 3], ls[2 * len(ls) // 3]


def noise(x, y, z, seed, scale):
    fx, fy, fz = x / scale, y / scale, z / scale
    ix, iy, iz = math.floor(fx), math.floor(fy), math.floor(fz)
    s = lambda t: t * t * (3 - 2 * t)  # noqa: E731
    tx, ty, tz = s(fx - ix), s(fy - iy), s(fz - iz)
    acc = 0.0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (tx if dx else 1 - tx) * (ty if dy else 1 - ty) * (tz if dz else 1 - tz)
                acc += w * hash01(ix + dx, iy + dy, iz + dz, seed)
    return acc


def toned(pic, pal, th, seed, rust=0.0, rust_cols=RUST):
    """A colour function: the part's dark / mid / light colour picked by the nearest picture pixel (flat, no blend),
    one cube in eight nudged to the neighbouring tone (the pixel look), rust in patches on metal."""
    def col(x, y, z):
        l = pic.lum(x, z)
        t = 1 if l is None else (0 if l < th[0] else 1 if l < th[1] else 2)
        h = hash01(math.floor(x * 2), math.floor(y * 2), math.floor(z * 2), seed)
        if h < 0.06:
            t = max(0, t - 1)
        elif h > 0.94:
            t = min(2, t + 1)
        if rust and noise(x, y, z, seed + 7, RUST_SCALE) > 1.0 - rust:
            return rust_cols[0 if t < 2 else 1]
        return pal[t]
    return col


# ---------------------------------------------------------------------------------------------- side outlines
class Profile:
    """A side outline [(x, z)] in main cubes on a quarter-cube grid, with the signed distance to its edge (+ inside)."""

    def __init__(self, poly):
        xs, zs = [p[0] for p in poly], [p[1] for p in poly]
        self.x0, self.z0 = math.floor(min(xs)) - 3, math.floor(min(zs)) - 3
        self.nx, self.nz = int((max(xs) - self.x0 + 3) * FINE) + 1, int((max(zs) - self.z0 + 3) * FINE) + 1
        self.xr, self.zr = (min(xs), max(xs)), (min(zs), max(zs))
        inside = [[False] * self.nx for _ in range(self.nz)]
        for gz in range(self.nz):
            zc = self.z0 + (gz + 0.5) / FINE
            cross = []
            for (ax, az), (bx, bz) in zip(poly, poly[1:] + poly[:1]):
                if (az > zc) != (bz > zc):
                    cross.append(ax + (bx - ax) * (zc - az) / (bz - az))
            cross.sort()
            for a, b in zip(cross[0::2], cross[1::2]):
                for gx in range(max(0, int((a - self.x0) * FINE)), min(self.nx, int((b - self.x0) * FINE) + 1)):
                    if a <= self.x0 + (gx + 0.5) / FINE < b:
                        inside[gz][gx] = True
        din = self._chamfer(inside, True)
        dout = self._chamfer(inside, False)
        self.d = [[(din[z][x] - 0.5 if inside[z][x] else 0.5 - dout[z][x]) / FINE for x in range(self.nx)]
                  for z in range(self.nz)]

    def _chamfer(self, inside, want):
        INF = 1e9
        nz, nx = self.nz, self.nx
        d = [[INF if inside[z][x] == want else 0.0 for x in range(nx)] for z in range(nz)]
        A, B = 1.0, math.sqrt(2.0)
        for z in range(nz):
            for x in range(nx):
                if d[z][x]:
                    for dz, dx, c in ((-1, -1, B), (-1, 0, A), (-1, 1, B), (0, -1, A)):
                        if 0 <= z + dz < nz and 0 <= x + dx < nx and d[z + dz][x + dx] + c < d[z][x]:
                            d[z][x] = d[z + dz][x + dx] + c
        for z in range(nz - 1, -1, -1):
            for x in range(nx - 1, -1, -1):
                if d[z][x]:
                    for dz, dx, c in ((1, 1, B), (1, 0, A), (1, -1, B), (0, 1, A)):
                        if 0 <= z + dz < nz and 0 <= x + dx < nx and d[z + dz][x + dx] + c < d[z][x]:
                            d[z][x] = d[z + dz][x + dx] + c
        return d

    def sd(self, x, z):
        gx, gz = int(math.floor((x - self.x0) * FINE)), int(math.floor((z - self.z0) * FINE))
        if 0 <= gx < self.nx and 0 <= gz < self.nz:
            return self.d[gz][gx]
        return -99.0

    def solid(self, half_w, rnd, grow=0.0):
        """inside(x, y, z): the outline pushed out across y, `half_w(x)` half wide, its edges rounded over `rnd`;
        grow > 0 swells it (a layer on top), grow < 0 shrinks it (the floor of a groove)."""
        def inside(x, y, z):
            s = self.sd(x, z) + grow
            if s <= 0:
                return False
            t = min(s / rnd, 1.0)
            return abs(y) < (half_w(x) + grow) * math.sqrt(max(0.0, 1.0 - (1.0 - t) ** 2))
        return inside

    def bounds(self, half_w_max, pad=1.0):
        return (self.xr[0] - pad, self.xr[1] + pad, -half_w_max - pad, half_w_max + pad, self.zr[0] - pad,
                self.zr[1] + pad)


def grooved(outer, inner, bands):
    """outer minus the shell between outer and inner wherever x falls in one of the bands: cut grooves."""
    def inside(x, y, z):
        if not outer(x, y, z):
            return False
        return not (any(a <= x < b for a, b in bands) and not inner(x, y, z))
    return inside


def darken(m, inside, k):
    """Shade the cubes inside a region (the floor and walls of a cut, as shadow, not as a painted gap)."""
    for cell, v in m.full.items():
        if inside(cell[0] + 0.5, cell[1] + 0.5, cell[2] + 0.5):
            v[0] = mul(v[0], k)
    done = set()
    for cell, sub in m.fine.items():
        for (i, j, k2), v in sub.items():
            if id(v) in done:
                continue
            if inside(cell[0] + (i + 0.5) / FINE, cell[1] + (j + 0.5) / FINE, cell[2] + (k2 + 0.5) / FINE):
                v[0] = mul(v[0], k)
                done.add(id(v))


def wear_half(m, parts, amount, toward, seed):
    """Lighten surface half cubes on outside edges (open on two sides at right angles): handled, chipped edges."""
    for cell, sub in m.fine.items():
        for (i, j, k), v in list(sub.items()):
            if i % 2 or j % 2 or k % 2 or v[2] not in parts:
                continue
            q = (cell[0] * FINE + i, cell[1] * FINE + j, cell[2] * FINE + k)
            open_ax = [m.get_q(q[0] - 1, q[1], q[2]) is None or m.get_q(q[0] + 2, q[1], q[2]) is None,
                       m.get_q(q[0], q[1] - 1, q[2]) is None or m.get_q(q[0], q[1] + 2, q[2]) is None,
                       m.get_q(q[0], q[1], q[2] - 1) is None or m.get_q(q[0], q[1], q[2] + 2) is None]
            if sum(open_ax) >= 2 and hash01(*q, seed) < 0.6:
                c = mix(v[0], toward, amount * (0.6 + 0.4 * hash01(*q, seed + 1)))
                for a in (0, 1):
                    for b in (0, 1):
                        for e in (0, 1):
                            w = m.get_q(q[0] + a, q[1] + b, q[2] + e)
                            if w is not None and w[1] == v[1]:
                                w[0] = c


# ---------------------------------------------------------------------------------------------- the gun
def build():
    pic = Picture()
    forge.NOISE = CUBE_NOISE
    m = Model(NAME)

    # --- receiver: a rounded box from the picture's outline, with cuts and added trim
    rec_poly = [(REC_X0, Z(5.0)), (X(13.0), REC_TOP), (REC_X1, REC_TOP), (REC_X1, REC_BOT), (REC_X0, REC_BOT)]
    rec = Profile(rec_poly)
    m.part = "receiver"
    m.fill(rec.solid(lambda x: REC_W / 2, REC_ROUND), rec.bounds(REC_W / 2),
           toned(pic, GUNMETAL, pic.thresholds(12, 30, 4, 11), 21, rust=0.16), size=1.0, edge=SURF)

    # --- barrel: round, flat muzzle, hollow; magazine tube under it with an end cap; the band that ties them
    m.part = "barrel"
    bore_col = toned(pic, BLUED, pic.thresholds(31, 56, 4, 6), 31, rust=0.10)

    def barrel_col(x, y, z):
        if math.hypot(y, z - BARREL_ZC) < BORE_R + 0.8:
            return BORE
        if x > MUZZLE_X - 0.6:
            return mix(bore_col(x, y, z), BRIGHT_METAL, 0.45)        # the muzzle face, worn bright
        return bore_col(x, y, z)

    m.cyl(BARREL_X0, MUZZLE_X, 0.0, BARREL_ZC, BARREL_R, barrel_col, hollow=BORE_R, edge=SURF, keep=True)
    m.part = "tube"
    tube_col = toned(pic, BLUED, pic.thresholds(51, 56, 7, 10), 41, rust=0.12)
    m.cyl(TUBE_X0, TUBE_X1, 0.0, TUBE_ZC, TUBE_R, tube_col, edge=SURF, keep=True)
    m.cyl(TUBE_X1, TUBE_X1 + CAP_LEN, 0.0, TUBE_ZC, CAP_R, lambda x, y, z: mix(tube_col(x, y, z), BRIGHT_METAL, 0.3),
          edge=SURF, keep=True)
    m.cyl(TUBE_X1 + CAP_LEN - 0.5, TUBE_X1 + CAP_LEN + 0.5, 0.0, TUBE_ZC, 1.2, None, carve=True, edge=None, size=0.5)
    m.part = "band"
    bx0, bx1 = X(52.6), X(53.8)

    def band(x, y, z):
        if not (bx0 <= x < bx1):
            return False
        return (math.hypot(y, z - BARREL_ZC) < BARREL_R + 1.0 or math.hypot(y, z - TUBE_ZC) < TUBE_R + 1.0
                or (abs(y) < TUBE_R + 1.0 and TUBE_ZC <= z <= BARREL_ZC))
    m.fill(band, (bx0, bx1, -BARREL_R - 2, BARREL_R + 2, TUBE_ZC - TUBE_R - 2, BARREL_TOP + 2),
           toned(pic, GUNMETAL, (0.2, 0.35), 51, rust=0.2), size=1.0, edge=SURF)

    # --- top rib along receiver and barrel (added cubes), serrated on the receiver (cut notches), brass front bead
    m.part = "receiver"
    m.box(X(13.2), REC_X1, -1.5, 1.5, REC_TOP - 1.0, REC_TOP + 1.0, GUNMETAL[1], size=SURF, keep=True)
    m.part = "barrel"
    m.box(REC_X1, MUZZLE_X - 1.0, -1.0, 1.0, BARREL_TOP - 1.0, BARREL_TOP + 1.0, BLUED[1], size=SURF, keep=True)
    for k in range(int((REC_X1 - X(13.2)) / 2.5)):
        x = X(13.2) + 1.0 + k * 2.5
        m.box(x, x + 1.0, -2, 2, REC_TOP + 0.5, REC_TOP + 1.0, None, size=SURF, carve=True)
    m.box(MUZZLE_X - 3.0, MUZZLE_X - 1.0, -1.0, 1.0, BARREL_TOP + 1.0, BARREL_TOP + 2.5, BRASS, size=SURF)

    # --- receiver cuts: ejection port (right side), the seam under it, the loading port underneath
    m.part = "receiver"
    # The port is as long as the pump stroke and a deep dark pocket; the bolt fills it and rides the pump, so pulling
    # the pump opens the port (Tefa, 2026-09-24, on the first cube shotgun: "it needs the 'lid' to open when the pump
    # handle is pulled down, and close when it is pushed up").
    port = (PORT_X0, PORT_X0 + PORT_LEN, -REC_W / 2 - 1, -REC_W / 2 + PORT_DEPTH, Z(7.6), Z(5.2))
    m.box(*port, None, size=SURF, carve=True)
    darken(m, lambda x, y, z: port[0] - 0.5 <= x < port[1] + 0.5 and -REC_W / 2 <= y < port[3] + 0.5
           and port[4] - 0.5 <= z < port[5] + 0.5, 0.45)
    m.part = "bolt"
    bolt_col = toned(pic, [mul(BRIGHT_METAL, 0.7), mul(BRIGHT_METAL, 0.85), BRIGHT_METAL], (0.25, 0.45), 91)
    m.box(port[0], port[1], -REC_W / 2 + 0.5, port[3], port[4] + 0.5, port[5] - 0.5, bolt_col, size=SURF)
    m.box(port[0], port[1], -REC_W / 2, -REC_W / 2 + 1.0, (port[4] + port[5]) / 2 - 0.5,
          (port[4] + port[5]) / 2 + 0.5, None, size=SURF, carve=True)         # a groove along the bolt
    m.part = "receiver"
    for side in (-1, 1):
        y0, y1 = (side * REC_W / 2 - 0.5, side * REC_W / 2 + 1) if side > 0 else (-REC_W / 2 - 1, -REC_W / 2 + 0.5)
        m.box(X(21.0), REC_X1, y0, y1, Z(8.7), Z(8.5), None, size=SURF, carve=True)  # the seam
    loadport = (X(22.0), X(30.6), -4.0, 4.0, REC_BOT - 1, REC_BOT + 3.0)
    m.box(*loadport, None, size=SURF, carve=True)
    darken(m, lambda x, y, z: loadport[0] - 0.5 <= x < loadport[1] + 0.5 and abs(y) < 4.5
           and REC_BOT <= z < REC_BOT + 3.5, 0.6)

    # --- receiver trim (added cubes): the bright U of the picture on both sides, and two trigger-group pins
    for side in (-1, 1):
        y0, y1 = (REC_W / 2 - 0.5, REC_W / 2 + 0.5) if side > 0 else (-REC_W / 2 - 0.5, -REC_W / 2 + 0.5)
        u = [(X(14.0), Z(9.0), X(14.6), Z(10.6)), (X(14.0), Z(10.6), X(20.9), Z(10.0)),
             (X(20.3), Z(10.6), X(20.9), Z(9.0))]
        for a0, z0, a1, z1 in u:
            m.box(a0, a1, y0, y1, min(z0, z1), max(z0, z1), mix(GUNMETAL[2], BRIGHT_METAL, 0.5), size=SURF, keep=True)
        for px_ in (16.0, 23.5):
            yc = side * (REC_W / 2 + 0.25)
            m.box(X(px_) - 1.0, X(px_) + 1.0, yc - 0.75, yc + 0.75, Z(8.0) - 1.0, Z(8.0) + 1.0,
                  mix(GUNMETAL[2], BRIGHT_METAL, 0.3), size=SURF, keep=True)

    # --- trigger guard: a loop with a real finger hole
    m.part = "guard"
    gpoly = [(GUARD_X0, REC_BOT + 0.5), (GUARD_X1, REC_BOT + 0.5), (GUARD_X1, GUARD_BOT + 3.5),
             (GUARD_X1 - 3.5, GUARD_BOT), (GUARD_X0 + 3.5, GUARD_BOT), (GUARD_X0, GUARD_BOT + 3.5)]
    gout = Profile(gpoly)
    hole = Profile([(GUARD_X0 + GUARD_BAR, REC_BOT + 1), (GUARD_X1 - GUARD_BAR, REC_BOT + 1),
                    (GUARD_X1 - GUARD_BAR, GUARD_BOT + GUARD_BAR + 2.0),
                    (GUARD_X1 - GUARD_BAR - 2.0, GUARD_BOT + GUARD_BAR),
                    (GUARD_X0 + GUARD_BAR + 2.0, GUARD_BOT + GUARD_BAR),
                    (GUARD_X0 + GUARD_BAR, GUARD_BOT + GUARD_BAR + 2.0)])
    gsolid = gout.solid(lambda x: GUARD_W / 2, 1.0)
    m.fill(lambda x, y, z: gsolid(x, y, z) and hole.sd(x, z) <= 0, gout.bounds(GUARD_W / 2),
           toned(pic, GUNMETAL, (0.2, 0.3), 61, rust=0.1), size=1.0, edge=SURF, keep=True)

    # --- trigger (moves): a blade leaning forward at the bottom
    m.part = "trigger"
    tx = X(18.4)

    def trig(x, y, z):
        if not (GUARD_BOT + GUARD_BAR + 1.0 <= z < REC_BOT) or abs(y) >= 1.0:
            return False
        lean = (REC_BOT - z) * 0.35
        return tx + lean - 1.0 <= x < tx + lean + 1.0
    m.fill(trig, (tx - 2, tx + 6, -1.5, 1.5, GUARD_BOT, REC_BOT), mix(GUNMETAL[2], BRIGHT_METAL, 0.4),
           size=SURF, keep=True)

    # --- stock: wood from the picture's outline, rounded, wider at the butt; rubber pad with cut grooves; straps
    m.part = "grip"
    spoly = [(X(13.0), Z(4.3)), (X(9.0), Z(5.0)), (X(7.0), Z(6.0)), (X(5.0), Z(7.0)), (X(3.0), Z(8.0)),
             (X(1.0), Z(9.0)), (X(0.0), Z(10.0)), (X(0.0), Z(15.0)), (X(1.0), Z(16.0)), (X(4.2), Z(16.0)),
             (X(5.6), Z(14.8)), (X(6.2), Z(12.6)), (X(7.5), Z(11.9)), (REC_X0 + 0.5, REC_BOT),
             (REC_X0 + 0.5, Z(5.0))]
    st = Profile(spoly)

    def hw_stock(x):
        t = min(max(x / X(8.0), 0.0), 1.0)
        return (STOCK_W_BUTT + (STOCK_W_WRIST - STOCK_W_BUTT) * t) / 2

    wood = toned(pic, STOCK_WOOD, pic.thresholds(0, 11, 5, 15), 71)

    def stock_col(x, y, z):
        if x < PAD_LEN:
            return mul(RUBBER, 0.9 + 0.2 * hash01(math.floor(y * 2), math.floor(z * 2), 3))
        c = wood(x, y, z)
        return mul(c, 0.8) if x > X(7.0) else c                              # the wrist darker, as in the picture
    outer = st.solid(hw_stock, STOCK_ROUND)
    inner = st.solid(hw_stock, STOCK_ROUND, grow=-0.5)
    m.fill(grooved(outer, inner, [(PAD_LEN, PAD_LEN + 0.5)]), st.bounds(STOCK_W_BUTT / 2), stock_col, size=1.0,
           edge=SURF, keep=True)
    for k in range(int((Z(10.0) - Z(15.0)) / 3.0)):
        z = Z(15.0) + 1.5 + k * 3.0
        m.box(-1, 0.5, -STOCK_W_BUTT, STOCK_W_BUTT, z, z + 1.0, None, size=SURF, carve=True)

    # leather straps round the wrist, standing one half cube proud
    wx = X(9.0)
    zmid = (Z(5.0) + Z(12.0)) / 2
    span = STRAPS * STRAP_W + (STRAPS - 1) * STRAP_GAP
    swell = st.solid(hw_stock, STOCK_ROUND, grow=STRAP_RAISE)
    for k in range(STRAPS):
        c0 = wx - span / 2 + k * (STRAP_W + STRAP_GAP)

        def strap(x, y, z, c0=c0):
            a = (x - c0) + STRAP_SLANT * (z - zmid)
            return 0.0 <= a < STRAP_W and swell(x, y, z)

        def strap_col(x, y, z, c0=c0):
            a = (x - c0) + STRAP_SLANT * (z - zmid)
            if a < 0.5 or a >= STRAP_W - 0.5:
                return LEATHER_DK
            if abs(a - STRAP_W / 2) < 0.5 and int(math.floor(z * 2)) % 4 == 0:
                return STITCH
            return mix(LEATHER, LEATHER_DK, 0.3 * hash01(math.floor(x * 2), math.floor(y * 2), math.floor(z * 2)))
        m.fill(strap, (c0 - 8, c0 + STRAP_W + 8, -STOCK_W_BUTT, STOCK_W_BUTT, Z(13.0), Z(4.0)), strap_col,
               size=SURF)

    # --- pump (moves): wood sleeve round the tube with cut ring grooves, and the two action bars to the receiver
    m.part = "pump"
    ppoly = [(PUMP_X0, PUMP_TOP), (PUMP_X1, PUMP_TOP), (PUMP_X1, Z(10.2)), (X(48.5), PUMP_BOT + 1.0),
             (X(44.5), PUMP_BOT), (X(35.0), PUMP_BOT), (PUMP_X0, Z(10.6))]
    pp = Profile(ppoly)
    bands = []
    x = PUMP_X0 + PUMP_GROOVE_MARGIN
    while x + PUMP_GROOVE_W <= PUMP_X1 - PUMP_GROOVE_MARGIN:
        bands.append((x, x + PUMP_GROOVE_W))
        x += PUMP_GROOVE_STEP
    pout = pp.solid(lambda x: PUMP_W / 2, PUMP_ROUND)
    pin = pp.solid(lambda x: PUMP_W / 2, PUMP_ROUND, grow=-PUMP_GROOVE_DEPTH)
    pg = grooved(pout, pin, bands)
    pwood = toned(pic, PUMP_WOOD, pic.thresholds(34, 50, 7, 11), 81)
    m.fill(lambda x, y, z: pg(x, y, z) and math.hypot(y, z - TUBE_ZC) >= TUBE_R, pp.bounds(PUMP_W / 2), pwood,
           size=1.0, edge=SURF)
    # the groove floors in shadow (the cut is geometry; this is only the shade at its bottom)
    pdeep = pp.solid(lambda x: PUMP_W / 2, PUMP_ROUND, grow=-PUMP_GROOVE_DEPTH - 0.5)
    darken(m, lambda x, y, z: any(a <= x < b for a, b in bands) and pin(x, y, z) and not pdeep(x, y, z), 0.62)
    # the tube again where the pump sleeve meets it, so no pump cube bites into the tube (seen when the pump racks)
    m.part = "tube"
    m.cyl(PUMP_X0 - 1, PUMP_X1 + 1, 0.0, TUBE_ZC, TUBE_R, tube_col, edge=SURF)
    m.part = "pump"
    for side in (-1, 1):
        y0 = side * (TUBE_R + 0.25)
        m.box(REC_X1, PUMP_X0 + 1, min(y0, y0 + side * 1.0), max(y0, y0 + side * 1.0), TUBE_ZC - 0.5, TUBE_ZC + 0.5,
              GUNMETAL[0], size=SURF, keep=True)

    # --- shells (move; hidden unless a reload frame shows them): one under the loading port, one at the ejection port
    def shell(part, x0, yc, zc, keep):
        m.part = part
        hull = lambda x, y, z: HULL[0 if hash01(math.floor(x * 2), math.floor(y * 2), math.floor(z * 2), 9) < 0.3  # noqa: E731
                                    else 1]
        m.cyl(x0, x0 + 4.0, yc, zc, 2.95, BRASS, edge=SURF, keep=keep)
        m.cyl(x0 - 0.5, x0, yc, zc, 3.3, mul(BRASS, 0.85), edge=SURF, keep=keep)
        m.cyl(x0 + 4.0, x0 + 20.0, yc, zc, 2.85, hull, edge=SURF, keep=keep)
        m.cyl(x0 + 19.5, x0 + 20.5, yc, zc, 1.0, None, carve=True, edge=None, size=0.5)

    shell("shell", loadport[0] + 2.0, 0.0, REC_BOT - 3.5, False)
    # built clear of the gun, beside the open port (SHELL2_OUT), so no cube of it is lost to the receiver; the reload
    # frames move it in (make_job_sharp.SHELL2)
    shell("shell2", port[0] - 5.0, -REC_W / 2 - SHELL2_OUT, (port[4] + port[5]) / 2, False)

    # --- muzzle flashes (move; hidden unless a firing frame shows them), all in the smallest cubes
    mx, mz = MUZZLE_X + 0.5, BARREL_ZC

    def flash(part, size, spin, seed, embers):
        m.part = part
        core = 5.0 * size
        spikes = [((1, 0, 0), 18.0 * size, 3.6 * size)]
        for k in range(4):
            a = spin + k * math.pi / 2
            spikes.append(((0.7, math.cos(a) * 0.7, math.sin(a) * 0.7), 11.0 * size, 2.2 * size))
            b = a + math.pi / 4
            spikes.append(((0.5, math.cos(b) * 0.85, math.sin(b) * 0.85), 7.0 * size, 1.4 * size))

        def heat(x, y, z):
            """0 at the hot centre, 1 at the edge of the flame; None outside it."""
            dx, dy, dz = x - mx, y, z - mz
            if dx < 0:
                return None
            best = None
            r = math.sqrt((dx / 1.2) ** 2 + dy * dy + dz * dz) / core
            if r < 1.0:
                best = r * 0.45                                               # the ball: white inside, yellow skin
            for (ux, uy, uz), L, R in spikes:
                n = math.sqrt(ux * ux + uy * uy + uz * uz)
                ux, uy, uz = ux / n, uy / n, uz / n
                t = dx * ux + dy * uy + dz * uz
                if 0 <= t <= L:
                    px_, py_, pz_ = dx - t * ux, dy - t * uy, dz - t * uz
                    rr = math.sqrt(px_ * px_ + py_ * py_ + pz_ * pz_)
                    lim = R * (1.0 - t / L) + 0.3
                    if rr < lim:
                        h = 0.15 + 0.85 * (t / L)                             # white at the root, red at the tip
                        best = h if best is None else min(best, h)
            if best is not None and best > 0.8 and hash01(math.floor(x * 4), math.floor(y * 4), math.floor(z * 4),
                                                          seed) < 0.2:
                return None                                                   # ragged pixel edge
            return best

        def col(x, y, z):
            h = heat(x, y, z) or 0.0
            return FLASH_COLS[0 if h < 0.25 else 1 if h < 0.5 else 2 if h < 0.78 else 3]
        reach, side = 19.0 * size + 1, 13.0 * size + 1
        m.fill(lambda x, y, z: heat(x, y, z) is not None, (mx, mx + reach, -side, side, mz - side, mz + side),
               col, size=FLASH)
        for k in range(embers):
            r = lambda j: hash01(seed, k, j)  # noqa: E731
            ex, ey, ez = mx + 4 + r(1) * 14 * size, (r(2) - 0.5) * 16 * size, mz + (r(3) - 0.5) * 16 * size
            m.put(ex, ey, ez, FLASH_COLS[2 if r(4) < 0.6 else 3], size=FLASH)

    flash("flash_a", 1.6, 0.0, 101, 14)
    flash("flash_b", 1.1, math.pi / 4, 102, 10)
    flash("flash_c", 0.55, 0.3, 103, 16)

    # --- wear: lighter outside edges on metal and wood (whole cubes and half cubes alike)
    m.wear_edges(0.3, (150, 150, 150))
    wear_half(m, {"receiver", "barrel", "tube", "band", "guard"}, 0.35, (150, 150, 152), 5)
    wear_half(m, {"grip", "pump"}, 0.25, (176, 130, 84), 6)
    return m
