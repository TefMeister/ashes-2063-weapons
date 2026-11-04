"""Pictures of a forge gun in chosen game frames, as the export job poses it (2026-11-04, the sharp cube shotgun):
moving parts shifted, hidden parts hidden, a right-side view each, so the animation can be checked without the game.
    blender -b <gun.blend> --python pose_sheet.py -- <job.json> <out folder> "<SPR L>" ["<SPR L>" ...]
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:]
job = json.load(open(args[0]))
out = os.path.abspath(args[1])
frames = args[2:]
os.makedirs(out, exist_ok=True)

sc = bpy.context.scene
root = next(o for o in sc.objects if o.type == 'EMPTY' and o.name.endswith("_root"))
prefix = root.name[:-len("root")]
parts = {o.name[len(prefix):]: o for o in sc.objects if o.type == 'MESH' and o.name.startswith(prefix)}
home = {n: o.location.copy() for n, o in parts.items()}
# which job (model) owns each moving part, and the hidden ones
owner = {}
for key, j in job.items():
    for p in j.get("parts", []):
        owner[p] = j

pts = [o.matrix_world @ Vector(c) for o in parts.values() for c in o.bound_box]
lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
mid = (lo + hi) / 2
cam_data = bpy.data.cameras.new("posecam")
cam = bpy.data.objects.new("posecam", cam_data)
sc.collection.objects.link(cam)
sc.camera = cam
cam_data.type = 'ORTHO'
cam_data.ortho_scale = (hi - lo).y * 1.08
sc.render.resolution_x, sc.render.resolution_y = 1200, 500
cam.location = mid + Vector((3, 0, 0))
cam.rotation_euler = (math.radians(90), 0, math.radians(90))

for fr in frames:
    for n, o in parts.items():
        o.location = home[n]
        j = owner.get(n)
        if j is None:
            o.hide_render = False
            continue
        pose = j["poses"][j.get("frame_pose", {}).get(fr, 0)]
        o.hide_render = n in j.get("hidden_parts", []) and n not in pose
        if n in pose:
            o.location = home[n] + Vector(pose[n])
    sc.render.filepath = os.path.join(out, fr.replace(" ", "_") + ".png")
    bpy.ops.render.render(write_still=True)
    print("POSE", fr)
