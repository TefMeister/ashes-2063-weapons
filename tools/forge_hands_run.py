# The approved Ashes gloves (fingerless black leather, 2026-09-23) on one forge gun, in its own .blend, with no
# Blender window. A first pass done alone, looked at together later (Tefa 2026-10-19: "can you do gloves on all the
# other weapons now? on both doom and ashes 2063?", then "Yes, alone, review later").
#   blender -b <forge blend> --python tools/forge_hands_run.py -- <gun> <check picture dir>
#
# Where the hands go follows the Ashes shotgun's hands (ashes shotgun/blender/vs_hands.py, fitted with Tefa):
#   right: hand space lands at x = grip front at its top - 27, y = -(grip half width + 1) - 4, z = grip top - 12,
#          fingers forward, back of the hand to the gun's right, leaning with the grip (r_axes / r_shear there)
#   left:  palm up under the gun at the support point (x - 2), knuckles at the gun's right side, palm 4 under its
#          bottom, the wrist dropping past half width + 1 (l_axes / l_shear); or, on an upright front grip, a right-hand
#          grip pose there, mirrored into a left hand
# The grip, front grip and support are found from the gun's own cubes by brutal-doom-3d-guns/gloves/fit_gloves.py
# (one finder for both games; cloned beside this repo).
import importlib.util
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
BACKUPS = os.path.dirname(REPO)
MEGA_BLENDER = os.path.join("D:" + os.sep, "MEGA transfer", "Game Files", "ashes-2063-weapons", "3D blender")
for p in (os.path.join(REPO, "forge"), os.path.join(BACKUPS, "blender-cubekit"),
          os.path.join(BACKUPS, "brutal-doom-3d-guns", "gloves"), os.path.join(MEGA_BLENDER, "ashes gloves", "blender")):
    sys.path.insert(0, p)

import fit_gloves                                         # noqa: E402
from gl_pose import build, place, painted               # noqa: E402
from gl_settings import SHADE, NOISE                     # noqa: E402
from bl import Space, make_objects                       # noqa: E402
from cube_size import VOXEL_M                            # noqa: E402

# the Ashes shotgun's approved hand poses (vs_hands.py)
R_CURLS = {"middle": (45, 55, 60), "ring": (45, 55, 60), "pinky": (40, 50, 50), "index": (10, 35, 30)}
R_THUMB = [(12, 5, 80), (10, -30, 20)]
L_CURLS = {"index": (65, 50, 20), "middle": (65, 50, 20), "ring": (65, 50, 20), "pinky": (60, 45, 15)}
L_THUMB = [(11, 88, 22), (11, 80, 60)]
L_THUMB_BASE = (-11, 12, -1)
L_THUMB_SIZE = (9, 7, 4)
WRIST_DROP = 0.7
ONE_HANDED = {"handgun", "police_pistol", "revolver", "crowbar", "machine_pistol", "lazer_gun"}

args = sys.argv[sys.argv.index("--") + 1:]
GUN, SHOTS = args[0], args[1]
spec = importlib.util.spec_from_file_location("design", os.path.join(REPO, "forge", GUN + ".py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
model = mod.build()
cells = set(model.full) | set(model.fine)
body = {c for c, v in model.full.items() if v[2] != 'mag'}
body |= {c for c, subs in model.fine.items() if any(s[2] != 'mag' for s in subs.values())}
px, py = model.pivot[0], model.pivot[1]


def grip_hand(front, top, rake, half, blocked):
    """A right hand round an upright grip whose front top is (front, top), leaning back `rake`."""
    x0, y0, z0 = front - 27, -(half + 1) - 4, top - 12
    hand = build("right", R_CURLS, R_THUMB)
    out = {}
    for k in ("hand", "thumb", "tip"):
        out.update(place(hand[k], lambda xh, yh, zh: (yh + x0, -zh + y0, -xh + z0),
                         shear=lambda x, y, z: (x - round(max(0, top - z) * rake), y, z), blocked=blocked))
    return out


def grip_half(front, top):
    ys = [abs(c[1] - py) for c in body if front - 12 <= c[0] <= front and top - 8 <= c[2] <= top - 2]
    return max(ys) if ys else 5


hands = {}
g = fit_gloves.grip(body, model.pivot)
front, top, rake = g if g else (int(round(px)) + 7, int(round(model.pivot[2])) - 1, 0.3)
found = (f"grip front {front} top {top} rake {rake:.2f}" if g else "no grip found under the pivot")
hands["right"] = grip_hand(front, top, rake, grip_half(front, top), cells)
if GUN not in ONE_HANDED:
    fg = fit_gloves.foregrip(body, front)
    if fg is not None:
        f2, t2, r2 = fg
        mirrored = {(x, 2 * py - y, z) for x, y, z in cells}
        hands["left"] = {(x, 2 * py - y, z): c for (x, y, z), c in grip_hand(f2, t2, r2, grip_half(f2, t2), mirrored).items()}
        found += f"; left hand on the upright front grip, front {f2} top {t2}"
    else:
        s = fit_gloves.support(body, front)
        if s is not None:
            x, bottom, half = s
            lx0, ly0, lz0 = x - 2, 27 - (half + 2), bottom - 4
            lh = build("left", L_CURLS, L_THUMB, thumb_base=L_THUMB_BASE, thumb_size=L_THUMB_SIZE)
            hands["left"] = {}
            for k in ("hand", "thumb"):
                hands["left"].update(place(lh[k], lambda xh, yh, zh: (xh + lx0, -yh + ly0, -zh + lz0),
                                           shear=lambda X, Y, Z: (X, Y, Z - round(max(0, Y - (half + 1)) * WRIST_DROP)),
                                           blocked=cells))
            found += f"; left hand under x {x}, bottom {bottom}, half width {half}"
        else:
            found += "; too short for a second hand"
else:
    found += "; one-handed"
print(f"HANDS {GUN}: {found}")

# into the blend: replaces its own objects each run, touches nothing else
tag = "AF_" + GUN
col = bpy.data.collections.get(GUN + " hands") or bpy.data.collections.new(GUN + " hands")
if col.name not in bpy.context.scene.collection.children:
    bpy.context.scene.collection.children.link(col)
for o in list(col.objects):
    bpy.data.objects.remove(o)
root = bpy.data.objects.new(tag + "_Hands_Root", None)
col.objects.link(root)
specs = [(f"{tag}_glove_{side}", painted(c), model.pivot) for side, c in hands.items() if c]
objs = make_objects(specs, root, os.path.join(os.path.dirname(bpy.data.filepath), GUN + "_hands_atlas.png"),
                    Space(VOXEL_M, model.pivot), SHADE, NOISE)
for o in objs.values():
    for c in list(o.users_collection):
        c.objects.unlink(o)
    col.objects.link(o)
print("hand cubes:", {k: len(v) for k, v in hands.items()})
bpy.ops.file.pack_all()
bpy.ops.wm.save_mainfile()

sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'STUDIO'
sc.display.shading.color_type = 'TEXTURE'
sc.render.resolution_x, sc.render.resolution_y = 640, 400
meshes = [o for o in sc.objects if o.type == 'MESH' and not o.hide_render]
pts = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
mid, size = (lo + hi) / 2, max((hi - lo).length, 0.1)
cam = bpy.data.objects.new("hand_check_cam", bpy.data.cameras.new("hand_check_cam"))
sc.collection.objects.link(cam)
sc.camera = cam
os.makedirs(SHOTS, exist_ok=True)
for view, d in (("side", Vector((-1, 0, 0.15))), ("player", Vector((0.35, -1, 0.45)))):
    cam.location = mid + d.normalized() * size * 1.35
    cam.rotation_euler = (mid - cam.location).to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(SHOTS, f"{GUN}_{view}.png")
    bpy.ops.render.render(write_still=True)
bpy.data.objects.remove(cam)
print(f"HANDS {GUN}: done")
