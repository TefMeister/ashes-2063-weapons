# Shotgun reload, stop-motion. One frame = one game tic (35 fps). Timing is the game's
# own, read from Actors/Weapons/Shotgun.txt (actor `pumpaction`).
#
# TWO VERSIONS, because the game has two (Tefa filmed both):
#   full    â€” fired dry. Reload -> Reloadpump: the action is cycled first, then six shells
#             go in one at a time. 1 + 26 + 47 + 15*5 + 15 = 164 tics.
#             (Tefa's `reload when fully out of ammo` folder holds 162 screenshots.)
#   partial â€” shells still in it. Reload -> ReloadStart: no opening pump cycle, a shorter
#             lift, then one loop per shell. 1 + 15 + 15*N + 15 tics.
#
# Run the partial one by adding `partial` to the arguments, and `static` for the version
# where the gun itself never moves:
#   blender -b --factory-startup --python kit/run_background.py -- anim_shotgun_reload.py partial static
exec(open(r"C:\Users\TD3KX\github-backups\ashes-2063-weapons\kit\anim_kit.py").read())
exec(open(r"C:\Users\TD3KX\github-backups\ashes-2063-weapons\kit\shotgun_settings.py").read())

import sys
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
STATIC = globals().get("STATIC", False)
PARTIAL = "partial" in ARGS
SHELLS = 3 if PARTIAL else 6           # how many go in; the dry gun takes all six

OUT = r"C:\Users\TD3KX\github-backups\ashes-2063-weapons\shotgun\Ashes_2063_EP1_shotgun_reload.blend"
if PARTIAL:
    OUT = OUT.replace("_reload.blend", "_reload_partial.blend")
if STATIC:
    OUT = OUT.replace(".blend", "_static.blend")

# ---- poses -----------------------------------------------------------------
REST = ((0, 0, 0), (0, 0, 0))
# tipped over and up so the loading port underneath faces the loading hand
TIP = ((-0.020, -0.050, 0.008), (24, -72, -10))
# where a shell is pushed in: the loading port on the underside of the receiver
PORT_IN = (0.0, 0.050, REC_Z - REC_H / 2 - 0.004)

reset_scene()
setup_scene("Shotgun_Reload" + ("_Partial" if PARTIAL else ""), 1)
ov, O = link_model(MODEL, "SHOTGUN")
root, pump, trig = O["SG_Root"], O["SG_Pump"], O["SG_Trigger"]
flash, casing, port_shell = O["SG_MuzzleFlash"], O["SG_Casing"], O["SG_PortShell"]
loader = O["SG_LoadShell"]
fp_view(lens=VIEW_LENS_SG)

PX, PY, PZ = PUMP_PIVOT


def gun(f, pose, pump_dy=0.0):
    loc, rot = pose
    if STATIC:
        loc, rot = (0, 0, 0), (0, 0, 0)
    key(root, f, loc=[a + b for a, b in zip(REST_LOC, loc)],
        rot_deg=[a + b for a, b in zip(REST_ROT, rot)])
    key(pump, f, loc=(PX, PY + pump_dy, PZ))


def blend(f0, f1, a, b, steps, pump_a=0.0, pump_b=0.0):
    """Stop-motion hops from pose a to pose b across f0..f1 (CONSTANT keys, so each
    hop is held â€” no sliding)."""
    for i in range(steps + 1):
        t = i / steps
        f = round(f0 + (f1 - f0) * t)
        loc = tuple(x + (y - x) * t for x, y in zip(a[0], b[0]))
        rot = tuple(x + (y - x) * t for x, y in zip(a[1], b[1]))
        gun(f, (loc, rot), pump_a + (pump_b - pump_a) * t)


# ---------------------------------------------------------------------------
# Phase 1 (dry gun only): cycle the action â€” GRIP A-D 2, D-G 1, H 3, I-M 2, GRIZ A 1
# ---------------------------------------------------------------------------
f = 1
gun(f, REST)
key(port_shell, f, hide=not PARTIAL)       # a dry gun has nothing in the port
key(loader, f, hide=True)
key(casing, f, hide=True)
key(flash, f, hide=True)
key(trig, f, rot_deg=(0, 0, 0))

if not PARTIAL:
    blend(2, 13, REST, ((0, 0.004, -0.004), (-3, -1, 2)), 5, 0.0, PUMP_BACK)   # rack back
    for ff in (14, 15, 16):                                                     # held open
        gun(ff, ((0, 0.004, -0.005), (-3, -1, 2)), PUMP_BACK)
    blend(17, 26, ((0, 0.004, -0.005), (-3, -1, 2)), REST, 5, PUMP_BACK, 0.0)   # forward
    gun(27, REST)
    f = 27

# ---------------------------------------------------------------------------
# Phase 2: tip the gun over to reach the loading port
#   dry gun : GRIR A-F 2 each (12 tics), then H 4 and I 3 while the hand comes up
#   partial : GRIR A-E 2 each (10 tics), Z 3, P 2
# ---------------------------------------------------------------------------
lift_len = 12 if not PARTIAL else 10
blend(f + 1, f + lift_len, REST, TIP, 5)
f += lift_len
hold_len = 7 if not PARTIAL else 5          # H 4 + I 3   /   Z 3 + P 2
for ff in range(f + 1, f + hold_len + 1):
    gun(ff, TIP)
f += hold_len

# ---------------------------------------------------------------------------
# Phase 3: the shells, one at a time.
#   The first shell of a dry reload gets the long slot (GRIR J 6, K L, M N N N N,
#   O P P P = 28 tics) because the action still has to close on it. Every shell
#   after that is the 15-tic Reloadloop (P Q R S 2, T U V 1, W 2, X Y 1).
# ---------------------------------------------------------------------------
def load_one(f0, length, close_action):
    """One shell: it rises from below the gun, goes into the port, and is pushed home."""
    steps = [(0.00, (0.030, -0.022, -0.155), (-25, 0, -12), True),
             (0.25, (0.020, 0.010, -0.095), (-15, 0, -7), True),
             (0.50, (0.010, 0.034, -0.040), (-6, 0, -3), True),
             (0.70, PORT_IN, (0, 0, 0), True),
             (0.82, (0, PORT_IN[1] + 0.012, PORT_IN[2] + 0.004), (0, 0, 0), True),
             (0.88, (0, 0, 0), (0, 0, 0), False)]
    for t, loc, rot, shown in steps:
        ff = round(f0 + length * t)
        key(loader, ff, loc=loc, rot_deg=rot, hide=not shown)
        # the gun rocks a little as the shell is pushed home
        nudge = ((TIP[0][0], TIP[0][1] + 0.004 * (t > 0.7), TIP[0][2] + 0.004 * (t > 0.7)),
                 (TIP[1][0] + 3 * (t > 0.7), TIP[1][1], TIP[1][2]))
        gun(ff, TIP if t < 0.7 else nudge)
    if close_action:
        # GRIR M N N N N then O P P P: the action is worked shut on the first round
        a = f0 + round(length * 0.62)
        blend(a, a + 8, TIP, TIP, 4, 0.0, PUMP_BACK * 0.55)
        blend(a + 9, f0 + length - 1, TIP, TIP, 4, PUMP_BACK * 0.55, 0.0)
        key(port_shell, f0 + length - 2, hide=False)     # a round is chambered again


first_len = 28 if not PARTIAL else 15
load_one(f + 1, first_len, close_action=not PARTIAL)
f += first_len
for _ in range(SHELLS - 1):
    load_one(f + 1, 15, close_action=False)
    f += 15

# ---------------------------------------------------------------------------
# Phase 4: ReloadDone â€” GRIR P Z 3, E 2, D C 2, B 2, A 1 = 15 tics back to rest
# ---------------------------------------------------------------------------
key(loader, f + 1, hide=True)
key(port_shell, f + 1, hide=False)
blend(f + 1, f + 14, TIP, REST, 6)
gun(f + 15, REST)
FRAME_END = f + 15

if STATIC:
    side_view(root, (-0.95, 0.15, 0.13), (0, 0.15, 0.02))

finish(OUT, FRAME_END)
print("frames:", FRAME_END, "shells:", SHELLS, "partial:", PARTIAL, "static:", STATIC)
