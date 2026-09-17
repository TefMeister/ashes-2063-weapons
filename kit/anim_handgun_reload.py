# Handgun reload, stop-motion: tip the gun up and over, old magazine drops out,
# new one comes up from below and slaps in, gun comes back down.
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\anim_kit.py").read())
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\handgun_settings.py").read())

OUT = r"C:\Users\TD3KX\ashes-2063-weapons\handgun\Ashes_2063_EP1_handgun_reload.blend"

# STATIC=True makes the "_static" version: the weapon itself stays put in its rest
# pose and only its parts move (for adding hands later).
STATIC = globals().get("STATIC", False)
if STATIC:
    OUT = OUT.replace(".blend", "_static.blend")
FRAME_END = 44

HALF = ((0.01, 0.05, 0.03), (15, -5, 35))
FULL = ((0.02, 0.11, 0.075), (30, -10, 65))
JOLT = ((0.02, 0.11, 0.088), (35, -10, 65))
REST = ((0, 0, 0), (0, 0, 0))
NEAR = ((0, 0, 0.005), (4, 0, 8))

# frame, gun pose
GUN = [(1, REST), (4, HALF), (7, FULL), (30, JOLT), (32, FULL), (35, HALF), (38, NEAR), (40, REST)]

# Old magazine: frame, distance out along the grip (m), tumble (deg). Falls well clear, then hides.
MAG_OUT = [(1, 0.0, 0), (10, 0.02, 0), (12, 0.08, 6), (14, 0.26, 30), (16, 0.60, 70)]
MAG_OUT_GONE = 18
# New magazine comes up from the player's LEFT HIP (world position, camera at the origin),
# swings over to the bottom of the grip, then pushes in along the grip.
HIP = (-0.28, 0.10, -0.50)
MAG_IN_FROM_HIP = [(21, 0.0, (-35, 0, 40)), (24, 0.5, (-15, 0, 15)), (26, 0.85, (-6, 0, 6))]   # frame, 0 hip .. 1 grip, rotation
MAG_IN_GRIP = [(28, 0.05, 0), (29, 0.02, 0), (30, 0.0, 0)]            # frame, distance out, tumble
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
