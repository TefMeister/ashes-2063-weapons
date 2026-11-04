"""The export job builder every sharp cube gun shares (2026-11-04; first the pump shotgun, make_job_sharp.py).

A gun is drawn as a few models together, so nothing heavy is stored once per frame: the still body (one frame), and
one model per group of moving parts with one frame per distinct pose of its parts. A gun's own job file says which
game classes it stands in for, which parts each model holds, which parts are hidden until a frame shows them, and,
per game frame, where each moving part is (pose()) and how the whole gun kicks (kick()). This turns that into the job
gz_forge_export.py exports (one model per key) and pack_models.py packs.

A part's pose is [dx, dy, dz] metres in the blend's axes, or seven numbers [dx, dy, dz, degrees nose up, hinge x, y,
z] to also turn it on a hinge (gz_forge_export.md3_corners), with an eighth for the axis (0 left-right, 1 along the
barrel, 2 up). bl() turns forge axes into the blend's.
"""
import os
import sys
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "brutal-doom-3d-guns", "tools"))
import forge_jobs as fj  # noqa: E402

CUBE_M = 0.0034


def bl(fx, fy, fz):
    """Forge axes (x muzzle-ward, y the gun's left, z up) to the blend's (forge_bl.to_bl): (-y, x, z)."""
    return [-fy, fx, fz]


def frames_of(src_file, classes, own=()):
    """{class: [(sprite, letter), ...]} for every frame the game shows of those classes (Actors/Weapons/<src_file>).
    Sprites another weapon draws (forge_jobs.ASHES_FOREIGN: the knife, GLOK ...) are left out unless named in `own`
    (the 9mm's own frames are GLOK, the Ingram's INGG)."""
    src = zipfile.ZipFile(fj.ASHES_SOURCE).read("Actors/Weapons/" + src_file).decode("latin-1")
    return {c: fj.hand_frames(src, c, fj.ASHES_FOREIGN - set(own)) for c in classes}


def build_job(classes, models, hidden, moving, pose, kick, model_path, names, scale):
    """classes: frames_of(); models: {key: [parts]} with [] for the body (everything not in `moving`); pose(spr, L) ->
    {part: pose}; kick(spr, L) -> (metres back, degrees nose up); names: {key: md3 name}."""
    frames = [f for fs in classes.values() for f in fs]
    poses = {k: [((), (0.0, 0.0))] for k in models}
    pose_of = {k: {} for k in models}
    for spr, L in frames:
        offs = {p: tuple(o) for p, o in pose(spr, L).items()}
        kk = tuple(kick(spr, L))
        for k, parts in models.items():
            key = (tuple(sorted((p, o) for p, o in offs.items() if p in parts)), kk)
            if key not in poses[k]:
                poses[k].append(key)
            pose_of[k][f"{spr} {L}"] = poses[k].index(key)

    def pose_dict(key):
        d = {p: list(o) for p, o in key[0]}
        if key[1] != (0.0, 0.0):
            d["*"] = list(key[1])
        return d

    base = {"scale": scale, "no_hands": True, "classes": classes, "model_path": model_path}
    job = {}
    for k, parts in models.items():
        sel = {"skip_parts": moving} if not parts else {"parts": parts}
        job[k] = dict(base, name=names[k], **sel, hidden_parts=[p for p in parts if p in hidden],
                      poses=[pose_dict(key) for key in poses[k]],
                      frame_pose={f: v for f, v in pose_of[k].items() if v})
    print(len(frames), "frames;", "; ".join(f"{k} {len(v)} poses" for k, v in poses.items()))
    return job
