# How the revolver goes into GZDoom: which animation files, size, pivot, and which
# game sprite frame shows which Blender frame. Used by gz_export.py.
NAME = "revolver"
ROOT = "RV_Root"
DIR = r"C:\Users\TD3KX\ashes-2063-weapons\revolver"
OUT_DIR = DIR + r"\gzdoom"
PK3 = "Ashes2063_revolver3d_test.pk3"
MODEL_PATH = "models/ashes2063/revolver"     # folder inside the pk3

# Animation files in model-frame order: name -> (file, frame count)
ANIMS = [
    ("shoot1", DIR + r"\Ashes_2063_EP1_revolver_shoot1.blend", 14),
    ("reload", DIR + r"\Ashes_2063_EP1_revolver_reload.blend", 68),
]

UNITS_PER_M = 250            # map units per metre; the VR pistol is ~50 units long, ours ~48
ORIGIN = (0.0, -0.05, 0.065) # model origin at the gun's top rear, like the VR pistol model

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
