"""The export job for the smudge-cube shotgun, round 12 (smudge_cube_pump_v12.py, 2026-11-12).

Rounds 8 to 11 took the sharp shotgun's poses unchanged (make_job_smudge.py). Round 12 has shells twice the size and a
port one big shell long, so it has its own: the pump keeps the sharp stroke (its handle length and travel as they
were), the shell guard (bolt) slides the whole longer port open on the same share, the port shell goes in to the gun's
middle line (the chamber), and the loading shells rise further, being bigger. Names and folder as round 8.

    python make_job_smudge_v12.py <out job.json>
    blender -b smudge_cube_pump_v12.blend --python brutal-doom-3d-guns/tools/gz_forge_export.py -- <job.json> <key> <out>
for key = smudge_body, smudge_pump, smudge_flash, smudge_bits, then
    python pack_models.py <job.json> <out.pk3> smudge_body=<out> ... --scale 0.7 0.7 0.7 --grip 30 0 -5
"""
import json
import sys

from make_job import CLASSES, PUMP_BACK, SPRITE_GUN_SCALE
from make_job_sharp import FLASH, HIDDEN, MOVING, PUMP_RELOAD, TRIGGER_BACK_M, kick
from sharp_job import bl, build_job, frames_of
from sharp_settings import CUBE_M, PUMP_STROKE_M, park_z
from smudge_settings import BOLT_STROKE_M, SHELL2_IN_M

MODEL_PATH = "models/ashes2063/sprite3d/smudgepump"
# the port shell: beside the open port and a little up (J), level with it (K), then in to the chamber (L, M)
SHELL2 = {"J": (0.0, -0.02, 0.02), "K": (0.0, 0.0, 0.0), "L": (0.0, SHELL2_IN_M * 0.55, 0.0),
          "M": (0.0, SHELL2_IN_M, 0.0)}
# every other shell rises into the loading port under the receiver and is pushed forward (Reloadloop P-V)
SHELL = {"P": (0.0, 0.0, -0.09), "Q": (0.0, 0.0, -0.06), "R": (0.0, 0.0, -0.035), "S": (0.0, 0.0, -0.012),
         "T": (0.0, 0.0, 0.012), "U": (0.006, 0.0, 0.03), "V": (0.03, 0.0, 0.046)}


def state(spr, L):
    """What the moving parts do in one game frame: (pump share, {bit part: forge offset in metres})."""
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
    """{part: blend offset}: the pump back by its share of the pump stroke, the shell guard by its share of the port."""
    share, bits = state(spr, L)
    offs = {p: bl(*o) for p, o in bits.items()}
    if share:
        offs["pump"] = bl(-share * PUMP_STROKE_M, 0.0, 0.0)
        offs["bolt"] = bl(-share * BOLT_STROKE_M, 0.0, 0.0)
    return offs


def main(out):
    models = {"smudge_body": [], "smudge_pump": ["pump", "bolt"],
              "smudge_flash": ["flash_a", "flash_b", "flash_c"], "smudge_bits": ["trigger", "shell", "shell2"]}
    names = {k: "as_smudge_pump_" + k.split("_")[1] for k in models}
    job = build_job(frames_of("Shotgun.txt", CLASSES), models, HIDDEN, MOVING, pose, kick, MODEL_PATH, names,
                    SPRITE_GUN_SCALE)
    json.dump(job, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
