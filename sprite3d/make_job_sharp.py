"""The export job for the sharp cube shotgun (sharp_cube_pump.py, 2026-11-04): which game frames show which pose.

    python make_job_sharp.py <out job.json>
then, from the built blend, one export per model:
    blender -b sharp_cube_pump.blend --python brutal-doom-3d-guns/tools/gz_forge_export.py -- <job.json> <key> <out>
for key = sharp_body, sharp_pump, sharp_flash, sharp_bits, and pack them with
    python pack_models.py <job.json> <out.pk3> sharp_body=<out> sharp_pump=<out> sharp_flash=<out> sharp_bits=<out>

Four models drawn together, so nothing heavy is stored once per frame: the still body (one frame), the pump (one
frame per pump position), the three muzzle flashes (four frames) and the small bits (trigger, two shells).

Tefa, 2026-11-04: "please animate it with all the game's animations". Every frame the two shotgun classes show
(Actors/Weapons/Shotgun.txt) has a pose here. Only the gun's own parts move: in VR the player's hand holds the gun, so
the flat game's whole-gun motion (the kick, tipping the gun over to load it, the bash and knife swings) stays out, as
on the cube sprite shotgun.
"""
import json
import sys

from make_job import CLASSES, PUMP_BACK, SPRITE_GUN_SCALE
from sharp_job import bl, build_job, frames_of
from sharp_settings import CUBE_M, KICK, PUMP_STROKE_M, park_z

MODEL_PATH = "models/ashes2063/sprite3d/sharppump"
MOVING = ["pump", "bolt", "trigger", "flash_a", "flash_b", "flash_c", "shell", "shell2"]
# the small moving parts, in two models so the heavy flash (smallest cubes) is stored only for its own four frames
GROUPS = {"sharp_flash": ["flash_a", "flash_b", "flash_c"], "sharp_bits": ["trigger", "shell", "shell2"]}
HIDDEN = ["flash_a", "flash_b", "flash_c", "shell", "shell2"]
TRIGGER_BACK_M = 0.003
# A dry reload in the order Tefa asked for on the first cube shotgun (2026-09-24): "pulls the pump handle down, then
# inserts the first round, then pushes the pump handle back up and then loads in the next 5 shells". The pump is back
# (the port open) for GRIR J K L M while the shell comes to the port and goes in, then closes over N O.
# The shell is built beside the port (sharp_cube_pump.SHELL2_OUT = 6 main cubes out, 20.4 mm); offsets from there.
SHELL2_IN = 8.0 * 0.0034                    # in 8 main cubes: its axis 2 cubes inside the right side, in the open port
SHELL2 = {"J": (0.0, -0.014, 0.014), "K": (0.0, 0.0, 0.0), "L": (0.0, SHELL2_IN * 0.6, 0.0),
          "M": (0.0, SHELL2_IN, 0.0)}
PUMP_RELOAD = {"J": 1.0, "K": 1.0, "L": 1.0, "M": 1.0, "N": 0.5, "O": 0.15}
# Every other shell rises to the loading port under the receiver and is pushed in and forward (Reloadloop P-V).
SHELL = {"P": (0.0, 0.0, -0.075), "Q": (0.0, 0.0, -0.05), "R": (0.0, 0.0, -0.03), "S": (0.0, 0.0, -0.012),
         "T": (0.0, 0.0, 0.004), "U": (0.004, 0.0, 0.012), "V": (0.02, 0.0, 0.016)}
FLASH = {"A": "flash_a", "B": "flash_b", "C": "flash_c"}
def kick(spr, L):
    """(metres back, degrees nose up) of the whole gun in one game frame: sharp_settings.KICK, else still."""
    return KICK.get((spr[3], L), (0.0, 0.0))


def state(spr, L):
    """What the moving parts do in one game frame: (pump share, {bit part: forge offset in metres})."""
    kind = spr[3]
    if kind == "F" and L in FLASH:                      # the shot: flash and trigger
        # each flash is built parked above the muzzle (sharp_kit.flashes): moved down into place
        k = "ABC".index(L)
        return 0.0, {FLASH[L]: (0.0, 0.0, -park_z(k) * CUBE_M), "trigger": (-TRIGGER_BACK_M, 0.0, 0.0)}
    if kind == "P":                                     # the pump stroke
        return PUMP_BACK.get(L, 0.0), {}
    if kind == "R":                                     # the reload
        if L in SHELL2:
            return PUMP_RELOAD[L], {"shell2": SHELL2[L]}
        if L in SHELL:
            return 0.0, {"shell": SHELL[L]}
        return PUMP_RELOAD.get(L, 0.0), {}
    return 0.0, {}                                      # ready, select, bash, knife: at rest


def pose(spr, L):
    """{part: blend offset} in one game frame: the bits from state(), the pump and bolt back by their share."""
    share, bits = state(spr, L)
    offs = {p: bl(*o) for p, o in bits.items()}
    if share:
        offs.update({p: bl(-share * PUMP_STROKE_M, 0.0, 0.0) for p in ("pump", "bolt")})
    return offs


def main(out):
    # the body is everything that never moves on its own; the bolt rides the pump, so the pump opens the port.
    # The kick moves every model round the hand (gz_forge_export.py: the pose key "*" = [metres back, degrees up]).
    models = {"sharp_body": [], "sharp_pump": ["pump", "bolt"], **GROUPS}
    names = {"sharp_body": "as_sharp_pump_body", "sharp_pump": "as_sharp_pump_pump",
             "sharp_flash": "as_sharp_pump_flash", "sharp_bits": "as_sharp_pump_bits"}
    job = build_job(frames_of("Shotgun.txt", CLASSES), models, HIDDEN, MOVING, pose, kick, MODEL_PATH, names,
                    SPRITE_GUN_SCALE)
    json.dump(job, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
