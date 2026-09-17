# Crowbar "shoot 1": one swing (one click), stop-motion. Wind up to the right, a big jump
# through the strike, follow through low left, come back.
# One frame = one game tic (35 fps). Timing is the game's own (Actors/Weapons/Crowbar.txt,
# Fire + Downswing, button not held):
#   CROW N O P Q 1, (hidden) 4, R S T U 1, [hit], V W X Y 1, (hidden) 2 + 5, CROR C B A 2 = 29 tics.
# Where the game hides the bar, it is swung out of view (above right, then below left).
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\anim_kit.py").read())

MODEL = r"C:\Users\TD3KX\ashes-2063-weapons\crowbar\Ashes_2063_EP1_crowbar_model.blend"
OUT = r"C:\Users\TD3KX\ashes-2063-weapons\crowbar\Ashes_2063_EP1_crowbar_shoot1.blend"
VIEW_LENS_CB = 24
FRAME_END = 30

# frame: (hand position, rotation in degrees: X tips the hook up, Y rolls, Z turns left)
REST = ((0.10, 0.22, -0.13), (38, 0, 32))
WIND1 = ((0.14, 0.18, -0.08), (55, -15, 10))
WIND2 = ((0.16, 0.18, -0.06), (75, -25, -5))
HIGH = ((0.22, 0.08, 0.12), (100, -30, -15))        # raised out of view
MID = ((0.11, 0.24, -0.04), (45, -5, 35))
STRIKE = ((0.05, 0.30, -0.05), (10, 10, 75))
FOLLOW = ((-0.04, 0.28, -0.13), (-20, 35, 110))
LOW = ((-0.14, 0.20, -0.34), (-40, 45, 130))        # swung out of view, low left
RETURN = ((0.02, 0.18, -0.28), (0, 20, 70))
RECOVER = ((0.06, 0.20, -0.22), (15, 10, 55))
TIMELINE = [(1, WIND1), (3, WIND2), (5, HIGH), (9, WIND2), (10, MID), (11, STRIKE), (13, STRIKE),
            (14, FOLLOW), (16, FOLLOW), (17, LOW), (24, RETURN), (26, RECOVER), (28, REST)]
#           N           P           hidden      R           S          T              V: hit
#           W             Y             hidden     CROR C         CROR B          CROR A

reset_scene()
setup_scene("Crowbar_Shoot1", FRAME_END)
ov, O = link_model(MODEL, "CROWBAR")
root = O["CB_Root"]
fp_view(lens=VIEW_LENS_CB)

for f, (loc, rot) in TIMELINE:
    key(root, f, loc=loc, rot_deg=rot)

finish(OUT, FRAME_END)
