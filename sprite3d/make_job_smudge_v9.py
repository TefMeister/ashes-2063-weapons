"""The export job for the smudge-cube shotgun, round 10 (smudge_cube_pump_v10.py, 2026-11-12; round 9 the same way): round 8 with a bulkier
body and the rail; the same poses and names as round 8 (make_job_smudge.py), packed with
    python pack_models.py ... --scale 0.7 0.784 0.784
(length 0.7, width and height 0.7 x the design's GIRTH; round 9: 0.735).

Tefa, 2026-11-07: "can you please put the shotgun in the game ashes, i really wanna see it in action". Round 8 has the
same moving parts, the same port and stroke (sharp_settings) and the same flashes and shells as the sharp cube shotgun,
so every game frame takes the sharp shotgun's pose (make_job_sharp.pose / kick); only the names and the folder are new,
so nothing of the sharp shotgun is overwritten. The skins are new names too, so the fire-lights pk3's shine material
(gldefs.shine, by texture name) never reaches this gun: it stays matte, as the look asks.

    python make_job_smudge_v9.py <out job.json>
    blender -b smudge_cube_pump_v10.blend --python brutal-doom-3d-guns/tools/gz_forge_export.py -- <job.json> <key> <out>
for key = smudge_body, smudge_pump, smudge_flash, smudge_bits, then
    python pack_models.py <job.json> <out.pk3> smudge_body=<out> smudge_pump=<out> smudge_flash=<out> smudge_bits=<out>
"""
import json
import sys

from make_job import CLASSES, SPRITE_GUN_SCALE
from make_job_sharp import HIDDEN, MOVING, kick, pose
from sharp_job import build_job, frames_of

MODEL_PATH = "models/ashes2063/sprite3d/smudgepump"


def main(out):
    models = {"smudge_body": [], "smudge_pump": ["pump", "bolt"],
              "smudge_flash": ["flash_a", "flash_b", "flash_c"], "smudge_bits": ["trigger", "shell", "shell2"]}
    names = {k: "as_smudge_pump_" + k.split("_")[1] for k in models}
    job = build_job(frames_of("Shotgun.txt", CLASSES), models, HIDDEN, MOVING, pose, kick, MODEL_PATH, names,
                    SPRITE_GUN_SCALE)
    json.dump(job, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
