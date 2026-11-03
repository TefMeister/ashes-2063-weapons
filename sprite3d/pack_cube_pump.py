"""Packs the cube sprite shotgun (2026-11-03): the still body and the moving pump, exported by gz_forge_export.py into
one folder each, into one pk3 with ONE modeldef that draws both together (Model 0 = body, Model 1 = pump).
    python pack_cube_pump.py <body out folder> <pump out folder> <job.json> <out.pk3>
"""
import json
import re
import sys
import zipfile


def surfaces(modeldef):
    return len(re.findall(r"^\s*SurfaceSkin 0 ", open(modeldef).read().split("}")[0], re.M))


def main(body, pump, jobs, out):
    job = json.load(open(jobs))
    jb, jp = job["cube_body"], job["cube_pump"]
    nb = surfaces(f"{body}/modeldef.{jb['name']}.txt")
    np_ = surfaces(f"{pump}/modeldef.{jp['name']}.txt")
    path = jb["model_path"]
    lines = ["// The cube sprite shotgun: sprite3d/pack_cube_pump.py. Model 0 the still body, model 1 the pump."]
    for cls, frames in jb["classes"].items():
        lines += [f"Model {cls}", "{", f'   Path "{path}"',
                  f'   Model 0 "{jb["name"]}.md3"', f'   Skin 0 "{jb["name"]}.png"',
                  f'   Model 1 "{jp["name"]}.md3"', f'   Skin 1 "{jp["name"]}.png"']
        lines += [f'   SurfaceSkin 0 {i} "{jb["name"]}.png"' for i in range(nb)]
        lines += [f'   SurfaceSkin 1 {i} "{jp["name"]}.png"' for i in range(np_)]
        lines += ["   Scale 1.0 1.0 1.0", "   NOINTERPOLATION"]
        for spr, L in frames:
            lines += [f"   FrameIndex {spr} {L} 0 0", f"   FrameIndex {spr} {L} 1 {jp['frame_pose'].get(f'{spr} {L}', 0)}"]
        lines += ["}", ""]
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for folder, j in ((body, jb), (pump, jp)):
            for ext in (".md3", ".png"):
                z.write(f"{folder}/{j['name']}{ext}", f"{path}/{j['name']}{ext}")
        z.writestr("modeldef.as_cube_pump.txt", "\n".join(lines))
    print(out, "packed:", nb, "body surfaces,", np_, "pump surfaces")


if __name__ == "__main__":
    main(*sys.argv[1:5])
