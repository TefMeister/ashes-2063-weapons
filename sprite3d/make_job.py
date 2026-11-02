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


def main(out):
    src = zipfile.ZipFile(fj.ASHES_SOURCE).read("Actors/Weapons/Shotgun.txt").decode("latin-1")
    classes = {c: fj.hand_frames(src, c, fj.ASHES_FOREIGN) for c in CLASSES}
    job = {"sprite_pump": {"name": "as_sprite_pump", "model_path": "models/ashes2063/sprite3d/pump",
                           "scale": fj.ASHES_GUN_SCALE, "no_hands": True, "classes": classes}}
    json.dump(job, open(out, "w"), indent=1)
    for c, f in classes.items():
        print(c, len(f), "frames")


if __name__ == "__main__":
    main(sys.argv[1])
