"""The export job for the sharp FAL (sharp_fal.py, 2026-11-04): which game frames show which pose.
    python make_job_fal.py <out job.json>
then export_pack.py; anim_preview.py plays SEQUENCE in Blender.

Every frame of the game's FAL (Actors/Weapons/FAL.txt) has a pose; the zoomed frames (FNFZ) show it at rest. Only
the gun's own parts move, plus the small kick:
- the shot: a flash (FFAF A or B), a dying flash (C), the trigger back
- the reload: the magazine drops out (empty: FFAR E K L, full: E F G), is gone (M / H), a new one comes up (N O / I J)
  and is pushed home (P Q); then the charging handle is pulled back and let go (T U V W X).
"""
import json
import sys

from sharp_job import CUBE_M, bl, build_job, frames_of
from sharp_settings import FAL_HANDLE_STROKE, park_z

MODEL_PATH = "models/ashes2063/sprite3d/sharpfal"
FLASHES = ["flash_a", "flash_b", "flash_c"]
BITS = ["trigger", "mag", "bolt"]
MOVING = FLASHES + BITS
HIDDEN = FLASHES + ["mag"]
FLASH = {"A": "flash_a", "B": "flash_b", "C": "flash_c"}
MAG_OUT = {"E": 3.0, "K": 12.0, "L": 34.0, "M": None, "N": 34.0, "O": 12.0, "F": 12.0, "G": 34.0, "H": None,
           "I": 34.0, "J": 12.0, "P": 3.0}
HANDLE = {"T": 0.3, "U": 0.8, "V": 1.0, "W": 0.5}
KICK = {"A": (0.012, 2.5), "B": (0.012, 2.5), "C": (0.006, 1.2), "D": (0.003, 0.5)}
TRIGGER_BACK_M = 0.002

SEQUENCE = ([("FFAL", "A", 20), ("FFAF", "A", 2), ("FFAF", "C", 2), ("FFAF", "D", 1), ("FFAF", "E", 1),
             ("FFAF", "F", 1), ("FFAL", "A", 10), ("FFAF", "B", 2), ("FFAF", "C", 2), ("FFAF", "D", 1),
             ("FFAF", "E", 1), ("FFAF", "F", 1), ("FFAL", "A", 15)]
            + [("FFAR", L, 2) for L in "ABCDEEKLMNOPPPPQRS"] + [("FFAR", L, 3) for L in "TUVV"]
            + [("FFAR", L, 2) for L in "WXYZCBA"] + [("FFAL", "A", 20)])


def pose(spr, L):
    out = {}
    if spr == "FFAF" and L in FLASH:
        name = FLASH[L]
        out[name] = bl(0.0, 0.0, -park_z(FLASHES.index(name)) * CUBE_M)
        out["trigger"] = bl(-TRIGGER_BACK_M, 0.0, 0.0)
    d = MAG_OUT.get(L, 0.0) if spr == "FFAR" else 0.0
    if d is not None:
        out["mag"] = bl(0.0, 0.0, -d * CUBE_M)
    if spr == "FFAR" and L in HANDLE:
        out["bolt"] = bl(-HANDLE[L] * FAL_HANDLE_STROKE * CUBE_M, 0.0, 0.0)
    return out


def kick(spr, L):
    return KICK.get(L, (0.0, 0.0)) if spr == "FFAF" else (0.0, 0.0)


def main(out):
    models = {"fal_body": [], "fal_flash": FLASHES, "fal_bits": BITS}
    names = {k: "as_sharp_" + k for k in models}
    job = build_job(frames_of("FAL.txt", ["FAL"]), models, HIDDEN, MOVING, pose, kick, MODEL_PATH, names, 1.0)
    json.dump(job, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
