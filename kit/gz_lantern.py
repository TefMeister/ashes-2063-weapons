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
SKIP = ("Floor",)                           # the studio floor stays in Blender
GLASS_ALPHA = 0.35                          # see-through glass, drawn additively over the tube and sparks
REAL_HEIGHT = 0.26                          # metres; the Blender lantern is drawn oversized
UNITS_PER_M = 34                            # map units per metre (vr_vunits_per_meter in the VR config)
GRIP_Z = 0.21                               # the grip bar: this point sits at the hand
ATLAS = 1024                                # 256 lost the pixel textures and the weathering (2026-09-17)
MODEL_SCALE = 1.5                           # Tefa, fifth wear: twice was too big; 25% off that is the size we want
YAW_OFFSET = 30                             # was 60, turned back 30 by Tefa (fifth wear); a sixth of a turn (their "one slice of a 6-slice pizza"), counter-clockwise seen from above
LIGHT_DROP = 8                              # light sits this many units below the hand, inside the glass (scales with the model)
LIGHT_SIZE = (55, 62)                       # flicker between these radii (first wear: 110/124 was twice too big)
# The GAME lights the room with its own short-lived invisible actor spawned at the player's chest
# (Ashes' Actors/Weapons/*.txt: A_SpawnItemEx("lanternglow",0,0,8,0); its light Lantern1 is size 130,
# offset 0 36 0). That is why the room barely changed when Tefa waved the hand. We move each one to
# the lantern, so the room really is lit by what the hand is holding.
GAME_GLOW = 'LanternGlow'
GAME_GLOW_LIGHT_UP = 36                     # its light sits this far above the actor, so put the actor that far below the hand
# Ashes is played in light mode 3 ("dark", forced by its own lightmodepatch.pk3). In every Doom light mode
# except the plainest, the engine fades surfaces to black WITH DISTANCE FROM THE EYE, so whatever you stand
# next to is the brightest thing in the room: Tefa, fifth wear, *"a spotlight that follows me around"*. It is
# not a light at all, so no light source of ours can beat it. The MAPINFO map flag `nolightfade` switches that
# distance fade off and leaves the dark look alone, so only real light sources - the lantern - pick things out.
KILL_LIGHT_FADE = True                      # set False to hand the game its own eye-follow brightness back
# The game's lantern glow has three fixed brightness steps (lantern/NOTES.md): sprite frame -> glow level
FLICKER_LEVELS = [("A", 1.0), ("B", 0.75), ("C", 0.52)]
# measured order across 66 game frames, one tic each: B bright, M mid, D dim
FLICKER_ORDER = "MDBMDBDBMDBDBBBDBDBBDBMDBDBMDBBMDBMBMDDMDMDDMDMDDMDBDDMDBMDMDBMDMD"

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
    # The lamp's own UVs map every face onto the tiny 16x16 pixel textures. The game atlas needs its own
    # layout, and it must be BOTH the active layer (unwrap, export) and the render layer (bake target);
    # baking onto the old layer is what made the first exports flat.
    uv = o.data.uv_layers.new(name="GZ_Atlas")
    o.data.uv_layers.active = uv
    uv.active_render = True
bpy.context.view_layer.objects.active = meshes[0]


def pack_faces_into_atlas(objs, size, pad_px=2):
    """Own UV layout, no Blender operators (smart_project / pack_islands silently did nothing in
    background mode here): every face is laid flat at its true size and shelf-packed, so big
    surfaces get proportionally more texture than small ones."""
    rects = []                                  # [w, h, obj, poly index, [(loop, u, v)]]
    for o in objs:
        M = o.matrix_world
        me = o.data
        for poly in me.polygons:
            pts = [M @ me.vertices[me.loops[li].vertex_index].co for li in poly.loop_indices]
            n = (M.to_3x3() @ poly.normal)
            if n.length < 1e-12:
                n = Vector((0, 0, 1))
            n.normalize()
            e = next(((pts[i + 1] - pts[i]) for i in range(len(pts) - 1) if (pts[i + 1] - pts[i]).length > 1e-9), Vector((1, 0, 0)))
            u = (e - n * e.dot(n)).normalized() if (e - n * e.dot(n)).length > 1e-9 else n.orthogonal().normalized()
            v = n.cross(u)
            flat = [(q.dot(u), q.dot(v)) for q in pts]
            u0 = min(f[0] for f in flat); v0 = min(f[1] for f in flat)
            w = max(f[0] for f in flat) - u0; h = max(f[1] for f in flat) - v0
            rects.append([w, h, o, [(li, f[0] - u0, f[1] - v0) for li, f in zip(poly.loop_indices, flat)]])
    rects.sort(key=lambda r: -r[1])
    pad = pad_px / size

    def layout(density):                       # density = uv units per metre; returns placements or None
        x = y = pad; row = 0.0; out = []
        for w, h, o, loops in rects:
            rw, rh = w * density + 2 * pad, h * density + 2 * pad
            if x + rw > 1.0:
                x = pad; y += row; row = 0.0
            if x + rw > 1.0 or y + rh > 1.0:
                return None
            out.append((x + pad, y + pad)); x += rw; row = max(row, rh)
        return out

    lo, hi = 0.0, 1000.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if layout(mid) is None: hi = mid
        else: lo = mid
    places = layout(lo)
    for (w, h, o, loops), (px_, py_) in zip(rects, places):
        data = o.data.uv_layers.active.data
        for li, fu, fv in loops:
            data[li].uv = (px_ + fu * lo, py_ + fv * lo)
    print("atlas texels per metre", round(lo * size))


pack_faces_into_atlas(meshes, ATLAS)

sc.render.engine = 'CYCLES'
sc.cycles.samples = 8
img = bpy.data.images.new("GZ_LanternAtlas", ATLAS, ATLAS, alpha=False)
mask = bpy.data.images.new("GZ_LanternGlowMask", ATLAS, ATLAS, alpha=False)
bake_nodes = []     # (emission node for the bake, glow?, image node)
for m in {s.material for o in meshes for s in o.material_slots if s.material}:
    m.use_nodes = True
    N, L = m.node_tree.nodes, m.node_tree.links
    out = next((n for n in N if n.type == 'OUTPUT_MATERIAL'), None) or N.new('ShaderNodeOutputMaterial')
    bsdf = next((n for n in N if n.type == 'BSDF_PRINCIPLED'), None)
    # Glowing materials (any Emission node, or Principled emission) are baked AS THEY ARE, so the cloudy
    # glass pattern and the white-hot core come out like the Blender render. Everything else bakes its
    # base colour (pixel texture + weathering), without Blender's lighting.
    own_glow = any(n.type == 'EMISSION' and n.inputs[1].default_value > 0.0 for n in N) or         (bsdf is not None and bsdf.inputs['Emission Strength'].default_value > 0.0)
    glow = own_glow
    em = None
    if not own_glow:
        em = N.new('ShaderNodeEmission')
        if bsdf:
            src = bsdf.inputs['Base Color']
            if src.links:
                L.new(src.links[0].from_socket, em.inputs['Color'])
            else:
                em.inputs['Color'].default_value = src.default_value
        L.new(em.outputs[0], out.inputs['Surface'])
    tex = N.new('ShaderNodeTexImage'); tex.image = img; tex.interpolation = 'Closest'
    N.active = tex
    bake_nodes.append((em, glow and "Glow" in m.name, tex))
bpy.ops.object.bake(type='EMIT', margin=2, use_clear=True)
# second bake: white where the LAMP glows (materials named ...Glow), black elsewhere, so the flicker
# dims only that; the lid screen and LEDs glow steadily (Tefa, 2026-09-17)
for em, glow, tex in bake_nodes:
    nt = tex.id_data
    if em is None:
        em = nt.nodes.new('ShaderNodeEmission')
        nt.links.new(em.outputs[0], next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL').inputs['Surface'])
    for l in list(em.inputs['Color'].links):
        nt.links.remove(l)
    em.inputs['Color'].default_value = (1, 1, 1, 1) if glow else (0, 0, 0, 1)
    tex.image = mask
bpy.ops.object.bake(type='EMIT', margin=2, use_clear=True)

import numpy as np
px = np.array(img.pixels[:]).reshape(-1, 4)
gl = np.array(mask.pixels[:]).reshape(-1, 4)[:, :1] > 0.5
pngs = []
for letter, level in FLICKER_LEVELS:
    v = px.copy()
    v[:, :3] = np.where(gl, v[:, :3] * level, v[:, :3])
    im = bpy.data.images.new("GZ_Lantern_" + letter, ATLAS, ATLAS, alpha=False)
    im.pixels = v.ravel().tolist()
    path = os.path.join(OUT_DIR, f"lantern_{letter}.png")
    im.filepath_raw = path; im.file_format = 'PNG'; im.save()
    pngs.append((letter, path))

# ---- three MD3s: body (opaque), glass (see-through), sparks (one frame per lightning pattern) ----
# World models: +X forward, +Y LEFT, +Z up (the first export used +Y right, as for held weapons, and
# the keypad came out mirrored in game), grip at the origin.
zs = [(o.matrix_world @ Vector(c)).z for o in meshes if not o.name.startswith(("Bolt", "Impact")) for c in o.bound_box]
S = REAL_HEIGHT / (max(zs) - min(zs)) * UNITS_PER_M


def part_of(o):
    if o.name.startswith(("Bolt", "Impact")):
        return "sparks"
    return "glass" if o.name == "Glass" else "body"


def snapshot(part):
    dg = bpy.context.evaluated_depsgraph_get()
    verts, uvs = [], []
    for o in sorted((o for o in meshes if part_of(o) == part), key=lambda o: o.name):
        eo = o.evaluated_get(dg); me = eo.to_mesh(); M = eo.matrix_world; R = M.to_3x3()
        uvl = me.uv_layers.active.data
        for poly in me.polygons:
            n = R @ poly.normal
            n = n.normalized() if n.length > 1e-9 else Vector((0, 0, 1))
            loops = list(poly.loop_indices)
            for k in range(1, len(loops) - 1):
                for li in (loops[0], loops[k], loops[k + 1]):
                    p = M @ me.vertices[me.loops[li].vertex_index].co
                    verts.append(((p.y * S, -p.x * S, (p.z - GRIP_Z) * S), (n.y, -n.x, n.z)))
                    uvs.append(tuple(uvl[li].uv))
        eo.to_mesh_clear()
    return verts, uvs


def save_md3(name, frames, uvs):
    tris = [(i, i + 1, i + 2) for i in range(0, len(uvs), 3)]
    path = os.path.join(OUT_DIR, name + ".md3")
    print("md3", name, write_md3(path, name, frames, (tris, uvs), f"{MODEL_PATH}/lantern_A.png"))
    return path


sc.frame_set(sc.frame_start)
md3s = []
for part in ("body", "glass"):
    v, uv = snapshot(part)
    md3s.append(save_md3("lantern_" + part, [v], uv))

# Lightning: walk the whole Blender loop; every distinct picture becomes one model frame, and the
# game plays them back with the same timing (one Blender frame = one tic).
spark_objs = [o for o in meshes if part_of(o) == "sparks"]
patterns, timeline, frames, spark_uvs = {}, [], [], None
for f in range(sc.frame_start, sc.frame_end + 1):
    sc.frame_set(f)
    key = tuple(o.name for o in spark_objs if min(abs(c) for c in o.scale) > 1e-4)
    if key not in patterns:
        v, uv = snapshot("sparks")
        spark_uvs = spark_uvs or uv
        patterns[key] = len(frames); frames.append(v)
    if timeline and timeline[-1][0] == patterns[key]:
        timeline[-1][1] += 1
    else:
        timeline.append([patterns[key], 1])
md3s.append(save_md3("lantern_sparks", frames, spark_uvs))
print("lightning pictures", len(frames), "timeline steps", len(timeline))


def spr(i):        # model frame -> (sprite name, frame letter); 26 letters per sprite name
    return "LHS" + "ABCDEFGHIJ"[i // 26], "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i % 26]


ZSCRIPT = '''version "4.10"
// Left-hand lantern test. Needs the GZDoomVR build that gives mods OffhandValid / OffhandPos / OffhandAngle.
class TefaLeftHandLantern : Actor
{
	Default { +NOGRAVITY +NOBLOCKMAP +NOINTERACTION +DONTSPLASH +NOTONAUTOMAP }
	States { Spawn:
FLICKER_STATES		Loop; }
}
class TefaLeftHandLanternGlass : TefaLeftHandLantern
{
	Default { RenderStyle "Add"; Alpha GLASS_ALPHA_VALUE; }
	States { Spawn: LHLG A -1 Bright; Stop; }
}
class TefaLeftHandLanternSparks : TefaLeftHandLantern
{
	Default { RenderStyle "Add"; }
	States { Spawn:
SPARK_STATES		Loop; }
}
class TefaLeftHandHandler : EventHandler
{
	Actor parts[3];
	Array<Actor> gameglows;		// the game's own room light, caught at spawn and moved to the hand
	override void WorldThingSpawned(WorldEvent e)
	{
		if (e.Thing && e.Thing.GetClassName() == 'GAME_GLOW_NAME') gameglows.Push(e.Thing);
	}
	override void WorldTick()
	{
		static const Class<Actor> kinds[] = { "TefaLeftHandLantern", "TefaLeftHandLanternGlass", "TefaLeftHandLanternSparks" };
		let pmo = players[consoleplayer].mo;
		if (!pmo) return;
		// The game's own "the lantern is lit" flag, toggled by the lantern/zoom key. Without this
		// the lantern was welded to the left hand for ever, so it could not be put away and the
		// off hand was never free -- which is exactly what stopped a rifle being held with both
		// hands [reported 2026-09-19, n=1 wear].
		bool lit = pmo.CountInv("lightlit") > 0;
		for (int i = 0; i < 3; i++)
		{
			if (!pmo.OffhandValid || !lit) { if (parts[i]) parts[i].bInvisible = true; continue; }
			if (!parts[i])
			{
				parts[i] = Actor.Spawn(kinds[i], pmo.OffhandPos);
				parts[i].FollowOffhand = true;		// the engine draws it locked to the hand on every rendered frame
			}
			parts[i].bInvisible = false;
			parts[i].SetOrigin(pmo.OffhandPos, true);	// game-side position (light, sector); the drawing ignores it
			parts[i].angle = pmo.OffhandAngle;
		}
		// Keep the game's own lantern light on the lantern instead of on the player's chest, every tic,
		// so the room lights from wherever the hand is pointing it.
		for (int i = gameglows.Size() - 1; i >= 0; i--)
		{
			let g = gameglows[i];
			if (!g || g.bDestroyed) { gameglows.Delete(i); continue; }
			if (pmo.OffhandValid && lit)
				g.SetOrigin((pmo.OffhandPos.X, pmo.OffhandPos.Y, pmo.OffhandPos.Z - GLOW_LIFT), true);
		}
	}
}
'''
def model_block(actor, md3name, skin, sprite, letter, frame):
    lines = [f"Model {actor}", "{", f'   Path "{MODEL_PATH}"', f'   Model 0 "{md3name}.md3"', f'   Skin 0 "{skin}"',
             f"   Scale {MODEL_SCALE} {MODEL_SCALE} {MODEL_SCALE}", f"   AngleOffset {YAW_OFFSET}",
             f"   FrameIndex {sprite} {letter} 0 {frame}", "}", ""]
    return chr(10).join(lines)


MODELDEF = "".join(model_block("TefaLeftHandLantern", "lantern_body", f"lantern_{l}.png", "LHLN", l, 0) for l, _ in FLICKER_LEVELS)
MODELDEF += model_block("TefaLeftHandLanternGlass", "lantern_glass", "lantern_A.png", "LHLG", "A", 0)
MODELDEF += "".join(model_block("TefaLeftHandLanternSparks", "lantern_sparks", "lantern_A.png", *spr(i), i) for i in range(len(frames)))
GLDEFS = f'''flickerlight2 TEFALEFTLANTERN
{{
    color 0.72 0.85 1.0
    size {LIGHT_SIZE[0]}
    secondarySize {LIGHT_SIZE[1]}
    interval 0.08
    offset 0 -{LIGHT_DROP} 0
}}
object TefaLeftHandLantern {{ frame LHLN {{ light TEFALEFTLANTERN }} }}
'''
MAPINFO = 'GameInfo { AddEventHandlers = "TefaLeftHandHandler" }\n'
if KILL_LIGHT_FADE:
    MAPINFO += 'gamedefaults { nolightfade }\n'


def _chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)


# 1x1 transparent PNG: MODELDEF needs the sprite name to exist
PIXEL = (bytes([0x89]) + b"PNG\r\n" + bytes([0x1A]) + b"\n"
         + _chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0))
         + _chunk(b"IDAT", zlib.compress(bytes(5))) + _chunk(b"IEND", b""))

frame_of = {"B": "A", "M": "B", "D": "C"}
ZSCRIPT = ZSCRIPT.replace("FLICKER_STATES", "".join("\t\tLHLN " + frame_of[c] + " 1 Bright;\n" for c in FLICKER_ORDER))
ZSCRIPT = ZSCRIPT.replace("GLASS_ALPHA_VALUE", str(GLASS_ALPHA))
ZSCRIPT = ZSCRIPT.replace("GAME_GLOW_NAME", GAME_GLOW).replace("GLOW_LIFT", str(GAME_GLOW_LIGHT_UP))
ZSCRIPT = ZSCRIPT.replace("SPARK_STATES", "".join("\t\t%s %s %d Bright;\n" % (*spr(i), n) for i, n in timeline))
with zipfile.ZipFile(os.path.join(OUT_DIR, PK3), "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("zscript.txt", ZSCRIPT); z.writestr("modeldef.lantern", MODELDEF)
    z.writestr("gldefs.lantern", GLDEFS); z.writestr("mapinfo.lantern", MAPINFO)
    for path in md3s:
        z.write(path, f"{MODEL_PATH}/{os.path.basename(path)}")
    z.writestr("sprites/LHLGA0.png", PIXEL)
    for i in range(len(frames)):
        z.writestr("sprites/%s%s0.png" % spr(i), PIXEL)
    for letter, path in pngs:
        z.writestr(f"sprites/LHLN{letter}0.png", PIXEL)
        z.write(path, f"{MODEL_PATH}/lantern_{letter}.png")
print("pk3", os.path.join(OUT_DIR, PK3))
