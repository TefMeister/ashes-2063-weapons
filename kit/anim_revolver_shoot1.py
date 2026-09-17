# Revolver "shoot 1": one shot, stop-motion. One frame = one game tic (35 fps).
# Timing is the game's own (Actors/Weapons/Revolver.txt, FireReal):
#   REVF A 2 (shot), B 1 (bright), D 1, E 2, F 2, G 2, H 1, REVG A 1+1 (ready).
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\anim_kit.py").read())
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\revolver_settings.py").read())
OUT = r"C:\Users\TD3KX\ashes-2063-weapons\revolver\Ashes_2063_EP1_revolver_shoot1.blend"

# STATIC=True makes the "_static" version: the weapon itself stays put in its rest
# pose and only its parts move (for adding hands later).
STATIC = globals().get("STATIC", False)
if STATIC:
    OUT = OUT.replace(".blend", "_static.blend")
FRAME_END = 14

# frame (game sprite), gun offset loc, gun extra rot, hammer deg, trigger deg,
# cylinder turn deg, flash state 0/1/2
POSES = [
    (1,  (0, 0, 0),               (0, 0, 0),     0,  0,   0,  0),   # ready
    (2,  (0.005, -0.015, 0.010),  (10, 0, -3),   0, -20, 60, 2),   # A: hammer falls, big flash
    (4,  (0.020, -0.025, 0.035),  (28, 4, -10),  0, -20, 60, 1),   # B: bright, kick
    (5,  (0.022, -0.020, 0.045),  (32, 5, -11),  0, -20, 60, 0),   # D: top of the kick
    (6,  (0.018, -0.015, 0.035),  (26, 4, -9),   0, -12, 60, 0),   # E
    (8,  (0.010, -0.008, 0.020),  (15, 2, -5),   0, -6,  60, 0),   # F
    (10, (0.004, -0.003, 0.008),  (6, 1, -2),    0, 0,   60, 0),   # G
    (12, (0.001, 0, 0.002),       (2, 0, 0),     0, 0,   60, 0),   # H
    (13, (0, 0, 0),               (0, 0, 0),     0, 0,   60, 0),   # ready
]
# Double action: the hammer is already down again on the shot tic (the game has no
# cocking frame), so the hammer never shows as pulled back here.

reset_scene()
setup_scene("Revolver_Shoot1", FRAME_END)
ov, O = link_model(MODEL, "REVOLVER")
root, hammer, trig, cyl = O["RV_Root"], O["RV_Hammer"], O["RV_Trigger"], O["RV_Cylinder"]
flash, light = O["RV_MuzzleFlash"], O["RV_FlashLight"]
fp_view()

for f, dl, dr, hd, td, cd, fs in POSES:
    if STATIC:
        dl, dr = (0, 0, 0), (0, 0, 0)
    key(root, f, loc=[a + b for a, b in zip(REST_LOC, dl)], rot_deg=[a + b for a, b in zip(REST_ROT, dr)])
    key(hammer, f, rot_deg=(hd, 0, 0))
    key(trig, f, rot_deg=(td, 0, 0))
    key(cyl, f, rot_deg=(0, cd, 0))
    key(flash, f, hide=(fs == 0), scale=(1.0, 1.0, 1.0) if fs == 2 else (0.65, 0.8, 0.65))
    key(light, f, hide=(fs == 0))

if STATIC:
    side_view(root, (-0.55, 0.03, 0.06), (0, 0.03, 0.0))

finish(OUT, FRAME_END)
