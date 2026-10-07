"""One unattended FLAT run of a light probe pk3 on the cube shotgun: launch, wait, screenshot, quit.
    python light_probe_run.py <probe pk3> <screenshot bmp> <log txt> [extra console commands...]
"""
import sys, os, time, subprocess, ctypes, ctypes.wintypes
sys.path.insert(0, r"C:\Users\TD3KX\github-backups\ashes-2063-weapons\tools")
import gzdrive as g

PROBE, SHOT, LOG = sys.argv[1], sys.argv[2], sys.argv[3]
EXTRA = sys.argv[4:]
SHOTGUN = r"D:\Ashes 2063\3D blender\ashes shotgun\blender\gzdoom\Ashes2063_cube_shotgun_VR_test.pk3"


def game_window(pid, timeout=60):
    want = ctypes.wintypes.DWORD(pid)
    for _ in range(timeout * 2):
        for h, _t in g.all_windows():
            got = ctypes.wintypes.DWORD()
            g.u32.GetWindowThreadProcessId(h, ctypes.byref(got))
            if got.value == want.value:
                return h
        time.sleep(0.5)
    return None


args = ["-iwad", r"Resources\freedoom-0.12.1\freedoom2.wad", "-file", r"Resources\AshesSAMenu.pk3",
        r"Resources\lightmodepatch.pk3", r"Resources\Ashes2063Enriched2_23.pk3",
        r"Resources\Ashes2063EnrichedFDPatch.pk3", SHOTGUN, PROBE,
        "-config", r"gzdoomvr-tefa\ashes-flat-test.ini", "+vr_mode", "0", "+vid_fullscreen", "0",
        "+win_w", "1280", "+win_h", "720", "+set", "language", "enu", "-skill", "3", "+map", "MAP01",
        "+give", "pumpaction", "+give", "shotgunammo", "40", "+use", "pumpaction", "+snd_musicvolume", "0"]
log = open(LOG, "w")
proc = subprocess.Popen([os.path.join(g.GAME, "gzdoomvr-tefa", "gzdoomvr.exe"), *args],
                        cwd=g.GAME, stdout=log, stderr=subprocess.STDOUT)
h = game_window(proc.pid)
if not h:
    proc.kill(); log.close(); raise SystemExit("no game window")
time.sleep(6)
# record the game window only (standing rule); OBS needs the window to exist first
OBS = r"C:\Users\TD3KX\claude-memory\tools\obs-rec.py"
LABEL = os.path.splitext(os.path.basename(PROBE))[0] + "-flat"
subprocess.run([sys.executable, OBS, "start", "gzdoomvr.exe", LABEL, "--game", "ashes-2063-weapons"])
g.fg(h)
time.sleep(2)
print("window", g.rect(h), "shot", g.shot(h, SHOT))
if EXTRA:
    for c in EXTRA:
        g.console(c)
    time.sleep(1.5)
    print("shot2", g.shot(h, SHOT.replace(".bmp", "_2.bmp")))
subprocess.run([sys.executable, OBS, "stop"])
g.console("quit")
try:
    proc.wait(timeout=60)
except subprocess.TimeoutExpired:
    proc.kill(); print("had to kill the game")
log.close()
text = open(LOG, encoding="utf-8", errors="replace").read()
for line in text.splitlines():
    low = line.lower()
    if "error" in low or "shader" in low or "lightprobe" in low or "warning" in low:
        print("  LOG:", line[:200])
print("exit", proc.returncode)
