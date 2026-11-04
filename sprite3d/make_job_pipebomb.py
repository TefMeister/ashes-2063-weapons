"""The export job for the sharp pipe bomb (sharp_pipebomb.py, 2026-11-04): which game frames show which pose.
    python make_job_pipebomb.py <out job.json>
then export_pack.py.

Every frame of the game's pipebomb (Actors/Weapons/pipebomb.txt) has a pose. The fuse sparks once it is lit (PIPE E
to P); the bomb is gone from the hand while it is thrown and the hand comes back empty (Q to W, and the placed one,
PIP2 H to K); a new one is in the hand again for the raise (X Y Z).
"""
import json
import sys

from sharp_job import CUBE_M, bl, build_job, frames_of
from sharp_settings import park_z

MODEL_PATH = "models/ashes2063/sprite3d/sharppipe"
BOMB = ["grip", "caps", "tape", "box", "wire", "fuse"]
SPARKS = ["spark_a", "spark_b"]
GONE = {("PIPE", L) for L in "QRSTUVW"} | {("PIP2", L) for L in "HIJK"}
SPARK = {L: SPARKS[i % 2] for i, L in enumerate("EFGHIJKLMNOP")}


def pose(spr, L):
    out = {} if (spr, L) in GONE else {p: [0.0, 0.0, 0.0] for p in BOMB}
    if spr == "PIPE" and L in SPARK:
        name = SPARK[L]
        out[name] = bl(0.0, 0.0, -park_z(SPARKS.index(name)) * CUBE_M)
    return out


def main(out):
    models = {"pipe_bomb": BOMB, "pipe_sparks": SPARKS}
    names = {k: "as_sharp_" + k for k in models}
    job = build_job(frames_of("pipebomb.txt", ["pipebomb"]), models, BOMB + SPARKS, BOMB + SPARKS, pose,
                    lambda s, L: (0.0, 0.0), MODEL_PATH, names, 1.0)
    json.dump(job, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
