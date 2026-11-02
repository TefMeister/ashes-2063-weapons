# The wasteland layer for the detailed Ashes guns (2026-11-02): duct tape, cloth and wire wraps, rust and pitting,
# chipped paint, soot, welded or riveted makeshift plates, scratched tally marks, a used soda bottle.
#
# Tefa, 2026-11-02: "mix both the games sprite looks and real life examples, then add a layer of post apocalyptic
# filters on top with scratches, cloth, duct tape, rust, chipped parts, makeshift parts, like having a used soda bottle
# for a canister on the flamethrower just for example."
#
# Everything here works in QUARTER cubes (0.85 mm) on top of what a design already built, so it reads as a thin layer:
# tape one quarter thick, cloth two, wire one. Units in the arguments are main cubes (3.4 mm), as in forge.py.
import math

from forge import FINE, hash01, mix, mul

DIRS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
AXIS = {'x': 0, 'y': 1, 'z': 2}

# colours (sRGB 0-255)
DUCT = (132, 132, 128)            # silver-grey duct tape, gone dull
DUCT_BLACK = (34, 34, 36)
TAPE_BLUE = (52, 84, 140)         # the Ashes shotgun's blue tape
TAPE_RED = (138, 36, 30)
CLOTH_KHAKI = (118, 102, 70)
CLOTH_RED = (112, 38, 30)
CLOTH_GREY = (88, 86, 80)
LEATHER = (92, 58, 34)
PARACORD = (70, 84, 52)
WIRE_COPPER = (176, 98, 52)
WIRE_STEEL = (150, 150, 146)
RUST = (122, 60, 26)
RUST_DK = (74, 34, 16)
RUST_HI = (168, 92, 44)
SOOT = (26, 24, 22)
BARE = (182, 184, 186)            # bright steel under chipped paint or a fresh scratch
WELD = (96, 88, 80)


def _q(v):
    return math.floor(v * FINE)


def _box_q(bounds):
    x0, x1, y0, y1, z0, z1 = bounds
    return range(_q(x0), _q(x1) + 1), range(_q(y0), _q(y1) + 1), range(_q(z0), _q(z1) + 1)


def _centre(q):
    return ((q[0] + 0.5) / FINE, (q[1] + 0.5) / FINE, (q[2] + 0.5) / FINE)


def surface_cells(m, bounds, region=None, skip_axis=None):
    """Quarter cells inside bounds (and region(x, y, z) if given) that have at least one open side, with the open
    directions. skip_axis: an axis ('x', 'y', 'z') whose two directions do not count (a wrap round a bar along x
    should not cap its ends)."""
    rx, ry, rz = _box_q(bounds)
    skip = AXIS.get(skip_axis)
    out = []
    for qx in rx:
        for qy in ry:
            for qz in rz:
                v = m.get_q(qx, qy, qz)
                if v is None:
                    continue
                if region is not None and not region(*_centre((qx, qy, qz))):
                    continue
                open_d = [d for d in DIRS if (skip is None or d[skip] == 0)
                          and m.get_q(qx + d[0], qy + d[1], qz + d[2]) is None]
                if open_d:
                    out.append(((qx, qy, qz), v, open_d))
    return out


def grow_layer(m, bounds, col, region=None, layers=1, skip_axis=None, part=None, gaps=0.0, seed=1):
    """Wrap whatever sits inside bounds in a skin `layers` quarter cubes thick (tape, cloth, a rubber sleeve).
    col: an rgb or f(x, y, z, layer) -> rgb. gaps: share of skin cells left out (frayed, torn)."""
    added = 0
    for layer in range(layers):
        new = {}
        for q, v, open_d in surface_cells(m, bounds, region, skip_axis):
            for d in open_d:
                n = (q[0] + d[0], q[1] + d[1], q[2] + d[2])
                if n in new:
                    continue
                if gaps and hash01(n[0], n[1], n[2], seed + layer * 31) < gaps:
                    continue
                c = col(*_centre(n), layer) if callable(col) else col
                new[n] = (c, part or v[2])
        for n, (c, p) in new.items():
            m.put_q(*n, c, None, p)
        added += len(new)
        # the next layer grows on this one: widen bounds by a quarter on every side
        x0, x1, y0, y1, z0, z1 = bounds
        g = 1.0 / FINE
        bounds = (x0 - g, x1 + g, y0 - g, y1 + g, z0 - g, z1 + g)
    return added


def tape(m, axis, a0, a1, bounds, col=DUCT, seed=11, part=None, frayed=0.08, creases=True):
    """Tape wound round a part along `axis` from a0 to a1 (main units on that axis), one quarter thick, with ragged
    edges, faint creases and grime in the creases."""
    ax = AXIS[axis]

    def region(x, y, z):
        t = (x, y, z)[ax]
        wob = (hash01(math.floor(t * 4), seed) - 0.5) * 0.4
        return a0 + wob <= t <= a1 - wob

    def paint(x, y, z, layer):
        t = (x, y, z)[ax]
        k = 1.0 + 0.07 * (hash01(_q(x), _q(y), _q(z), seed) - 0.5) * 2
        if creases and math.floor(t * 4 + 0.6 * math.sin((x + y + z) * 1.7)) % 5 == 0:
            k *= 0.82                                           # a crease where the strip overlaps
        c = mul(col, k)
        if hash01(_q(x) // 2, _q(y) // 2, _q(z) // 2, seed + 5) < 0.12:
            c = mix(c, (70, 60, 48), 0.45)                       # dirt ground into it
        return c

    return grow_layer(m, bounds, paint, region, 1, skip_axis=axis, part=part, gaps=frayed, seed=seed)


def cloth(m, axis, a0, a1, bounds, col=CLOTH_KHAKI, seed=21, part=None, layers=2, tail=None):
    """A rag wound round a part, two quarters thick, woven (two tones in a fine checker), torn at the edges.
    tail = (x, y, z, length, dz): a loose end hanging from that point."""
    ax = AXIS[axis]
    dark = mul(col, 0.72)

    def region(x, y, z):
        t = (x, y, z)[ax]
        wob = (hash01(math.floor(t * 4), seed) - 0.5) * 0.7
        return a0 + wob <= t <= a1 - wob

    def paint(x, y, z, layer):
        qa, qb, qc = _q(x), _q(y), _q(z)
        c = col if (qa // 2 + qb // 2 + qc // 2) % 2 == 0 else mix(col, dark, 0.35)   # weave in half cubes
        if hash01(qa // 3, qb // 3, qc // 3, seed + 3) < 0.18:
            c = mix(c, (52, 40, 30), 0.5)                        # stains
        return mul(c, 0.92 if layer == 0 else 1.0)

    n = grow_layer(m, bounds, paint, region, layers, skip_axis=axis, part=part, gaps=0.05, seed=seed)
    if tail:
        x, y, z, length, dz = tail
        for i in range(int(length * FINE)):
            t = i / FINE
            wig = math.sin(i * 0.7 + seed) * 0.25
            for w in range(3):
                m.put_q(_q(x + wig), _q(y) + w - 1, _q(z - t * dz), paint(x, y, z - t * dz, 1), None,
                        part or m.part)
    return n


def wire_wrap(m, x0, x1, yc, zc, r, pitch=1.0, col=WIRE_COPPER, part=None, turns_offset=0.0):
    """Wire wound round a cylinder along x (radius r = the part's outside), one quarter thick, `pitch` main units
    per turn, the ends twisted together into a little pigtail."""
    steps = int((x1 - x0) * FINE * 6)
    for s in range(steps + 1):
        x = x0 + (x1 - x0) * s / steps
        a = (x - x0) / pitch * math.tau + turns_offset
        y, z = yc + math.cos(a) * (r + 0.2), zc + math.sin(a) * (r + 0.2)
        m.put_q(_q(x), _q(y), _q(z), mul(col, 0.9 + 0.2 * math.cos(a * 0.5)), None, part or m.part)
    for i in range(5):                                           # the pigtail at the end, sticking up
        m.put_q(_q(x1) + (i % 2), _q(yc), _q(zc + r + 0.3) + i, col, None, part or m.part)


def rust(m, bounds, amount=0.3, seed=31, region=None, pits=0.04, scale=2.5):
    """Rust on the outside cells: soft patches by value noise, darker in their middle, the odd pit dug one quarter
    deep with dark rust at the bottom. Leaves cells that are already rust-free colours like wood alone only when
    region says so."""
    def noise(x, y, z):
        return (math.sin(x / scale + seed) * math.sin(z / scale * 1.3 + seed * 0.7) * math.sin(y / scale + seed * 1.9)
                * 0.5 + 0.5) * 0.6 + hash01(math.floor(x * 2), math.floor(y * 2), math.floor(z * 2), seed) * 0.4

    for q, v, open_d in surface_cells(m, bounds, region):
        x, y, z = _centre(q)
        n = noise(x, y, z)
        if n > 1.0 - amount:
            t = min(1.0, (n - (1.0 - amount)) / max(0.05, amount) * 1.6)
            c = mix(v[0], RUST if t < 0.7 else RUST_DK, min(1.0, t))
            if hash01(q[0], q[1], q[2], seed + 9) < 0.15:
                c = mix(c, RUST_HI, 0.5)                          # flaky orange bits
            m.put_q(*q, c, v[1], v[2])
            if pits and hash01(q[0], q[1], q[2], seed + 4) < pits and len(open_d) == 1:
                d = open_d[0]
                m.clear_q(*q)
                b = (q[0] - d[0], q[1] - d[1], q[2] - d[2])
                w = m.get_q(*b)
                if w is not None:
                    m.put_q(*b, RUST_DK, w[1], w[2])


def soot(m, bounds, amount=0.6, seed=41, region=None):
    """Burnt powder: darken the outside cells inside bounds, strongest at the middle of bounds."""
    x0, x1, y0, y1, z0, z1 = bounds
    cx, cy, cz = (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2
    rr = max(x1 - x0, y1 - y0, z1 - z0) / 2 or 1.0
    for q, v, _ in surface_cells(m, bounds, region):
        x, y, z = _centre(q)
        d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2) / rr
        k = max(0.0, 1.0 - d) * amount * (0.6 + 0.4 * hash01(q[0], q[1], q[2], seed))
        if k > 0.05:
            m.put_q(*q, mix(v[0], SOOT, min(0.9, k)), v[1], v[2])


def chips(m, side, region, count, seed, under=BARE, size=(1, 3)):
    """Paint chipped off: small ragged patches one quarter deep, the floor showing bright metal (or `under`).
    region = (a0, a1, b0, b1) on the face seen from side, as forge's scratches."""
    a0, a1, b0, b1 = region
    for i in range(count):
        r = lambda k: hash01(seed, i, k)
        a, b = a0 + (a1 - a0) * r(1), b0 + (b1 - b0) * r(2)
        w = size[0] + int((size[1] - size[0] + 1) * r(3))
        cells = []
        for da in range(w):
            for db in range(w):
                if hash01(seed, i, da, db) < 0.7:
                    cells.append(((da, db), under))
        m._stamp(side, _q(a), _q(b), cells, under, 'carve')


def tally(m, side, a, b, n, height=2.5, col=BARE, seed=51):
    """Scratched tally marks: groups of four strokes with a fifth across, cut one quarter deep and bright."""
    for i in range(n):
        g, k = divmod(i, 5)
        x = a + g * 2.4 + k * 0.5
        if k < 4:
            pts = [(x, b), (x + 0.15 * (hash01(seed, i) - 0.5), b + height)]
        else:
            pts = [(a + g * 2.4 - 0.3, b + 0.4), (a + g * 2.4 + 2.0, b + height - 0.4)]
        m.groove(pts, side, depth=1, width=1, col=col)


def plate(m, side, a0, a1, b0, b1, col, rivets=True, weld=False, raise_by=1, seed=61):
    """A makeshift steel plate laid on the surface seen from side: raise_by quarter cubes proud, rivets at the
    corners and along long edges, or a lumpy weld bead round it. a/b as in forge's surface tools."""
    if callable(col):
        col = col(a0, 0.0, b0)
    for qa in range(_q(a0), _q(a1)):
        for qb in range(_q(b0), _q(b1)):
            cells = [((0, 0), mul(col, 0.92 + 0.16 * hash01(qa // 2, qb // 2, seed)))]
            for h in range(raise_by):
                m._stamp(side, qa, qb, cells, col, 'raise')
    if rivets:
        n = max(2, int((a1 - a0) / 3))
        for i in range(n):
            a = a0 + 0.6 + (a1 - a0 - 1.2) * i / (n - 1)
            for b in (b0 + 0.6, b1 - 0.6):
                m.screw(a, b, side, mul(col, 1.2), kind='rivet')
    if weld:
        edge = [(a0, b0), (a1, b0), (a1, b1), (a0, b1), (a0, b0)]
        m.raised(edge, side, WELD, height=1, width=1)


def bottle(m, x0, yc, zc, length=22.0, r=4.4, col=(96, 132, 104), label=(170, 40, 36), cap=(210, 200, 60),
           part='bottle', axis_up=False, seed=71):
    """A used plastic soda bottle lying along x from x0 (its base) to x0 + length (its cap): a petal base, a ribbed
    body with a faded, peeling label band, a tapered shoulder, the neck ring and a ribbed cap. Solid (only the skin
    is drawn), murky fuel colour along its bottom."""
    old = m.part
    m.part = part
    body0, body1 = x0 + 2.0, x0 + length * 0.66
    shoulder1 = x0 + length * 0.86
    neck_r, cap_r = r * 0.38, r * 0.44

    def radius(x):
        if x < body0:                                    # the petal base: five lobes
            return r * (0.82 + 0.18 * (x - x0) / 2.0)
        if x < body1:
            return r
        if x < shoulder1:
            t = (x - body1) / (shoulder1 - body1)
            return r - (r - neck_r) * (1 - math.cos(t * math.pi)) / 2
        return neck_r

    def shell(x, y, z):
        if not (x0 <= x <= shoulder1 + 1.5):
            return False
        d = math.hypot(y - yc, z - zc)
        rr = radius(x)
        if x < body0:
            ang = math.atan2(z - zc, y - yc)
            rr *= 0.9 + 0.1 * math.cos(ang * 5)
        return d <= rr          # solid: the inside is never drawn, a hollow shell would draw a second skin inside

    def paint(x, y, z):
        c = col
        if body0 + 2 <= x <= body0 + 7.5:                   # the label band, faded and peeling
            ang = math.atan2(z - zc, y - yc)
            if not (0.6 < ang < 1.4 and hash01(math.floor(x * 4), seed) < 0.7):
                c = mix(label, (220, 210, 190), 0.25 * hash01(math.floor(x * 2), math.floor(ang * 6), seed))
                if abs(x - (body0 + 4.5)) < 0.6:
                    c = (230, 226, 214)                       # a white stripe across the label
        if body1 - 1 > x > body0 and math.floor(x * 2) % 4 == 0 and not (body0 + 2 <= x <= body0 + 7.5):
            c = mul(c, 0.82)                                  # moulded ribs
        return mul(c, 0.9 + 0.2 * hash01(math.floor(x * 4), math.floor(y * 4), math.floor(z * 4), seed))

    m.fill(shell, (x0, shoulder1 + 1.5, yc - r - 1, yc + r + 1, zc - r - 1, zc + r + 1), paint, 0.25)
    # neck ring and cap with ribs
    m.cyl(shoulder1 + 0.5, shoulder1 + 1.0, yc, zc, neck_r + 0.5, mul(col, 0.9), size=0.25, edge=0.25)
    m.cyl(shoulder1 + 1.0, shoulder1 + 3.5, yc, zc, cap_r, cap, size=0.25, edge=0.25)
    for k in range(10):
        a = k * math.tau / 10
        m.box(shoulder1 + 1.0, shoulder1 + 3.25, yc + math.cos(a) * cap_r - 0.125, yc + math.cos(a) * cap_r + 0.125,
              zc + math.sin(a) * cap_r - 0.125, zc + math.sin(a) * cap_r + 0.125, mul(cap, 0.75), size=0.25)
    # murky fuel showing at the bottom
    m.fill(lambda x, y, z: body0 <= x <= body1 and math.hypot(y - yc, z - zc) <= r - 0.5 and z < zc - r * 0.55,
           (body0, body1, yc - r, yc + r, zc - r, zc), (120, 92, 40), 0.25)
    m.part = old
    return shoulder1 + 3.5                               # where the cap ends (a hose goes on here)


def hose_clamp(m, x, yc, zc, r, col=WIRE_STEEL, part=None):
    """A worm-drive hose clamp round a round part at x: a thin band and the screw housing on top."""
    m.cyl(x, x + 0.75, yc, zc, r + 0.25, col, size=0.25, edge=0.25, part=part)
    m.box(x - 0.25, x + 1.0, yc - 0.5, yc + 0.5, zc + r, zc + r + 0.75, mul(col, 0.85), size=0.25, part=part)
    m.box(x + 0.25, x + 0.5, yc - 0.25, yc + 0.25, zc + r + 0.75, zc + r + 1.0, (40, 40, 42), size=0.25, part=part)


def stipple(m, side, region, seed, depth_share=0.5, dark=0.6):
    """Rubber grip stippling: every other quarter on the face pressed in or darkened at random."""
    a0, a1, b0, b1 = region
    cells = []
    for qa in range(_q(a0), _q(a1)):
        for qb in range(_q(b0), _q(b1)):
            if hash01(qa, qb, seed) < depth_share:
                cells.append(((qa - _q(a0), qb - _q(b0)), None))
    for (da, db), _ in cells:
        q = m.surface_q(side, _q(a0) + da, _q(b0) + db)
        if q is None:
            continue
        v = m.get_q(*q)
        m.put_q(*q, mul(v[0], dark), v[1], v[2])


def cavity(m, strength=0.38, levels=3, lift=0.10):
    """Painted depth, because cube guns are drawn without real shading: every outside cube sitting in a groove,
    corner or recess (solid cubes beside it on the open side) is darkened, in a few steps so faces still merge;
    lone outer edges are lifted a little. Whole cubes are judged as whole cubes (splitting them would multiply the
    faces), quarter cells as quarter cells. Run it after all carving and before grime."""
    perp = {d: [e for e in DIRS if all(d[n] * e[n] == 0 for n in range(3))] for d in DIRS}

    def shade(c, open_d, solid):
        k = 0
        for d in open_d:
            k += sum(1 for e in perp[d] if solid(d, e))
        k = k / max(1, 4 * len(open_d))
        if k > 0.01:
            step = math.ceil(k * levels) / levels
            return mul(c, 1.0 - strength * step)
        if len(open_d) >= 3:
            return mul(c, 1.0 + lift)
        return c

    full = m.full
    changes = []
    for (x, y, z), v in full.items():
        open_d = [d for d in DIRS if (x + d[0], y + d[1], z + d[2]) not in full
                  and (x + d[0], y + d[1], z + d[2]) not in m.fine]
        if not open_d:
            continue
        solid = lambda d, e: (x + d[0] + e[0], y + d[1] + e[1], z + d[2] + e[2]) in full
        changes.append((v, shade(v[0], open_d, solid)))
    for cell, sub in m.fine.items():
        for (i, j, k), v in sub.items():
            q = (cell[0] * FINE + i, cell[1] * FINE + j, cell[2] * FINE + k)
            open_d = [d for d in DIRS if m.get_q(q[0] + d[0], q[1] + d[1], q[2] + d[2]) is None]
            if not open_d:
                continue
            solid = lambda d, e, q=q: m.get_q(q[0] + d[0] + e[0], q[1] + d[1] + e[1], q[2] + d[2] + e[2]) is not None
            changes.append((v, shade(v[0], open_d, solid)))
    for v, c in changes:
        v[0] = c


def wear_lines(m, side, region, count, seed, lighten=1.18, length=(4.0, 14.0), along=0.0):
    """Holster and handling wear: faint, nearly straight lines along the gun (heading `along`, radians from x)."""
    a0, a1, b0, b1 = region
    for i in range(count):
        r = lambda k: hash01(seed, i, k)
        a, b = a0 + (a1 - a0) * r(1), b0 + (b1 - b0) * r(2)
        L = length[0] + (length[1] - length[0]) * r(3)
        h = along + (r(4) - 0.5) * 0.12
        pts = [(a, b), (a + math.cos(h) * L, b + math.sin(h) * L)]
        m.paint_line(pts, side, lambda c: mul(mix(c, (190, 188, 182), 0.15), lighten))


def simplify(m, step=10, block=1.0, parts=None):
    """Keep the game's load sane (2026-11-02: the first detailed flamethrower came out at 327 000 faces, three times
    the heaviest first-pass gun). Quarter cells only join into bigger faces when they share a colour AND a cube id
    (the id sets each cube's brightness wobble). So: round every small cell's colour to `step`, and give small cells
    of the same part and rounded colour inside one `block` (main cubes) a shared id. The wobble then works per block
    instead of per quarter; flat runs of tape, wood, rust and paint join up, edges and features stay exact."""
    ids = {}
    for cell, sub in m.fine.items():
        for (i, j, k), v in sub.items():
            if parts is not None and v[2] not in parts:
                continue
            c = tuple(int(round(ch / step) * step) for ch in v[0])
            x, y, z = (cell[0] + i / FINE) / block, (cell[1] + j / FINE) / block, (cell[2] + k / FINE) / block
            key = (v[2], c, math.floor(x), math.floor(y), math.floor(z))
            if key not in ids:
                ids[key] = 10_000_000 + len(ids)
            v[0], v[1] = c, ids[key]
