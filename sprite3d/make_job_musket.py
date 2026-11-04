"""The export job for the sharp Junker Musket (sharp_musket.py, 2026-11-04): which game frames show which pose.
    python make_job_musket.py <out job.json>
then export_pack.py; anim_preview.py plays SEQUENCE in Blender.

Every frame of the game's JunkerMusket (Actors/Weapons/Musket.txt) has a pose; the zoomed frames (MSKT V) show it at
rest. Only the gun's own parts move, plus the small kick:
- the shot: three flashes (MSKF A B C), the trigger back, then the bolt is worked (H I J)
- the reload (MSKT): the handle lifts (C D E) and the bolt runs back (F to I), a round drops in through the open
  action (K to O) and is pushed forward (P to S); the bolt closes the same way back (J I H G F) and the handle is
  turned down (Y X W).
"""
import json
import sys

from sharp_job import CUBE_M, bl, build_job, frames_of
from sharp_settings import MSK_BOLT_LIFT_DEG, MSK_BOLT_ROW, MSK_BOLT_STROKE, MSK_S, park_z

MODEL_PATH = "models/ashes2063/sprite3d/sharpmusket"
FLASHES = ["flash_a", "flash_b", "flash_c"]
BITS = ["trigger", "bolt", "round"]
MOVING = FLASHES + BITS
HIDDEN = FLASHES + ["round"]
AXIS = bl(0.0, 0.0, -MSK_BOLT_ROW * MSK_S * CUBE_M)       # a point on the bolt's axis (it turns round blend y)
FLASH = {"A": "flash_a", "B": "flash_b", "C": "flash_c"}
# (handle lift share, bolt back share) per reload letter; the shot's bolt cycle (MSKF) has its own
RELOAD_BOLT = {"C": (0.3, 0.0), "D": (0.7, 0.0), "E": (1.0, 0.0), "F": (1.0, 0.3), "G": (1.0, 0.6), "H": (1.0, 0.9),
               **{L: (1.0, 1.0) for L in "IJKLMNOPQRS"}, "Y": (0.7, 0.0), "X": (0.3, 0.0)}
SHOT_BOLT = {"H": (1.0, 1.0), "I": (1.0, 0.5), "J": (0.5, 0.0)}
# the round: (main cubes above the port, main cubes back) per reload letter
ROUND = {"K": (14.0, 0.0), "L": (8.0, 0.0), "M": (4.0, 0.0), "N": (1.5, 0.0), "O": (0.0, 0.0), "P": (0.0, -3.0),
         "Q": (0.0, -6.0), "R": (0.0, -9.0), "S": (0.0, -10.0)}
KICK = {"A": (0.014, 3.0), "B": (0.010, 2.0), "C": (0.006, 1.0), "D": (0.003, 0.5)}
TRIGGER_BACK_M = 0.002

SEQUENCE = ([("MSKT", "B", 20), ("MSKF", "A", 1), ("MSKF", "B", 1), ("MSKF", "C", 1), ("MSKF", "D", 1)]
            + [("MSKF", L, 1) for L in "EFG"] + [("MSKF", "H", 3), ("MSKF", "I", 2), ("MSKF", "J", 2),
                                                 ("MSKT", "B", 15)]
            + [("MSKT", L, 2) for L in "CDEFGHIJKKLMMNO"] + [("MSKT", "O", 3)] + [("MSKT", L, 3) for L in "PQRSS"]
            + [("MSKT", L, 2) for L in "JIHGFYXW"] + [("MSKT", "B", 20)])


def bolt(lift, back):
    return bl(-back * MSK_BOLT_STROKE * CUBE_M, 0.0, 0.0) + [MSK_BOLT_LIFT_DEG * lift] + AXIS + [1]


def pose(spr, L):
    out = {}
    if spr == "MSKF" and L in FLASH:
        name = FLASH[L]
        out[name] = bl(0.0, 0.0, -park_z(FLASHES.index(name)) * CUBE_M)
        out["trigger"] = bl(-TRIGGER_BACK_M, 0.0, 0.0)
    if spr == "MSKF" and L in SHOT_BOLT:
        out["bolt"] = bolt(*SHOT_BOLT[L])
    if spr == "MSKT" and L in RELOAD_BOLT:
        out["bolt"] = bolt(*RELOAD_BOLT[L])
    if spr == "MSKT" and L in ROUND:
        up, fwd = ROUND[L]
        out["round"] = bl(-fwd * CUBE_M if fwd else 0.0, 0.0, (up - park_z(1)) * CUBE_M)
    return out


def kick(spr, L):
    return KICK.get(L, (0.0, 0.0)) if spr == "MSKF" else (0.0, 0.0)


def main(out):
    models = {"msk_body": [], "msk_flash": FLASHES, "msk_bits": BITS}
    names = {k: "as_sharp_" + k for k in models}
    job = build_job(frames_of("Musket.txt", ["JunkerMusket"]), models, HIDDEN, MOVING, pose, kick, MODEL_PATH, names,
                    1.0)
    json.dump(job, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
