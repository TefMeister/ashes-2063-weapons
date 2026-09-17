# One-off pass (2026-09-17): make the hand-built lantern file show the unlit game look.
#   blender.exe -b lantern/Ashes_2063_EP1_lantern.blend --python kit/unlit_lantern.py
# The lit version is kept as Ashes_2063_EP1_lantern_v07_lit_backup.blend.
import bpy

for m in bpy.data.materials:
    if not m.node_tree:
        continue
    N, L = m.node_tree.nodes, m.node_tree.links
    out = next((n for n in N if n.type == 'OUTPUT_MATERIAL'), None)
    bsdf = next((n for n in N if n.type == 'BSDF_PRINCIPLED'), None)
    glows = any(n.type == 'EMISSION' and n.inputs[1].default_value > 0.0 for n in N)
    if out is None or glows or bsdf is None:
        continue                                  # glow materials already look the same with no lights
    flat = N.new('ShaderNodeEmission'); flat.name = "GameColor"
    lit = bsdf.inputs['Emission Strength'].default_value > 0.0
    src = bsdf.inputs['Emission Color' if lit else 'Base Color']
    if src.links:
        L.new(src.links[0].from_socket, flat.inputs['Color'])
    else:
        flat.inputs['Color'].default_value = src.default_value
    L.new(flat.outputs[0], out.inputs['Surface'])

for o in [o for o in bpy.data.objects if o.type == 'LIGHT']:
    bpy.data.objects.remove(o)
floor = bpy.data.objects.get("Floor")
if floor:
    bpy.data.objects.remove(floor)              # it only existed to catch the lamp's light
bpy.ops.wm.save_mainfile()
print("unlit lantern saved")
