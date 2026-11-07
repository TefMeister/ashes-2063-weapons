"""The smudge-cube look, shared by every Ashes gun from now on (2026-11-07, home PC). Runs in Blender, inside a forge
design.

Tefa, on the shotgun's round 8 (smudge_cube_pump_v8.py, kept as the reference): "Yesssss!!!! finally, this is the
look i have been chasing ever since we made the first revolver and lantern. looks awesome and dangerous ... in the
colouring and style of this shotgun for all going forward". What made it, in one place:
- COLOUR: every cube shows the game's own side picture under it, on a grid three cells per picture pixel, half the
  nearest pixel and half the smooth (bicubic) read: SMUDGE. No palettes, wear, rust, straps or darkening; only the
  floors of real cuts are shaded. A cube the hand-drawn shape puts outside the picture's outline takes the nearest
  solid pixel's colour. (Smudge.pc)
- SHAPE: robust, not soft: flat faces and square-cut ends, small roundings only on the long edges of boxy parts; round
  parts (barrels, tubes, rods, hoops) truly round.
- CUBES: the kit's mixed cubes (sharp_kit.chunky): big cubes inside and on flat faces, half cubes on slopes; round
  parts go down to quarter cubes (round_fill).
- SCRATCHES: carved two quarter cubes deep, long (8-20 cubes on metal), the floor in the cut cube's own colour, drawn
  as joined lines (carve_scratches; the forge line stepper leaves gaps, FAULTS 2026-11-07).
- MATTE: no shine material on the export (the fire-lights pk3's gldefs shine), and Blender's viewport with its
  specular highlight off, each face lit on its own.
- A part that must stand apart (the shotgun's shell guard) gets blocky smudged steel of its own (blocky_steel).
"""
import math

import forge
import sharp_kit
from forge import FINE, hash01, mix, mul

SMUDGE = 0.5                           # 0 = the nearest picture pixel (hard), 1 = the full bicubic smudge
COLOUR_FINE = 3                        # colour cells per picture pixel
ROUND_EDGE = 0.25                      # the smallest cube, for round parts
SCRATCH_DEPTH = 2                      # quarter cubes deep
SCRATCH_WIDTH = 2                      # quarter cubes wide
SCRATCH_LEN = (8.0, 20.0)              # main cubes, on metal
SCRATCH_LEN_WOOD = (5.0, 12.0)         # main cubes, on wood, rope and rubber
STEEL_BASE = (78, 80, 86)              # blocky_steel's middle tone
STEEL_SPREAD = 0.22                    # +- brightness from block to block


def _cubic(t):
    return (((-t + 2) * t - 1) * t / 2, ((3 * t - 5) * t * t + 2) / 2, ((-3 * t + 4) * t + 1) * t / 2,
            (t - 1) * t * t / 2)


class Smudge:
    """A gun's side picture as the smudge look's colour source. `s` = main cubes per picture pixel; `pic_u(x)` (optional)
    maps a point's x back to a picture column when the design stretched part of the gun."""

    def __init__(self, sprite, s, pic_u=None):
        self.W, self.H, self.rows = sharp_kit.load_sprite(sprite)
        self.s = s
        self.pic_u = pic_u or (lambda x: x / s)
        solid = [(u, v) for v in range(self.H) for u in range(self.W) if self.rows[v][u][3] >= 0.5]
        self.near = [[min(solid, key=lambda q: (q[0] - u) ** 2 + (q[1] - v) ** 2) for u in range(self.W)]
                     for v in range(self.H)]

    def X(self, px):
        return px * self.s

    def Z(self, row):
        return -row * self.s

    def _smooth(self, u, v):
        u0, v0 = math.floor(u - 0.5), math.floor(v - 0.5)
        wu, wv = _cubic(u - 0.5 - u0), _cubic(v - 0.5 - v0)
        acc = [0.0] * 4
        for j in range(4):
            yy = min(max(v0 - 1 + j, 0), self.H - 1)
            for i in range(4):
                xx = min(max(u0 - 1 + i, 0), self.W - 1)
                r, g, b, a = self.rows[yy][xx]
                w = wu[i] * wv[j]
                acc[0] += w * r * a
                acc[1] += w * g * a
                acc[2] += w * b * a
                acc[3] += w * a
        if acc[3] < 0.5:
            return None
        return tuple(min(max(c / acc[3], 0.0), 1.0) * 255 for c in acc[:3])

    def pc(self, x, y, z):
        """A cube's colour: the picture under it (side view), SMUDGE of the way to smooth."""
        u = (math.floor(self.pic_u(x) * COLOUR_FINE) + 0.5) / COLOUR_FINE
        v = (math.floor(-z / self.s * COLOUR_FINE) + 0.5) / COLOUR_FINE
        iu, iv = min(max(int(u), 0), self.W - 1), min(max(int(v), 0), self.H - 1)
        nu, nv = self.near[iv][iu]
        r, g, b, _ = self.rows[nv][nu]
        sharp = (r * 255, g * 255, b * 255)
        smooth = self._smooth(u, v) if (nu, nv) == (iu, iv) else None
        return sharp if smooth is None else mix(sharp, smooth, SMUDGE)

    def at(self, px, row):
        """A colour function showing the picture at one fixed spot whatever the point (a part the picture hides)."""
        return lambda x, y, z: self.pc(self.X(px), y, self.Z(row))


def round_fill(fn, *args, **kw):
    """One fill (m.fill, m.cyl ...) with the mixed cubes going down to ROUND_EDGE on the curve."""
    old = sharp_kit.SURF
    sharp_kit.SURF = ROUND_EDGE
    try:
        kw["edge"] = ROUND_EDGE
        fn(*args, **kw)
    finally:
        sharp_kit.SURF = old


def blocky_steel(block, base=STEEL_BASE, spread=STEEL_SPREAD):
    """A colour function: steel in `block`-cube blocks of their own brightness, smudged into each other."""
    def blk(i, j):
        return 1.0 + spread * (hash01(i, j, 23) - 0.5) * 2

    def col(x, y, z):
        bu, bv = x / block, z / block
        sharp = blk(math.floor(bu), math.floor(bv))
        u0, v0 = math.floor(bu - 0.5), math.floor(bv - 0.5)
        fu, fv = bu - 0.5 - u0, bv - 0.5 - v0
        smooth = ((blk(u0, v0) * (1 - fu) + blk(u0 + 1, v0) * fu) * (1 - fv)
                  + (blk(u0, v0 + 1) * (1 - fu) + blk(u0 + 1, v0 + 1) * fu) * fv)
        return mul(base, sharp + (smooth - sharp) * SMUDGE)
    return col


def scratch_cells(pts, width=SCRATCH_WIDTH):
    """Every quarter cell (a, b) a polyline in main units passes over, joined (at most half a quarter cell per step),
    widened by `width` cells across b; in order, no repeats."""
    seen, out = set(), []
    for (a0, b0), (a1, b1) in zip(pts, pts[1:]):
        n = max(1, math.ceil(max(abs(a1 - a0), abs(b1 - b0)) * FINE * 2))
        for st in range(n + 1):
            t = st / n
            qa = math.floor((a0 + (a1 - a0) * t) * FINE)
            qb = math.floor((b0 + (b1 - b0) * t) * FINE)
            for w in range(width):
                c = (qa, qb + w)
                if c not in seen:
                    seen.add(c)
                    out.append(c)
    return out


def carve_scratches(m, side, region, count, seed, parts, length=SCRATCH_LEN, along=0.5):
    """Carve `count` scratches into the surface seen from `side` inside region (a0, a1, b0, b1), main cubes, in the
    two axes other than the side's (x, y, z order). Only cells whose outermost cube belongs to `parts` are cut; the
    floor keeps the cut cube's colour. `along`: how far a scratch may turn from the gun's length (radians)."""
    ax, sign = forge.SIDES[side]
    a0, a1, b0, b1 = region
    for i in range(count):
        def r(k):
            return hash01(seed, i, k)
        a = a0 + (a1 - a0) * r(1)
        b = b0 + (b1 - b0) * r(2)
        L = length[0] + (length[1] - length[0]) * r(3)
        h = (r(4) - 0.5) * 2 * along + (math.pi if r(5) > 0.5 else 0.0)
        pts = [(a, b)]
        for st in range(int(L * 2)):
            h += (r(10 + st) - 0.5) * 0.4
            a += math.cos(h) * 0.5
            b += math.sin(h) * 0.5
            pts.append((a, b))
        for q in [m.surface_q(side, qa, qb) for qa, qb in scratch_cells(pts)]:
            if q is None:
                continue
            v = m.get_q(*q)
            if v is None or v[2] not in parts:
                continue
            qq = list(q)
            for _ in range(SCRATCH_DEPTH):
                m.clear_q(*qq)
                qq[ax] -= sign
            w = m.get_q(*qq)
            if w is not None:
                m.put_q(*qq, v[0], w[1], w[2])
