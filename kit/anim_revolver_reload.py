# Revolver reload, stop-motion. One frame = one game tic (35 fps).
# Timing is the game's own (Actors/Weapons/Revolver.txt, Work1 + ReloadDone):
#   REVR A B 3 | C C C D E F 2 | G G H I J L L L L 2 | M N O P 2 | P P P Q R S 2 |
#   T U V W X 1 | REVL C B A 2  = 67 tics.
# Cylinder swings out left, gun tips muzzle-up and the spent cases drop out,
# gun tips down, a speedloader comes up from the left hip and seats six rounds,
# a flick of the wrist closes the cylinder.
exec(open(r"C:\Users\TD3KX\github-backups\ashes-2063-weapons\kit\anim_kit.py").read())
exec(open(r"C:\Users\TD3KX\github-backups\ashes-2063-weapons\kit\revolver_settings.py").read())
OUT = r"C:\Users\TD3KX\github-backups\ashes-2063-weapons\revolver\Ashes_2063_EP1_revolver_reload.blend"

STATIC = globals().get("STATIC", False)
if STATIC:
    OUT = OUT.replace(".blend", "_static.blend")
FRAME_END = 68

REST = ((0, 0, 0), (0, 0, 0))
# frame (game sprite), gun pose (offset loc, extra rot), crane swing deg
GUN = [
    (1,  REST,                                       0),                 # A
    (4,  ((-0.020, -0.010, 0.025), (18, -8, 14)),    CRANE_OPEN_DEG * 0.4),   # B: latch, swing starts
    (7,  ((-0.030, -0.020, 0.035), (22, -5, 16)),    CRANE_OPEN_DEG),    # C: open, cases in view
    (13, ((-0.030, -0.020, 0.045), (35, -5, 14)),    CRANE_OPEN_DEG),    # D
    (15, ((-0.030, -0.030, 0.060), (50, -5, 12)),    CRANE_OPEN_DEG),    # E
    (17, ((-0.030, -0.035, 0.070), (62, -5, 10)),    CRANE_OPEN_DEG),    # F
    (19, ((-0.030, -0.040, 0.080), (70, -8, 10)),    CRANE_OPEN_DEG),    # G: muzzle up
    (25, ((-0.030, -0.040, 0.090), (72, -8, 10)),    CRANE_OPEN_DEG),    # I: ejector slap
    (27, ((-0.030, -0.040, 0.080), (70, -8, 10)),    CRANE_OPEN_DEG),    # J
    (37, ((-0.020, -0.020, 0.030), (30, -10, 12)),   CRANE_OPEN_DEG),    # M: tipping down
    (39, ((-0.015, -0.015, 0.025), (0, -15, 10)),   CRANE_OPEN_DEG),    # N
    (41, ((-0.010, -0.030, 0.025), (-15, -20, 8)),  CRANE_OPEN_DEG),    # O: back of cylinder faces you
    (53, ((-0.010, -0.030, 0.031), (-12, -20, 8)),  CRANE_OPEN_DEG),    # R: rounds seated, small jolt
    (55, ((-0.010, -0.030, 0.025), (-15, -20, 8)),  CRANE_OPEN_DEG),    # S
    (57, ((-0.010, -0.030, 0.030), (25, -10, 10)),   CRANE_OPEN_DEG),    # T
    (58, ((0.000, -0.030, 0.050), (45, -5, 5)),      CRANE_OPEN_DEG),    # U
    (60, ((0.025, -0.020, 0.050), (40, 20, -8)),     0),                 # W: flick closed
    (61, ((0.030, -0.020, 0.055), (38, 24, -9)),     0),                 # X
    (62, ((0.020, -0.010, 0.030), (22, 12, -5)),     0),                 # REVL C
    (64, ((0.010, 0.000, 0.010), (8, 5, -2)),        0),                 # REVL B
    (66, REST,                                       0),                 # REVL A
]
# Ejector: frame, how far the star is pushed back (m)
EJECT = [(1, 0.0), (23, 0.012), (25, 0.026), (29, 0.0)]
# Spent cases ride the ejector out, then fall in the WORLD (straight down, fast), then vanish.
CASE_FALL = [(27, 0.10), (29, 0.35), (31, 0.80)]     # frame, drop below where they left the cylinder (m)
CASE_GONE = 33
# Speedloader: from the LEFT HIP (world position, camera at the origin) to behind the cylinder.
HIP = (-0.28, 0.10, -0.50)
LOADER = [(45, "hip", 0.0), (47, "hip", 0.5), (49, "cyl", 0.06), (51, "cyl", 0.02)]  # frame, from, blend / gap (m)
LOADER_TILT = (-35, 0, 40)                            # extra turn while it is still near the hip (deg)
SEATED = 53                                           # rounds are in, the empty loader is gone

reset_scene()
setup_scene("Revolver_Reload", FRAME_END)
ov, O = link_model(MODEL, "REVOLVER")
root, crane, cyl, ejector = O["RV_Root"], O["RV_Crane"], O["RV_Cylinder"], O["RV_Ejector"]
cases, rounds = O["RV_Casings"], O["RV_Rounds"]
loader, loader_body = O["RV_Speedloader"], O["RV_SpeedloaderBody"]
fp_view()

for f, (dl, dr), crane_deg in GUN:
    if STATIC:
        dl, dr = (0, 0, 0), (0, 0, 0)
    key(root, f, loc=[a + b for a, b in zip(REST_LOC, dl)], rot_deg=[a + b for a, b in zip(REST_ROT, dr)])
    key(crane, f, rot_deg=(0, crane_deg, 0))
for f, back in EJECT:
    key(ejector, f, loc=(0, -back, 0))

# spent cases in the cylinder at the start, new rounds only once seated
key(rounds, 1, hide=True)
key(rounds, SEATED, hide=False)
key(cases, 1, hide=False, loc=(0, 0, 0))
for f, back in EJECT[1:3]:
    key(cases, f, loc=(0, -back, 0))
out_world = world_at(cyl, CASE_FALL[0][0], (0, -EJECT[2][1], 0))
for f, drop in CASE_FALL:
    key(cases, f, loc=local_at(cyl, f, out_world - Vector((0, 0, drop))))
key(cases, CASE_GONE, hide=True)


def cyl_back_in_root(frame, gap):
    """Speedloader pose (root space) that sits `gap` behind the cylinder's back face."""
    all_constant()
    bpy.context.scene.frame_set(frame)
    bpy.context.view_layer.update()
    M = root.matrix_world.inverted() @ cyl.matrix_world
    return M @ Matrix.Translation((0, -CYL_L / 2 - gap, 0))


for o in (loader, loader_body):
    key(o, 1, hide=True)
    key(o, LOADER[0][0], hide=False)
    key(o, SEATED, hide=True)
for f, src, amount in LOADER:
    if src == "cyl":
        M = cyl_back_in_root(f, amount)
    else:
        M = cyl_back_in_root(f, 0.06)
        hip_local = local_at(root, f, HIP)
        rot = M.to_euler()
        rot = (Euler(rot).to_matrix() @ Euler([math.radians(a * (1 - amount)) for a in LOADER_TILT]).to_matrix())
        M = Matrix.Translation(hip_local.lerp(M.to_translation(), amount)) @ rot.to_4x4()
    key(loader, f, loc=M.to_translation(), rot_deg=[math.degrees(a) for a in M.to_euler()])
key(loader, SEATED, loc=cyl_back_in_root(SEATED, 0.0).to_translation())

if STATIC:
    side_view(root, (-0.50, -0.30, 0.20), (-0.02, 0.02, 0.0))

finish(OUT, FRAME_END)
