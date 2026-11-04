"""The sharp cube look, shared by every Ashes gun built that way (2026-11-04, home PC; first used on the pump shotgun,
sharp_cube_pump.py). Runs in Blender, inside a forge design.

Tefa, after the sharp cube shotgun: "it looks pretty damn great, can you please do all the episode 1 weapons like you
did that?" So what made the shotgun look that way lives here once:
- surfaces in HALF cubes over whole-cube insides; quarter cubes only for the muzzle flash
- flat colour palettes per part, the game's side picture only choosing WHICH colour a cube gets (nearest pixel)
- side outlines (Profile) pushed out and rounded, grooves cut (grooved), the floors of cuts shaded (darken)
- worn outside edges (wear_half), the muzzle flash in the smallest cubes (flash), a 12 gauge shell (shell)
- a little darker all over (finish), as Tefa asked on the shotgun.
A design reads its gun's side picture with Picture(<sprite>, <gun length in metres>) and works in main cubes, with
pic.X(pixel column) and pic.Z(pixel row) to place things on that picture.
"""
import math
import os
import sys
import zipfile

import bpy

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "blender-cubekit")))
import forge  # noqa: E402
from forge import FINE, hash01, mix, mul  # noqa: E402
from sharp_settings import CUBE_M, DARKEN, park_z  # noqa: E402

GAME_PK3S = (r"C:/NonSteam/Ashes 2063 VR/Resources/Ashes2063Enriched2_23.pk3",
             r"D:/ashes2063vr/Ashes 2063 VR/Resources/Ashes2063Enriched2_23.pk3")
SURF = 0.5                             # surface cube: the half cube (Tefa: "one measure bigger")
FLASH = 0.25                           # the smallest cube, for the flash only
CUBE_NOISE = 0.03                      # each cube's brightness wobble (forge default 0.06: busy, reads as noise in VR)
# 2026-11-05, Tefa after wearing all eleven: "still need to go up one notch in the cube size ... combine the looks with
# the game's own original sprite weapon looks, they need to look a little blurrier still, so can you use a mixture of
# even bigger cubes for more chunky parts of the gun, to make round edges and slopes use smaller cubes"
PIC_MIX = 0.45                         # how much of the game picture's own colour goes into each cube's colour
CHUNK = 2.0                            # the biggest cube, for the inside and the flat faces of chunky parts

# ---------------------------------------------------------------------------------------------- shared palettes (sRGB)
GUNMETAL = [(40, 42, 48), (58, 60, 67), (82, 84, 91)]
BLUED = [(36, 38, 46), (52, 55, 64), (76, 79, 88)]
BRIGHT_METAL = (142, 142, 146)
BORE = (14, 14, 16)
RUST = [(78, 52, 34), (102, 66, 40)]
RUST_SCALE = 10.0                      # main cubes: rust in a few big patches, not specks
PUMP_WOOD = [(84, 46, 22), (122, 72, 34), (156, 96, 46)]
STOCK_WOOD = [(70, 40, 20), (102, 60, 30), (134, 82, 42)]
RUBBER = (34, 30, 28)
LEATHER, LEATHER_DK, STITCH = (78, 46, 24), (48, 28, 14), (150, 122, 84)
BRASS = (196, 160, 78)
HULL = [(132, 26, 22), (170, 38, 30)]
FLASH_COLS = [(255, 252, 226), (255, 222, 104), (250, 150, 44), (222, 86, 26)]


# ---------------------------------------------------------------------------------------------- the game picture
def load_sprite(sprite):
    """The game's picture `sprite` (path inside the pk3) as rows of (r, g, b, a), top row first."""
    data = None
    for pk3 in GAME_PK3S:
        if os.path.exists(pk3):
            data = zipfile.ZipFile(pk3).read(sprite)
            break
    assert data, "the game's pk3 was not found"
    path = os.path.join(bpy.app.tempdir, os.path.basename(sprite))
    open(path, "wb").write(data)
    img = bpy.data.images.load(path)
    W, H = img.size
    px = list(img.pixels)
    bpy.data.images.remove(img)
    return W, H, [[(px[((H - 1 - y) * W + x) * 4], px[((H - 1 - y) * W + x) * 4 + 1],
                    px[((H - 1 - y) * W + x) * 4 + 2], px[((H - 1 - y) * W + x) * 4 + 3]) for x in range(W)]
                  for y in range(H)]


class Picture:
    """A gun's side picture laid over the model: its full width spans `length_m`. Nearest-pixel brightness, and
    per-part thresholds that split a part's pixels in three tones."""

    def __init__(self, sprite, length_m):
        self.W, self.H, self.rows = load_sprite(sprite)
        self.s = length_m / self.W / CUBE_M            # main cubes per picture pixel

    def X(self, px):
        return px * self.s

    def Z(self, row):
        return -row * self.s

    def lum(self, x, z):
        u, v = int(math.floor(x / self.s)), int(math.floor(-z / self.s))
        if not (0 <= u < self.W and 0 <= v < self.H):
            return None
        r, g, b, a = self.rows[v][u]
        return None if a < 0.5 else (r + g + b) / 3

    def rgb(self, x, z):
        """The nearest picture pixel's own colour (0-255), or None off the picture or on a clear pixel."""
        u, v = int(math.floor(x / self.s)), int(math.floor(-z / self.s))
        if not (0 <= u < self.W and 0 <= v < self.H):
            return None
        r, g, b, a = self.rows[v][u]
        if a < 0.5:
            return None
        return (255.0 * r, 255.0 * g, 255.0 * b)          # an 8-bit picture's pixels come through as stored (sRGB)

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
        c = pic.rgb(x, z)
        return pal[t] if c is None else mix(pal[t], c, PIC_MIX)
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


# ---------------------------------------------------------------------------------------------- shared pieces
def shell(m, part, x0, yc, zc, keep):
    """A 12 gauge shell lying along x, rim at x0 (brass head, red hull, crimp hole): 20.5 main cubes long."""
    m.part = part
    hull = lambda x, y, z: HULL[0 if hash01(math.floor(x * 2), math.floor(y * 2), math.floor(z * 2), 9) < 0.3  # noqa: E731
                                else 1]
    m.cyl(x0, x0 + 4.0, yc, zc, 2.95, BRASS, edge=SURF, keep=keep)
    m.cyl(x0 - 0.5, x0, yc, zc, 3.3, mul(BRASS, 0.85), edge=SURF, keep=keep)
    m.cyl(x0 + 4.0, x0 + 20.0, yc, zc, 2.85, hull, edge=SURF, keep=keep)
    m.cyl(x0 + 19.5, x0 + 20.5, yc, zc, 1.0, None, carve=True, edge=None, size=0.5)


def flash(m, part, mx, mz, size, spin, seed, embers, my=0.0):
    """A muzzle flash in the smallest cubes, pointing +x from (mx, my, mz): a white-hot ball, a long forward spike and
    eight side spikes going yellow, orange, red to the tips, a ragged edge and a few loose embers."""
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
        dx, dy, dz = x - mx, y - my, z - mz
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
    m.fill(lambda x, y, z: heat(x, y, z) is not None, (mx, mx + reach, my - side, my + side, mz - side, mz + side),
           col, size=FLASH)
    for k in range(embers):
        r = lambda j: hash01(seed, k, j)  # noqa: E731
        ex, ey, ez = mx + 4 + r(1) * 14 * size, my + (r(2) - 0.5) * 16 * size, mz + (r(3) - 0.5) * 16 * size
        m.put(ex, ey, ez, FLASH_COLS[2 if r(4) < 0.6 else 3], size=FLASH)


def flashes(m, mx, mz, my=0.0, scale=1.0, names=("flash_a", "flash_b", "flash_c"), first=0):
    """The three flashes the firing frames show (A biggest, C the dying one), as on the pump shotgun. Each is built
    in its own spot above the muzzle (sharp_settings.park_z) and the job moves it down when a frame shows it: built in
    one spot, a smaller flash overwrote the cubes of the bigger one it overlapped (a model holds one part per cube)."""
    for k, (name, size, spin, seed, embers) in enumerate(zip(names, (1.6, 1.1, 0.55), (0.0, math.pi / 4, 0.3),
                                                               (101, 102, 103), (14, 10, 16))):
        flash(m, name, mx, mz + park_z(first + k), size * scale, spin, seed + 3 * first, embers, my)


def finish(m, metal, wood):
    """Worn lighter outside edges on metal and wood, then a little darker all over (Tefa, 2026-11-04); the flash
    keeps its own colours."""
    m.wear_edges(0.3, (150, 150, 150))
    wear_half(m, set(metal), 0.35, (150, 150, 152), 5)
    wear_half(m, set(wood), 0.25, (176, 130, 84), 6)
    for v in list(m.full.values()) + [w for sub in m.fine.values() for w in sub.values()]:
        if not v[2].startswith("flash"):
            v[0] = mul(v[0], DARKEN)


def chunky(m, inside, bounds, col, part=None, keep=False):
    """Fill a shape in mixed cubes (2026-11-05): CHUNK cubes wherever they fit, whole cubes where the surface is flat
    (the cube's corners split cleanly along one axis), half cubes only where it slopes or curves."""
    part = part or m.part

    def place(cx, cy, cz, s):
        if keep and m.at(cx, cy, cz) is not None:
            return
        m.put(cx - s / 2, cy - s / 2, cz - s / 2, col(cx, cy, cz) if callable(col) else col, s, part)

    def visit(cx, cy, cz, s):
        h = s / 2 * 0.98
        ins = [inside(cx + a * h, cy + b * h, cz + c * h) for a in (-1, 1) for b in (-1, 1) for c in (-1, 1)]
        n = sum(ins)
        mid = inside(cx, cy, cz)
        if n == 8:
            place(cx, cy, cz, s)
            return
        if n == 0 and not mid:
            return
        if s <= SURF + 1e-9:
            if mid:
                place(cx, cy, cz, s)
            return
        if s <= 1.0 + 1e-9 and n == 4:
            # corners ordered (a, b, c) over x, y, z: a flat face splits them into two halves along one axis
            halves = ([ins[i] for i in (0, 1, 2, 3)], [ins[i] for i in (0, 1, 4, 5)], [ins[i] for i in (0, 2, 4, 6)])
            if any(all(hv) or not any(hv) for hv in halves):
                if mid:
                    place(cx, cy, cz, s)
                return
        q = s / 4
        for a in (-1, 1):
            for b in (-1, 1):
                for c in (-1, 1):
                    visit(cx + a * q, cy + b * q, cz + c * q, s / 2)

    x0, x1, y0, y1, z0, z1 = bounds
    s = CHUNK
    xs = math.floor(x0 / s) * s
    while xs < x1:
        ys = math.floor(y0 / s) * s
        while ys < y1:
            zs = math.floor(z0 / s) * s
            while zs < z1:
                visit(xs + s / 2, ys + s / 2, zs + s / 2, s)
                zs += s
            ys += s
        xs += s


def start(name):
    """A new model with the sharp look's settings. Every solid fill the designs make in whole cubes with half-cube
    edges goes through chunky() instead (2026-11-05), so the whole set changed size in one place."""
    forge.NOISE = CUBE_NOISE
    m = forge.Model(name)
    plain = m.fill

    def fill(inside, bounds, col, size=1.0, edge=None, part=None, carve=False, keep=False):
        if not carve and col is not None and size == 1.0 and edge == SURF:
            return chunky(m, inside, bounds, col, part, keep)
        return plain(inside, bounds, col, size, edge, part, carve, keep)
    m.fill = fill
    return m


# ---------------------------------------------------------------------------------------------- building pieces
# (added for the other Episode 1 guns, 2026-11-04: the same pieces the pump and sawn-off build by hand)
def body(m, part, poly, half_w, rnd, col, keep=False, size=1.0, exclude=None):
    """A part from a side outline pushed out `half_w` (a number or a function of x) and rounded over `rnd`;
    `exclude(x, y, z)` keeps cubes out (a bore, a tube another part fills). Returns the Profile."""
    m.part = part
    pr = Profile(poly)
    hw = half_w if callable(half_w) else (lambda x, h=half_w: h)
    sol = pr.solid(hw, rnd)
    hmax = max(hw(x) for x in (pr.xr[0], (pr.xr[0] + pr.xr[1]) / 2, pr.xr[1]))
    inside = sol if exclude is None else (lambda x, y, z: sol(x, y, z) and not exclude(x, y, z))
    m.fill(inside, pr.bounds(hmax), col, size=size, edge=SURF, keep=keep)
    return pr


def barrel(m, part, x0, x1, yc, zc, r, bore, col, keep=True):
    """A round barrel along x, hollow, its flat muzzle worn bright, the bore dark."""
    m.part = part

    def c(x, y, z):
        if math.hypot(y - yc, z - zc) < bore + 0.8:
            return BORE
        if x > x1 - 0.6:
            return mix(col(x, y, z), BRIGHT_METAL, 0.45)
        return col(x, y, z)
    m.cyl(x0, x1, yc, zc, r, c, hollow=bore, edge=SURF, keep=keep)


GUARD_UP = 3.5                         # main cubes the finger hole runs up into the gun (Tefa, 2026-11-05)


def guard(m, x0, x1, top, bot, col, w=4.0, bar=2.2, part="guard", up=GUARD_UP):
    """A trigger guard: a loop under the gun from x0 to x1, from `top` down to `bot`, with a real finger hole, and the
    hole carried `up` into the gun above it as a dark recess the trigger hangs from (2026-11-05, Tefa: "the trigger
    guards have to expand upwards"). blade() triggers should hang from top + up."""
    if up:
        m.box(x0 + bar, x1 - bar, -2.5, 2.5, top - 0.5, top + up, None, size=SURF, carve=True)
        darken(m, lambda x, y, z: x0 + bar - 0.5 <= x < x1 - bar + 0.5 and abs(y) < 3.0 and top - 1 <= z < top + up + 0.5,
               0.55)
    m.part = part
    out = Profile([(x0, top + 0.5), (x1, top + 0.5), (x1, bot + 3.0), (x1 - 3.0, bot), (x0 + 3.0, bot),
                   (x0, bot + 3.0)])
    hole = Profile([(x0 + bar, top + 1), (x1 - bar, top + 1), (x1 - bar, bot + bar + 1.5),
                    (x1 - bar - 1.5, bot + bar), (x0 + bar + 1.5, bot + bar), (x0 + bar, bot + bar + 1.5)])
    sol = out.solid(lambda x: w / 2, 1.0)
    m.fill(lambda x, y, z: sol(x, y, z) and hole.sd(x, z) <= 0, out.bounds(w / 2), col, size=1.0, edge=SURF,
           keep=True)


def blade(m, tx, top, bot, col, w=0.75, lean=0.3, part="trigger", up=GUARD_UP):
    """A trigger blade hanging from `top` (+ `up`, into the guard's recess) down to `bot` at x = tx, leaning forward
    at the bottom."""
    m.part = part
    top = top + up
    w = max(w, 1.0)                                   # whole-cube wide since the cubes went up a notch (2026-11-05)

    def inside(x, y, z):
        if not (bot <= z < top) or abs(y) >= 1.0:
            return False
        d = (top - z) * lean
        return tx + d - w <= x < tx + d + w
    m.fill(inside, (tx - 2, tx + (top - bot) * lean + 2, -1.5, 1.5, bot, top), col, size=SURF, keep=True)


def plates(m, x0, x1, z0, z1, half, col, raised=0.5):
    """The same raised plate on both sides of a part `half` wide (grip panels, side plates, trim)."""
    for side in (-1, 1):
        y0, y1 = (half - raised, half + raised) if side > 0 else (-half - raised, -half + raised)
        m.box(x0, x1, y0, y1, z0, z1, col, size=SURF, keep=True)


def screws(m, pts, half, col=(164, 162, 158)):
    """Screw heads standing proud on both sides at (x, z) points."""
    for x, z in pts:
        for side in (-1, 1):
            yc = side * (half + 0.5)
            m.box(x - 0.5, x + 0.5, yc - 0.5, yc + 0.5, z - 0.5, z + 0.5, col, size=SURF)


def seam(m, x0, x1, z, half, depth=0.5):
    """A cut line along both sides at height z."""
    for side in (-1, 1):
        y0, y1 = (half - depth, half + 1) if side > 0 else (-half - 1, -half + depth)
        m.box(x0, x1, y0, y1, z - 0.25, z + 0.25, None, size=SURF, carve=True)
