# Shotgun "shoot 1": one shot and the pump stroke that follows, stop-motion.
# One frame = one game tic (35 fps). Timing is the game's own, read from
# Actors/Weapons/Shotgun.txt (actor `pumpaction`, states FireReal then Pump):
#   GRIF A 1 (shot, bright) B 1 (bright) C 1 | GRIP C 4 | GRIP B 2
#   Pump: GRIP A-G 1 each (7) | GRIP H 3 | GRIP I-M 2 each (10) | GRIZ A 1
# = 30 tics. The spent shell (`grizzlySpawner`) is thrown right after frame G,
# so it leaves while the pump is fully back.
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\anim_kit.py").read())
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\shotgun_settings.py").read())
OUT = r"C:\Users\TD3KX\ashes-2063-weapons\shotgun\Ashes_2063_EP1_shotgun_shoot1.blend"

# STATIC=True makes the "_static" version: the weapon itself stays put in its rest
# pose and only its parts move (for adding hands later).
STATIC = globals().get("STATIC", False)
if STATIC:
    OUT = OUT.replace(".blend", "_static.blend")
FRAME_END = 30
EJECT_F = 17                    # the tic the spent shell leaves the port

# frame, gun offset loc, gun extra rot (deg), pump slide along -Y, trigger deg,
# flash 0/1/2, is a live round showing in the port
POSES = [
    (1,  (0.004, -0.020, 0.012), (8, 0, -2),    0.000, -18, 2, True),   # GRIF A: the shot
    (2,  (0.012, -0.045, 0.030), (20, 2, -5),   0.000, -18, 1, True),   # GRIF B: still bright
    (3,  (0.014, -0.050, 0.038), (24, 3, -6),   0.000, -18, 0, True),   # GRIF C: top of the kick
    (4,  (0.010, -0.038, 0.029), (18, 2, -4),   0.000, -10, 0, True),   # GRIP C (4 tics)
    (6,  (0.006, -0.024, 0.018), (11, 1, -3),   0.000, -4,  0, True),
    (8,  (0.003, -0.012, 0.009), (5, 1, -1),    0.000, 0,   0, True),   # GRIP B (2 tics)
    (10, (0.001, -0.004, 0.003), (2, 0, 0),    -0.012, 0,   0, True),   # pump starts back
    (11, (0.000, -0.002, 0.001), (1, 0, 0),    -0.026, 0,   0, True),
    (12, (0.000, 0.000, 0.000),  (0, 0, 0),    -0.038, 0,   0, True),
    (13, (0.000, 0.002, -0.002), (-1, 0, 1),   -0.050, 0,   0, True),
    (14, (0.000, 0.003, -0.003), (-2, 0, 1),   -0.060, 0,   0, True),
    (15, (0.000, 0.004, -0.004), (-2, -1, 2),  -0.066, 0,   0, True),
    (16, (0.000, 0.004, -0.004), (-3, -1, 2),  -0.070, 0,   0, True),   # fully back
    (17, (0.000, 0.004, -0.005), (-3, -1, 2),  -0.070, 0,   0, False),  # GRIP H: shell thrown
    (20, (0.000, 0.003, -0.004), (-2, -1, 2),  -0.058, 0,   0, False),  # GRIP I-M: forward
    (22, (0.000, 0.002, -0.003), (-2, 0, 1),   -0.044, 0,   0, False),
    (24, (0.000, 0.001, -0.002), (-1, 0, 1),   -0.030, 0,   0, False),
    (26, (0.000, 0.000, -0.001), (0, 0, 0),    -0.016, 0,   0, True),   # fresh round chambered
    (28, (0.000, -0.004, 0.002), (2, 0, 0),     0.000, 0,   0, True),   # slams shut
    (29, (0.000, 0.000, 0.000),  (0, 0, 0),     0.000, 0,   0, True),
    (30, (0.000, 0.000, 0.000),  (0, 0, 0),     0.000, 0,   0, True),   # GRIZ A: ready
]

reset_scene()
setup_scene("Shotgun_Shoot1", FRAME_END)
ov, O = link_model(MODEL, "SHOTGUN")
root, pump, trig = O["SG_Root"], O["SG_Pump"], O["SG_Trigger"]
flash, casing, port_shell = O["SG_MuzzleFlash"], O["SG_Casing"], O["SG_PortShell"]
loader = O["SG_LoadShell"]
fp_view()

PORT_LOCAL = (REC_W / 2 + 0.012, PORT_Y, BORE_Z - 0.006)

for f, dl, dr, pdy, td, fs, live in POSES:
    if STATIC:
        dl, dr = (0, 0, 0), (0, 0, 0)
    key(root, f, loc=[a + b for a, b in zip(REST_LOC, dl)],
        rot_deg=[a + b for a, b in zip(REST_ROT, dr)])
    px, py, pz = PUMP_PIVOT
    key(pump, f, loc=(px, py + pdy, pz))
    key(trig, f, rot_deg=(td, 0, 0))
    key(flash, f, hide=(fs == 0),
        scale=(1.0, 1.0, 1.0) if fs == 2 else (0.6, 0.75, 0.6))
    key(port_shell, f, hide=not live)
    key(loader, f, hide=True)

# ---- the spent shell, thrown in WORLD space so turning the gun cannot bend its
# path (the standing rule set for the handgun on 2026-09-17) --------------------
start = world_at(root, EJECT_F, PORT_LOCAL)
TRAIL = [(EJECT_F, (0, 0, 0), (0, 0, 0)),
         (EJECT_F + 1, (0.30, 0.05, 0.03), (40, 0, 30)),
         (EJECT_F + 2, (0.80, 0.12, -0.14), (95, 0, 70))]
for f, off, rot in TRAIL:
    key(casing, f, loc=local_at(root, f, start + Vector(off)), rot_deg=rot, hide=False)
key(casing, EJECT_F + 3, hide=True)
key(casing, 1, hide=True)

if STATIC:
    side_view(root, (-0.95, 0.15, 0.13), (0, 0.15, 0.02))

finish(OUT, FRAME_END)
