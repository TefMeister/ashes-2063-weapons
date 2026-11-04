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
import os
import sys
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "brutal-doom-3d-guns", "tools"))
import forge_jobs as fj  # noqa: E402
from make_job import CLASSES, PUMP_BACK, PUMP_STROKE_M, SPRITE_GUN_SCALE  # noqa: E402

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


def bl(fx, fy, fz):
    """Forge axes (x muzzle-ward, y the gun's left, z up) to the blend's (forge_bl.to_bl): (-y, x, z)."""
    return [-fy, fx, fz]


def state(spr, L):
    """What the moving parts do in one game frame: (pump share, {bit part: forge offset in metres})."""
    kind = spr[3]
    if kind == "F" and L in FLASH:                      # the shot: flash and trigger
        return 0.0, {FLASH[L]: (0.0, 0.0, 0.0), "trigger": (-TRIGGER_BACK_M, 0.0, 0.0)}
    if kind == "P":                                     # the pump stroke
        return PUMP_BACK.get(L, 0.0), {}
    if kind == "R":                                     # the reload
        if L in SHELL2:
            return PUMP_RELOAD[L], {"shell2": SHELL2[L]}
        if L in SHELL:
            return 0.0, {"shell": SHELL[L]}
        return PUMP_RELOAD.get(L, 0.0), {}
    return 0.0, {}                                      # ready, select, bash, knife: at rest


def main(out):
    src = zipfile.ZipFile(fj.ASHES_SOURCE).read("Actors/Weapons/Shotgun.txt").decode("latin-1")
    classes = {c: fj.hand_frames(src, c, fj.ASHES_FOREIGN) for c in CLASSES}
    frames = [f for fs in classes.values() for f in fs]
    pump_poses, pump_of = [0.0], {}
    group_poses = {k: [()] for k in GROUPS}
    group_of = {k: {} for k in GROUPS}
    for spr, L in frames:
        share, bits = state(spr, L)
        if share not in pump_poses:
            pump_poses.append(share)
        pump_of[f"{spr} {L}"] = pump_poses.index(share)
        for g, parts in GROUPS.items():
            key = tuple(sorted((p, tuple(bl(*o))) for p, o in bits.items() if p in parts))
            if key not in group_poses[g]:
                group_poses[g].append(key)
            group_of[g][f"{spr} {L}"] = group_poses[g].index(key)
    base = {"scale": SPRITE_GUN_SCALE, "no_hands": True, "classes": classes, "model_path": MODEL_PATH}
    job = {
        "sharp_body": dict(base, name="as_sharp_pump_body", skip_parts=MOVING),
        # the bolt rides the pump, so pulling the pump opens the ejection port
        "sharp_pump": dict(base, name="as_sharp_pump_pump", parts=["pump", "bolt"],
                           poses=[{p: bl(-s * PUMP_STROKE_M, 0.0, 0.0) for p in ("pump", "bolt")} if s else {}
                                  for s in pump_poses],
                           frame_pose={k: v for k, v in pump_of.items() if v}),
    }
    for g, parts in GROUPS.items():
        job[g] = dict(base, name="as_" + g.replace("sharp_", "sharp_pump_"), parts=parts,
                      hidden_parts=[p for p in parts if p in HIDDEN],
                      poses=[{p: list(o) for p, o in k} for k in group_poses[g]],
                      frame_pose={k: v for k, v in group_of[g].items() if v})
    json.dump(job, open(out, "w"), indent=1)
    print(len(frames), "frames;", len(pump_poses), "pump poses;",
          "; ".join(f"{len(group_poses[g])} {g} poses" for g in GROUPS))


if __name__ == "__main__":
    main(sys.argv[1])
