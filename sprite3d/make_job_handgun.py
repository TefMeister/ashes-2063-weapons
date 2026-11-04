"""The export job for the sharp 9mm (sharp_handgun.py, 2026-11-04): which game frames show which pose.
    python make_job_handgun.py <out job.json>
then export_pack.py; anim_preview.py plays SEQUENCE in Blender.

Every frame of the game's Glock (Actors/Weapons/Glock.txt) has a pose; its lantern frames (GLKL) show the gun at rest
except their own shot. Only the gun's own parts move, plus the small kick:
- the shot: two flashes (GLKF A B, lantern GLKL J K), the slide runs back and returns (GLOK B C), the trigger back
- empty: every GLKE frame has the slide locked back (the game draws the empty gun that way)
- the reload: the magazine slides out down the grip (E to H), is gone (I J), a new one comes up (K to N); the slide is
  racked or released at the end (GLOK Q R S).
"""
import json
import sys

from sharp_job import CUBE_M, bl, build_job, frames_of
from sharp_settings import GLK_MAG_AXIS, GLK_SLIDE_STROKE, park_z

MODEL_PATH = "models/ashes2063/sprite3d/sharpglock"
FLASHES = ["flash_a", "flash_b"]
BITS = ["trigger", "mag"]
MOVING = ["slide"] + FLASHES + BITS
HIDDEN = FLASHES + ["mag"]
SLIDE = {("GLOK", "B"): 1.0, ("GLOK", "C"): 0.5, ("GLOK", "Q"): 1.0, ("GLOK", "R"): 0.6, ("GLOK", "S"): 0.2}
MAG_OUT = {"F": 3.0, "G": 10.0, "H": 26.0, "I": None, "J": None, "K": 26.0, "L": 10.0, "M": 3.0}
FLASH = {("GLKF", "A"): "flash_a", ("GLKF", "B"): "flash_b", ("GLKL", "J"): "flash_a", ("GLKL", "K"): "flash_b"}
KICK = {("GLKF", "A"): (0.008, 2.5), ("GLKF", "B"): (0.005, 1.5), ("GLOK", "B"): (0.003, 0.8),
        ("GLKL", "J"): (0.008, 2.5), ("GLKL", "K"): (0.005, 1.5), ("GLKL", "L"): (0.003, 0.8)}
TRIGGER_BACK_M = 0.002

SEQUENCE = ([("GLOK", "A", 20), ("GLKF", "A", 1), ("GLKF", "B", 1), ("GLOK", "B", 2), ("GLOK", "C", 1),
             ("GLOK", "A", 12), ("GLKF", "A", 1), ("GLKF", "B", 1), ("GLOK", "B", 2), ("GLOK", "C", 1),
             ("GLKE", "D", 15)]
            + [("GLKE", L, 1) for L in "DEFG"] + [("GLKE", L, 2) for L in "HIJ"] + [("GLKE", "K", 5)]
            + [("GLKE", L, 2) for L in "LMNOOP"] + [("GLOK", L, 2) for L in "QQQRST"]
            + [("GLOK", L, 1) for L in "GFE"] + [("GLOK", "A", 20)])


def pose(spr, L):
    out = {}
    if (spr, L) in FLASH:
        name = FLASH[(spr, L)]
        out[name] = bl(0.0, 0.0, -park_z(FLASHES.index(name)) * CUBE_M)
        out["trigger"] = bl(-TRIGGER_BACK_M, 0.0, 0.0)
    share = 1.0 if spr == "GLKE" else SLIDE.get((spr, L), 0.0)
    if share:
        out["slide"] = bl(-share * GLK_SLIDE_STROKE * CUBE_M, 0.0, 0.0)
    d = MAG_OUT.get(L, 0.0) if spr in ("GLOK", "GLKE") else 0.0
    if d is not None:                                       # the magazine is always shown, except while it is out
        out["mag"] = bl(d * GLK_MAG_AXIS[0] * CUBE_M, 0.0, d * GLK_MAG_AXIS[1] * CUBE_M)
    return out


def kick(spr, L):
    return KICK.get((spr, L), (0.0, 0.0))


def main(out):
    models = {"glk_body": [], "glk_slide": ["slide"], "glk_flash": FLASHES, "glk_bits": BITS}
    names = {k: "as_sharp_" + k for k in models}
    job = build_job(frames_of("Glock.txt", ["Glock"], own=["GLOK"]), models, HIDDEN, MOVING, pose, kick, MODEL_PATH, names, 1.0)
    json.dump(job, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1])
