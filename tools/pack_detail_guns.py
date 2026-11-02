# The detailed Ashes guns (forge/detail, 2026-11-02) into one test pk3: export every detailed gun whose .blend exists
# (gun only, 1.5x, grip from its "grip" part), give each skin a faint shine, zip it.
#   python tools/pack_detail_guns.py [<out pk3>]
# Default out: MEGA .../3D blender/forge-2026-11-02/gzdoom/Ashes2063_detailed_guns_VR_test.pk3
# Load it AFTER the first-pass forge pk3 so its models win for the same weapons.
# Tefa, 2026-11-02: "guns need to be about 1.5 times as big", "reduce the light reflection ... 2.5x".
import json, os, shutil, subprocess, sys, tempfile, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
BD = os.path.normpath(os.path.join(HERE, "..", "..", "brutal-doom-3d-guns"))
BLENDER = os.environ.get("BLENDER", r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe")
MEGA = os.path.join("D:" + os.sep, "MEGA transfer", "Game Files", "ashes-2063-weapons", "3D blender",
                    "forge-2026-11-02", "gzdoom")
SHINE_LEVEL = "0.8"                # 2026-11-02 (Tefa: "glassy ... worse than having no shine at all"): 1.2 -> 0.8,
SHINE_STYLE = ["--vary", "--bumpy", "0.18"]   # and uneven: grime shines less, every cube a little tilted (make_shine.py)


def main():
    out = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(MEGA, "Ashes2063_detailed_guns_VR_test.pk3")
    work = tempfile.mkdtemp(prefix="ashes-detail-")
    jobs_path = os.path.join(work, "jobs.json")
    subprocess.run([sys.executable, os.path.join(BD, "tools", "forge_jobs.py"), "ashes-detail", jobs_path], check=True)
    jobs = json.load(open(jobs_path))
    stage = os.path.join(work, "pk3")
    skins = []
    for gun, j in jobs.items():
        gdir = os.path.join(stage, *j["model_path"].split("/"))
        r = subprocess.run([BLENDER, "-b", j["blend"], "--python", os.path.join(BD, "tools", "gz_forge_export.py"), "--",
                            jobs_path, gun, gdir], capture_output=True, text=True, errors="replace")
        lines = [ln for ln in r.stdout.splitlines() if ln.startswith(gun + ":")]
        print("\n".join(lines) or r.stdout[-2000:] + r.stderr[-2000:])
        if r.returncode or not os.path.exists(os.path.join(gdir, j["name"] + ".md3")):
            raise SystemExit(f"export failed: {gun}")
        shutil.move(os.path.join(gdir, f"modeldef.{j['name']}.txt"), os.path.join(stage, f"modeldef.{j['name']}"))
        skins.append(f"{j['model_path']}/{j['name']}.png={os.path.join(gdir, j['name'] + '.png')}")
    subprocess.run([sys.executable, os.path.join(BD, "lights", "make_shine.py"), stage, "--level", SHINE_LEVEL] + SHINE_STYLE + skins,
                   check=True)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(stage):
            for f in files:
                p = os.path.join(root, f)
                z.write(p, os.path.relpath(p, stage).replace(os.sep, "/"))
    print(f"{len(jobs)} guns -> {out} ({os.path.getsize(out) // 1048576} MB)")
    shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
