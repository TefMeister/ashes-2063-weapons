# Crowbar "shoot 1": one swing, stop-motion. Wind up to the right, a big jump
# through the strike, follow through low left, hold, come back.
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\anim_kit.py").read())

MODEL = r"C:\Users\TD3KX\ashes-2063-weapons\crowbar\Ashes_2063_EP1_crowbar_model.blend"
OUT = r"C:\Users\TD3KX\ashes-2063-weapons\crowbar\Ashes_2063_EP1_crowbar_shoot1.blend"
VIEW_LENS_CB = 24
FRAME_END = 24

# frame: (hand position, rotation in degrees: X tips the hook up, Y rolls, Z turns left)
REST = ((0.10, 0.22, -0.13), (38, 0, 32))
WIND1 = ((0.14, 0.18, -0.08), (55, -15, 10))
WIND2 = ((0.16, 0.18, -0.06), (75, -25, -5))
STRIKE = ((0.05, 0.30, -0.05), (10, 10, 75))
FOLLOW = ((-0.04, 0.28, -0.13), (-20, 35, 110))
RECOVER = ((0.06, 0.20, -0.22), (15, 10, 55))
TIMELINE = [(1, REST), (4, WIND1), (7, WIND2), (10, STRIKE), (11, FOLLOW), (15, FOLLOW),
            (18, RECOVER), (21, REST)]

reset_scene()
setup_scene("Crowbar_Shoot1", FRAME_END)
ov, O = link_model(MODEL, "CROWBAR")
root = O["CB_Root"]
fp_view(lens=VIEW_LENS_CB)

for f, (loc, rot) in TIMELINE:
    key(root, f, loc=loc, rot_deg=rot)

finish(OUT, FRAME_END)
