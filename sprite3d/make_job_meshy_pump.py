"""The export job for the Meshy shotgun (meshy_cube_pump.py, 2026-11-15): round 12's job (make_job_smudge_v12.py)
with this gun's own numbers. The pump keeps the kit's stroke; the shell guard ("bolt") slides the whole port open
(38 cubes) on the same share, so pulling the pump opens it (Tefa: "it needs to open when the pump handle is pulled
down"); the port shell goes in from beside the port to the gun's middle line; the loading shells rise into the
receiver from under it, as on round 12.

    python make_job_meshy_pump.py <out job.json>
    python export_pack.py meshy_cube_pump.blend <job.json> <out folder> <out.pk3>
    (pack with --scale 0.7 0.7 0.7 --grip 30 0 -5 as round 12: pack_models.py)
"""
import json
import sys

from make_job import CLASSES, PUMP_BACK, SPRITE_GUN_SCALE
from make_job_sharp import FLASH, HIDDEN, MOVING, PUMP_RELOAD, TRIGGER_BACK_M, kick
from make_job_smudge_v12 import SHELL
from sharp_job import bl, build_job, frames_of
from sharp_settings import CUBE_M, PUMP_STROKE_M, park_z

PORT_LEN = 166 - 128                       # meshy_cube_pump.PORT
BOLT_STROKE_M = PORT_LEN * CUBE_M
SHELL2_IN_M = (12.0 + 8.0) * CUBE_M         # meshy_cube_pump.SHELL2_IN
MODEL_PATH = "models/ashes2063/sprite3d/meshypump"
SHELL2 = {"J": (0.0, -0.02, 0.02), "K": (0.0, 0.0, 0.0), "L": (0.0, SHELL2_IN_M * 0.55, 0.0),
          "M": (0.0, SHELL2_IN_M, 0.0)}


def state(spr, L):
    kind = spr[3]
    if kind == "F" and L in FLASH:
        k = "ABC".index(L)
        return 0.0, {FLASH[L]: (0.0, 0.0, -park_z(k) * CUBE_M), "trigger": (-TRIGGER_BACK_M, 0.0, 0.0)}
    if kind == "P":
        return PUMP_BACK.get(L, 0.0), {}
    if kind == "R":
        if L in SHELL2:
            return PUMP_RELOAD[L], {"shell2": SHELL2[L]}
        if L in SHELL:
            return 0.0, {"shell": SHELL[L]}
        return PUMP_RELOAD.get(L, 0.0), {}
    return 0.0, {}


def pose(spr, L):
    share, bits = state(spr, L)
    offs = {p: bl(*o) for p, o in bits.items()}
    if share:
        offs["pump"] = bl(-share * PUMP_STROKE_M, 0.0, 0.0)
        offs["bolt"] = bl(-share * BOLT_STROKE_M, 0.0, 0.0)
    return offs


def main(out):
    models = {"meshy_body": [], "meshy_pump": ["pump", "bolt"],
              "meshy_flash": ["flash_a", "flash_b", "flash_c"], "meshy_bits": ["trigger", "shell", "shell2"]}
    names = {k: "as_meshy_pump_" + k.split("_")[1] for k in models}
    job = build_job(frames_of("Shotgun.txt", CLASSES), models, HIDDEN, MOVING, pose, kick, MODEL_PATH, names,
                    SPRITE_GUN_SCALE)
    json.dump(job, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
