"""The 2026-11-27 Meshy set: every Ashes gun Tefa remade in Meshy, in the cube look (Build PC). Runs in Blender inside a
forge design (forge_make.py), on top of meshy_kit.py.

Tefa, 2026-11-27: "please give them the blocky cubekit treatment, using different cube sizes, scratches need to be cut
out continuously (not dotted cut outs) with very fine small cubes. gun barrels have to be empty inside like actual pipes
and the moving parts on the weapon all have to move as expected ... don't put hands on the weapons just yet ... size
them up referencing the pump action shotgun's size".
- SIZE: every gun at its real length (SPEC lengths in m2_guns.py); all of them are packed with the one scale the Meshy
  shotgun Tefa wore and liked (0.7, make_job_meshy_pump.py), so they keep the same size against each other and the shotgun.
- CUBES: meshy_kit.Meshy.model, the kit's mixed sizes (2-cube chunks inside, whole on flat faces, half on curves).
- SCRATCHES (cut_scratches): wandering lines cut one quarter cube deep, walked in half-quarter steps so every cell along
  the line goes (forge._line_q), the floor of the cut showing bright metal (on wood: darker wood).
- BARRELS (bore): a round hole along the barrel in quarter cubes, open at the muzzle, its lining darker the deeper it is.
Axes as every forge gun: x to the muzzle (0 at the butt), y to the gun's LEFT (the right side is -y), z up, main cubes.
"""
import math
import os

import forge
from forge import FINE, SIDES, hash01, mix, mul
from meshy_kit import Meshy, fill_box, set_part   # noqa: F401  (designs import them from here)
from sharp_kit import flashes                     # noqa: F401

MESHY_DIR = os.path.join(os.path.expanduser("~"), "Desktop", "doom and ashes stuff", "Ashes latest from Meshy")

SCRATCH_METAL = (196, 194, 186)     # what a cut through paint or bluing shows
SCRATCH_MIX = 0.55
SCRATCH_WOOD_DARK = 0.62            # a cut in wood reads darker
BORE_DARK = 0.30                    # the lining deep in the barrel, as a share of its own colour
BORE_LIP = 0.80                     # ... and right at the muzzle
BORE_FADE = 12.0                    # main cubes over which it goes from the lip to the deep shade


def glb(name):
    return os.path.join(MESHY_DIR, name + ".glb")


def load(name, file, length_m, tint=None, tilt_deg=0.0):
    """The Meshy file in the kit's mixed cubes; returns (meshy, model)."""
    g = Meshy(glb(file), length_m, tilt_deg=tilt_deg)
    if tint:
        g.tint = tint
    m = g.model(name)
    _manifest_at_exit(m)
    return g, m


PARTS_DIR = os.path.join("D:" + os.sep, "Ashes 2063", "3D blender", "meshy set 2026-11-27", "blend")


def _manifest_at_exit(m):
    """When Blender is done with the design, note which parts the finished model really has (m2_make.py's export
    leaves any other out of the poses: a box that caught no cubes makes no part)."""
    import atexit
    import json

    def write():
        parts = {v[2] for v in m.full.values()} | {w[2] for s in m.fine.values() for w in s.values()}
        os.makedirs(PARTS_DIR, exist_ok=True)
        json.dump(sorted(parts), open(os.path.join(PARTS_DIR, m.name + ".parts.json"), "w"))
    atexit.register(write)


def cells_in(m, box):
    """Every (centre, value) of the model inside box (x0, x1, y0, y1, z0, z1), whole and quarter cubes."""
    x0, x1, y0, y1, z0, z1 = box
    for cell, v in m.full.items():
        c = (cell[0] + 0.5, cell[1] + 0.5, cell[2] + 0.5)
        if x0 <= c[0] < x1 and y0 <= c[1] < y1 and z0 <= c[2] < z1:
            yield c, v
    for cell, sub in m.fine.items():
        if not (x0 - 1 <= cell[0] < x1 + 1 and y0 - 1 <= cell[1] < y1 + 1 and z0 - 1 <= cell[2] < z1 + 1):
            continue
        for (i, j, k), v in sub.items():
            c = (cell[0] + (i + 0.5) / FINE, cell[1] + (j + 0.5) / FINE, cell[2] + (k + 0.5) / FINE)
            if x0 <= c[0] < x1 and y0 <= c[1] < y1 and z0 <= c[2] < z1:
                yield c, v


def bore(m, x0, x1, yc, zc, r, axis_dir=1):
    """Hollow a barrel like a real pipe: a round hole of radius r (main cubes) along x from x0 to the muzzle x1 (or the
    other way for axis_dir -1, a muzzle at x0), cut in quarter cubes so it stays round, then the cubes lining it
    darkened, more the deeper they sit. Returns how many quarter cells went."""
    before = sum(len(s) for s in m.fine.values()) + 64 * len(m.full)
    lo, hi = (x0, x1 + 3) if axis_dir > 0 else (x0 - 3, x1)
    m.cyl(lo, hi, yc, zc, r, None, carve=True, size=0.25, edge=None)
    muzzle = x1 if axis_dir > 0 else x0
    for c, v in cells_in(m, (x0 - 1, x1 + 1, yc - r - 1.5, yc + r + 1.5, zc - r - 1.5, zc + r + 1.5)):
        d = math.hypot(c[1] - yc, c[2] - zc)
        if d > r + 0.55:                  # the lining only: a thin barrel wall must keep its outside colour
            continue
        depth = abs(muzzle - c[0])
        t = min(1.0, depth / BORE_FADE)
        v[0] = mul(v[0], BORE_LIP + (BORE_DARK - BORE_LIP) * t)
    after = sum(len(s) for s in m.fine.values()) + 64 * len(m.full)
    return before - after


def is_wood(rgb):
    r, g, b = rgb
    return r > g + 12 and g > b + 4 and r > 60


def _cut(m, side, a, b, parts):
    """Cut the outermost quarter cell seen from `side` at quarter coords (a, b); paint the cell under it."""
    q = m.surface_q(side, a, b)
    if q is None:
        return False
    v = m.get_q(*q)
    if parts is not None and v[2] not in parts:
        return False
    ax, sign = SIDES[side]
    under = list(q)
    under[ax] -= sign
    w = m.get_q(*under)
    if w is None:                         # a wall one quarter thin: leave it, a hole would show through
        return False
    col = w[0]
    new = mul(col, SCRATCH_WOOD_DARK) if is_wood(col) else mix(col, SCRATCH_METAL, SCRATCH_MIX)
    m.clear_q(*q)
    m.put_q(*under, new, w[1], w[2])
    return True


def cut_scratches(m, seed, count, box=None, sides=("+y", "-y", "+z"), parts=None, length=(5.0, 16.0),
                  along=0.75):
    """`count` scratches cut into the faces seen from `sides`, inside box (x0, x1, z0 or y0, z1 or y1 of the face's
    own two axes; None = the whole model): each a wandering line, mostly along the gun (share `along`), the rest
    across at any angle. Every quarter cell the line passes is cut, so it reads as one unbroken groove."""
    lo, hi = m._qbounds()
    n = 0
    for i in range(count):
        r = lambda k: hash01(seed, i, k)  # noqa: E731
        side = sides[int(r(0) * len(sides)) % len(sides)]
        ax = SIDES[side][0]
        others = [k for k in range(3) if k != ax]
        if box is None:
            a0, a1 = lo[others[0]] / FINE, hi[others[0]] / FINE
            b0, b1 = lo[others[1]] / FINE, hi[others[1]] / FINE
        else:
            a0, a1, b0, b1 = box[0], box[1], box[2], box[3]
            if ax != 1:                   # the top face: (x, y)
                b0, b1 = box[4], box[5]
        # a start point on the gun: a few tries
        for t in range(12):
            a = a0 + (a1 - a0) * hash01(seed, i, 20 + t)
            b = b0 + (b1 - b0) * hash01(seed, i, 40 + t)
            if m.surface_q(side, math.floor(a * FINE), math.floor(b * FINE)) is not None:
                break
        else:
            continue
        L = length[0] + (length[1] - length[0]) * r(3)
        if r(4) < along:
            h = (r(5) - 0.5) * 0.5 + (math.pi if r(6) > 0.5 else 0.0)
        else:
            h = r(5) * math.tau
        pts = [(a, b)]
        for s in range(int(L * 4)):
            h += (r(100 + s) - 0.5) * 0.25
            a += math.cos(h) * 0.25
            b += math.sin(h) * 0.25
            pts.append((a, b))
        for qa, qb in m._line_q(pts):
            n += _cut(m, side, qa, qb, parts)
    return n


def darken_box(m, box, k, part=None):
    for c, v in cells_in(m, box):
        if part is None or v[2] == part:
            v[0] = mul(v[0], k)


def move_cells(m, test, dx=0, dy=0, dz=0):
    """Shift every whole cube passing test(x, y, z) by whole cubes (a part built in its rest spot elsewhere)."""
    moved = {c: v for c, v in m.full.items() if test(c[0] + 0.5, c[1] + 0.5, c[2] + 0.5)}
    for c in moved:
        del m.full[c]
    for (x, y, z), v in moved.items():
        m.full[(x + dx, y + dy, z + dz)] = v
    fm = {c: s for c, s in m.fine.items() if test(c[0] + 0.5, c[1] + 0.5, c[2] + 0.5)}
    for c in fm:
        del m.fine[c]
    for (x, y, z), s in fm.items():
        m.fine[(x + dx, y + dy, z + dz)] = s
    m._qb = None
    return len(moved) + len(fm)


def copy_part(m, src_part, new_part, dz):
    """A copy of a part lifted dz whole cubes (a hidden spare: the magazine that comes in on a reload)."""
    for c, v in list(m.full.items()):
        if v[2] == src_part:
            m.full[(c[0], c[1], c[2] + dz)] = [v[0], v[1], new_part]
    for c, s in list(m.fine.items()):
        if any(w[2] == src_part for w in s.values()):
            m.fine[(c[0], c[1], c[2] + dz)] = {k: [w[0], w[1], new_part] for k, w in s.items() if w[2] == src_part}
    m._qb = None


def finish(m, seed, scratches_per_100=10, sides=("+y", "-y", "+z"), parts=None):
    """The common last step of every gun: scratches by its length."""
    lo, hi = m._qbounds()
    length = (hi[0] - lo[0]) / FINE
    return cut_scratches(m, seed, max(4, int(length * scratches_per_100 / 100.0)), sides=sides, parts=parts)
