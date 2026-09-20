# One unattended in-game check of the shotgun model: launch (flat, windowed), take the
# shotgun, capture the idle gun, one shot with its pump stroke, and a reload from dry.
# Writes contact sheets and quits through the console.
#   python tools/shotgun_test.py <tag>
# Same shape as revolver_test.py; the differences are the weapon and that the shotgun has
# to be given and selected first (the player does not spawn with it).
import sys, time, glob, os, ctypes
from ctypes import wintypes as w
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gzdrive as g
from PIL import Image

TAG = sys.argv[1] if len(sys.argv) > 1 else "run"
ENGINE = sys.argv[2] if len(sys.argv) > 2 else "gzdoomvr-tefa"
PK3 = r"C:\Users\TD3KX\github-backups\ashes-2063-weapons\shotgun\gzdoom\Ashes2063_shotgun3d_test.pk3"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_renders", "live", TAG)
os.makedirs(OUT, exist_ok=True)


class MI(ctypes.Structure):
    _fields_ = [("dx", w.LONG), ("dy", w.LONG), ("mouseData", w.DWORD), ("dwFlags", w.DWORD),
                ("time", w.DWORD), ("dwExtraInfo", ctypes.POINTER(w.ULONG))]
class MU(ctypes.Union): _fields_ = [("mi", MI), ("pad", ctypes.c_ubyte * 32)]
class MIN(ctypes.Structure): _fields_ = [("type", w.DWORD), ("u", MU)]


def click():
    for fl in (2, 4):
        i = MIN(); i.type = 0; i.u.mi = MI(0, 0, 0, fl, 0, None)
        g.u32.SendInput(1, ctypes.byref(i), ctypes.sizeof(MIN)); time.sleep(0.03)


def game_window(pid, timeout=60):
    for _ in range(timeout * 2):
        for h, t in g.all_windows():
            p = ctypes.c_ulong(); g.u32.GetWindowThreadProcessId(h, ctypes.byref(p))
            if p.value == pid and " - " in t:      # the title gains the map name once in a level
                return h
        time.sleep(0.5)
    raise SystemExit("no game window")


def burst(h, name, n, gap):
    for k in range(n):
        g.shot(h, os.path.join(OUT, f"{name}_{k:02d}.bmp")); time.sleep(gap)


def sheet(name, cols):
    fs = sorted(glob.glob(os.path.join(OUT, f"{name}_*.bmp")))
    ims = [Image.open(f).resize((316, 170)) for f in fs]
    o = Image.new("RGB", (cols * 316, ((len(ims) + cols - 1) // cols) * 170))
    for i, im in enumerate(ims):
        o.paste(im, ((i % cols) * 316, (i // cols) * 170))
    o.save(os.path.join(OUT, f"sheet_{name}.png"))
    for f in fs:
        os.remove(f)


if __name__ != "__main__":
    raise ImportError("shotgun_test.py is a script, run it directly")

proc = g.launch(extra_files=(PK3,), engine=ENGINE)
h = game_window(proc.pid)
time.sleep(4)
if not g.fg(h):
    raise SystemExit("could not bring the game to the front")

g.console("bind r +reload")
g.console("give pumpaction")
g.console("give shotgunammo 30")
g.key('3')                      # slot 3 is the shotgun
time.sleep(1.5)
burst(h, "idle", 1, 0)
Image.open(os.path.join(OUT, "idle_00.bmp")).save(os.path.join(OUT, "idle_full.png"))

# one shot and the pump stroke that follows (30 tics, so ~0.9 s)
click(); burst(h, "fire", 20, 0.02)
time.sleep(1.5)

# empty it, then the dry reload: the action is cycled and six shells go in (164 tics, ~4.7 s)
for _ in range(6):
    click(); time.sleep(1.1)
time.sleep(0.5)
g.key('r'); burst(h, "reload", 48, 0.10)

for n, c in (("idle", 1), ("fire", 5), ("reload", 8)):
    sheet(n, c)
g.console("quit")
proc.wait(timeout=30)
print("done", OUT, "exit", proc.returncode)
