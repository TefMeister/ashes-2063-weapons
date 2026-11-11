# One unattended FLAT check of the framey gun build (2026-11-11).
# It cannot show the glide itself -- that runs only with a tracked controller -- but it proves the
# new engine starts, loads Ashes with no script errors, and knows the new settings.
#   python tools/glide_test.py
# No keyboard or mouse input at all (another session may be using the PC): the settings are asked
# for on the command line and the game is closed with a window close.
import sys, os, time, subprocess, ctypes, ctypes.wintypes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gzdrive as g

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_renders", "live", "glide-test.log")
os.makedirs(os.path.dirname(LOG), exist_ok=True)
SETTINGS = ("vr_weapon_glide", "vr_weapon_glide_rate", "vr_weapon_glide_percent", "vr_weapon_glide_raw")
SECONDS_IN_LEVEL = 12

log = open(LOG, "w")
args = ["-iwad", r"Resources\freedoom-0.12.1\freedoom2.wad", "-file", r"Resources\AshesSAMenu.pk3",
        r"Resources\lightmodepatch.pk3", r"Resources\Ashes2063Enriched2_23.pk3",
        r"Resources\Ashes2063EnrichedFDPatch.pk3",
        "-config", r"gzdoomvr-tefa\ashes-flat-test.ini", "+vr_mode", "0", "+vid_fullscreen", "0",
        "+win_w", "1280", "+win_h", "720", "+set", "language", "enu", "+snd_musicvolume", "0",
        "-skill", "3", "+map", "MAP01", "+give", "pumpaction", "+give", "Crowbar",
        "+set", "vr_weapon_glide", "1"]
for s in SETTINGS:
    args.append("+" + s)          # a setting with no value prints itself to the console
proc = subprocess.Popen([os.path.join(g.GAME, "gzdoomvr-tefa", "gzdoomvr.exe"), *args],
                        cwd=g.GAME, stdout=log, stderr=subprocess.STDOUT)


def level_window(pid, timeout=90):
    """The game window of OUR process (title has " - " in it; the startup art window has not)."""
    want = pid
    for _ in range(timeout * 2):
        if proc.poll() is not None:
            return None
        for h, t in g.all_windows():
            got = ctypes.wintypes.DWORD()
            g.u32.GetWindowThreadProcessId(h, ctypes.byref(got))
            if got.value == want and " - " in t:
                return h
        time.sleep(0.5)
    return None


h = level_window(proc.pid)
if h:
    time.sleep(SECONDS_IN_LEVEL)
alive = proc.poll() is None
if alive:
    g.quit(proc)
try:
    code = proc.wait(timeout=60)
except subprocess.TimeoutExpired:
    code = None
log.close()

text = open(LOG, encoding="utf-8", errors="replace").read()
lines = text.splitlines()
version = next((l for l in lines if "gvr4" in l), "(no version line)")
found = {s: next((l.strip() for l in lines if l.strip().startswith('"%s"' % s)), None) for s in SETTINGS}
errors = [l for l in lines if "error" in l.lower() and "0 errors" not in l.lower()]
print("engine:", version.strip())
print("level window appeared:", bool(h), "| still running after %d s:" % SECONDS_IN_LEVEL, alive, "| exit code:", code)
for s in SETTINGS:
    print("  ", found[s] or "%s: NOT KNOWN TO THE ENGINE" % s)
print("lines with 'error':", len(errors))
for l in errors[:10]:
    print("   ", l)
print("log:", os.path.abspath(LOG))
ok = bool(h) and alive and all(found.values()) and found["vr_weapon_glide"].endswith('"true"')
raise SystemExit(0 if ok else 1)
