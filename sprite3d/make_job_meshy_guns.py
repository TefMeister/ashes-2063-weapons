"""Export jobs for the Meshy guns that follow the shotgun and the 9mm into the game (2026-11-16, Developer PC).
    python make_job_meshy_guns.py <gun key> <out job.json>
Each gun stands in for the game class its sharp gun does and borrows that sharp job's frames, poses and kick
(make_job_<gun>.py), drawn from the Meshy gun's own parts under its own model names. A pose naming a part this gun
does not have yet (most Meshy guns are still one piece plus the grip, meshy_game_prep.py) is left out of that pose,
so the gun kicks and flashes but that part stays still: round 1, to hold them in VR and judge their size. The revolver
has all its parts, so it moves as the sharp one does; its cylinder swings on the sharp crane moved by the same
offset as its cylinder (meshy_game_prep.GUNS).
"""
import importlib
import json
import os
import sys

from sharp_job import build_job, frames_of

# key: (sharp job module, INGRAM_BUILD or None, game source file, classes, own sprites, parts this gun has,
#       model short name)
GUNS = {
    "revolver": ("make_job_revolver", None, "Revolver.txt", ["revolver"], (),
                 {"cylinder", "trigger", "rounds", "flash_a", "flash_b"}, "mrev"),
    "fal": ("make_job_fal", None, "FAL.txt", ["FAL"], (), {"bolt", "flash_a", "flash_b", "flash_c"}, "mfal"),
    "musket": ("make_job_musket", None, "Musket.txt", ["JunkerMusket"], (), {"flash_a", "flash_b", "flash_c"}, "mmsk"),
    "mq11": ("make_job_ingram", 1, "Ingram.txt", ["Ingram"], ("INGG",), {"bolt", "flash_a", "flash_b", "flash_c"},
             "mq11"),
    "mq11_silenced": ("make_job_ingram", 2, "Ingram.txt", ["Ingram2"], ("INGG",), {"bolt"}, "mq11s"),
    "heavy_mq11": ("make_job_ingram", 3, "Ingram.txt", ["Ingram3"], ("INGG",), set(), "mq11h"),
    "stun_ram": ("make_job_jackhammer", None, "Hammer.txt", ["JACKHAMMER"], (), {"chisel", "trigger"}, "mram"),
    # the slim Meshy-look sawn-off (meshy_look_sawed_off.py): breaks open on its own hinge (sharp_settings.MSAWN_HINGE)
    "sawed_off": ("make_job_sawed_off", None, "Sawedoff.txt", ["SawedOff"], (),
                  {"barrels", "rib", "bead", "lug", "forend", "flash_ra", "flash_rb", "flash_la", "flash_lb", "trigger",
                   "lever", "shell_r", "shell_l"}, "msawn"),
    "crowbar": ("make_job_crowbar", None, "Crowbar.txt", ["Crowbar"], (), set(), "mcrow"),
}
REVOLVER_SHIFT = (0.0, -0.0045, -0.010)      # the Meshy revolver's cylinder centre minus the sharp one's


def sawn_hinge():
    from sharp_job import CUBE_M
    from sharp_settings import MSAWN_HINGE
    return [0.0, MSAWN_HINGE[0] * CUBE_M, MSAWN_HINGE[1] * CUBE_M]      # sharp_job.bl(x, 0, z)


def main(key, out):
    mod_name, build, src, classes, own, have, short = GUNS[key]
    if build:
        os.environ["INGRAM_BUILD"] = str(build)
    sharp = importlib.import_module(mod_name)
    flashes = [p for p in getattr(sharp, "FLASHES", []) if p in have]
    bits = [p for p in getattr(sharp, "BITS", []) if p in have]
    moving = list(getattr(sharp, "MOVING", []))
    hidden = list(getattr(sharp, "HIDDEN", []))
    pose_fn = getattr(sharp, "pose", lambda s, L: {})
    kick_fn = getattr(sharp, "kick", lambda s, L: (0.0, 0.0))

    def pose(spr, L):
        p = {k: list(v) for k, v in pose_fn(spr, L).items() if k in have}
        if key == "revolver":
            for k, v in p.items():
                if len(v) >= 7:          # a hinge: the crane moves with the cylinder
                    v[4:7] = [v[4 + i] + REVOLVER_SHIFT[i] for i in range(3)]
        if key == "sawed_off":
            for k, v in p.items():
                if len(v) >= 7:          # every turning part turns on this gun's own hinge
                    v[4:7] = sawn_hinge()
        return p

    models = {short + "_body": []}
    if key == "revolver":
        models[short + "_cylinder"] = ["cylinder"]
    if key == "sawed_off":
        models[short + "_barrels"] = list(sharp.BARRELS)
    if flashes:
        models[short + "_flash"] = flashes
    if bits:
        models[short + "_bits"] = bits
    names = {k: "as_meshy_" + k for k in models}
    model_path = "models/ashes2063/sprite3d/meshy" + short
    job = build_job(frames_of(src, classes, own=list(own)), models, hidden, moving, pose, kick_fn, model_path,
                    names, 1.0)
    json.dump(job, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
