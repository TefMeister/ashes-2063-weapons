"""Plays a sharp cube gun's game animation in Blender, tic for tic (35 a second), from its export job, so Tefa can
watch it before it goes into the game (2026-11-04; the pump's kick_preview.py made general). Run from the GUI:
    blender <gun.blend> --python anim_preview.py -- <job module, e.g. make_job_sawed_off> <job.json>
The job module's SEQUENCE lists (sprite, letter, tics). Every model of the job.json poses its parts as the game will:
offsets, hinge turns (seven numbers), hidden parts hidden, and the whole gun's kick ("*") round the hand.
Space plays it (it loops).
"""
import importlib
import json
import math
import os
import sys

import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[sys.argv.index("--") + 1:]
mod = importlib.import_module(args[0])
job = json.load(open(args[1]))

sc = bpy.context.scene
root = next(o for o in sc.objects if o.type == 'EMPTY' and o.name.endswith("_root"))
pre = root.name[:-len("root")]
parts = {o.name[len(pre):]: o for o in sc.objects if o.type == 'MESH' and o.name.startswith(pre)}
home = {n: o.location.copy() for n, o in parts.items()}
owner = {p: j for j in job.values() for p in j.get("parts", [])}
hidden = {p for j in job.values() for p in j.get("hidden_parts", [])}

# the hand: the middle of the grip, as gz_forge_export.py measures it
g = parts["grip"]
pts = [g.matrix_world @ Vector(c) for c in g.bound_box]
GRIP = sum(pts, Vector()) / len(pts)
pivot = bpy.data.objects.get("kick_pivot") or bpy.data.objects.new("kick_pivot", None)
if pivot.name not in sc.collection.objects:
    sc.collection.objects.link(pivot)
pivot.location = GRIP
root.parent = pivot
root.location = -GRIP
for o in [pivot] + list(parts.values()):
    o.animation_data_clear()

sc.render.fps = 35
f = 1
for spr, L, tics in mod.SEQUENCE:
    fr = f"{spr} {L}"
    kick = (0.0, 0.0)
    pose_of = {}
    for j in job.values():
        pz = j["poses"][j.get("frame_pose", {}).get(fr, 0)]
        kick = tuple(pz.get("*", kick))
        pose_of.update({p: v for p, v in pz.items() if p != "*"})
    for t in range(tics):
        pivot.location = GRIP + Vector((0.0, -kick[0], 0.0))
        pivot.rotation_euler = (math.radians(kick[1]), 0.0, 0.0)
        pivot.keyframe_insert("location", frame=f)
        pivot.keyframe_insert("rotation_euler", frame=f)
        for n, o in parts.items():
            d = pose_of.get(n) if n in owner else None
            loc, rot = home[n].copy(), 0.0
            if d:
                if len(d) == 7:
                    h, rot = Vector(d[4:7]), math.radians(d[3])
                    loc = h + Matrix.Rotation(rot, 3, 'X') @ (loc - h)
                loc = loc + Vector(d[:3])
            o.location = loc
            o.rotation_euler = (rot, 0.0, 0.0)
            o.keyframe_insert("location", frame=f)
            o.keyframe_insert("rotation_euler", frame=f)
            o.hide_viewport = o.hide_render = n in hidden and d is None
            o.keyframe_insert("hide_viewport", frame=f)
            o.keyframe_insert("hide_render", frame=f)
        f += 1
for o in [pivot] + list(parts.values()):
    ad = o.animation_data
    if ad and ad.action:
        # one pose per tic, as the game shows it (Blender 5 keeps the curves in layers, strips and channel bags)
        bags = [cb for lay in ad.action.layers for st in lay.strips for cb in st.channelbags]
        for fc in [fc for cb in bags for fc in cb.fcurves]:
            for k in fc.keyframe_points:
                k.interpolation = 'CONSTANT'
sc.frame_start, sc.frame_end = 1, f - 1
sc.frame_set(1)
print("ANIM PREVIEW:", f - 1, "frames at 35 fps")


def show():
    """Colours on, helpers out of sight, the gun's left side (what the player sees), playing."""
    from mathutils import Euler
    for o in sc.objects:
        if o.type == 'EMPTY':
            o.empty_display_size = 0.001
    for win in bpy.context.window_manager.windows:
        for area in win.screen.areas:
            if area.type != 'VIEW_3D':
                continue
            sp = area.spaces.active
            sp.shading.type, sp.shading.light, sp.shading.color_type = 'SOLID', 'FLAT', 'TEXTURE'
            ov = sp.overlay
            ov.show_floor = ov.show_axis_x = ov.show_axis_y = ov.show_cursor = ov.show_extras = False
            ov.show_relationship_lines = False
            r3d = sp.region_3d
            r3d.view_perspective = 'PERSP'
            r3d.view_location = GRIP + Vector((0.0, 0.2, 0.05))
            r3d.view_rotation = Euler((math.radians(75), 0, math.radians(-110)), 'XYZ').to_quaternion()
            r3d.view_distance = 0.75
            with bpy.context.temp_override(window=win, area=area):
                if not bpy.context.screen.is_animation_playing:
                    bpy.ops.screen.animation_play()
            return None
    return None


bpy.app.timers.register(show, first_interval=1.0)


def start_mcp():
    try:
        bpy.ops.blendermcp.start_server()
    except Exception as e:  # noqa: BLE001
        print("MCP not started:", e)
    return None


bpy.app.timers.register(start_mcp, first_interval=2.0)
