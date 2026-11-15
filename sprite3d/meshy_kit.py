"""Meshy guns in the smudge-cube look (2026-11-15, Developer PC). Runs in Blender, inside a forge design.

Tefa: "i know meshy generates stuff that needs more work on our side, but i like how they come out, and should make our
life easier in the end, all that needs to be done is filling the loose gaps and putting the bullet/shell eject on one
side only". So a Meshy model (a .glb with its own texture) is turned into the smudge-cube look (smudge_kit.py) by:
- SHAPE: every main cube whose centre is inside the Meshy mesh, half cubes on the surface (forge fill, edge 0.5). The
  Meshy meshes are not closed everywhere, so inside is a vote of six rays (Solid);
- COLOUR: the Meshy texture shrunk to TEX_SIDE, read at the nearest surface point; half the colour of the cube's
  BLOCK-sized block and half its own (the kit's SMUDGE), so it reads blocky, not photo-smooth;
- GAPS: each gun's design names boxes to fill solid (fill_box) and the one side's port that stays open.
Axes as every forge gun: x to the muzzle, y to the gun's LEFT (so the right side is -y), z up, in main cubes."""
import math

import bmesh
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform

import forge
import sharp_kit
from sharp_settings import CUBE_M

SMUDGE = 0.5                     # half the block colour, half the cube's own (smudge_kit.SMUDGE)
BLOCK = 3                        # main cubes per colour block (smudge_kit: three cells per picture pixel)
TEX_SIDE = 256                   # the texture is shrunk to this before reading
WELD = 0.02                      # main cubes: glTF opens the mesh at every UV seam; this closes them again
TOP_M = -0.0578                  # where every Meshy gun's top sits, in Blender metres (the round 12 shotgun's barrel)


class Meshy:
    """A Meshy .glb in main cubes. Meshy points the muzzle down -x with the gun's right toward +y."""

    def __init__(self, glb, length_m, top_m=TOP_M, tilt_deg=0.0):
        """tilt_deg: Meshy sometimes builds the gun nose-up (copying an angled picture); it is turned this many degrees
        nose-down about its left-right axis before anything else (2026-11-16, the heavy machine gun: 10)."""
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=glb)
        ob = [o for o in bpy.data.objects if o not in before and o.type == 'MESH'][0]   # not a start-up cube
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        bm.transform(ob.matrix_world)
        if tilt_deg:
            from mathutils import Matrix
            bm.transform(Matrix.Rotation(math.radians(-tilt_deg), 4, 'Y'))
        bmesh.ops.triangulate(bm, faces=bm.faces)
        xs = [v.co.x for v in bm.verts]
        zs = [v.co.z for v in bm.verts]
        k = length_m / (max(xs) - min(xs)) / CUBE_M
        x_butt, z_top = max(xs), max(zs)
        for v in bm.verts:
            x, y, z = v.co
            v.co = Vector(((x_butt - x) * k, -y * k, (z - z_top) * k + top_m / CUBE_M))
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=WELD)
        bm.normal_update()
        uv = bm.loops.layers.uv.active
        nt = ob.data.materials[0].node_tree
        bsdf = next(n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED')
        small = bsdf.inputs[0].links[0].from_node.image.copy()        # what feeds Base Color
        small.scale(TEX_SIDE, TEX_SIDE)
        px = list(small.pixels)
        self.tex = [(px[i], px[i + 1], px[i + 2]) for i in range(0, len(px), 4)]
        bm.faces.ensure_lookup_table()
        self.tris = [(tuple(lp.vert.co.copy() for lp in f.loops), tuple(lp[uv].uv.copy() for lp in f.loops))
                     for f in bm.faces]
        self.bvh = BVHTree.FromBMesh(bm)
        self.lo = Vector([min(v.co[i] for v in bm.verts) for i in range(3)])
        self.hi = Vector([max(v.co[i] for v in bm.verts) for i in range(3)])
        bpy.data.objects.remove(ob)
        self.inside = Solid(self.bvh, self.lo, self.hi)

    def tex_at(self, p):
        loc, nor, i, d = self.bvh.find_nearest(Vector(p))
        (a, b, c), (ua, ub, uc) = self.tris[i]
        u = barycentric_transform(loc, a, b, c, ua.to_3d(), ub.to_3d(), uc.to_3d())
        s = min(TEX_SIDE - 1, max(0, int((u.x % 1.0) * TEX_SIDE)))
        t = min(TEX_SIDE - 1, max(0, int((u.y % 1.0) * TEX_SIDE)))
        return self.tex[t * TEX_SIDE + s]

    tint = None                  # a design may set tint(x, y, z, rgb) -> rgb (the Glock's frame: less rust)

    def col(self, x, y, z):
        bx, bz = (math.floor(x / BLOCK) + 0.5) * BLOCK, (math.floor(z / BLOCK) + 0.5) * BLOCK
        blk, own = self.tex_at((bx, y, bz)), self.tex_at((x, y, z))
        rgb = tuple(_byte(blk[i] * (1 - SMUDGE) + own[i] * SMUDGE) for i in range(3))
        return self.tint(x, y, z, rgb) if self.tint else rgb

    def model(self, name, part="body"):
        """The whole gun in the kit's mixed cubes (sharp_kit.start: chunky fills and the cube-to-cube brightness
        wobble): 2-cube chunks inside and on flat faces, whole cubes on flat surfaces, half cubes on slopes and curves.
        Tefa, 2026-11-15: "use different size cubes, that gave the latest shotgun that ... not-perfect look"."""
        m = sharp_kit.start(name)
        m.part = part
        lo, hi = self.lo, self.hi
        m.fill(self.inside, (lo.x - 1, hi.x + 1, lo.y - 1, hi.y + 1, lo.z - 1, hi.z + 1), self.col, size=1.0,
               edge=sharp_kit.SURF)
        return m


def derust(rgb, k, dim=0.8):
    """Take the orange out of a colour by share k (0 none, 1 all), keeping its brightness (times dim where it was
    orange), so a rust fleck becomes a lighter worn scuff in grey."""
    r, g, b = rgb
    orange = max(0.0, min(1.0, (r - max(g, b)) / 30.0))      # 0 grey .. 1 orange or rust-brown
    if orange <= 0:
        return rgb
    lum = 0.30 * r + 0.59 * g + 0.11 * b
    grey = lum * (1 - (1 - dim) * orange)
    t = k * orange
    return tuple(int(round(c * (1 - t) + grey * t)) for c in rgb)


# Wood, from the photo Tefa picked for the shotgun (2026-11-15, a Texturelabs plank): its colours at the 2, 10, 25, 45,
# 65 and 85 % brightness steps. Only these numbers are kept, not the picture.
WOOD = [(99, 53, 27), (120, 71, 41), (136, 83, 51), (151, 94, 60), (163, 105, 69), (181, 119, 80)]
WOOD_REF_LUM = 140.0             # how bright Meshy's orange is where it is lit; brighter or darker orange keeps that
WOOD_SHADE = (0.6, 1.15)         # ... as a share of the wood's brightness, within these bounds
ORANGE_FROM, ORANGE_FULL = 15, 35    # red over blue: from where a colour counts as orange, and where it fully does


def orangeness(rgb):
    r, g, b = rgb
    if r < g:
        return 0.0
    return max(0.0, min(1.0, (r - b - ORANGE_FROM) / float(ORANGE_FULL)))


def wood(x, y, z, rgb, seed=7):
    """Turn any orange in rgb into wood (Tefa: "be thorough with getting even the smallest specs of orange"): grain
    running along the gun's length (x), in the photo's colours, keeping how lit or shaded the orange was."""
    t = orangeness(rgb)
    if t <= 0:
        return rgb
    grain = 0.65 * sharp_kit.noise(x / 6.0, y, z * 1.6, seed, 1.0) + 0.35 * sharp_kit.noise(x, y * 2, z * 3, seed + 1,
                                                                                               2.0)
    i = max(0.0, min(len(WOOD) - 1.001, (grain - 0.2) / 0.6 * (len(WOOD) - 1)))
    a, f = int(i), i - int(i)
    w = [WOOD[a][c] * (1 - f) + WOOD[a + 1][c] * f for c in range(3)]
    lum = 0.30 * rgb[0] + 0.59 * rgb[1] + 0.11 * rgb[2]
    k = max(WOOD_SHADE[0], min(WOOD_SHADE[1], lum / WOOD_REF_LUM))
    return tuple(int(round(rgb[c] * (1 - t) + w[c] * k * t)) for c in range(3))


def big_shell(m, part, x0, yc, zc, k):
    """smudge_cube_pump_v12.big_shell (a 12 gauge shell lying along x, rim at x0, k times the kit's size), copied so
    a Meshy design need not import round 12's whole design."""
    m.part = part

    def hull(x, y, z):
        return sharp_kit.HULL[0 if forge.hash01(math.floor(x), math.floor(y), math.floor(z), 9) < 0.3 else 1]
    m.cyl(x0, x0 + 4.0 * k, yc, zc, 2.95 * k, sharp_kit.BRASS, edge=sharp_kit.SURF)
    m.cyl(x0 - 0.5 * k, x0, yc, zc, 3.3 * k, forge.mul(sharp_kit.BRASS, 0.85), edge=sharp_kit.SURF)
    m.cyl(x0 + 4.0 * k, x0 + 20.0 * k, yc, zc, 2.85 * k, hull, edge=sharp_kit.SURF)
    m.cyl(x0 + 19.5 * k, x0 + 20.5 * k, yc, zc, 1.0 * k, None, carve=True, edge=None, size=0.5)


def set_part(m, test, part, recolour=None):
    """Move every cube whose centre passes test(x, y, z) to `part` (optionally recoloured: recolour(x, y, z) -> rgb).
    Whole and 2-cube cubes that straddle the line are split to quarter cells first so the cut follows it."""
    from forge import FINE
    for cell in list(m.full):
        corners = [test(cell[0] + a, cell[1] + b, cell[2] + c) for a in (0.05, 0.95) for b in (0.05, 0.95)
                   for c in (0.05, 0.95)]
        if any(corners) and not all(corners):
            m._split(cell)
    groups = {}                                      # a 2-cube chunk is 8 main cells sharing one id
    for cell, v in m.full.items():
        groups.setdefault(v[1], []).append(cell)
    n = 0
    for cid, cells in groups.items():
        hit = [c for c in cells if test(c[0] + 0.5, c[1] + 0.5, c[2] + 0.5)]
        if not hit:
            continue
        whole = len(hit) == len(cells)               # the chunk moves as one; a straddling one becomes single cubes
        for c in hit:
            v = m.full[c]
            v[2] = part
            if not whole:
                v[1] = m.new_id()
            if recolour:
                v[0] = recolour(c[0] + 0.5, c[1] + 0.5, c[2] + 0.5)
            n += 1
    for cell, sub in m.fine.items():
        for (i, j, k), v in sub.items():
            p = (cell[0] + (i + 0.5) / FINE, cell[1] + (j + 0.5) / FINE, cell[2] + (k + 0.5) / FINE)
            if test(*p):
                v[2] = part
                if recolour:
                    v[0] = recolour(*p)
                n += 1
    return n


def _byte(c):
    """Byte images keep their stored (already sRGB) values in .pixels."""
    return int(round(255 * min(1.0, max(0.0, c))))


def fill_box(m, box, col, keep_open=None, rows=None):
    """Fill every empty main cell in box = (x0, x1, y0, y1, z0, z1) (integers, ends excluded). keep_open(x, y, z) ->
    True leaves a cell empty (the one port that stays). rows(z) -> (y0, y1) narrows a row (rounded top edges)."""
    x0, x1, y0, y1, z0, z1 = box
    n = 0
    for x in range(x0, x1):
        for z in range(z0, z1):
            ya, yb = rows(z) if rows else (y0, y1)
            for y in range(ya, yb):
                if m.at(x + 0.5, y + 0.5, z + 0.5) is not None:
                    continue
                if keep_open and keep_open(x, y, z):
                    continue
                m.put(x, y, z, col(x + 0.5, y + 0.5, z + 0.5))
                n += 1
    return n


def fill_between(m, box, axis, max_gap=1):
    """Close loose gaps: every empty main cell in box that has a cube within max_gap on BOTH sides along axis (0 x,
    1 y, 2 z) is filled, in the colour of the nearer of the two. A slit between two parts, a pinhole in a wall."""
    x0, x1, y0, y1, z0, z1 = box
    found = []
    for x in range(x0, x1):
        for y in range(y0, y1):
            for z in range(z0, z1):
                c = (x + 0.5, y + 0.5, z + 0.5)
                if m.at(*c) is not None:
                    continue
                near = []
                for sign in (-1, 1):
                    for d in range(1, max_gap + 1):
                        p = list(c)
                        p[axis] += sign * d
                        v = m.at(*p)
                        if v is not None:
                            near.append((d, v[0]))
                            break
                if len(near) == 2:
                    found.append(((x, y, z), min(near)[1]))
    for (x, y, z), rgb in found:                     # filled after the search, so a fill never feeds another
        m.put(x, y, z, rgb)
    return len(found)


class Solid:
    """Inside or outside a mesh that is not closed everywhere. Rays are shot through the whole gun along all three
    axes, both ways, on a half-cube grid; a point gets one vote per ray: inside when the last surface that ray crossed
    before it faced the ray (it went in). Inside = at least VOTES of the six."""
    STEP = 0.5
    VOTES = 4

    def __init__(self, bvh, lo, hi):
        self.bvh = bvh
        self.lo = lo - Vector((2, 2, 2))
        self.hi = hi + Vector((2, 2, 2))
        self.cols = {}

    def _hits(self, axis, a, b, sign):
        key = (axis, a, b, sign)
        h = self.cols.get(key)
        if h is not None:
            return h
        o = [0.0, 0.0, 0.0]
        oth = [i for i in range(3) if i != axis]
        o[oth[0]] = (a + 0.5) * self.STEP
        o[oth[1]] = (b + 0.5) * self.STEP
        d = Vector((0, 0, 0))
        d[axis] = sign
        o[axis] = self.lo[axis] if sign > 0 else self.hi[axis]
        p = Vector(o)
        span = self.hi[axis] - self.lo[axis]
        h = []
        while True:
            loc, nor, i, dist = self.bvh.ray_cast(p, d, span)
            if loc is None:
                break
            h.append(((loc[axis] - o[axis]) * sign, nor.dot(d) < 0))      # True = going in
            p = loc + d * 1e-4
        self.cols[key] = h
        return h

    def __call__(self, x, y, z):
        p = (x, y, z)
        if any(p[i] < self.lo[i] or p[i] > self.hi[i] for i in range(3)):
            return False
        votes = 0
        for axis in range(3):
            oth = [i for i in range(3) if i != axis]
            a, b = math.floor(p[oth[0]] / self.STEP), math.floor(p[oth[1]] / self.STEP)
            for sign in (1, -1):
                t = (p[axis] - (self.lo[axis] if sign > 0 else self.hi[axis])) * sign
                state = False
                for th, going_in in self._hits(axis, a, b, sign):
                    if th > t:
                        break
                    state = going_in
                votes += state
        return votes >= self.VOTES


def side_map(meshy, step_x=3, step_z=2):
    """A text picture of the gun from the side, to measure gaps by: # solid wall to wall, o thin, H hollow inside,
    . nothing. Printed by measure runs, not by builds."""
    lo, hi, S = meshy.lo, meshy.hi, meshy.inside
    out = []
    for z in range(int(hi.z) + 1, int(lo.z) - 1, -step_z):
        line = ""
        for x in range(int(lo.x), int(hi.x) + 1, step_x):
            ys = [y for y in range(int(lo.y) - 1, int(hi.y) + 2) if S(x + .5, y + .5, z + .5)]
            if not ys:
                line += "."
            else:
                full = max(ys) - min(ys) + 1
                line += ("#" if len(ys) > 14 else "o") if len(ys) == full else "H"
        out.append("%5d %s" % (z, line))
    out.append("x of column i = %d + %d * i" % (int(lo.x), step_x))
    return "\n".join(out)


def section(meshy, x, z0, z1, y0=-20, y1=20, step=3):
    """Cross-sections at one x, top down: y from the right side (-y) to the left."""
    S = meshy.inside
    return "\n".join("  z=%4d %s" % (z, "".join("#" if S(x + .5, y + .5, z + .5) else "." for y in range(y0, y1)))
                     for z in range(z1, z0, -step))
