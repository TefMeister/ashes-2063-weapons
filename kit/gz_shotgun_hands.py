# How the shotgun WITH HANDS goes into GZDoom.
#   blender -b --factory-startup --python kit/gz_export.py -- gz_shotgun_hands.py [flat|vr]
#
# This is the hand-free shotgun's own export profile with three things changed, and it reads that
# profile rather than copying it. The sprite sheet below it -- which game sprite letter shows which
# Blender frame -- was read letter by letter out of the mod's Actors/Weapons/Shotgun.txt, and it is
# the one thing here that must never exist in two places and drift apart.
#
# What changes:
#   1. the model and texture are named shotgun_hands, so the hand-free build stays installable;
#   2. every animation comes from the ONE all-in-one file rather than from two separate ones;
#   3. reload frames are shifted by where RELOAD_FULL starts on that shared timeline.
import os

_KIT = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(_KIT, "gz_shotgun.py"), encoding="utf-8-sig").read())

# Where RELOAD_FULL begins in Ashes_2063_EP1_shotgun_hands_all.blend, minus one: the driver puts
# SHOOT at 1..30, then a gap, then the full reload. Frame N of the old reload file is frame
# N + RELOAD_OFFSET here.
# ⚠️ Keep in step with GAP and the animation lengths in anim_shotgun_hands_all.py. The assert at
# the foot of this file is what actually catches it if they drift.
RELOAD_OFFSET = 42

NAME = "shotgun_hands"
ALL_IN_ONE = DIR + r"\Ashes_2063_EP1_shotgun_hands_all.blend"

ANIMS = [
    ("shoot1", ALL_IN_ONE, SHOOT_FRAMES),
    ("reload", ALL_IN_ONE, [f + RELOAD_OFFSET for f in RELOAD_FRAMES]),
]
SPRITES = [(spr, letter, anim, frame + (RELOAD_OFFSET if anim == "reload" else 0))
           for spr, letter, anim, frame in SPRITES]

PK3 = ("Ashes2063_shotgun3d_hands_VR_test.pk3" if VARIANT == "vr"
       else "Ashes2063_shotgun3d_hands_test.pk3")

# Frame 1 is still the SHOT, not the gun at rest, so the neutral pose still has to be named or the
# whole gun comes out 8.61 degrees nose-down (the fault found on the 2026-09-19 wear).
REST_FRAME = ("shoot1", 30)

assert max(ANIMS[1][2]) < 219, (
    "the reload frames now run into RELOAD_PARTIAL - RELOAD_OFFSET is out of step with "
    "anim_shotgun_hands_all.py")
