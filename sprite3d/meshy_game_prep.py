"""Readies a Meshy gun's blend for the game export (2026-11-16, Developer PC). Runs in Blender.
    blender -b <meshy gun.blend> --python meshy_game_prep.py -- <gun key> <out.blend>

Tefa: "please put all the meshy guns in the game". The Meshy guns were built as one or two parts; the export needs:
- a part named "grip": the export puts its middle in the player's hand. GRIP below is that box, in the blend's metres
  (x across, y back of the gun to the muzzle, z up), read off a side view; faces whose middle is in it move into it;
- the muzzle flashes (and the revolver's reload rounds): copied from the sharp gun of the same game class, whose job
  supplies the poses, moved so the flash's back sits on this gun's muzzle (MUZZLE: y of the front, z of the bore);
- the moving parts named as the sharp job names them (RENAME: part -> the job's part).
Nothing else changes: the look is the design's.
"""
import sys

import bmesh
import bpy
from mathutils import Vector

D = r"D:\Ashes 2063\3D blender"
SHARP = {
    "revolver": D + r"\ashes revolver sprite\sharp\sharp_revolver.blend",
    "fal": D + r"\ashes fal sprite\sharp\sharp_fal.blend",
    "musket": D + r"\ashes musket sprite\sharp\sharp_musket.blend",
    "mq11": D + r"\ashes ingram sprite\sharp\sharp_ingram1.blend",
}
GUNS = {
    # key: (sharp blend or None, grip box (y0, y1, z0, z1) or None if the gun has one, muzzle (y, z) or None, renames,
    #       extra sharp parts moved with the cylinder (the revolver's rounds) and by how much)
    "revolver": ("revolver", None, (0.4505, -0.0782), {}, {"rounds": (0.0, -0.0045, -0.010)}),
    "fal": ("fal", (0.37, 0.47, -0.43, -0.285), (1.328, -0.208), {"charging_handle": "bolt"}, {}),
    "musket": ("musket", (0.32, 0.43, -0.38, -0.26), (1.391, -0.205), {}, {}),
    "mq11": ("mq11", (0.29, 0.40, -0.30, -0.16), (0.590, -0.115), {}, {}),
    "mq11_silenced": (None, (0.29, 0.40, -0.30, -0.16), None, {"suppressor": "body"}, {}),
    "heavy_mq11": (None, None, None, {"stock": "body"}, {}),
    "crowbar": (None, (0.075, 0.20, -1.0, 1.0), None, {}, {}),
    # the Stun Ram stands in for the JackHammer (Tefa 2026-11-16): held by the chainsaw's rear handle, the ram head
    # in front is the jackhammer job's "chisel" (it punches out on the firing frames), the throttle its "trigger"
    "stun_ram": (None, (0.03, 0.17, -0.27, -0.19), None, {}, {}),
    "sawed_off": (None, None, None, {}, {}),         # meshy_look_sawed_off.py already has every part
}
# more parts cut out of the body by a box (y0, y1, z0, z1), after the grip
BOXES = {"stun_ram": [("chisel", (0.55, 1.0, -1.0, 1.0)), ("trigger", (0.075, 0.17, -0.285, -0.24))]}


def root():
    return next(o for o in bpy.data.objects if o.type == 'EMPTY' and o.name.endswith("_root"))


def split_grip(r, box, name="grip"):
    y0, y1, z0, z1 = box
    base = r.name[:-len("_root")]
    src = bpy.data.objects[base + "_body"]
    me = src.data
    bm = bmesh.new(); bm.from_mesh(me)
    inside = [f for f in bm.faces if y0 <= (src.matrix_world @ f.calc_center_median()).y < y1
              and z0 <= (src.matrix_world @ f.calc_center_median()).z < z1]
    gm = bmesh.new()
    vmap = {}
    uvs, uvd = bm.loops.layers.uv.active, None
    if uvs is not None:
        uvd = gm.loops.layers.uv.new(uvs.name)
    for f in inside:
        vs = []
        for v in f.verts:
            if v not in vmap:
                vmap[v] = gm.verts.new(v.co)
            vs.append(vmap[v])
        nf = gm.faces.new(vs)
        nf.material_index = f.material_index
        if uvs is not None:
            for la, lb in zip(f.loops, nf.loops):
                lb[uvd].uv = la[uvs].uv
    bmesh.ops.delete(bm, geom=inside, context='FACES')
    bm.to_mesh(me); bm.free()
    gme = bpy.data.meshes.new(base + "_" + name)
    gm.to_mesh(gme); gm.free()
    for m in me.materials:
        gme.materials.append(m)
    # colour attributes on the faces (CubeKit pick meshes) are not carried; forge exports colour through UVs
    g = bpy.data.objects.new(base + "_" + name, gme)
    bpy.context.scene.collection.objects.link(g)
    g.parent = r
    g.matrix_world = src.matrix_world.copy()
    print(name + ":", len(inside), "faces")


def copy_parts(r, sharp_blend, names, offset_of):
    with bpy.data.libraries.load(sharp_blend) as (src, dst):
        sroot = next(n for n in src.objects if n.endswith("_root"))
        base = sroot[:-len("_root")]
        dst.objects = [base + "_" + n for n in names if base + "_" + n in src.objects]
    out = {}
    for o in dst.objects:
        part = o.name[len(base) + 1:]
        o.name = r.name[:-len("_root")] + "_" + part
        o["part"] = part
        bpy.context.scene.collection.objects.link(o)
        o.parent = None
        o.location = o.location + Vector(offset_of(o))
        o.parent = r
        o.matrix_parent_inverse = r.matrix_world.inverted()
        out[part] = o
    return out


def main(key, out):
    sharp, grip, muzzle, renames, extra = GUNS[key]
    r = root()
    base = r.name[:-len("_root")]
    for o in list(bpy.data.objects):
        if o.type == 'MESH' and o.name.startswith(base + "_"):
            part = o.name[len(base) + 1:]
            if part in renames:
                o["part"] = renames[part]
    if grip:
        split_grip(r, grip)
    for name, box in BOXES.get(key, []):
        split_grip(r, box, name)
    if sharp and muzzle:
        with bpy.data.libraries.load(SHARP[sharp]) as (src, dst):
            sroot = next(n for n in src.objects if n.endswith("_root"))
            dst.objects = [sroot[:-len("_root")] + "_flash_a"]
        fa = dst.objects[0]
        ys = [(fa.matrix_world @ Vector(c)).y for c in fa.bound_box]
        zs = [(fa.matrix_world @ Vector(c)).z for c in fa.bound_box]
        d = (0.0, muzzle[0] - min(ys), muzzle[1] - (min(zs) + max(zs)) / 2)
        bpy.data.objects.remove(fa)
        got = copy_parts(r, SHARP[sharp], ["flash_a", "flash_b", "flash_c"], lambda o: d)
        print("flashes:", sorted(got), "moved", tuple(round(x, 4) for x in d))
    for part, d in extra.items():
        got = copy_parts(r, SHARP[sharp], [part], lambda o, d=d: d)
        print("copied:", sorted(got))
    bpy.ops.wm.save_as_mainfile(filepath=out, copy=True)


if __name__ == "__main__":
    a = sys.argv[sys.argv.index("--") + 1:]
    main(a[0], a[1])
