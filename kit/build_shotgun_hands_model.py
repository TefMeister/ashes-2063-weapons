# The shotgun WITH the gloved hands, as one model file the game can be built from.
#   blender -b --factory-startup --python kit/run_background.py -- build_shotgun_hands_model.py
#
# WHY THIS FILE EXISTS RATHER THAN THE HANDS BEING BUILT STRAIGHT INTO THE ANIMATION FILE
# GZDoom cannot read Blender node materials, so every part of a weapon shares ONE UV layout and
# the flat colours are baked into a single PNG (kit/gz_bake.py). Unwrapping needs real, local mesh
# data -- and an animation file only LINKS its model, so its meshes are library data and cannot be
# unwrapped. The hands therefore have to live in a model file of their own, which is this one:
# the gun is APPENDED (a real copy, not a link), the hands are added to it, and the whole lot is
# unwrapped and baked together.
#
# The result is a normal weapon model as far as everything downstream is concerned:
#   Ashes_2063_EP1_shotgun_hands_model.blend   collection "SHOTGUN_HANDS"
#   gzdoom/shotgun_hands.png                   the baked atlas, gun and hands in one sheet
#
# ⚠️ The plain shotgun model is untouched. This is a second model beside it, so the hands can be
# added to the game without taking the hand-free version away.
import os

KIT = globals().get("KIT") or os.path.dirname(os.path.abspath(__file__))


def _read(name):
    return open(os.path.join(KIT, name), encoding="utf-8-sig").read()


exec(_read("pixel_kit.py"))
exec(_read("shotgun_settings.py"))
exec(_read("shotgun_hands.py"))

OUT = os.path.abspath(os.path.join(KIT, "..", "shotgun",
                                   "Ashes_2063_EP1_shotgun_hands_model.blend"))
ATLAS = os.path.abspath(os.path.join(KIT, "..", "shotgun", "gzdoom", "shotgun_hands.png"))
COLL_NAME = "SHOTGUN_HANDS"

reset_scene()
setup_scene("Shotgun_Hands_Model")

# APPEND, not link: appended data is local and can be unwrapped. SHOTGUN_FX is a child of
# SHOTGUN, so the casing, the loading shell and the muzzle flash come across with it.
with bpy.data.libraries.load(MODEL, link=False) as (src, dst):
    dst.collections = ["SHOTGUN"]
gun = dst.collections[0]
gun.name = COLL_NAME                       # so an animation file can ask for it by name
bpy.context.scene.collection.children.link(gun)

O = {o.name: o for o in gun.all_objects}
root, pump = O["SG_Root"], O["SG_Pump"]

hand_l, hand_r = build_hands(root, pump, gun, globals())
print("hands added:", hand_l.name, "->", hand_l.parent.name,
      "|", hand_r.name, "->", hand_r.parent.name)

studio(target=(0, 0.17, 0.03), dist=0.95, name="SGH_ModelCam")

# ⚠️ Saves the .blend, THEN bakes, because baking rewires every material. Same order as
# build_shotgun.py, and for the same reason.
exec(_read("gz_bake.py"))
ATLAS_SIZE = 1024                          # the gun already needed this; the hands add to it
uv_save_bake(OUT, ATLAS)
print("shotgun+hands model:", OUT)
