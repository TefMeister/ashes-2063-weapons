"""The export job for the Meshy Glock (meshy_glock.py, 2026-11-15): the sharp 9mm's job (make_job_handgun.py), its
poses unchanged (the shot, the slide locked back when empty, the magazine out and in down the grip, the rack), drawn
from this gun's parts under its own model names.
    python make_job_meshy_glock.py <out job.json>
    python export_pack.py meshy_glock.blend <job.json> <out folder> <out.pk3>
"""
import json
import sys

from make_job_handgun import BITS, FLASHES, HIDDEN, MOVING, kick, pose
from sharp_job import build_job, frames_of

MODEL_PATH = "models/ashes2063/sprite3d/meshyglock"


def main(out):
    models = {"mglk_body": [], "mglk_slide": ["slide"], "mglk_flash": FLASHES, "mglk_bits": BITS}
    names = {k: "as_meshy_" + k for k in models}
    job = build_job(frames_of("Glock.txt", ["Glock"], own=["GLOK"]), models, HIDDEN, MOVING, pose, kick, MODEL_PATH,
                    names, 1.0)
    json.dump(job, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
