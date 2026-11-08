"""Our GZDoom VR build in the OpenXR Simulator (through OpenComposite), the cube shotgun + a light probe, the right
hand turned through a set of poses by VR Bench, a two-eye picture after each.
    python vr_probe.py <probe pk3 | none> <out folder> [wait s]
"""
import ctypes
import ctypes.wintypes
import os
import shutil
import subprocess
import sys
import time



def _conf(key, default=""):
    """`key = value` from this PC's lanes.conf (2026-11-08: the folders below were the dev PC's, written in)"""
    import re
    path = os.environ.get("LANES_CONFIG") or os.path.expanduser(os.path.join("~", ".claude", "lanes.conf"))
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                m = re.match(r"^\s*" + re.escape(key) + r"\s*=\s*(.*?)\s*(?:\s#.*)?$", line.rstrip("\r\n"))
                if m:
                    return m.group(1).strip().strip('"')
    except OSError:
        pass
    return default


def _lanes_root():
    """the Lanes this PC runs (active-root.txt); the newest plugin-cache folder only as a last resort"""
    cand = os.environ.get("LANES_PLUGIN_ROOT", "")
    if cand and os.path.isdir(cand):
        return cand
    try:
        with open(os.path.expanduser(os.path.join("~", ".claude", "lanes", "active-root.txt")), encoding="utf-8") as f:
            cand = f.read().strip()
        if os.path.isdir(cand):
            return cand
    except OSError:
        pass
    cache = os.path.expanduser(os.path.join("~", ".claude", "plugins", "cache", "lanes-plugin", "lanes"))
    newest = max(os.listdir(cache), key=lambda v: tuple(int(p) for p in v.split(".") if p.isdigit()))
    return os.path.join(cache, newest)


TOOLS = os.path.join(_lanes_root(), "tools", "vrbench")
sys.path.insert(0, TOOLS)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gzdrive as g  # noqa: E402
import vb_input as I  # noqa: E402
import vb_settings as S  # noqa: E402
import vb_sim  # noqa: E402

PROBE, OUT = sys.argv[1], sys.argv[2]
WAIT = float(sys.argv[3]) if len(sys.argv) > 3 else 25
DEV = _conf("ashes_dev", r"E:\Ashes2063VR-dev")                       # our engine copies (engine-oc = OpenComposite)
RES = _conf("ashes_res", r"D:\ashes2063vr\Ashes 2063 VR\Resources")   # the game's own files
GZ = _conf("ashes_shotgun_gz", r"E:\MEGA transfer\Game Files\ashes-2063-weapons\3D blender\ashes shotgun\blender\gzdoom")
EXE = os.path.join(DEV, "engine-oc", "gzdoomvr.exe")
SIM_JSON = os.path.join(_conf("openxr_sim", r"D:\claude video game stuff\tools\OpenXR-Simulator"), "openxr_simulator.json")
CFG = os.path.join(DEV, "ashes-dev-vr.ini")
VRBENCH = [sys.executable, os.path.join(TOOLS, "vrbench.py")]

HAND_AT = (0.18, 1.35, -0.40)        # right hand: a little right, below the eyes, ahead (room metres)
LEFT_AT = (-0.05, 1.38, -0.70)       # left hand out along the barrel, for the two-handed hold
POSES = [                            # (name, yaw, pitch, roll) of the right hand, degrees
    ("rest", 0, 0, 0), ("yaw_left_30", 30, 0, 0), ("yaw_right_30", -30, 0, 0),
    ("pitch_up_25", 0, 25, 0), ("pitch_down_25", 0, -25, 0), ("roll_left_45", 0, 0, 45), ("roll_right_45", 0, 0, -45),
]
os.makedirs(OUT, exist_ok=True)


def windows_of(pid):
    out = []
    for h, t in g.all_windows():
        got = ctypes.wintypes.DWORD()
        g.u32.GetWindowThreadProcessId(h, ctypes.byref(got))
        if got.value == pid:
            out.append((h, t))
    return out


def hands(yaw, pitch, roll):
    inp = I.Input().mode(poses="set", buttons="pass")
    inp.hand(S.HAND_RIGHT, grip=I.pose_from_ypr(HAND_AT, yaw, pitch, roll), aim=I.pose_from_ypr(HAND_AT, yaw, pitch, roll))
    inp.hand(S.HAND_LEFT, grip=I.pose_from_ypr(LEFT_AT, 0, 0, 0), aim=I.pose_from_ypr(LEFT_AT, 0, 0, 0))
    I.write(inp)


if not os.path.exists(CFG) and os.path.exists(os.path.join(DEV, "ashes-dev-flat.ini")):
    shutil.copy(os.path.join(DEV, "ashes-dev-flat.ini"), CFG)
_SET = os.path.join(DEV, "3DWeapons", "set-settings.ps1")   # the dev PC's settings helper; the home PC has none
if os.path.exists(_SET):
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", _SET, CFG])
print("bench start:", subprocess.run(VRBENCH + ["start", EXE], capture_output=True, text=True).stdout.strip()[-300:])
hands(0, 0, 0)
vb_sim.head(0.0, 1.6, 0.0, 0, -10)

files = [os.path.join(RES, n) for n in ("AshesSAMenu.pk3", "lightmodepatch.pk3", "Ashes2063Enriched2_23.pk3",
                                       "Ashes2063EnrichedFDPatch.pk3")]
files += [os.path.join(GZ, "Ashes2063_cube_shotgun_VR_test.pk3")] + ([PROBE] if PROBE != "none" else [])
args = ["-iwad", os.path.join(RES, "freedoom-0.12.1", "freedoom2.wad"), "-file", *files, "-config", CFG,
        "+vr_mode", "10", "+vid_fullscreen", "0", "+win_w", "1280", "+win_h", "720", "+set", "language", "enu",
        "-skill", "3", "+map", "MAP01", "+give", "pumpaction", "+give", "shotgunammo", "40", "+use", "pumpaction",
        "+set", "vr_two_handed_min_sep", "0", "+set", "vr_two_handed_max_disagree", "180", "+snd_musicvolume", "0"] + os.environ.get("VRPROBE_ARGS", "").split()
env = dict(os.environ, XR_RUNTIME_JSON=SIM_JSON)
log = open(os.path.join(OUT, "game.log"), "w")
proc = subprocess.Popen([EXE, *args], cwd=os.path.dirname(EXE), stdout=log, stderr=subprocess.STDOUT, env=env)
try:
    t0 = time.time()
    h = None
    while time.time() - t0 < 120 and proc.poll() is None:
        lv = [w for w in windows_of(proc.pid) if " - " in w[1]]
        if lv:
            h = lv[0][0]
            break
        time.sleep(0.5)
    print("level window:", bool(h), "after %.0f s" % (time.time() - t0), "exit" if proc.poll() is not None else "")
    time.sleep(WAIT)
    print("simulator loaded in game:", vb_sim.loaded_in(proc.pid))
    print("windows:", [t for _h, t in windows_of(proc.pid)])
    for name, yaw, pitch, roll in POSES:
        hands(yaw, pitch, roll)
        time.sleep(1.5)
        ok = vb_sim.screenshot(os.path.join(OUT, "vr_%s.png" % name), timeout_s=8)
        print("pose", name, "picture", ok)
    hands(0, 0, 0)
finally:
    if proc.poll() is None:
        g.quit(proc, timeout=40)     # closes the window; never types, so it needs nothing in front
    log.close()
    print("bench stop:", subprocess.run(VRBENCH + ["stop"], capture_output=True, text=True).stdout.strip()[-200:])
    for line in open(os.path.join(OUT, "game.log"), encoding="utf-8", errors="replace"):
        low = line.lower()
        if any(k in low for k in ("error", "openvr", "openxr", "vr ", "lightprobe", "hmd", "fatal")):
            print("  LOG:", line.rstrip()[:200])
    print("exit", proc.returncode)
