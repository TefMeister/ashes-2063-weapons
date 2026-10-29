"""run_body_test_sim.py -- the body rig in the OpenXR Simulator on the dev PC: no headset, nobody in front (2026-10-29).

Our GZDoom VR build talks OpenVR; OpenComposite's openvr_api.dll turns that into OpenXR, the simulator plays the
headset and VR Bench plays the hands (the route tools/light_probe/vr_probe.py proved on 2026-10-18). The body test
pk3 (build_body_test.py) is loaded with a tiny walker pk3 written here, which pushes the player forward and then
sideways for a few seconds so the legs have a speed to step with. A two-eye picture is taken at every step.

    python body/run_body_test_sim.py <out folder>            (needs build_body_test.py --deploy done first)
    python body/run_body_test_sim.py <out folder> flat       (a flat run only: proves the pack and engine load)

Never types into the game and needs nothing in front: the walker, the head and the hands are all driven from here.
"""
import ctypes
import ctypes.wintypes
import io
import os
import subprocess
import sys
import time
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
_LANES = os.path.expanduser(r"~\.claude\plugins\cache\lanes-plugin\lanes")
_NEWEST = max(os.listdir(_LANES), key=lambda v: tuple(int(p) for p in v.split(".") if p.isdigit()))
TOOLS = os.path.join(_LANES, _NEWEST, "tools", "vrbench")
sys.path.insert(0, TOOLS)
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import gzdrive as g  # noqa: E402
import vb_input as I  # noqa: E402
import vb_settings as S  # noqa: E402
import vb_sim  # noqa: E402

OUT = sys.argv[1]
FLAT = len(sys.argv) > 2 and sys.argv[2] == "flat"
DEV = r"E:\Ashes2063VR-dev"
RES = r"D:\ashes2063vr\Ashes 2063 VR\Resources"
TEST = os.path.join(DEV, "body-test")
EXE = os.path.join(TEST, "engine" if FLAT else "engine-oc", "gzdoom.exe")
BODY_PK3 = os.path.join(TEST, "Ashes2063_body_test.pk3")
SIM_JSON = r"D:\claude video game stuff\tools\OpenXR-Simulator\openxr_simulator.json"
CFG = os.path.join(DEV, "ashes-dev-vr.ini")
VRBENCH = [sys.executable, os.path.join(TOOLS, "vrbench.py")]

EYE_Y = 1.65                          # standing eye height, metres (the rig's own standing case)
CROUCH_Y = 1.15
WALK_AT_S = 45                         # the walker starts this many seconds after the level has been running...
WALK_FWD_S = 4                        # ...walks forward this long...
WALK_SIDE_S = 3                       # ...then strafes right this long
WALK_SPEED = 4.0                      # map units per tic (~8.2 m/s at 34 units/m: a Doom run; the rig caps stride at 1.2 m/s)
LEVEL_WAIT_S = 120
RECORD = os.environ.get("BODYTEST_RECORD")         # a label: record the game window (and the simulator preview) with OBS
OBS_REC = [sys.executable, os.path.join(_LANES, _NEWEST, "tools", "obs-rec.py")]
if RECORD:
    SETTLE_S = 3.5                    # slower, so each pose can be seen in the clip
LOOK_AHEAD = os.environ.get("BODYTEST_LOOK_AHEAD")   # set with vr_body_preview: every picture looks ahead at the body
SETTLE_S = 1.5                        # after moving the head or hands, before a picture

WALKER_ZS = """version "4.10"
// Test only: pushes the player so the body rig's legs have a speed. Started by maptime, logged to the console.
// First it turns the player toward the most open of 16 directions, so the walk is not straight into a wall.
class TefaBodyWalker : EventHandler
{
	double side;
	override void WorldTick()
	{
		let pmo = players[consoleplayer].mo;
		if (!pmo) return;
		int t = Level.maptime, a = %d * 35, b = a + %d * 35, c = b + %d * 35;
		if (t == a - 35)
		{
			double best = -1, bestAng = pmo.angle;
			FLineTraceData d;
			for (int i = 0; i < 16; i++)
			{
				double ang = i * 22.5;
				pmo.LineTrace(ang, 4096, 0, TRF_THRUACTORS, 24, data: d);
				if (d.Distance > best) { best = d.Distance; bestAng = ang; }
			}
			FLineTraceData l, r;
			pmo.LineTrace(bestAng + 90, 4096, 0, TRF_THRUACTORS, 24, data: l);
			pmo.LineTrace(bestAng - 90, 4096, 0, TRF_THRUACTORS, 24, data: r);
			side = (l.Distance > r.Distance) ? 90 : -90;
			pmo.A_SetAngle(bestAng, SPF_INTERPOLATE);
			Console.Printf("BODYTEST turned to %%.0f (%%.0f units open), will strafe %%s", bestAng, best, side > 0 ? "left" : "right");
		}
		if (t == a) Console.Printf("BODYTEST walk forward");
		if (t == b) Console.Printf("BODYTEST walk side");
		if (t == c) Console.Printf("BODYTEST walk stop");
		if (t >= a && t < b) pmo.Vel.XY = Actor.AngleToVector(pmo.angle, %g);
		else if (t >= b && t < c) pmo.Vel.XY = Actor.AngleToVector(pmo.angle + side, %g);
		else if (t == c) pmo.Vel.XY = (0, 0);
	}
}
""" % (WALK_AT_S, WALK_FWD_S, WALK_SIDE_S, WALK_SPEED, WALK_SPEED)


def walker_pk3(path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("zscript.txt", WALKER_ZS)
        z.writestr("mapinfo.walker", 'GameInfo { AddEventHandlers = "TefaBodyWalker" }\n')


def windows_of(pid):
    out = []
    for h, t in g.all_windows():
        got = ctypes.wintypes.DWORD()
        g.u32.GetWindowThreadProcessId(h, ctypes.byref(got))
        if got.value == pid:
            out.append((h, t))
    return out


def hands(left, right, pitch=0.0):
    """Both controllers at room positions (metres), pointing ahead and pitched by `pitch` degrees."""
    inp = I.Input().mode(poses="set", buttons="pass")
    for side, at in ((S.HAND_LEFT, left), (S.HAND_RIGHT, right)):
        p = I.pose_from_ypr(at, 0, pitch, 0)
        inp.hand(side, grip=p, aim=p)
    I.write(inp)


def log_lines(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.readlines()
    except OSError:
        return []


def wait_for(path, text, timeout):
    t0 = time.time()
    while time.time() - t0 < timeout:
        if any(text in l for l in log_lines(path)):
            return True
        time.sleep(0.25)
    return False


STEPS = [  # (picture name, head (y, pitch), left hand, right hand, hand pitch)
    ("stand_ahead", (EYE_Y, 0), (-0.22, 1.10, -0.22), (0.22, 1.10, -0.22), 0),
    ("stand_look_down", (EYE_Y, -60), (-0.22, 1.10, -0.22), (0.22, 1.10, -0.22), 0),
    ("hands_out_front", (EYE_Y, -20), (-0.15, 1.40, -0.50), (0.15, 1.40, -0.50), 0),
    ("hands_down_sides", (EYE_Y, -55), (-0.30, 0.90, 0.0), (0.30, 0.90, 0.0), -60),
    ("hands_wide", (EYE_Y, -10), (-0.60, 1.40, -0.25), (0.60, 1.40, -0.25), 0),
    ("crouch_look_down", (CROUCH_Y, -55), (-0.22, 0.75, -0.30), (0.22, 0.75, -0.30), 0),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    walker = os.path.join(OUT, "bodytest_walker.pk3")
    walker_pk3(walker)
    log_path = os.path.join(OUT, "game.log")
    files = [os.path.join(RES, n) for n in ("AshesSAMenu.pk3", "lightmodepatch.pk3", "Ashes2063Enriched2_23.pk3",
                                           "Ashes2063EnrichedFDPatch.pk3")] + [BODY_PK3, walker]
    args = ["-iwad", os.path.join(RES, "freedoom-0.12.1", "freedoom2.wad"), "-file", *files, "-config", CFG,
            "+vr_mode", "0" if FLAT else "10", "+vid_fullscreen", "0", "+win_w", "1280", "+win_h", "720",
            "+set", "language", "enu", "-skill", "3", "+map", "MAP01", "+snd_musicvolume", "0",
            "+set", "vr_body", "1", "+set", "vr_body_debug", "1", "+set", "vr_floor_offset", "0", "+notarget"] + os.environ.get("BODYTEST_ARGS", "").split()
    env = dict(os.environ)
    if not FLAT:
        env["XR_RUNTIME_JSON"] = SIM_JSON
        print("bench start:", subprocess.run(VRBENCH + ["start", EXE], capture_output=True, text=True).stdout.strip()[-300:])
        hands(*STEPS[0][2:])
        vb_sim.head(0.0, EYE_Y, 0.0, 0, 0)
    log = open(log_path, "w")
    proc = subprocess.Popen([EXE, *args], cwd=os.path.dirname(EXE), stdout=log, stderr=subprocess.STDOUT, env=env)
    try:
        t0 = time.time()
        h = None
        while time.time() - t0 < LEVEL_WAIT_S and proc.poll() is None:
            lv = [w for w in windows_of(proc.pid) if " - " in w[1]]
            if lv:
                h = lv[0][0]
                break
            time.sleep(0.5)
        print("level window:", bool(h), "after %.0f s" % (time.time() - t0), "EXITED" if proc.poll() is not None else "")
        if FLAT or not h:
            time.sleep(10 if h else 0)
            if h:
                g.shot(h, os.path.join(OUT, "flat.png"))
            return
        print("simulator loaded in game:", vb_sim.loaded_in(proc.pid))
        if RECORD:
            r = subprocess.run(OBS_REC + ["start", "gzdoom.exe", RECORD, "--game", "ashes-2063-weapons"], capture_output=True, text=True)
            print("record start:", (r.stdout + r.stderr).strip()[-300:])
        time.sleep(6)                 # the level is often still fading in when the window appears
        for name, (hy, hp), left, right, hpitch in STEPS:
            vb_sim.head(0.0, hy, 0.0, 0, -8 if LOOK_AHEAD else hp)
            hands(left, right, hpitch)
            time.sleep(SETTLE_S)
            print("picture", name, vb_sim.screenshot(os.path.join(OUT, "vr_%s.png" % name), timeout_s=8))
        # walking: look down at the legs while the walker pushes the player
        vb_sim.head(0.0, EYE_Y, 0.0, 0, -8 if LOOK_AHEAD else -55)
        hands((-0.22, 1.10, -0.22), (0.22, 1.10, -0.22), 0)
        if wait_for(log_path, "BODYTEST walk forward", 120):
            for i in range(4):
                time.sleep(0.7)
                print("picture walk_fwd_%d" % i, vb_sim.screenshot(os.path.join(OUT, "vr_walk_fwd_%d.png" % i), timeout_s=8))
            if wait_for(log_path, "BODYTEST walk side", 10):
                for i in range(3):
                    time.sleep(0.7)
                    print("picture walk_right_%d" % i, vb_sim.screenshot(os.path.join(OUT, "vr_walk_right_%d.png" % i), timeout_s=8))
            if wait_for(log_path, "BODYTEST walk stop", 10):
                time.sleep(1.2)
                print("picture walk_stopped", vb_sim.screenshot(os.path.join(OUT, "vr_walk_stopped.png"), timeout_s=8))
        else:
            print("walker never started (no 'BODYTEST walk forward' in the log)")
    finally:
        if RECORD:
            time.sleep(2)
            r = subprocess.run(OBS_REC + ["stop"], capture_output=True, text=True)
            print("record stop:", (r.stdout + r.stderr).strip()[-400:])
            subprocess.run(OBS_REC + ["done"], capture_output=True, text=True)
        if proc.poll() is None:
            g.quit(proc, timeout=40)
        log.close()
        if not FLAT:
            print("bench stop:", subprocess.run(VRBENCH + ["stop"], capture_output=True, text=True).stdout.strip()[-200:])
        keys = ("error", "unknown", "openvr", "openxr", "body:", "bodytest", "fatal", "script")
        for line in log_lines(log_path):
            if any(k in line.lower() for k in keys):
                print("  LOG:", line.rstrip()[:240])
        print("exit", proc.returncode)


if __name__ == "__main__":
    main()
