# Shared helpers for the animation files. Each animation file LINKS its weapon's
# model file (so model fixes flow into every animation) and makes an editable
# override of it to animate. All keys are CONSTANT: stop-motion, no in-betweens.
exec(open(r"C:\Users\TD3KX\github-backups\ashes-2063-weapons\kit\pixel_kit.py").read())

VIEW_LENS = 32          # first-person camera lens (mm)


def link_model(blend_path, coll_name):
    with bpy.data.libraries.load(blend_path, link=True, relative=True) as (src, dst):
        dst.collections = [coll_name]
    linked = dst.collections[0]
    sc = bpy.context.scene
    sc.collection.children.link(linked)
    ov = linked.override_hierarchy_create(sc, bpy.context.view_layer, do_fully_editable=True)
    try:
        sc.collection.children.unlink(linked)
    except RuntimeError:
        pass
    objs = {o.name: o for o in ov.all_objects}
    return ov, objs


def fp_view(cam_loc=(0, 0, 0), lens=VIEW_LENS):
    """First-person camera at cam_loc looking down +Y. No lights: materials are unlit."""
    c = bpy.context.scene.collection
    cam = bpy.data.cameras.new("ViewCam"); cam.lens = lens
    cam.clip_start = 0.01
    co = bpy.data.objects.new("ViewCam", cam); c.objects.link(co)
    co.location = cam_loc
    co.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.scene.camera = co
    return co


def key(obj, frame, loc=None, rot_deg=None, hide=None, energy=None, scale=None):
    if loc is not None:
        obj.location = loc
        obj.keyframe_insert("location", frame=frame)
    if rot_deg is not None:
        obj.rotation_euler = [math.radians(a) for a in rot_deg]
        obj.keyframe_insert("rotation_euler", frame=frame)
    if scale is not None:
        obj.scale = scale
        obj.keyframe_insert("scale", frame=frame)
    if hide is not None:
        obj.hide_viewport = obj.hide_render = hide
        obj.keyframe_insert("hide_viewport", frame=frame)
        obj.keyframe_insert("hide_render", frame=frame)
    if energy is not None:
        obj.data.energy = energy
        obj.data.keyframe_insert("energy", frame=frame)


def all_constant():
    for act in bpy.data.actions:
        curves = list(getattr(act, "fcurves", []) or [])
        for layer in getattr(act, "layers", []):
            for strip in layer.strips:
                for bag in strip.channelbags:
                    curves += list(bag.fcurves)
        for fc in curves:
            for k in fc.keyframe_points:
                k.interpolation = 'CONSTANT'


def finish(path, frame_end):
    all_constant()
    sc = bpy.context.scene
    sc.frame_start, sc.frame_end = 1, frame_end
    sc.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=path, relative_remap=True)
    print("saved", path)


def render_frames(frames, prefix, res=(640, 480)):
    sc = bpy.context.scene
    old = (sc.render.resolution_x, sc.render.resolution_y, sc.render.filepath)
    sc.render.resolution_x, sc.render.resolution_y = res
    for f in frames:
        sc.frame_set(f)
        sc.render.filepath = f"{prefix}_{f:03d}.png"
        bpy.ops.render.render(write_still=True)
    sc.render.resolution_x, sc.render.resolution_y, sc.render.filepath = old


def side_view(root, cam_offset, look_offset, lens=50):
    """Extra camera beside the weapon that shows all of it; used as the active
    camera in the "_static" files so parts moving outside the player's view show."""
    bpy.context.scene.frame_set(1)
    bpy.context.view_layer.update()
    M = root.matrix_world
    cam = bpy.data.cameras.new("SideCam"); cam.lens = lens; cam.clip_start = 0.01
    co = bpy.data.objects.new("SideCam", cam)
    bpy.context.scene.collection.objects.link(co)
    co.location = M @ Vector(cam_offset)
    co.rotation_euler = (M @ Vector(look_offset) - co.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = co
    return co


def local_at(obj, frame, world_pos):
    """Where a child of obj must sit at this frame to be at world_pos (world space).
    Keys on obj must already exist; they are made CONSTANT first so in-between frames are right."""
    all_constant()
    bpy.context.scene.frame_set(frame)
    bpy.context.view_layer.update()
    return obj.matrix_world.inverted() @ Vector(world_pos)


def world_at(obj, frame, local_pos):
    all_constant()
    bpy.context.scene.frame_set(frame)
    bpy.context.view_layer.update()
    return obj.matrix_world @ Vector(local_pos)
