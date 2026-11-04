"""The export job for the sharp JackHammer (sharp_jackhammer.py, 2026-11-04): which game frames show which pose.
    python make_job_jackhammer.py <out job.json>
then export_pack.py; anim_preview.py plays SEQUENCE in Blender.

Every frame of the game's JACKHAMMER (Actors/Weapons/Hammer.txt) has a pose. Only its own parts move, plus a small
judder: the chisel hammers out and back through the firing frames (HAMM E to N), the throttle lever is squeezed while
it runs, and the idling motor makes the whole thing judder a little (HAMM B C D).
"""
import json
import sys

from sharp_job import CUBE_M, bl, build_job, frames_of
from sharp_settings import JCK_CHISEL_STROKE

MODEL_PATH = "models/ashes2063/sprite3d/sharpjack"
BITS = ["chisel", "trigger"]
MOVING = BITS
OUT = {"E": 1.0, "F": 0.4, "G": 1.0, "H": 0.4, "I": 1.0, "J": 0.6, "K": 0.3, "L": 0.8, "M": 1.0, "N": 0.5}
KICK = {"E": (0.004, 0.6), "G": (0.004, 0.6), "I": (0.004, 0.6), "M": (0.004, 0.6), "B": (0.001, 0.15),
        "D": (0.001, -0.15)}
THROTTLE_M = 0.003

SEQUENCE = ([("HAMM", L, 2) for L in "ABCDCB" * 3] + [("HAMM", "E", 1), ("HAMM", "F", 1)]
            + [("HAMM", L, 1) for L in "GHE"] * 3 + [("HAMM", L, 2) for L in "HIHEABCDCB"]
            + [("HAMM", L, 1) for L in "EIHEI"] + [("HAMM", "H", 1), ("HAMM", "F", 2)]
            + [("HAMM", L, 1) for L in "HIJKLMMNNLLKKJJA"] + [("HAMM", L, 2) for L in "ABCDCB" * 2])


def pose(spr, L):
    out = {}
    if L in OUT:
        out["chisel"] = bl(OUT[L] * JCK_CHISEL_STROKE * CUBE_M, 0.0, 0.0)
        out["trigger"] = bl(-THROTTLE_M, 0.0, 0.0)
    return out


def kick(spr, L):
    return KICK.get(L, (0.0, 0.0))


def main(out):
    models = {"jck_body": [], "jck_bits": BITS}
    names = {k: "as_sharp_" + k for k in models}
    job = build_job(frames_of("Hammer.txt", ["JACKHAMMER"]), models, [], MOVING, pose, kick, MODEL_PATH, names, 1.0)
    json.dump(job, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
