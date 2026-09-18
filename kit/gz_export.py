# Export a weapon's animation files to GZDoom: one MD3 with every frame, the baked
# atlas, a MODELDEF mapping game sprite frames to model frames, and a test .pk3.
#   blender.exe -b --factory-startup --python kit/gz_export.py -- gz_revolver.py [flat|vr]
import bpy, sys, os, zipfile
from mathutils import Vector, Matrix, Quaternion

KIT = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[sys.argv.index("--") + 1:]
exec(open(os.path.join(KIT, "gz_md3.py")).read())
VARIANT = args[1] if len(args) > 1 else "flat"      # "flat" (screen) or "vr" (controller)
exec(open(os.path.join(KIT, args[0])).read())


VIEW = globals().get("SPACE", "hand") == "view"
O = (0.0, 0.0, 0.0) if VIEW else ORIGIN


def to_md3(p):
    # GZDoom draws MD3 +Y on the viewer's RIGHT (hh79/gzdoomvr gvr4.13.2.2, models.cpp) [verified-live 2026-09-17]:
    # writing -x mirrored the gun, so the cylinder swung out to the right in game.
    return ((p.y - O[1]) * UNITS_PER_M, (p.x - O[0]) * UNITS_PER_M, (p.z - O[2]) * UNITS_PER_M)


def gather(blend, want, rest, want_uvs, motion_scale=1.0):
    """The wanted frames of one animation file, in the root's rest space."""
    bpy.ops.wm.open_mainfile(filepath=blend)
    sc = bpy.context.scene
    objs = sorted((o for o in sc.objects if o.type == 'MESH'), key=lambda o: o.name)
    frames, uvs = [], []
    for f in want:
        sc.frame_set(f)
        dg = bpy.context.evaluated_depsgraph_get()
        if rest is None:
            # "view": keep the Blender first-person camera space (camera at the origin, looking +Y);
            # "hand": relative to the gun's rest pose, for attaching to a VR controller
            rest = Matrix.Identity(4) if VIEW else sc.objects[ROOT].matrix_world.copy()
        inv = rest.inverted()
        k = motion_scale
        if k != 1.0:
            # shrink how far the whole gun moves away from its rest pose (parts still move fully)
            D = rest.inverted() @ sc.objects[ROOT].matrix_world
            q = Quaternion().slerp(D.to_quaternion(), k)
            D_small = Matrix.Translation(D.to_translation() * k) @ q.to_matrix().to_4x4()
            inv = D_small @ D.inverted() @ rest.inverted()
        verts = []
        for o in objs:
            eo = o.evaluated_get(dg)
            me = eo.to_mesh()
            M = inv @ eo.matrix_world
            R = M.to_3x3()
            shown = not o.hide_render
            centre = M @ Vector((0, 0, 0))
            uvl = me.uv_layers.active.data
            for poly in me.polygons:
                n = (R @ poly.normal).normalized()
                loops = list(poly.loop_indices)
                for k in range(1, len(loops) - 1):
                    # HUD models are not back-face culled, so one copy per triangle is enough.
                    # The x -> md3 Y mapping is a mirror, so the winding is reversed to match.
                    for li in (loops[0], loops[k + 1], loops[k]):
                        p = M @ me.vertices[me.loops[li].vertex_index].co if shown else centre
                        verts.append((to_md3(p), (n.y, n.x, n.z)))
                        if want_uvs and f == 1:
                            uvs.append(tuple(uvl[li].uv))
            eo.to_mesh_clear()
        frames.append(verts)
    return frames, uvs, rest


# An animation entry is (name, file, N) for frames 1..N, or (name, file, [frames]) to export only
# the ones MODELDEF actually shows. The shotgun uses the second form: 194 frames of a gun that size
# would be a ~30 MB model in the repo, and the game can only ever display the ~45 that sprite
# letters point at.
# ⚠️ For a VR build every frame is expressed relative to the root's REST pose, and by default
# that is taken from the first frame of the first animation. That is only correct if frame 1 is
# the gun at rest. The revolver's is; the shotgun's frame 1 is the SHOT, kicked 8 degrees nose-up
# -- so the whole gun came out 8 degrees nose-DOWN in the hand and shot above where it pointed
# [verified-live 2026-09-19, n=1 wear: "aiming below where the red dot is"].
# REST_FRAME = (animation name, frame) names the neutral pose instead.
all_frames, uvs, rest, index_of = [], None, None, {}
REST_FRAME = globals().get("REST_FRAME")
if REST_FRAME and not VIEW:
    _name, _fr = REST_FRAME
    _blend = {n: b for n, b, _ in ANIMS}[_name]
    bpy.ops.wm.open_mainfile(filepath=_blend)
    bpy.context.scene.frame_set(_fr)
    bpy.context.view_layer.update()
    rest = bpy.context.scene.objects[ROOT].matrix_world.copy()
    print(f"rest pose taken from {_name} frame {_fr}")
for name, blend, spec in ANIMS:
    want = list(range(1, spec + 1)) if isinstance(spec, int) else list(spec)
    for i, f in enumerate(want):
        index_of[(name, f)] = len(all_frames) + i
    fr, uv, rest = gather(blend, want, rest, uvs is None, globals().get("GUN_MOTION_SCALE", {}).get(name, 1.0))
    if uvs is None:
        uvs = uv
    assert len(fr[0]) == len(uvs), f"{name}: vertex count differs from the first animation"
    all_frames += fr

os.makedirs(OUT_DIR, exist_ok=True)
md3_path = os.path.join(OUT_DIR, NAME + ".md3")
tris = [(i, i + 1, i + 2) for i in range(0, len(uvs), 3)]
nsurf, nv, nt = write_md3(md3_path, NAME, all_frames, (tris, uvs), f"{MODEL_PATH}/{NAME}.png")
print(f"md3: {len(all_frames)} frames, {nsurf} surfaces, {nv} verts, {nt} tris")

# ⚠️ The name after `Model` is the ACTOR CLASS, not the file. It only looked like the file for
# the revolver because Ashes happens to call that actor `revolver`. The shotgun's class is
# `pumpaction`, and getting this wrong shows the flat sprite with no error at all
# [verified-live 2026-09-19, n=1 launch].
ACTOR_CLASS = globals().get("ACTOR_CLASS", NAME)
lines = [f"// Generated by kit/gz_export.py from kit/{args[0]}. Do not edit by hand.",
         f"Model {ACTOR_CLASS}", "{", f'   Path "{MODEL_PATH}"', f'   Model 0 "{NAME}.md3"', f'   Skin 0 "{NAME}.png"']
lines += [f'   SurfaceSkin 0 {i} "{NAME}.png"' for i in range(nsurf)]
lines += ["   Scale 1.0 1.0 1.0", "   NOINTERPOLATION", ""]
for spr, letter, anim, frame in SPRITES:
    assert (anim, frame) in index_of, f"{spr} {letter}: frame {frame} of {anim} was not exported"
lines += [f"   FrameIndex {spr} {letter} 0 {index_of[(anim, frame)]}" for spr, letter, anim, frame in SPRITES]
lines += ["}"]
modeldef = "\n".join(lines) + "\n"
with open(os.path.join(OUT_DIR, "modeldef." + NAME + ".txt"), "w") as f:
    f.write(modeldef)

pk3 = os.path.join(OUT_DIR, PK3)
with zipfile.ZipFile(pk3, "w", zipfile.ZIP_DEFLATED) as z:
    # Anything else the weapon's config wants inside the pk3 (ZScript, MAPINFO, ...), as
    # {path inside the pk3: text}. The shotgun uses it to switch two-handed aiming on.
    for lump, text in globals().get("EXTRA_LUMPS", {}).items():
        z.writestr(lump, text)
    z.writestr("modeldef." + NAME, modeldef)
    z.write(md3_path, f"{MODEL_PATH}/{NAME}.md3")
    z.write(os.path.join(OUT_DIR, NAME + ".png"), f"{MODEL_PATH}/{NAME}.png")
print("pk3", pk3)
