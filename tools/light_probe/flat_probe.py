"""One flat run of our GZDoom VR build (v0.1.1 engine) on the dev PC with the cube shotgun + a light probe.
    python flat_probe.py <probe pk3> <out folder> [console commands...]
"""
import ctypes
import ctypes.wintypes
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gzdrive as g  # noqa: E402

PROBE, OUT = sys.argv[1], sys.argv[2]
EXTRA = sys.argv[3:]
DEV = r"E:\Ashes2063VR-dev"
RES = r"D:\ashes2063vr\Ashes 2063 VR\Resources"
GZ = r"E:\MEGA transfer\Game Files\ashes-2063-weapons\3D blender\ashes shotgun\blender\gzdoom"
EXE = os.path.join(DEV, "3DWeapons", "engine", "gzdoomvr.exe")
os.makedirs(OUT, exist_ok=True)


def game_window(pid, timeout=90):
    for _ in range(timeout * 2):
        for h, t in g.all_windows():
            got = ctypes.wintypes.DWORD()
            g.u32.GetWindowThreadProcessId(h, ctypes.byref(got))
            if got.value == pid and " - " in t:      # the level window, not the startup screen
                return h
        time.sleep(0.5)
    return None


files = [os.path.join(RES, n) for n in ("AshesSAMenu.pk3", "lightmodepatch.pk3", "Ashes2063Enriched2_23.pk3",
                                       "Ashes2063EnrichedFDPatch.pk3")]
files += [os.path.join(GZ, "Ashes2063_cube_shotgun_VR_test.pk3")] + ([PROBE] if PROBE != "none" else [])
args = ["-iwad", os.path.join(RES, "freedoom-0.12.1", "freedoom2.wad"), "-file", *files,
        "-config", os.path.join(DEV, "ashes-dev-flat.ini"), "+vr_mode", "0", "+vid_fullscreen", "0",
        "+win_w", "1280", "+win_h", "720", "+set", "language", "enu", "-skill", "3", "+map", "MAP01",
        "+give", "pumpaction", "+give", "shotgunammo", "40", "+use", "pumpaction", "+snd_musicvolume", "0"]
log = open(os.path.join(OUT, "game.log"), "w")
proc = subprocess.Popen([EXE, *args], cwd=os.path.dirname(EXE), stdout=log, stderr=subprocess.STDOUT)
h = game_window(proc.pid)
if not h:
    proc.kill()
    raise SystemExit("no game window")
time.sleep(10)
g.fg(h)
time.sleep(1.5)
print("window", g.rect(h), "shot", g.shot(h, os.path.join(OUT, "flat_1.bmp")))
for i, c in enumerate(EXTRA):
    g.console(c)
    time.sleep(1.5)
    print("shot", g.shot(h, os.path.join(OUT, "flat_%d.bmp" % (i + 2))))
g.quit(proc)
log.close()
for line in open(os.path.join(OUT, "game.log"), encoding="utf-8", errors="replace"):
    low = line.lower()
    if "error" in low or "shader" in low or "lightprobe" in low or "warning" in low or "openvr" in low:
        print("  LOG:", line.rstrip()[:200])
print("exit", proc.returncode)
