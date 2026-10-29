# The FAL with its live scope, as one test pk3 for Ashes 2063 VR (2026-10-29): the forge FAL exported with its glass as
# surface 0, the scope script (this folder), and the shine that makes the gun catch the game's lights
# (brutal-doom-3d-guns/lights/make_shine.py, the same as the hand-made guns have).
#   python scope/build_scope_test.py <export folder> <out pk3>
# <export folder> is what gz_forge_export.py wrote for battle_rifle (af_battle_rifle.md3/.png, _glass.png, modeldef).
# Load it after the forge guns test pk3, so this FAL replaces the one there.
import os
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SHINE = os.path.join(HERE, "..", "..", "brutal-doom-3d-guns", "lights", "make_shine.py")
MODEL_PATH = "models/ashes2063/forge/battle_rifle"
NAME = "af_battle_rifle"

src, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
with tempfile.TemporaryDirectory() as shine:
    subprocess.run([sys.executable, SHINE, shine, f"{MODEL_PATH}/{NAME}.png={os.path.join(src, NAME + '.png')}"],
                   check=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in (NAME + ".md3", NAME + ".png", NAME + "_glass.png"):
            z.write(os.path.join(src, f), f"{MODEL_PATH}/{f}")
        z.write(os.path.join(src, f"modeldef.{NAME}.txt"), f"modeldef.{NAME}")
        for root, _, files in os.walk(shine):
            for f in files:
                p = os.path.join(root, f)
                z.write(p, os.path.relpath(p, shine).replace(os.sep, "/"))
        for f in ("zscript.txt", "animdefs.ashesscope", "mapinfo.ashesscope", "zscript/ashes_scope.zs"):
            z.write(os.path.join(HERE, f), f)
    print(out)
    for n in zipfile.ZipFile(out).namelist():
        print("  " + n)
