# GZDoom needs an image texture, not Blender node textures. After a model is built:
# 1) give every mesh one shared UV layout (one atlas), 2) save the model .blend,
# 3) bake each material's base colour into the atlas PNG. Step 3 rewires materials,
# so the .blend is saved BEFORE it and never after.
import os

ATLAS_SIZE = 512
ISLAND_MARGIN = 0.004


def atlas_uvs():
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    for o in meshes:
        o.hide_viewport = False
        o.hide_set(False)
    bpy.ops.object.select_all(action='DESELECT')
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=ISLAND_MARGIN)
    bpy.ops.object.mode_set(mode='OBJECT')
    return meshes


def bake_atlas(meshes, png_path):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = 1
    img = bpy.data.images.new("GZ_Atlas", ATLAS_SIZE, ATLAS_SIZE, alpha=False)
    for m in {s.material for o in meshes for s in o.material_slots if s.material}:
        N, L = m.node_tree.nodes, m.node_tree.links
        # pixel_mat materials are already a plain Emission shader ("GameColor"): bake them as they are
        tex = N.new('ShaderNodeTexImage'); tex.image = img; tex.interpolation = 'Closest'
        N.active = tex
    for o in meshes:
        o.hide_render = o.hide_viewport = False
        o.hide_set(False)
        o.select_set(True)
    bpy.ops.object.bake(type='EMIT', margin=2, use_clear=True)
    os.makedirs(os.path.dirname(png_path), exist_ok=True)
    img.filepath_raw = png_path
    img.file_format = 'PNG'
    img.save()
    print("baked", png_path)


def uv_save_bake(blend_path, png_path):
    hidden = {o.name: (o.hide_viewport, o.hide_render) for o in bpy.context.scene.objects}
    meshes = atlas_uvs()
    for o in bpy.context.scene.objects:
        o.hide_viewport, o.hide_render = hidden[o.name]
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print("saved", blend_path)
    bake_atlas(meshes, png_path)
