"""Flat load check of the 2026-11-27 Meshy set, one episode per run (Build PC):
    python tools/m2_flatcheck.py ep1|afterglow|hardreset
Starts the episode exactly as its "meshy set" launcher does, but flat and windowed, selects every first-version weapon
in turn, takes a picture of each in the hand, quits through the console (so the log is written) and lists every line
of the log that looks like a load problem. It proves the packs load and the models show; it cannot judge VR placement
or the moving parts in the hand (that is the headset's job)."""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "sprite3d")]
import gzdrive as g  # noqa: E402
import m2_launchers as L  # noqa: E402
from draw_test_helpers import game_window  # noqa: E402

BAD = ("error", "unknown", "not found", "invalid", "couldn't", "could not", "missing", "warning", "bad ")


def main(ep):
    e = dict(L.EPISODES[ep])
    if os.environ.get("M2_ONLY"):               # check a few weapons on their own: M2_ONLY="Thumper Xbow"
        e["give"] = os.environ["M2_ONLY"]
    out = os.path.join(L.OUT, "flatcheck", ep)
    os.makedirs(out, exist_ok=True)
    packs = L.HELPERS + [L.LANTERN] + sorted(
        os.path.join(L.OUT, "pk3", ep, f) for f in os.listdir(os.path.join(L.OUT, "pk3", ep)))
    files = [r"Resources\AshesSAMenu.pk3", r"Resources\lightmodepatch.pk3"] + [f.lstrip(".\\") for f in e["files"]] + packs
    args = ["-iwad", r"Resources\freedoom-0.12.1\freedoom2.wad", "-file", *files,
            "-config", r"gzdoomvr-tefa\ashes-flat-test.ini", "+vr_mode", "0", "+vid_fullscreen", "0",
            "+win_w", "1280", "+win_h", "720", "+set", "language", "enu", "+set", "snd_musicvolume", "0",
            "-skill", "3", "+map", "MAP01"]
    for w in e["give"].split():
        args += ["+give", w]
    for a in e["ammo"].split():
        args += ["+give", a, "999"]
    log_path = os.path.join(out, "console.log")
    log = open(log_path, "w")
    proc = subprocess.Popen([os.path.join(g.GAME, "gzdoomvr-tefa", "gzdoomvr.exe"), *args], cwd=g.GAME,
                            stdout=log, stderr=subprocess.STDOUT)
    h = game_window(proc.pid)
    if not h:
        proc.kill()
        raise SystemExit("no game window")
    time.sleep(8)
    g.fg(h)
    for w in e["give"].split():
        if w in ("LanternFound", "Lantern"):
            continue
        g.console("use " + w)
        time.sleep(2.2)
        g.shot(h, os.path.join(out, w + ".png"))
    g.quit(proc)
    try:
        proc.wait(timeout=60)
    except subprocess.TimeoutExpired:
        proc.kill()
    log.close()
    text = open(log_path, encoding="utf-8", errors="replace").read().splitlines()
    hits = [ln for ln in text if any(b in ln.lower() for b in BAD)]
    print(ep, ":", len(text), "log lines,", len(hits), "look like problems")
    for ln in hits[:60]:
        print("  ", ln)
    print("pictures:", out)


if __name__ == "__main__":
    main(sys.argv[1])
