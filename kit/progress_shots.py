# Render progress pictures from a saved .blend, in the background:
#   blender.exe -b <file.blend> --python kit/progress_shots.py -- <out_prefix> <frames> [cam x,y,z look x,y,z lens]
# Without a camera spec it uses the file's own active camera.
import bpy, sys
from mathutils import Vector
args = sys.argv[sys.argv.index("--") + 1:]
prefix, frames = args[0], [int(f) for f in args[1].split(",")]
sc = bpy.context.scene
if len(args) > 2:
    loc = Vector([float(v) for v in args[2].split(",")])
    look = Vector([float(v) for v in args[3].split(",")])
    cam = bpy.data.cameras.new("ProgressCam"); cam.lens = float(args[4]); cam.clip_start = 0.005
    co = bpy.data.objects.new("ProgressCam", cam); sc.collection.objects.link(co)
    co.location = loc
    co.rotation_euler = (look - loc).to_track_quat('-Z', 'Y').to_euler()
    sc.camera = co
sc.render.resolution_x, sc.render.resolution_y = 640, 480
for f in frames:
    sc.frame_set(f)
    sc.render.filepath = f"{prefix}_{f:03d}.png"
    bpy.ops.render.render(write_still=True)
