"""The export job for the sharp sawn-off (sharp_sawed_off.py, 2026-11-04): which game frames show which pose.

    python make_job_sawed_off.py <out job.json>
then one gz_forge_export.py run per key (sawn_body, sawn_barrels, sawn_flash, sawn_bits) and pack_models.py, as for
the pump (make_job_sharp.py). anim_preview.py plays SEQUENCE in Blender.

Every frame of the game's SawedOff (Actors/Weapons/Sawedoff.txt) has a pose. Only the gun's own parts move, plus the
small kick Tefa approved on the pump (2026-11-04: "it has to kick a little. all the rest has to stay still"):
- the shot: the right barrel fires first (frames C D), then the left (A B), each with its own flash, the triggers back
- the reload: the top lever swings aside, the barrels with fore-end and ribs break open on the hinge (C D, open E to M,
  closing N D C), the two spent shells slide out (E F) and are gone (G: the game throws real casings), two new shells
  come in from behind (H to L) and sit in the chambers.
"""
import json
import math
import sys

from sharp_job import CUBE_M, bl, build_job, frames_of
from sharp_settings import SAWN_HINGE_PX, SAWN_OPEN_DEG, SAWN_S, park_z

MODEL_PATH = "models/ashes2063/sprite3d/sharpsawn"
BARRELS = ["barrels", "rib", "bead", "lug", "forend"]
FLASHES = ["flash_ra", "flash_rb", "flash_la", "flash_lb"]       # built parked 0, 1, 2, 3 steps up (sharp_kit.flashes)
BITS = ["trigger", "lever", "shell_r", "shell_l"]
SHELL_PARK = {"shell_r": 1, "shell_l": 2}                         # sharp_sawed_off: shells built parked above
MOVING = BARRELS + FLASHES + BITS
HIDDEN = FLASHES + ["shell_r", "shell_l"]
HINGE = bl(SAWN_HINGE_PX[0] * SAWN_S * CUBE_M, 0.0, -SAWN_HINGE_PX[1] * SAWN_S * CUBE_M)
TRIGGER_BACK_M = 0.003
LEVER_ASIDE_M = 3.0 * CUBE_M                                       # to the right

# how far open the barrels are (share of SAWN_OPEN_DEG), per reload letter (SAWR, SAWS, SAWH share the letters)
OPEN = {"C": 0.35, "D": 0.7, "N": 0.7, **{L: 1.0 for L in "EFGHIJKLM"}}
LEVER = set("BCDEFGHIJKLMN")
# main cubes each shell sits back out of its chamber, along the barrel; None = not shown
SHELL_OUT = {"E": 4.0, "F": 13.0, "H": 26.0, "I": 18.0, "J": 10.0, "K": 4.0, "L": 0.0, "M": 0.0}
FLASH = {"C": "flash_ra", "D": "flash_rb", "A": "flash_la", "B": "flash_lb"}
KICK = {"A": (0.014, 3.0), "C": (0.014, 3.0), "B": (0.010, 2.0), "D": (0.010, 2.0), "E": (0.006, 1.2),
        "F": (0.003, 0.6), "G": (0.001, 0.2)}

# for anim_preview.py: (sprite, letter, tics) as the game plays them: ready, both barrels fired, a full reload
SEQUENCE = ([("SAWN", "A", 20)]
            + [("SAWF", "C", 1), ("SAWF", "D", 1), ("SAWF", "E", 3), ("SAWF", "F", 2), ("SAWF", "G", 1),
               ("SAWN", "A", 15)]
            + [("SAWF", "A", 1), ("SAWF", "B", 1), ("SAWF", "E", 3), ("SAWF", "F", 2), ("SAWF", "G", 1),
               ("SAWN", "A", 10)]
            + [("SAWR", "A", 2), ("SAWR", "B", 4), ("SAWR", "C", 1), ("SAWR", "D", 1), ("SAWR", "E", 2),
               ("SAWR", "F", 2), ("SAWR", "G", 9), ("SAWR", "H", 2), ("SAWR", "I", 2), ("SAWR", "J", 2),
               ("SAWR", "K", 2), ("SAWR", "L", 5), ("SAWR", "M", 6), ("SAWR", "N", 2), ("SAWR", "D", 2),
               ("SAWR", "C", 2), ("SAWR", "A", 3), ("SAWF", "E", 2), ("SAWF", "F", 2), ("SAWF", "G", 2),
               ("SAWN", "A", 20)])


def turn(a, v):
    """v = (x, y, z) in the blend's axes turned nose up by a radians round the left-right axis."""
    return [v[0], v[1] * math.cos(a) - v[2] * math.sin(a), v[1] * math.sin(a) + v[2] * math.cos(a)]


def pose(spr, L):
    kind = spr[3]
    out = {}
    if kind == "F" and L in FLASH:
        name = FLASH[L]
        out[name] = bl(0.0, 0.0, -park_z(FLASHES.index(name)) * CUBE_M)
        out["trigger"] = bl(-TRIGGER_BACK_M, 0.0, 0.0)
    if kind in "RSH":
        share = OPEN.get(L, 0.0)
        deg = -SAWN_OPEN_DEG * share
        if share:
            for p in BARRELS:
                out[p] = [0.0, 0.0, 0.0, deg] + HINGE
        if L in LEVER:
            out["lever"] = bl(0.0, -LEVER_ASIDE_M, 0.0)
        if L in SHELL_OUT:
            a = math.radians(deg)
            for p, k in SHELL_PARK.items():
                # built parked park_z above its chamber: down by that, back along the barrel, all turned with it
                v = [0.0, -SHELL_OUT[L] * CUBE_M, -park_z(k) * CUBE_M]
                out[p] = turn(a, v) + [deg] + HINGE
    return out


def kick(spr, L):
    return KICK.get(L, (0.0, 0.0)) if spr[3] == "F" else (0.0, 0.0)


def main(out):
    models = {"sawn_body": [], "sawn_barrels": BARRELS, "sawn_flash": FLASHES, "sawn_bits": BITS}
    names = {k: "as_sharp_" + k for k in models}
    job = build_job(frames_of("Sawedoff.txt", ["SawedOff"]), models, HIDDEN, MOVING, pose, kick, MODEL_PATH, names,
                    1.0)
    json.dump(job, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
