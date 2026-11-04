"""Opens the sharp cube shotgun in Blender with the game's shot and pump played tic for tic (35 a second), kick
included, so Tefa can watch it and say how much kick (2026-11-04). Run from the GUI:
    blender <sharp_cube_pump.blend> --python kick_preview.py
Space plays it (it loops). Kick sizes live in make_job_sharp.KICK; change them there and run again.
"""
import math
import os
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_job_sharp as mj  # noqa: E402

GRIP = Vector((0.0, 0.105, -0.17))        # the hand (gz_forge_export.py measures it from the stock: printed on export)
# Shotgun.txt, pumpaction: FireReal then Pump, as (sprite, letter, tics); then a rest so the loop reads as shots
SEQUENCE = ([("GRIZ", "A", 20), ("GRIF", "A", 1), ("GRIF", "B", 1), ("GRIF", "C", 1), ("GRIP", "C", 4),
             ("GRIP", "B", 2), ("GRIP", "A", 5)]
            + [("GRIP", L, 1) for L in "ABCDEFG"] + [("GRIP", "H", 3)] + [("GRIP", L, 2) for L in "IJKLM"]
            + [("GRIZ", "A", 15)]
            # then a dry reload (Reloadpump after its pump cycle, one Reloadloop shell, ReloadDone)
            + [("GRIR", L, 2) for L in "ABCDEF"] + [("GRIR", "H", 4), ("GRIR", "I", 3), ("GRIR", "J", 6),
                                                    ("GRIR", "K", 2), ("GRIR", "L", 2), ("GRIR", "M", 2),
                                                    ("GRIR", "N", 8), ("GRIR", "O", 2), ("GRIR", "P", 6)]
            + [("GRIR", L, 2) for L in "PQRS"] + [("GRIR", L, 1) for L in "TUV"]
            + [("GRIR", "W", 2), ("GRIR", "X", 1), ("GRIR", "Y", 1), ("GRIR", "P", 3), ("GRIR", "Z", 3)]
            + [("GRIR", L, 2) for L in "EDCB"] + [("GRIR", "A", 1), ("GRIZ", "A", 20)])

sc = bpy.context.scene
root = next(o for o in sc.objects if o.type == 'EMPTY' and o.name.endswith("_root"))
pre = root.name[:-len("root")]
parts = {o.name[len(pre):]: o for o in sc.objects if o.type == 'MESH' and o.name.startswith(pre)}
home = {n: o.location.copy() for n, o in parts.items()}

pivot = bpy.data.objects.get("kick_pivot") or bpy.data.objects.new("kick_pivot", None)
if pivot.name not in sc.collection.objects:
    sc.collection.objects.link(pivot)
pivot.location = GRIP
root.parent = pivot
root.location = -GRIP                      # the gun stays where it was; the pivot (the hand) is what tips
for o in [pivot] + list(parts.values()):
    o.animation_data_clear()

sc.render.fps = 35
bpy.context.preferences.edit.keyframe_new_interpolation_type = 'CONSTANT'   # one pose per tic, as the game
f = 1
for spr, L, tics in SEQUENCE:
    share, bits = mj.state(spr, L)
    back, pitch = mj.kick(spr, L)
    for t in range(tics):
        sc.frame_set(f)
        pivot.location = GRIP + Vector((0.0, -back, 0.0))
        pivot.rotation_euler = (math.radians(pitch), 0.0, 0.0)
        pivot.keyframe_insert("location", frame=f)
        pivot.keyframe_insert("rotation_euler", frame=f)
        for n, o in parts.items():
            off = Vector((0.0, 0.0, 0.0))
            if n in ("pump", "bolt"):
                off = Vector(mj.bl(-share * mj.PUMP_STROKE_M, 0.0, 0.0))
            if n in bits:
                off = Vector(mj.bl(*bits[n]))
            o.location = home[n] + off
            o.keyframe_insert("location", frame=f)
            hide = n in mj.HIDDEN and n not in bits
            o.hide_viewport = o.hide_render = hide
            o.keyframe_insert("hide_viewport", frame=f)
            o.keyframe_insert("hide_render", frame=f)
        f += 1
for o in [pivot] + list(parts.values()):
    if o.animation_data and o.animation_data.action:
        for fc in getattr(o.animation_data.action, "fcurves", []):
            for k in fc.keyframe_points:
                k.interpolation = 'CONSTANT'   # one pose per tic, as the game shows it
sc.frame_start, sc.frame_end = 1, f - 1
sc.frame_set(1)
print("KICK PREVIEW:", f - 1, "frames at 35 fps")


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
            r3d.view_location = Vector((0.0, 0.45, -0.12))
            r3d.view_rotation = Euler((math.radians(75), 0, math.radians(-110)), 'XYZ').to_quaternion()
            r3d.view_distance = 0.95
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
