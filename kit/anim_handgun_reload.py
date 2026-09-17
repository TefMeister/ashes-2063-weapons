# Handgun reload, stop-motion: tip the gun up and over, old magazine drops out,
# new one comes up from the left hip and slaps in, gun comes back down.
# One frame = one game tic (35 fps). Timing is the game's own (Actors/Weapons/Glock.txt,
# Work2 + ReloadDone, the reload with a round still chambered, so no slide pull):
#   GLOK E 2, F G 1, (hidden) 1, H I J 2, K 5, L M N 2, O O P 2 | Q Q Q R S T 2, (hidden) 3, G F E 1 = 46 tics.
# Where the game hides the gun for a tic or three, the 3D gun holds its pose.
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\anim_kit.py").read())
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\handgun_settings.py").read())

OUT = r"C:\Users\TD3KX\ashes-2063-weapons\handgun\Ashes_2063_EP1_handgun_reload.blend"

# STATIC=True makes the "_static" version: the weapon itself stays put in its rest
# pose and only its parts move (for adding hands later).
STATIC = globals().get("STATIC", False)
if STATIC:
    OUT = OUT.replace(".blend", "_static.blend")
FRAME_END = 47

HALF = ((0.01, 0.05, 0.03), (15, -5, 35))
FULL = ((0.02, 0.11, 0.075), (30, -10, 65))
JOLT = ((0.02, 0.11, 0.088), (35, -10, 65))
REST = ((0, 0, 0), (0, 0, 0))
NEAR = ((0, 0, 0.005), (4, 0, 8))

# frame (game sprite), gun pose
GUN = [(1, NEAR), (3, HALF), (4, FULL), (27, JOLT), (29, FULL), (45, HALF), (46, NEAR), (47, REST)]
#      E          F          G          P: slap    Q          F          E          ready

# Old magazine (H I J): frame, distance out along the grip (m), tumble (deg). Falls well clear, then hides.
MAG_OUT = [(1, 0.0, 0), (6, 0.02, 0), (8, 0.08, 6), (10, 0.26, 30), (11, 0.60, 70)]
MAG_OUT_GONE = 12
# New magazine (K is the reach, L M N bring it up) comes from the player's LEFT HIP
# (world position, camera at the origin), swings to the bottom of the grip, then pushes in (O O P).
HIP = (-0.28, 0.10, -0.50)
MAG_IN_FROM_HIP = [(17, 0.0, (-35, 0, 40)), (19, 0.5, (-15, 0, 15)), (21, 0.85, (-6, 0, 6))]   # frame, 0 hip .. 1 grip, rotation
MAG_IN_GRIP = [(23, 0.05, 0), (25, 0.02, 0), (27, 0.0, 0)]            # frame, distance out, tumble
LINE_UP = 0.07                                                        # hip path aims at this point below the grip

reset_scene()
setup_scene("Handgun_Reload", FRAME_END)
ov, O = link_model(MODEL, "HANDGUN")
root, mag = O["HG_Root"], O["HG_Mag"]
fp_view()

mag_rest = Vector(mag.location)
t = math.radians(GRIP_TILT_DEG)
out_dir = Vector((0, math.sin(t), -math.cos(t)))    # down the grip

for f, (dl, dr) in GUN:
    if STATIC:
        dl, dr = (0, 0, 0), (0, 0, 0)
    key(root, f, loc=[a + b for a, b in zip(REST_LOC, dl)], rot_deg=[a + b for a, b in zip(REST_ROT, dr)])

for f, dist, tumble in MAG_OUT:
    key(mag, f, loc=mag_rest + out_dir * dist, rot_deg=(tumble, 0, 0), hide=False)
drop_world = world_at(root, MAG_OUT[-1][0], mag_rest + out_dir * MAG_OUT[-1][1])
key(mag, MAG_OUT_GONE, loc=local_at(root, MAG_OUT_GONE, drop_world), hide=True)

for f, blend, rot in MAG_IN_FROM_HIP:
    target = world_at(root, f, mag_rest + out_dir * LINE_UP)
    w = Vector(HIP).lerp(target, blend)
    key(mag, f, loc=local_at(root, f, w), rot_deg=rot, hide=False)
for f, dist, tumble in MAG_IN_GRIP:
    key(mag, f, loc=mag_rest + out_dir * dist, rot_deg=(tumble, 0, 0), hide=False)

if STATIC:
    side_view(root, (0.75, 0.0, -0.08), (0, 0.0, -0.10))

finish(OUT, FRAME_END)
