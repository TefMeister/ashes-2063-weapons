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
from sharp_settings import CUBE_M

SMUDGE = 0.5                     # half the block colour, half the cube's own (smudge_kit.SMUDGE)
BLOCK = 3                        # main cubes per colour block (smudge_kit: three cells per picture pixel)
TEX_SIDE = 256                   # the texture is shrunk to this before reading
WELD = 0.02                      # main cubes: glTF opens the mesh at every UV seam; this closes them again
TOP_M = -0.0578                  # where every Meshy gun's top sits, in Blender metres (the round 12 shotgun's barrel)


class Meshy:
    """A Meshy .glb in main cubes. Meshy points the muzzle down -x with the gun's right toward +y."""

    def __init__(self, glb, length_m, top_m=TOP_M):
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=glb)
        ob = [o for o in bpy.data.objects if o not in before and o.type == 'MESH'][0]   # not a start-up cube
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        bm.transform(ob.matrix_world)
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

    def col(self, x, y, z):
        bx, bz = (math.floor(x / BLOCK) + 0.5) * BLOCK, (math.floor(z / BLOCK) + 0.5) * BLOCK
        blk, own = self.tex_at((bx, y, bz)), self.tex_at((x, y, z))
        return tuple(_byte(blk[i] * (1 - SMUDGE) + own[i] * SMUDGE) for i in range(3))

    def model(self, name, part="body"):
        m = forge.Model(name)
        m.part = part
        lo, hi = self.lo, self.hi
        m.fill(self.inside, (lo.x - 1, hi.x + 1, lo.y - 1, hi.y + 1, lo.z - 1, hi.z + 1), self.col, size=1.0,
               edge=0.5)
        return m


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
