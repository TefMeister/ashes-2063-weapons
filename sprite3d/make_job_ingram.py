"""The export job for one sharp Ingram build (sharp_ingram.py, 2026-11-04): which game frames show which pose.
    python make_job_ingram.py <1|2|3> <out job.json>
then export_pack.py with sharp_ingram<n>.blend; anim_preview.py plays SEQUENCE[<n>] (set INGRAM_BUILD) in Blender.

Every frame of the game's Ingram, Ingram2 and Ingram3 (Actors/Weapons/Ingram.txt) has a pose. Only the gun's own
parts move, plus the small kick:
- the bare gun's shots flash (INGF A B C, the side-held burst INGS D E F); the silenced builds' shots (INF2/INF3 A D E)
  only kick: the game draws no flash for them. The cocking knob runs back on each shot.
- the reload: the magazine drops out (bare gun INGR/INGE B to E, silenced C to F), is gone, a new one comes up; after
  an empty reload the knob is pulled back and let go (INGR/I2GR/I3GR U to Z).
"""
import json
import os
import sys

from sharp_job import CUBE_M, bl, build_job, frames_of
from sharp_settings import ING_BOLT_STROKE, park_z

BUILD = int(os.environ.get("INGRAM_BUILD", sys.argv[1] if len(sys.argv) > 2 else 1))
CLASS = {1: "Ingram", 2: "Ingram2", 3: "Ingram3"}[BUILD]
MODEL_PATH = "models/ashes2063/sprite3d/sharpingram%d" % BUILD
FLASHES = ["flash_a", "flash_b", "flash_c"] if BUILD == 1 else []
BITS = ["trigger", "mag", "bolt"]
MOVING = FLASHES + BITS
HIDDEN = FLASHES + ["mag"]
# the sprite families of this build: (shot, reload, empty reload, cocking)
FIRE = {1: "INGF", 2: "INF2", 3: "INF3"}[BUILD]
RELOAD = {1: ("INGR", "INGE"), 2: ("ING2", "I2E2"), 3: ("ING3", "I3E2")}[BUILD]
COCK = {1: "INGR", 2: "I2GR", 3: "I3GR"}[BUILD]
if BUILD == 1:
    MAG_OUT = {"B": 3.0, "C": 8.0, "D": 16.0, "E": 30.0, "F": None, "G": None, "H": None, "I": 30.0, "J": 16.0,
               "K": 8.0, "L": 3.0}
    FLASH = {("INGF", "A"): "flash_a", ("INGF", "B"): "flash_b", ("INGF", "C"): "flash_c",
             ("INGS", "D"): "flash_a", ("INGS", "E"): "flash_b", ("INGS", "F"): "flash_c"}
    SHOTS = set(FLASH)
else:
    MAG_OUT = {"C": 3.0, "D": 8.0, "E": 16.0, "F": 30.0, "G": None, "H": None, "I": 30.0, "J": 16.0, "K": 8.0,
               "L": 3.0}
    FLASH = {}
    SHOTS = {(FIRE, "A"), (FIRE, "C")} | {("ING%d" % BUILD, L) for L in "WY"}
COCKED = {"U": 0.3, "V": 0.7, "W": 1.0, "X": 1.0, "Y": 0.5}
TRIGGER_BACK_M = 0.002

SEQUENCE = {1: [("INGG", "A", 20)] + [("INGF", L, 1) for L in "ABC" * 4] + [("INGG", "B", 2), ("INGG", "C", 2),
                                                                           ("INGG", "D", 2), ("INGG", "A", 15)]
            + [("INGE", L, 2) for L in "NOPABCDEFGHIIIIJKLLLMMQRS"] + [("INGR", L, 2) for L in "UVWWXYZPON"]
            + [("INGG", "A", 20)]}
for b, f, (r, e), c in ((2, "INF2", ("ING2", "I2E2"), "I2GR"), (3, "INF3", ("ING3", "I3E2"), "I3GR")):
    SEQUENCE[b] = ([(r, "A", 20)] + [(f, L, 1) for L in "AD" * 5] + [(f, "E", 2), (f, "F", 2), (r, "A", 15)]
                   + [(e, L, 2) for L in "OPQCDEFGHHHIJKLLMMMNRST"] + [(c, L, 2) for L in "UVWWXYZ"]
                   + [(r, L, 2) for L in "QPO"] + [(r, "A", 20)])


def pose(spr, L):
    out = {}
    if (spr, L) in FLASH:
        name = FLASH[(spr, L)]
        out[name] = bl(0.0, 0.0, -park_z(FLASHES.index(name)) * CUBE_M)
    if (spr, L) in SHOTS or spr == FIRE and L in "ABC":
        out["trigger"] = bl(-TRIGGER_BACK_M, 0.0, 0.0)
        out["bolt"] = bl(-ING_BOLT_STROKE * CUBE_M, 0.0, 0.0)
    if spr == COCK and L in COCKED:
        out["bolt"] = bl(-COCKED[L] * ING_BOLT_STROKE * CUBE_M, 0.0, 0.0)
    d = MAG_OUT.get(L, 0.0) if spr in RELOAD else 0.0
    if d is not None:                                       # the magazine is always shown, except while it is out
        out["mag"] = bl(0.0, 0.0, -d * CUBE_M)
    return out


def kick(spr, L):
    if (spr, L) in SHOTS or spr == FIRE and L in "ABC":
        return (0.006, 1.8)
    if spr == FIRE and L in "DE":
        return (0.003, 0.8)
    return (0.0, 0.0)


def main(out):
    models = {"body": [], "bits": BITS}
    if FLASHES:
        models["flash"] = FLASHES
    names = {k: "as_sharp_ingram%d_%s" % (BUILD, k) for k in models}
    job = build_job(frames_of("Ingram.txt", [CLASS], own=["INGG"]), models, HIDDEN, MOVING, pose, kick, MODEL_PATH,
                    names, 1.0)
    json.dump(job, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[2])
