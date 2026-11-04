"""The export job for the sharp revolver (sharp_revolver.py, 2026-11-04): which game frames show which pose.
    python make_job_revolver.py <out job.json>
then export_pack.py; anim_preview.py plays SEQUENCE in Blender.

Every frame of the game's revolver (Actors/Weapons/Revolver.txt) has a pose; the lantern versions of the frames
(REVL) show the gun at rest except their own shot. Only the gun's own parts move, plus the small kick:
- the shot: a big then a small flash, the trigger back (REVF A B, with the lantern REVL M N)
- the reload: the cylinder swings out to the left (REVR C D, out E to P, back in Q R S), the six rounds are pushed
  out (H I, gone J: the game throws its own casings) and six new ones go in (L to O).
"""
import json
import math
import sys

from sharp_job import CUBE_M, bl, build_job, frames_of
from sharp_settings import REV_CRANE, REV_CYL_PX, REV_S, REV_SWING_DEG, park_z

MODEL_PATH = "models/ashes2063/sprite3d/sharprev"
FLASHES = ["flash_a", "flash_b"]
BITS = ["trigger", "rounds"]
MOVING = ["cylinder"] + FLASHES + BITS
HIDDEN = FLASHES + ["rounds"]
CZ = -REV_CYL_PX[2] * REV_S
# the crane: left of (forge +y) and below the cylinder's axis; the blend's x is the forge's -y
CRANE = bl(0.0, REV_CRANE[0] * CUBE_M, (CZ + REV_CRANE[1]) * CUBE_M)
OUT = {"C": 0.33, "D": 0.66, "Q": 0.6, "R": 0.25, **{L: 1.0 for L in "EFGHIJKLMNOP"}}
ROUNDS_BACK = {"G": 0.0, "H": 4.0, "I": 9.0, "L": 14.0, "M": 8.0, "N": 3.0, "O": 0.0, "P": 0.0, "Q": 0.0,
               "R": 0.0}                                   # main cubes back out of the chambers; else not shown
FLASH = {("F", "A"): "flash_a", ("F", "B"): "flash_b", ("L", "M"): "flash_a", ("L", "N"): "flash_b"}
KICK = {"A": (0.010, 3.0), "M": (0.010, 3.0), "B": (0.007, 2.0), "N": (0.007, 2.0), "D": (0.004, 1.0),
        "O": (0.004, 1.0), "E": (0.002, 0.4), "P": (0.002, 0.4)}
TRIGGER_BACK_M = 0.002

SEQUENCE = ([("REVG", "A", 20)]
            + [("REVF", "A", 2), ("REVF", "B", 1), ("REVF", "D", 1), ("REVF", "E", 2), ("REVF", "F", 2),
               ("REVF", "G", 2), ("REVF", "H", 1), ("REVG", "A", 20)]
            + [("REVR", "A", 3), ("REVR", "B", 3)] + [("REVR", "C", 2)] * 3
            + [("REVR", L, 2) for L in "DEFGGHIJLLLLMNOP"] + [("REVR", "P", 2)] * 3
            + [("REVR", L, 2) for L in "QRS"] + [("REVR", L, 1) for L in "TUVWX"] + [("REVG", "A", 20)])


def pose(spr, L):
    kind, out = spr[3], {}
    if (kind, L) in FLASH:
        name = FLASH[(kind, L)]
        out[name] = bl(0.0, 0.0, -park_z(FLASHES.index(name)) * CUBE_M)
        out["trigger"] = bl(-TRIGGER_BACK_M, 0.0, 0.0)
    if kind == "R" and L in OUT:
        deg = REV_SWING_DEG * OUT[L]
        out["cylinder"] = [0.0, 0.0, 0.0, deg] + CRANE + [1]
        if L in ROUNDS_BACK:
            # built parked one step above the cylinder: down by that and back out of the chambers, then the swing
            a = math.radians(deg)
            v = bl(-ROUNDS_BACK[L] * CUBE_M, 0.0, -park_z(1) * CUBE_M)
            v = [v[0] * math.cos(a) + v[2] * math.sin(a), v[1], -v[0] * math.sin(a) + v[2] * math.cos(a)]
            out["rounds"] = v + [deg] + CRANE + [1]
    return out


def kick(spr, L):
    return KICK.get(L, (0.0, 0.0)) if (spr[3], L) in FLASH or (spr == "REVF" and L in KICK) or \
        (spr == "REVL" and L in "MNOP") else (0.0, 0.0)


def main(out):
    models = {"rev_body": [], "rev_cylinder": ["cylinder"], "rev_flash": FLASHES, "rev_bits": BITS}
    names = {k: "as_sharp_" + k for k in models}
    job = build_job(frames_of("Revolver.txt", ["revolver"]), models, HIDDEN, MOVING, pose, kick, MODEL_PATH, names,
                    1.0)
    json.dump(job, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
