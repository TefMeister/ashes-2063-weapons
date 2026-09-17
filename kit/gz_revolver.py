# How the revolver goes into GZDoom: which animation files, size, pivot, and which
# game sprite frame shows which Blender frame. Used by gz_export.py.
NAME = "revolver"
ROOT = "RV_Root"
DIR = r"C:\Users\TD3KX\ashes-2063-weapons\revolver"
OUT_DIR = DIR + r"\gzdoom"
PK3 = "Ashes2063_revolver3d_test.pk3"    # the flat build; the VR build overrides this below
MODEL_PATH = "models/ashes2063/revolver"     # folder inside the pk3

# Animation files in model-frame order: name -> (file, frame count)
ANIMS = [
    ("shoot1", DIR + r"\Ashes_2063_EP1_revolver_shoot1.blend", 14),
    ("reload", DIR + r"\Ashes_2063_EP1_revolver_reload.blend", 68),
]

# Two builds, because the engine places the model differently (hh79/gzdoomvr gvr4.13.2.2,
# models.cpp + hw_models.cpp) [inferred-static 2026-09-17; flat build verified-live 2026-09-17]:
# - flat: the model origin is the player's EYE, units are free (only ratios show).
#   We export the Blender first-person camera space, so the game shows what ViewCam shows.
# - vr: the model hangs off the CONTROLLER in real centimetres (100 units per metre); the hand
#   lands at MD3 (30, 0, -5), so ORIGIN is chosen to put the grip centre there.
if VARIANT == "vr":
    SPACE = "hand"
    UNITS_PER_M = 100
    # grip centre G = (0, -0.0522, -0.0426) in root space. The engine's hand point is MD3 (30, 0, -5),
    # but in the headset that sat the gun 8-10 cm too high (Tefa, Quest 3 + Virtual Desktop)
    # [reported 2026-09-17, n=1], so the grip centre goes 9 cm lower: (G - ORIGIN) * 100 = (30, 0, -14)
    VR_GRIP_DROP = 0.09
    # second wear: move it 3 cm down, 2 cm right, 3 cm back toward the player [reported 2026-09-17, n=1]
    VR_NUDGE_RIGHT, VR_NUDGE_BACK, VR_NUDGE_DOWN = 0.02, 0.03, 0.03
    # third wear: "still 2cm lower"; "back my way" was not noticeable and the handle still sits away
    # from the controller when turned sideways, so a bigger step back (+5 cm, 8 cm in all) to make the
    # direction obvious [reported 2026-09-17, n=1]
    VR_NUDGE_BACK += 0.05
    VR_NUDGE_DOWN += 0.02
    # fourth wear: "up please now 3cm and back 2cm" [reported 2026-09-17, n=1]
    VR_NUDGE_DOWN -= 0.03
    VR_NUDGE_BACK += 0.02
    # The player tilts the controller by instinct while reloading, so the whole-gun movement in the
    # reload keeps only 40% of the Blender animation (rotation and position) [reported 2026-09-17, n=1]
    GUN_MOTION_SCALE = {"reload": 0.4}
    ORIGIN = (0.0 - VR_NUDGE_RIGHT, -0.3522 + VR_NUDGE_BACK, 0.0074 + VR_GRIP_DROP + VR_NUDGE_DOWN)
    PK3 = "Ashes2063_revolver3d_VR_test.pk3"
else:
    SPACE = "view"
    UNITS_PER_M = 250
    ORIGIN = (0.0, 0.0, 0.0)

# Sprite frame -> (animation, Blender frame). One sprite letter can only show one pose,
# so each letter uses the pose at its FIRST tic (see Revolver.txt timings in NOTES.md).
SPRITES = [
    ("REVG", "A", "shoot1", 1),
    ("REVF", "A", "shoot1", 2), ("REVF", "B", "shoot1", 4), ("REVF", "D", "shoot1", 5),
    ("REVF", "E", "shoot1", 6), ("REVF", "F", "shoot1", 8), ("REVF", "G", "shoot1", 10),
    ("REVF", "H", "shoot1", 12),
    ("REVR", "A", "reload", 1), ("REVR", "B", "reload", 4), ("REVR", "C", "reload", 7),
    ("REVR", "D", "reload", 13), ("REVR", "E", "reload", 15), ("REVR", "F", "reload", 17),
    ("REVR", "G", "reload", 19), ("REVR", "H", "reload", 23), ("REVR", "I", "reload", 25),
    ("REVR", "J", "reload", 27), ("REVR", "L", "reload", 29), ("REVR", "M", "reload", 37),
    ("REVR", "N", "reload", 39), ("REVR", "O", "reload", 41), ("REVR", "P", "reload", 49),
    ("REVR", "Q", "reload", 51), ("REVR", "R", "reload", 53), ("REVR", "S", "reload", 55),
    ("REVR", "T", "reload", 57), ("REVR", "U", "reload", 58), ("REVR", "V", "reload", 59),
    ("REVR", "W", "reload", 60), ("REVR", "X", "reload", 61),
    # REVL A-C end the reload, but the game also uses them when raising the lantern.
    ("REVL", "C", "reload", 62), ("REVL", "B", "reload", 64), ("REVL", "A", "reload", 66),
]
