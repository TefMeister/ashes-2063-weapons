"""The export job for the sprite-faced shotgun (2026-11-03): which game classes and frames it stands in for.

    python make_job.py <out job.json>
then
    blender -b sprite_pump.blend --python brutal-doom-3d-guns/tools/gz_forge_export.py -- <job.json> sprite_pump <out folder>
and pack <out folder> as: models/ashes2063/sprite3d/pump/<md3 + png> and modeldef.as_sprite_pump.txt at the root.
"""
import json, os, sys, zipfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "brutal-doom-3d-guns", "tools"))
import forge_jobs as fj  # noqa: E402

CLASSES = ("pumpaction", "pumpaction2")     # the shotgun and its upgrade
# 2026-11-03, Tefa after wearing it at 1.5x: "1.5 was way over doing it, maybe 1.1x the original size". This gun only;
# the other Ashes guns keep forge_jobs.ASHES_GUN_SCALE.
SPRITE_GUN_SCALE = 1.0                      # then, after 1.1x: "still looked too big ... 1.0"

# The pump stroke (2026-11-03, Tefa: "can you also already animate it to the games animations?"). Only the pump moves:
# in VR the player's own hand holds the gun, so the whole-gun kick and the reload tip-over of the flat game stay out
# (the cube shotgun's kick is what drew the gun too close for a few tics: the "extra step" row on the board).
# How far back the pump is at each game frame, as a share of the stroke, read from the cube shotgun's tic-for-tic
# animation (kit/anim_shotgun_shoot1.py POSES, letters as kit/gz_shotgun.py SPRITES): GRIP A-H back, I-M forward.
# GRIP B and C also show the recoil right after the shot, so they stay at rest, as on the cube shotgun.
# The same GRIP letters cycle the action at the start of a dry reload.
PUMP_STROKE_PX = 3                  # the gap between the pump and the receiver in the 60 x 21 side picture
PUMP_STROKE_M = PUMP_STROKE_PX / 60.0
PUMP_BACK = {"A": 0.17, "D": 0.71, "E": 0.86, "F": 0.94, "G": 1.0, "H": 1.0,
             "I": 0.83, "J": 0.63, "K": 0.43, "L": 0.23}


def main(out):
    src = zipfile.ZipFile(fj.ASHES_SOURCE).read("Actors/Weapons/Shotgun.txt").decode("latin-1")
    classes = {c: fj.hand_frames(src, c, fj.ASHES_FOREIGN) for c in CLASSES}
    job = {"sprite_pump": {"name": "as_sprite_pump", "model_path": "models/ashes2063/sprite3d/pump",
                           "scale": SPRITE_GUN_SCALE, "no_hands": True, "classes": classes}}
    shares = sorted(set(PUMP_BACK.values()))
    job["sprite_pump"]["poses"] = [{}] + [{"pump": [0.0, -share * PUMP_STROKE_M, 0.0]} for share in shares]
    # GRIP for the shotgun, GR2P for its upgrade: the same letters on the same tics (Shotgun.txt, state Pump)
    job["sprite_pump"]["frame_pose"] = {f"{spr} {L}": 1 + shares.index(v)
                                        for spr in ("GRIP", "GR2P") for L, v in PUMP_BACK.items()}
    shown = {f"{s} {L}" for f in classes.values() for s, L in f}
    missing = [k for k in job["sprite_pump"]["frame_pose"] if k not in shown]
    assert not missing, f"pump frames the classes never show: {missing}"
    json.dump(job, open(out, "w"), indent=1)
    # the cube version (sprite_cube_pump.py): two models drawn together, the still body (one frame) and the pump alone
    # (its poses), so the heavy body is not stored once per pump position
    base = {"scale": SPRITE_GUN_SCALE, "no_hands": True, "classes": classes,
            "model_path": "models/ashes2063/sprite3d/cubepump"}
    job["cube_body"] = dict(base, name="as_cube_pump_body", skip_parts=["pump"])
    job["cube_pump"] = dict(base, name="as_cube_pump_pump", parts=["pump"], poses=job["sprite_pump"]["poses"],
                            frame_pose=job["sprite_pump"]["frame_pose"])
    json.dump(job, open(out, "w"), indent=1)
    for c, f in classes.items():
        print(c, len(f), "frames")


if __name__ == "__main__":
    main(sys.argv[1])
