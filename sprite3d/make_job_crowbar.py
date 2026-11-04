"""The export job for the sharp crowbar (sharp_crowbar.py, 2026-11-04): one still model for every frame.
    python make_job_crowbar.py <out job.json>
then export_pack.py. Its swings move the whole crowbar, which in VR is the player's own hand, so every frame of the
game's Crowbar (Actors/Weapons/Crowbar.txt) shows it at rest.
"""
import json
import sys

from sharp_job import build_job, frames_of

MODEL_PATH = "models/ashes2063/sprite3d/sharpcrowbar"


def main(out):
    job = build_job(frames_of("Crowbar.txt", ["Crowbar"]), {"crow_body": []}, [], [], lambda s, L: {},
                    lambda s, L: (0.0, 0.0), MODEL_PATH, {"crow_body": "as_sharp_crow_body"}, 1.0)
    json.dump(job, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
