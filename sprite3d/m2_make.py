"""Builds the 2026-11-27 Meshy set end to end with no Blender window (Build PC):
    python m2_make.py build <gun> [...]       the .blend and preview pictures (forge_make.py)
    python m2_make.py export <gun> [...]      one pk3 per gun and episode (job from m2_anim, export_pack, pack_models)
    python m2_make.py all <gun> [...]         both
    python m2_make.py list
<gun> is the design's short name (m2_<gun>.py) or "all". Blends go to OUT/blend, pictures to OUT/renders, pk3s to
OUT/pk3/<episode>/. Every gun is packed at the Meshy shotgun's scale (PACK_SCALE, its grip kept in the hand)."""
import glob
import importlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(HERE, "..", "..", "blender-cubekit")]
import m2_anim  # noqa: E402
from sharp_job import build_job  # noqa: E402
from sharp_settings import park_z  # noqa: E402

OUT = os.path.join("D:" + os.sep, "Ashes 2063", "3D blender", "meshy set 2026-11-27")
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"
CUBEKIT = os.path.join(HERE, "..", "..", "blender-cubekit")
PACK_SCALE = 0.7                     # make_job_meshy_pump.py: the Meshy shotgun Tefa wore ("the guns felt amazing")
PACK_GRIP = (30, 0, -5)


def guns():
    return sorted(os.path.basename(p)[3:-3] for p in glob.glob(os.path.join(HERE, "m2_*.py"))
                  if os.path.basename(p)[3:-3] not in ("kit", "anim", "make", "probe", "lantern_world"))


def _stub_blender():
    """Designs import Blender's modules at the top; out here only their numbers (CLASSES, RIG, NAME) are read, so
    empty stand-ins let them load."""
    import types

    class Stub(types.ModuleType):
        def __getattr__(self, name):
            return Stub(name)

        def __call__(self, *a, **k):
            return Stub("call")
    for name in ("bpy", "bmesh", "mathutils", "mathutils.bvhtree", "mathutils.geometry"):
        sys.modules.setdefault(name, Stub(name))


def design(gun):
    try:
        import bpy  # noqa: F401
    except ImportError:
        _stub_blender()
    return importlib.import_module("m2_" + gun)


def build(gun):
    env = dict(os.environ, BLENDER=BLENDER)
    subprocess.run([sys.executable, os.path.join(CUBEKIT, "forge_make.py"), os.path.join(OUT, "blend"),
                    os.path.join(OUT, "renders"), os.path.join(HERE, "m2_" + gun + ".py")], check=True, env=env)


def job_for(gun, ep):
    d = design(gun)
    wfile, classes = d.CLASSES[ep]
    src = m2_anim.source(ep, wfile)
    frames, ctx = {}, {}
    foreign = m2_anim.FOREIGN - set(getattr(d, "OWN", ()))
    for c in classes:
        cx = m2_anim.frame_contexts(src, c, foreign)
        frames[c] = sorted(cx)
        ctx.update(cx)
    rig = d.RIG
    pose0, kick = m2_anim.pose_fn(rig, ctx, park_z)
    have_path = os.path.join(OUT, "blend", d.NAME + ".parts.json")
    have = set(json.load(open(have_path))) if os.path.exists(have_path) else None
    moving = [p for p in rig.parts() if have is None or p in have]
    if have is not None and len(moving) < len(rig.parts()):
        print(gun, "has no", sorted(set(rig.parts()) - set(moving)), "- left out of its poses")

    def pose(spr, L):
        return {p: v for p, v in pose0(spr, L).items() if p in moving}
    mech = [p for p in moving if p not in rig.flashes]
    models = {"body": []}
    if mech:
        models["mech"] = mech
    if rig.flashes:
        models["flash"] = list(rig.flashes)
    short = d.NAME[3:]
    names = {k: "m2_%s_%s_%s" % (short, ep, k) for k in models}
    hidden = [p for p in rig.hidden() if p in moving]
    return build_job(frames, models, hidden, moving, pose, kick, "models/ashes2063/m2/" + short, names, 1.0)


def export(gun):
    d = design(gun)
    blend = os.path.join(OUT, "blend", d.NAME + ".blend")
    for ep in d.CLASSES:
        work = os.path.join(OUT, "export", d.NAME, ep)
        os.makedirs(work, exist_ok=True)
        jpath = os.path.join(work, "job.json")
        json.dump(job_for(gun, ep), open(jpath, "w"), indent=1)
        pk3dir = os.path.join(OUT, "pk3", ep)
        os.makedirs(pk3dir, exist_ok=True)
        pk3 = os.path.join(pk3dir, "%s.pk3" % d.NAME)
        env = dict(os.environ, BLENDER=BLENDER)
        # export_pack.py, then pack again with the shared scale and grip
        r = subprocess.run([sys.executable, os.path.join(HERE, "export_pack.py"), blend, jpath, work, pk3],
                           env=env, capture_output=True, text=True, errors="replace")
        print(r.stdout[-1500:], r.stderr[-1500:])
        if r.returncode:
            raise SystemExit("export failed: " + gun + " " + ep)
        keys = list(json.load(open(jpath)))
        subprocess.run([sys.executable, os.path.join(HERE, "pack_models.py"), jpath, pk3]
                       + ["%s=%s" % (k, os.path.join(work, k)) for k in keys]
                       + ["--scale"] + [str(PACK_SCALE)] * 3 + ["--grip"] + [str(v) for v in PACK_GRIP], check=True)


if __name__ == "__main__":
    what, names = sys.argv[1], sys.argv[2:]
    if what == "list":
        print("\n".join(guns()))
        raise SystemExit
    if names == ["all"]:
        names = guns()
    for gun in names:
        if what in ("build", "all"):
            build(gun)
        if what in ("export", "all"):
            export(gun)
