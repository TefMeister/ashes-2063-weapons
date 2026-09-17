# Jackhammer "shoot 1": a looping hammering cycle, stop-motion (each pose held 2 tics).
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\anim_kit.py").read())

MODEL = r"C:\Users\TD3KX\ashes-2063-weapons\jackhammer\Ashes_2063_EP1_jackhammer_model.blend"
OUT = r"C:\Users\TD3KX\ashes-2063-weapons\jackhammer\Ashes_2063_EP1_jackhammer_shoot1.blend"

# STATIC=True makes the "_static" version: the weapon itself stays put in its rest
# pose and only its parts move (for adding hands later).
STATIC = globals().get("STATIC", False)
if STATIC:
    OUT = OUT.replace(".blend", "_static.blend")

REST_LOC = (0.025, 0.52, -0.23)      # machine below and in front of the player
REST_ROT = (25, 0, -4)               # top tipped toward the camera
VIEW_LENS_JH = 20                    # wider view, like the game's 90-degree field of view
FRAME_END = 12                       # loops: frame 13 == frame 1

# frame, body offset (x, y, z), body extra rot (deg), bit travel down (m), puff: 0 off / 1 small / 2 big
POSES = [
    (1,  (0, 0, 0),           (0, 0, 0),       0.000, 0),
    (3,  (0.004, 0, -0.016),  (1.5, 0, 1.5),   0.035, 0),
    (5,  (-0.003, 0, 0.008),  (-1.0, 0, -1.0), 0.000, 1),
    (7,  (-0.004, 0, -0.013), (1.0, 0, -1.5),  0.030, 2),
    (9,  (0.003, 0, 0.010),   (-1.5, 0, 1.0),  0.000, 1),
    (11, (0, 0, -0.004),      (0.5, 0, 0),     0.012, 0),
]

reset_scene()
setup_scene("Jackhammer_Shoot1", FRAME_END)
ov, O = link_model(MODEL, "JACKHAMMER")
root, bit, puff = O["JH_Root"], O["JH_Bit"], O["JH_Puff"]
fp_view(lens=VIEW_LENS_JH)

bit_rest = Vector(bit.location)
puff_rest = Vector(puff.location)
for f, dl, dr, travel, pf in POSES:
    if STATIC:
        dl, dr = (0, 0, 0), (0, 0, 0)
    key(root, f, loc=[a + b for a, b in zip(REST_LOC, dl)], rot_deg=[a + b for a, b in zip(REST_ROT, dr)])
    key(bit, f, loc=bit_rest - Vector((0, 0, travel)))
    s = 1.0 if pf == 2 else 0.6
    key(puff, f, hide=(pf == 0), scale=(s, s, s), loc=puff_rest + Vector((0, 0, 0.03 * pf)))

if STATIC:
    side_view(root, (1.6, -0.5, 0.1), (0, 0, -0.15))

finish(OUT, FRAME_END)
