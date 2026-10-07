"""Probe D: the test light plus a SPECULAR map on the cube shotgun's skin, so the engine's own lights put a moving
glint on the metal (GZDoom material_specular: per-pixel, uses the surface normal, the eye and each dynamic light).

The specular map is made from the skin itself: grey, not-too-dark texels (metal) shine; coloured texels (wood,
leather, cloth) and near-black ones barely do.  python build_spec_probe.py <out dir> <shotgun pk3>
"""
import os, sys, zipfile, io
from PIL import Image

OUT, SHOTGUN = sys.argv[1], sys.argv[2]
SKIN = "models/ashes2063/cubeshotgun/cube_shotgun.png"
SPEC = "models/ashes2063/cubeshotgun/cube_shotgun_spec.png"
NORM = "models/ashes2063/cubeshotgun/cube_shotgun_norm.png"   # a FLAT normal map: the engine only switches to its shiny shader when a normal map is there too (hw_material.cpp)
METAL_SAT = 0.12      # above this colour saturation a texel is not metal (same number as the old shine shader)

with zipfile.ZipFile(SHOTGUN) as z:
    skin = Image.open(io.BytesIO(z.read(SKIN))).convert("RGBA")

px = skin.load()
spec = Image.new("L", skin.size)
sp = spec.load()
w, h = skin.size
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        hi, lo = max(r, g, b), min(r, g, b)
        sat = (hi - lo) / hi if hi else 0.0
        metal = max(0.0, 1.0 - sat / METAL_SAT)
        bright = min(1.0, hi / 140.0)          # very dark texels shine less
        sp[x, y] = int(255 * metal * (0.35 + 0.65 * bright))

buf = io.BytesIO(); spec.save(buf, "PNG")
nbuf = io.BytesIO(); Image.new("RGB", (4, 4), (128, 128, 255)).save(nbuf, "PNG")

GLDEFS = f"""
pointlight LightProbeLight
{{
    color 1.0 0.7 0.3
    size 300
}}
object LightProbeGlow
{{
    frame TNT1 {{ light LightProbeLight }}
}}

material texture "{SKIN}"
{{
    normal "{NORM}"
    specular "{SPEC}"
    glossiness 3.0     // low = a broad sheen; the engine raises it to the 4th power, so 24 gave a pin-point nobody could see
    specularlevel 1.5
}}
"""

ZSCRIPT = open(os.path.join(OUT, "zscript_probe.txt")).read() if os.path.exists(os.path.join(OUT, "zscript_probe.txt")) else None
if ZSCRIPT is None:
    # same light actor + once-only spawner as the other probes
    import re
    src = open(os.path.join(OUT, "build_light_probe.py")).read()
    ZSCRIPT = re.search(r'ZSCRIPT = """(.*?)"""', src, re.S).group(1)
    MAPINFO = re.search(r'MAPINFO = """(.*?)"""', src, re.S).group(1)

path = os.path.join(OUT, "lightprobe_E.pk3")
with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("zscript.lightprobe", ZSCRIPT)
    z.writestr("mapinfo.lightprobe", MAPINFO)
    z.writestr("gldefs.lightprobe", GLDEFS)
    z.writestr(SPEC, buf.getvalue())
    z.writestr(NORM, nbuf.getvalue())
spec.save(os.path.join(OUT, "cube_shotgun_spec.png"))
print("built", path, "spec map", skin.size)
