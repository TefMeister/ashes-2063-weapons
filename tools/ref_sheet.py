# Several reference pictures on one numbered sheet, so they can be looked at together.
#   python tools/ref_sheet.py <out.png> <picture> [<picture> ...]   (cols 3, each cell 520 px wide)
import os, sys
from PIL import Image, ImageDraw

out, files = sys.argv[1], sys.argv[2:]
W, COLS = 520, 3
cells = []
for f in files:
    im = Image.open(f).convert("RGB")
    im.thumbnail((W, W))
    cells.append(im)
rows = [cells[i:i + COLS] for i in range(0, len(cells), COLS)]
H = [max(c.size[1] for c in r) for r in rows]
sheet = Image.new("RGB", (W * COLS, sum(H)), (40, 40, 44))
d = ImageDraw.Draw(sheet)
y = 0
for r, h in zip(rows, H):
    for k, c in enumerate(r):
        sheet.paste(c, (k * W, y))
        d.rectangle((k * W, y, k * W + 26, y + 18), fill=(0, 0, 0))
        d.text((k * W + 4, y + 3), str(len([1 for rr in rows[:rows.index(r)] for _ in rr]) + k + 1), fill=(255, 255, 0))
    y += h
sheet.save(out)
print(out, sheet.size)
