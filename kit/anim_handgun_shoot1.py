# Handgun "shoot 1": one shot, stop-motion. Frame numbers are game tics at 35 fps.
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\anim_kit.py").read())
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\handgun_settings.py").read())
OUT = r"C:\Users\TD3KX\ashes-2063-weapons\handgun\Ashes_2063_EP1_handgun_shoot1.blend"

# STATIC=True makes the "_static" version: the weapon itself stays put in its rest
# pose and only its parts move (for adding hands later).
STATIC = globals().get("STATIC", False)
if STATIC:
    OUT = OUT.replace(".blend", "_static.blend")

SLIDE_REST = (0, 0.0, 0.046)
SLIDE_BACK = 0.034                   # how far the slide travels
FRAME_END = 16

# pose table: frame -> (gun offset loc, gun extra rot, slide back 0..1, hammer deg,
#                       trigger deg, flash state 0/1/2)
POSES = [
    (1,  (0, 0, 0),           (0, 0, 0),    0.0, 0,   0,  0),
    (5,  (0, -0.022, 0.012),  (14, 0, -2),  1.0, 40, -18, 2),
    (7,  (0, -0.016, 0.010),  (11, 0, -1),  1.0, 40, -18, 1),
    (9,  (0, -0.008, 0.005),  (6, 0, 0),    0.4, 20, -8,  0),
    (11, (0, -0.003, 0.002),  (2, 0, 0),    0.0, 0,   0,  0),
    (13, (0, 0, 0),           (0, 0, 0),    0.0, 0,   0,  0),
]

# The spent casing leaves fast and far, travelling in the WORLD (not with the gun),
# so turning the gun never bends its path. Gone after 2 frames.
CASING_PORT = (0.030, 0.035, 0.060)          # on the gun, at the ejection port
CASING_PATH = [                              # frame, world offset from the port (m), spin (deg)
    (5, (0.0, 0.0, 0.0), (0, 0, 30)),
    (6, (0.30, -0.05, 0.13), (95, 0, 150)),
    (7, (0.78, -0.12, 0.12), (220, 0, 290)),
]
CASING_GONE = 8

reset_scene()
setup_scene("Handgun_Shoot1", FRAME_END)
ov, O = link_model(MODEL, "HANDGUN")
root, slide, hammer, trig = O["HG_Root"], O["HG_Slide"], O["HG_Hammer"], O["HG_Trigger"]
flash, light, casing = O["HG_MuzzleFlash"], O["HG_FlashLight"], O["HG_Casing"]
fp_view()

for f, dl, dr, sb, hd, td, fs in POSES:
    if STATIC:
        dl, dr = (0, 0, 0), (0, 0, 0)
    key(root, f, loc=[a + b for a, b in zip(REST_LOC, dl)], rot_deg=[a + b for a, b in zip(REST_ROT, dr)])
    key(slide, f, loc=(0, SLIDE_REST[1] - SLIDE_BACK * sb, SLIDE_REST[2]))
    key(hammer, f, rot_deg=(hd, 0, 0))
    key(trig, f, rot_deg=(td, 0, 0))
    key(flash, f, hide=(fs == 0), scale=(1.0, 1.0, 1.0) if fs == 2 else (0.65, 0.8, 0.65))
    key(light, f, hide=(fs == 0))

port_world = world_at(root, CASING_PATH[0][0], CASING_PORT)
key(casing, 1, hide=True)
for f, off, spin in CASING_PATH:
    key(casing, f, hide=False, loc=local_at(root, f, port_world + Vector(off)), rot_deg=spin)
key(casing, CASING_GONE, hide=True)

if STATIC:
    side_view(root, (0.55, 0.03, 0.02), (0, 0.03, -0.01))

finish(OUT, FRAME_END)
