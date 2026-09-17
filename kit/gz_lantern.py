# Export the lantern as a WORLD model (an object in the level, not a held-weapon model) for the
# left-hand test: needs our GZDoomVR build, which tells mods where the off hand is.
#   blender.exe -b lantern/Ashes_2063_EP1_lantern.blend --python kit/gz_lantern.py
# Writes lantern/gzdoom/: lantern.md3, lantern.png and Ashes2063_lefthand_lantern_test.pk3.
import bpy, os, math, zipfile, struct, zlib
from mathutils import Vector

KIT = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(KIT, "gz_md3.py")).read())

OUT_DIR = os.path.join(KIT, "..", "lantern", "gzdoom")
PK3 = "Ashes2063_lefthand_lantern_test.pk3"
MODEL_PATH = "models/ashes2063/lantern"
SKIP = ("Floor", "Impact", "Bolt")          # studio floor and lightning effects stay in Blender
REAL_HEIGHT = 0.26                          # metres; the Blender lantern is drawn oversized
UNITS_PER_M = 34                            # map units per metre (vr_vunits_per_meter in the VR config)
GRIP_Z = 0.21                               # the grip bar: this point sits at the hand
ATLAS = 256
LIGHT_DROP = 5                              # light sits this many units below the hand, inside the glass

os.makedirs(OUT_DIR, exist_ok=True)
sc = bpy.context.scene
sc.frame_set(sc.frame_start)

# ---- curves (the bail handle) become meshes; drop what is not part of the lamp ----
for o in list(sc.objects):
    if o.name.startswith(SKIP) or o.type in ('LIGHT', 'CAMERA'):
        bpy.data.objects.remove(o)
for o in [o for o in sc.objects if o.type == 'CURVE']:
    bpy.ops.object.select_all(action='DESELECT')
    o.hide_viewport = False; o.hide_set(False); o.select_set(True)
    bpy.context.view_layer.objects.active = o
    bpy.ops.object.convert(target='MESH')
meshes = [o for o in sc.objects if o.type == 'MESH']

# ---- one shared UV atlas, then bake each material's visible colour into it ----
bpy.ops.object.select_all(action='DESELECT')
for o in meshes:
    o.hide_viewport = o.hide_render = False; o.hide_set(False); o.select_set(True)
    if not o.data.materials:
        o.data.materials.append(bpy.data.materials.new("L_Fallback"))
bpy.context.view_layer.objects.active = meshes[0]
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.01)
bpy.ops.object.mode_set(mode='OBJECT')

sc.render.engine = 'CYCLES'
sc.cycles.samples = 1
img = bpy.data.images.new("GZ_LanternAtlas", ATLAS, ATLAS, alpha=False)
for m in {s.material for o in meshes for s in o.material_slots if s.material}:
    m.use_nodes = True
    N, L = m.node_tree.nodes, m.node_tree.links
    out = next((n for n in N if n.type == 'OUTPUT_MATERIAL'), None) or N.new('ShaderNodeOutputMaterial')
    bsdf = next((n for n in N if n.type == 'BSDF_PRINCIPLED'), None)
    em = N.new('ShaderNodeEmission')
    if bsdf:
        glow = bsdf.inputs['Emission Strength'].default_value > 0.0
        src = bsdf.inputs['Emission Color' if glow else 'Base Color']
        if src.links:
            L.new(src.links[0].from_socket, em.inputs['Color'])
        else:
            em.inputs['Color'].default_value = src.default_value
    L.new(em.outputs[0], out.inputs['Surface'])
    tex = N.new('ShaderNodeTexImage'); tex.image = img; tex.interpolation = 'Closest'
    N.active = tex
bpy.ops.object.bake(type='EMIT', margin=2, use_clear=True)
png = os.path.join(OUT_DIR, "lantern.png")
img.filepath_raw = png; img.file_format = 'PNG'; img.save()

# ---- one-frame MD3: +X forward, +Y right (this engine), +Z up, grip at the origin ----
zs = [(o.matrix_world @ Vector(c)).z for o in meshes for c in o.bound_box]
S = REAL_HEIGHT / (max(zs) - min(zs)) * UNITS_PER_M
dg = bpy.context.evaluated_depsgraph_get()
verts, uvs = [], []
for o in meshes:
    eo = o.evaluated_get(dg); me = eo.to_mesh(); M = eo.matrix_world; R = M.to_3x3()
    uvl = me.uv_layers.active.data
    for poly in me.polygons:
        n = (R @ poly.normal).normalized()
        loops = list(poly.loop_indices)
        for k in range(1, len(loops) - 1):
            for li in (loops[0], loops[k + 1], loops[k]):
                p = M @ me.vertices[me.loops[li].vertex_index].co
                verts.append(((p.y * S, p.x * S, (p.z - GRIP_Z) * S), (n.y, n.x, n.z)))
                uvs.append(tuple(uvl[li].uv))
    eo.to_mesh_clear()
tris = [(i, i + 1, i + 2) for i in range(0, len(uvs), 3)]
md3 = os.path.join(OUT_DIR, "lantern.md3")
print("md3", write_md3(md3, "lantern", [verts], (tris, uvs), f"{MODEL_PATH}/lantern.png"), "scale", round(S, 2))

ZSCRIPT = '''version "4.10"
// Left-hand lantern test. Needs the GZDoomVR build that gives mods OffhandValid / OffhandPos / OffhandAngle.
class TefaLeftHandLantern : Actor
{
	Default { +NOGRAVITY +NOBLOCKMAP +NOINTERACTION +DONTSPLASH +NOTONAUTOMAP }
	States { Spawn: LHLN A -1 Bright; Stop; }
}
class TefaLeftHandHandler : EventHandler
{
	Actor lamp;
	override void WorldTick()
	{
		let pmo = players[consoleplayer].mo;
		if (!pmo) return;
		if (!pmo.OffhandValid) { if (lamp) lamp.bInvisible = true; return; }
		if (!lamp) lamp = Actor.Spawn("TefaLeftHandLantern", pmo.OffhandPos);
		lamp.bInvisible = false;
		lamp.SetOrigin(pmo.OffhandPos, true);
		lamp.angle = pmo.OffhandAngle;		// it hangs from its handle, so it stays upright and only turns
	}
}
'''
MODELDEF = f'''Model TefaLeftHandLantern
{{
   Path "{MODEL_PATH}"
   Model 0 "lantern.md3"
   Skin 0 "lantern.png"
   Scale 1.0 1.0 1.0
   FrameIndex LHLN A 0 0
}}
'''
GLDEFS = f'''flickerlight2 TEFALEFTLANTERN
{{
    color 1.0 0.78 0.45
    size 110
    secondarySize 124
    interval 0.08
    offset 0 -{LIGHT_DROP} 0
}}
object TefaLeftHandLantern {{ frame LHLN {{ light TEFALEFTLANTERN }} }}
'''
MAPINFO = 'GameInfo { AddEventHandlers = "TefaLeftHandHandler" }\n'


def _chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


# 1x1 transparent PNG: MODELDEF needs the sprite name to exist
PIXEL = (bytes([0x89]) + b"PNG\r\n" + bytes([0x1A]) + b"\n"
         + _chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0))
         + _chunk(b"IDAT", zlib.compress(bytes(5))) + _chunk(b"IEND", b""))

with zipfile.ZipFile(os.path.join(OUT_DIR, PK3), "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("zscript.txt", ZSCRIPT); z.writestr("modeldef.lantern", MODELDEF)
    z.writestr("gldefs.lantern", GLDEFS); z.writestr("mapinfo.lantern", MAPINFO)
    z.writestr("sprites/LHLNA0.png", PIXEL)
    z.write(md3, f"{MODEL_PATH}/lantern.md3"); z.write(png, f"{MODEL_PATH}/lantern.png")
print("pk3", os.path.join(OUT_DIR, PK3))
