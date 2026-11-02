# The game's own pictures of one weapon, enlarged on one sheet (in-hand frames + pickup), to set beside real photos.
#   python tools/game_sprites_sheet.py <out.png> <Graphics folder> [<pickup sprite prefix> ...] [--n 6] [--zoom 3]
# Reads Ashes2063Enriched2_23.pk3 from the usual install places. Nothing is written into git.
import io, os, sys, zipfile
from PIL import Image

PK3S = [r"C:\NonSteam\AshesStandalone_V1_51\Resources\Ashes2063Enriched2_23.pk3",
        r"C:\NonSteam\Ashes 2063 VR\Resources\Ashes2063Enriched2_23.pk3"]
args = [a for a in sys.argv[1:]]
n = int(args[args.index("--n") + 1]) if "--n" in args else 6
zoom = int(args[args.index("--zoom") + 1]) if "--zoom" in args else 3
args = [a for i, a in enumerate(args) if a not in ("--n", "--zoom") and (i == 0 or args[i - 1] not in ("--n", "--zoom"))]
out, folder, pickups = args[0], args[1], args[2:]
z = zipfile.ZipFile(next(p for p in PK3S if os.path.exists(p)))
names = sorted(x for x in z.namelist() if x.startswith(f"Graphics/{folder}/") and x.lower().endswith(".png"))
step = max(1, len(names) // n)
pick = names[::step][:n] + [x for x in z.namelist() for p in pickups if x.split("/")[-1].startswith(p)]
ims = []
for x in pick:
    try:
        im = Image.open(io.BytesIO(z.read(x))).convert("RGBA")
    except Exception:                       # a Doom-format picture with a .png name: skip it
        continue
    ims.append(im.resize((im.width * zoom, im.height * zoom), Image.NEAREST))
W = sum(i.width for i in ims) + 10 * len(ims)
H = max(i.height for i in ims)
sheet = Image.new("RGB", (min(W, 3000), H * (1 + W // 3000)), (70, 70, 80))
x = y = 0
for im in ims:
    if x + im.width > 3000:
        x, y = 0, y + H
    sheet.paste(im, (x, y), im)
    x += im.width + 10
sheet.save(out)
print(out, sheet.size, [p.split("/")[-1] for p in pick])
