"""Exports every model of a sharp cube gun's job from its blend and packs them into one pk3 (2026-11-04).
    python export_pack.py <gun.blend> <job.json> <out folder> <out.pk3>
One gz_forge_export.py run per job key (into <out folder>/<key>), the runs side by side, then pack_models.py.
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
EXPORT = os.path.join(HERE, "..", "..", "brutal-doom-3d-guns", "tools", "gz_forge_export.py")
BLENDER = os.environ.get("BLENDER", r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe")


def export(blend, jobs, key, out):
    r = subprocess.run([BLENDER, "-b", blend, "--python", EXPORT, "--", jobs, key, out], capture_output=True,
                       text=True, errors="replace")
    if r.returncode or not os.path.exists(out):
        raise SystemExit(f"export of {key} failed:\n{r.stdout[-2000:]}\n{r.stderr[-2000:]}")
    return key, [ln for ln in r.stdout.splitlines() if "triangles" in ln and ":" in ln][-1:]


def main(blend, jobs, out, pk3):
    keys = list(json.load(open(jobs)))
    with ThreadPoolExecutor(len(keys)) as ex:
        for key, lines in ex.map(lambda k: export(blend, jobs, k, os.path.join(out, k)), keys):
            print(key, *lines)
    subprocess.run([sys.executable, os.path.join(HERE, "pack_models.py"), jobs, pk3]
                   + [f"{k}={os.path.join(out, k)}" for k in keys], check=True)


if __name__ == "__main__":
    main(*sys.argv[1:5])
