"""One unattended FLAT run of the darkness test (2026-10-25): the player's sector is held at each test light,
and the shotgun is pictured with vr_gun_darkness at each strength. No recording (standing rule).
    python darkness_run.py <out dir>
Prints, per picture, the mean brightness of the gun area against the room around it.
"""
import sys, os, time, zipfile, subprocess, ctypes, ctypes.wintypes
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gzdrive as g
from PIL import Image

OUT = os.path.abspath(sys.argv[1])
os.makedirs(OUT, exist_ok=True)
SHOTGUN = r"D:\Ashes 2063\3D blender\ashes shotgun\blender\gzdoom\Ashes2063_cube_shotgun_VR_test.pk3"
LIGHTS = (64, 96, 128, 160)          # room light levels to test
STRENGTHS = (0, 1, 2)                # vr_gun_darkness values
SETTLE = 1.2                         # seconds after a console change before the picture
GUN_BOX = (0.35, 0.62, 0.75, 1.0)    # gun area, fractions of the picture (left, top, right, bottom)
ROOM_BOX = (0.0, 0.25, 1.0, 0.55)    # a band of the room above the gun

pk3 = os.path.join(OUT, "darkness_test.pk3")
with zipfile.ZipFile(pk3, "w", zipfile.ZIP_DEFLATED) as z:
    for name in os.listdir(os.path.join(HERE, "pk3")):
        z.write(os.path.join(HERE, "pk3", name), name)


def game_window(pid, timeout=90):
    want = pid
    for _ in range(timeout * 2):
        for h, title in g.all_windows():
            got = ctypes.wintypes.DWORD()
            g.u32.GetWindowThreadProcessId(h, ctypes.byref(got))
            if got.value == want and " - " in title:
                return h
        time.sleep(0.5)
    return None


def mean(img, box):
    w, h = img.size
    crop = img.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h))).convert("L")
    data = list(crop.getdata())
    return sum(data) / len(data)


args = ["-iwad", r"Resources\freedoom-0.12.1\freedoom2.wad", "-file", r"Resources\AshesSAMenu.pk3",
        r"Resources\lightmodepatch.pk3", r"Resources\Ashes2063Enriched2_23.pk3",
        r"Resources\Ashes2063EnrichedFDPatch.pk3", SHOTGUN, pk3,
        "-config", r"gzdoomvr-tefa\ashes-flat-test.ini", "+vr_mode", "0", "+vid_fullscreen", "0",
        "+win_w", "1280", "+win_h", "720", "+set", "language", "enu", "-skill", "3", "+map", "MAP01",
        "+give", "pumpaction", "+give", "shotgunammo", "40", "+use", "pumpaction", "+snd_musicvolume", "0"]
log_path = os.path.join(OUT, "run.log")
log = open(log_path, "w")
proc = subprocess.Popen([os.path.join(g.GAME, "gzdoomvr-tefa", "gzdoomvr.exe"), *args],
                        cwd=g.GAME, stdout=log, stderr=subprocess.STDOUT)
h = game_window(proc.pid)
if not h:
    proc.kill(); log.close(); raise SystemExit("no game window")
time.sleep(20)
g.fg(h)
time.sleep(1)
g.console("vr_gun_darkness")      # prints the setting, proving the new engine is the one running
rows = []
for light in LIGHTS:
    g.console("tefa_testlight %d" % light)
    for s in STRENGTHS:
        g.console("vr_gun_darkness %d" % s)
        time.sleep(SETTLE)
        path = os.path.join(OUT, "light%03d_dark%d.bmp" % (light, s))
        g.shot(h, path)
        img = Image.open(path)
        rows.append((light, s, mean(img, GUN_BOX), mean(img, ROOM_BOX)))
        print("light %3d  darkness %d   gun %6.1f   room %6.1f" % rows[-1], flush=True)
g.console("tefa_testlight -1")
g.console("vr_gun_darkness 1")
g.quit(proc)
try:
    proc.wait(timeout=60)
except subprocess.TimeoutExpired:
    proc.kill(); print("had to kill the game")
log.close()
for line in open(log_path, encoding="utf-8", errors="replace"):
    low = line.lower()
    if "error" in low or "darkness" in low or "tefa" in low:
        print("  LOG:", line.rstrip()[:200])
print("exit", proc.returncode)
