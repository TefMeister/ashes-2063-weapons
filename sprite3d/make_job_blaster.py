"""The export job for the sharp Master Blaster (sharp_blaster.py, 2026-11-04): which game frames show which pose.
    python make_job_blaster.py <out job.json>
then export_pack.py; anim_preview.py plays SEQUENCE in Blender.

Every frame of the game's NapalmGun (Actors/Weapons/MBlaster.txt) has a pose. Only the gun's own parts move, plus a
very small push:
- firing (NPLM B to L, the alt fire U V): the flame at the nozzle cycles through its three shapes, the trigger back
- the reload (NPLM M to T, then back S to M): the red valve wheel turns and the gauge's needle climbs, then both
  return as the game plays the frames backwards.
"""
import json
import sys

from sharp_job import CUBE_M, bl, build_job, frames_of
from sharp_settings import BLS_GAUGE_PX, BLS_S, BLS_TANK_Y, BLS_VALVE_PX, park_z

MODEL_PATH = "models/ashes2063/sprite3d/sharpblaster"
FLASHES = ["flash_a", "flash_b", "flash_c"]
BITS = ["trigger", "valve", "needle"]
MOVING = FLASHES + BITS
HIDDEN = FLASHES
FLAME = {L: FLASHES[i % 3] for i, L in enumerate("BCDEFGHIJKL")}
FLAME.update({"U": "flash_a", "V": "flash_b"})
TURN = {"M": 0.15, "N": 0.3, "O": 0.45, "P": 0.6, "Q": 0.75, "R": 0.9, "S": 1.0, "T": 1.0}
VALVE = bl(BLS_VALVE_PX[0] * BLS_S * CUBE_M, BLS_TANK_Y * CUBE_M, -BLS_VALVE_PX[1] * BLS_S * CUBE_M)
GAUGE = bl(BLS_GAUGE_PX[0] * BLS_S * CUBE_M, 0.0, -BLS_GAUGE_PX[1] * BLS_S * CUBE_M)
TRIGGER_BACK_M = 0.002

SEQUENCE = ([("NPLM", "A", 20)] + [("NPLM", L, 2) for L in "BCDEFGHIJKL" * 2] + [("NPLM", "A", 15)]
            + [("NPLM", L, 3) for L in "MNOPQRSST"] + [("NPLM", "T", 4)] * 8 + [("NPLM", L, 3) for L in "SRQPONM"]
            + [("NPLM", "A", 20)])


def pose(spr, L):
    out = {}
    if L in FLAME:
        name = FLAME[L]
        out[name] = bl(0.0, 0.0, -park_z(FLASHES.index(name)) * CUBE_M)
        out["trigger"] = bl(-TRIGGER_BACK_M, 0.0, 0.0)
    if L in TURN:
        out["valve"] = [0.0, 0.0, 0.0, 270.0 * TURN[L]] + VALVE + [2]
        out["needle"] = [0.0, 0.0, 0.0, -150.0 * TURN[L]] + GAUGE + [1]
    return out


def kick(spr, L):
    return (0.002, 0.3) if L in FLAME else (0.0, 0.0)


def main(out):
    models = {"bls_body": [], "bls_flash": FLASHES, "bls_bits": BITS}
    names = {k: "as_sharp_" + k for k in models}
    job = build_job(frames_of("MBlaster.txt", ["NapalmGun"]), models, HIDDEN, MOVING, pose, kick, MODEL_PATH, names,
                    1.0)
    json.dump(job, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
