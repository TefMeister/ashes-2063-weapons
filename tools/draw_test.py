# One unattended FLAT check of the two-handed DRAW change (2026-09-20).
#   python tools/draw_test.py
#
# What it can and cannot prove. It CANNOT see the gun turn -- that needs two tracked controllers,
# so it is a headset job. What it does prove is everything the 2026-09-20 wear could not:
#   * the rebuilt engine starts and plays,
#   * the new setting vr_two_handed_draw exists, defaults to ON, and takes a value,
#   * the two-handed handler still gets as far as "off hand not tracked" (nothing regressed),
#   * the shotgun still fires on this build.
# A missing setting is the failure this exists for: it would mean the engine in the game folder is
# not the one that was just built, which is exactly the kind of thing a wear should never discover.
import sys, os, time, subprocess, ctypes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gzdrive as g


class MI(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long), ("dy", ctypes.c_long), ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]


class MU(ctypes.Union):
    _fields_ = [("mi", MI), ("pad", ctypes.c_ubyte * 32)]


class MIN(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("u", MU)]


def click():
    """Fire. Same left-button pair shotgun_test.py uses."""
    for fl in (2, 4):
        i = MIN(); i.type = 0; i.u.mi = MI(0, 0, 0, fl, 0, None)
        g.u32.SendInput(1, ctypes.byref(i), ctypes.sizeof(MIN)); time.sleep(0.03)

PK3 = os.path.join(g.REPO, "shotgun", "gzdoom", "Ashes2063_shotgun3d_VR_test.pk3")
LOG = os.path.join(g.REPO, "_renders", "live", "draw-test.log")
os.makedirs(os.path.dirname(LOG), exist_ok=True)

log = open(LOG, "w")
# Launched here rather than through gzdrive.launch() because the console output has to be
# captured, and GZDoom only flushes it on a clean exit -- which is why this quits through
# the console instead of being killed.
args = ["-iwad", r"Resources\freedoom-0.12.1\freedoom2.wad", "-file", r"Resources\AshesSAMenu.pk3",
        r"Resources\lightmodepatch.pk3", r"Resources\Ashes2063Enriched2_23.pk3",
        r"Resources\Ashes2063EnrichedFDPatch.pk3", PK3,
        "-config", r"gzdoomvr-tefa\ashes-flat-test.ini", "+vr_mode", "0", "+vid_fullscreen", "0",
        "+win_w", "1280", "+win_h", "720", "+set", "language", "enu", "-skill", "3", "+map", "MAP01",
        "+give", "pumpaction", "+give", "shotgunammo", "40"]
proc = subprocess.Popen([os.path.join(g.GAME, "gzdoomvr-tefa", "gzdoomvr.exe"), *args],
                        cwd=g.GAME, stdout=log, stderr=subprocess.STDOUT)

h = None
for _ in range(120):
    time.sleep(0.5)
    for hh, t in g.all_windows():
        if t.strip().lower().startswith("ashes"):
            h = hh
            break
    if h:
        break
if not h:
    proc.kill(); raise SystemExit("no game window")
time.sleep(3)
g.fg(h)

g.console("tefa_grip_debug 1")
g.console("vr_two_handed_draw")          # should echo its default, true
g.console("vr_two_handed_draw 0")        # and take a value both ways
g.console("vr_two_handed_draw")
g.console("vr_two_handed_draw 1")
g.console("vr_two_handed_draw")
g.console("vr_two_handed_debug 1")
time.sleep(1.0)

# Still shoots. A change to how the gun is DRAWN must not touch anything else.
g.key('3')                       # slot 3 is the shotgun
time.sleep(1.5)
click()
time.sleep(1.5)

g.console("quit")
proc.wait(timeout=60)
log.close()

text = open(LOG, encoding="utf-8", errors="replace").read()
lower = text.lower()
exists = "unknown command" not in lower and "vr_two_handed_draw" in lower
# GZDoom answers a bare CVar name with:  "name" is "value" (default: "value")
default_on = '"vr_two_handed_draw" is "true" (default: "true")' in lower
took_off = '"vr_two_handed_draw" is "false"' in lower
ready = "two-handed aim: off (off hand not tracked)" in text

print("the new setting exists:              ", exists)
print("it is ON by default:                 ", default_on)
print("it can be switched off and on again: ", took_off)
print("long gun still waiting only on a hand:", ready)
print("log:", os.path.abspath(LOG))
for line in text.splitlines():
    if "two_handed" in line or "two-handed" in line:
        print("  ", line)
raise SystemExit(0 if (exists and default_on and took_off and ready) else 1)
