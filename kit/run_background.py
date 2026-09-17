# Rebuild weapon files with Blender in the background (no window, never takes focus):
#   blender.exe -b --factory-startup --python kit/run_background.py -- <script> [static] [render:1,5,9]
# e.g. -- anim_handgun_reload.py static render:1,12,22
import sys, os
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
KIT = os.path.dirname(os.path.abspath(__file__))
g = {"__name__": "__main__", "STATIC": "static" in args}
exec(open(os.path.join(KIT, args[0])).read(), g)
for a in args[1:]:
    if a.startswith("render:"):
        frames = [int(x) for x in a[7:].split(",")]
        out = os.environ.get("RENDER_PREFIX", os.path.join(KIT, "..", "_renders", os.path.splitext(args[0])[0]))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        g["render_frames"](frames, out + ("_static" if g["STATIC"] else ""), res=(400, 300))
