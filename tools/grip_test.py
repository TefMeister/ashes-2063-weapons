# One unattended FLAT check of the two-handed handler. It cannot test the aim itself -- that
# needs two tracked hands -- but it proves everything up to that point: the gun is recognised as
# a long gun, nothing else is being asked for, and the ONLY thing standing between it and
# two-handed aiming is a second tracked hand, which the headset supplies.
#   python tools/grip_test.py
# Passes when the game's own console says "two-handed aim: off (off hand not tracked)" -- i.e.
# it got as far as it can get with one hand -- and when the (now optional) grip button is seen.
import sys, os, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gzdrive as g

# Repo-relative; the old absolute path stopped existing when the clone root moved (2026-08-31).
PK3 = os.path.join(g.REPO, "shotgun", "gzdoom", "Ashes2063_shotgun3d_VR_test.pk3")
LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_renders", "live", "grip-test.log")
os.makedirs(os.path.dirname(LOG), exist_ok=True)
KEY = 'k'                 # a keyboard stand-in for the controller's grip
HOLD_SECONDS = 1.5

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
g.console("bind %s +tefagrip" % KEY)
time.sleep(0.5)

# hold the stand-in grip, then let go
g._raw(g.SC[KEY], False)
time.sleep(HOLD_SECONDS)
g._raw(g.SC[KEY], True)
time.sleep(1.0)

g.console("quit")
proc.wait(timeout=60)
log.close()

text = open(LOG, encoding="utf-8", errors="replace").read()
ready = "two-handed aim: off (off hand not tracked)" in text
held = "grip: HELD" in text
letgo = "grip: let go" in text
print("long gun recognised, waiting only on the off hand:", ready)
print("grip button seen:", held, "/", letgo)
print("log:", os.path.abspath(LOG))
for line in text.splitlines():
    if "grip" in line or "two-handed" in line:
        print("  ", line)
raise SystemExit(0 if (ready and held and letgo) else 1)
