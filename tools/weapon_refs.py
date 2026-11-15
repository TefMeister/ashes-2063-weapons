"""Reference pictures of every weapon in the Ashes series, for making models (2026-11-15, Developer PC).

Tefa: "please put on a desktop a folder with all the reference pictures of all the weapons in the series, and if
possible, the pictures in different folders for the same weapons with an attachment on and off" (the machine pistol
with and without its suppressor). Each game's own weapon files (Actors/Weapons/*.txt) are read: every weapon class
(a variant with an attachment is its own class, e.g. Ingram / Ingram2 / Ingram3) gets a folder named after its in-game
name (Tag), holding
  pickup  - the picture lying on the floor (Spawn state; the side view, best for image-to-3D),
  hand    - the first picture in the hand (Ready),
  icon    - the inventory icon,
  frames/ - every picture that class draws (firing, reloading ...),
each also 8x bigger (nearest pixel, no smoothing) for tools that want a large image. Pictures come out of the
installed game files and stay on this PC: nothing of them is committed.
    python weapon_refs.py <game Resources folder> <out folder>
"""
import io
import os
import re
import struct
import sys
import zipfile

from PIL import Image

GAMES = [("Ashes 2063 (Episode 1)", "Ashes2063Enriched2_23.pk3"), ("Ashes Afterglow (Episode 2)", "AshesAfterglow1_16.pk3"),
         ("Ashes Hard Reset", "AshesHardReset_105.pk3")]
BIG = 8
SKIP_SPRITES = {"TNT1", "TNT0"}


def palette(z):
    for n in z.namelist():
        if n.split("/")[-1].upper().startswith("PLAYPAL"):
            raw = z.read(n)[:768]
            return [tuple(raw[i:i + 3]) for i in range(0, 768, 3)]
    return None


def doom_patch(raw, pal):
    """A picture in Doom's own column format, as a transparent RGBA image."""
    w, h, _, _ = struct.unpack_from("<hhhh", raw, 0)
    if not (0 < w < 4096 and 0 < h < 4096) or pal is None:
        return None
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = im.load()
    for x in range(w):
        ofs = struct.unpack_from("<I", raw, 8 + 4 * x)[0]
        while ofs < len(raw) and raw[ofs] != 0xFF:
            top, n = raw[ofs], raw[ofs + 1]
            for i in range(n):
                y = top + i
                if y < h:
                    px[x, y] = pal[raw[ofs + 3 + i]] + (255,)
            ofs += n + 4
    return im


def picture(z, name, pal):
    raw = z.read(name)
    try:
        return Image.open(io.BytesIO(raw)).convert("RGBA")
    except Exception:
        return doom_patch(raw, pal)


PICTURE_DIRS = ("sprites", "graphics", "patches", "textures", "hires")
NOT_WEAPONS = {"hazardsuitoverlay", "holsterweapon"}


def sprite_index(z):
    """{lump name (upper, no extension): path} for every loose picture."""
    idx = {}
    for n in z.namelist():
        if n.split("/")[0].lower() in PICTURE_DIRS and not n.endswith("/"):
            idx.setdefault(os.path.splitext(n.split("/")[-1])[0].upper(), n)
    return idx


class Composites:
    """The pictures a TEXTURES lump builds out of pieces (Sprite "REVGA0", w, h { Patch "PISTOL1", x, y ... }): the
    Ashes games draw most of their guns in the hand this way."""

    def __init__(self, z, idx, pal):
        self.z, self.idx, self.pal, self.defs = z, idx, pal, {}
        for n in z.namelist():
            base = n.split("/")[-1].upper()
            if (base.startswith("TEXTURES") and n.count("/") == 0) and not n.endswith("/"):
                self._parse(z.read(n).decode("latin-1", "replace"))

    def _parse(self, text):
        for m in re.finditer(r'(?is)\b(?:Sprite|Graphic|WallTexture|Texture)\s+"?([\w\[\]\\]+)"?\s*,\s*(\d+)\s*,\s*(\d+)'
                             r'\s*\{(.*?)\n\s*\}', text):
            patches = []
            for p in re.finditer(r'(?is)Patch\s+"?([\w\[\]\\/.]+)"?\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*(\{[^{}]*\})?', m.group(4)):
                opts = (p.group(4) or "").lower()
                patches.append((p.group(1).upper(), int(p.group(2)), int(p.group(3)), "flipx" in opts, "flipy" in opts))
            self.defs.setdefault(m.group(1).upper(), (int(m.group(2)), int(m.group(3)), patches))

    def __contains__(self, name):
        return name in self.defs

    def picture(self, name):
        w, h, patches = self.defs[name]
        canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        for pname, x, y, fx, fy in patches:
            path = self.idx.get(os.path.splitext(pname.split("/")[-1])[0])
            im = picture(self.z, path, self.pal) if path else None
            if im is None:
                continue
            if fx:
                im = im.transpose(Image.FLIP_LEFT_RIGHT)
            if fy:
                im = im.transpose(Image.FLIP_TOP_BOTTOM)
            canvas.alpha_composite(im, (max(0, x), max(0, y)), (max(0, -x), max(0, -y)))
        box = canvas.getbbox()
        return canvas.crop(box) if box else None


def language(z):
    """{$KEY: text} from the English part of the LANGUAGE lump(s), for names written as $WEAPON_..."""
    out = {}
    for n in z.namelist():
        if n.split("/")[-1].upper().startswith("LANGUAGE") and not n.endswith("/"):
            text = z.read(n).decode("latin-1", "replace")
            for sec in re.split(r"(?m)^\s*\[", text):
                if not re.match(r"(?i)(enu|en|default)\b", sec.strip()):
                    continue
                for m in re.finditer(r'(?ms)^\s*(\w+)\s*=\s*((?:"[^"]*"\s*)+);', sec):
                    out.setdefault("$" + m.group(1).upper(), "".join(re.findall(r'"([^"]*)"', m.group(2))))
    return out


def frames_of(spr, letters, idx, comp=None):
    """The pictures for sprite spr with these frame letters: [(lump name, image getter)]. A lump name holds one or two
    frame+rotation pairs; a TEXTURES composite of that name wins over a loose picture (as in the engine)."""
    out = []
    for L in letters:
        if comp is not None:
            hit = next((n for n in comp.defs if n[:4] == spr and (n[4:5] == L or n[6:7] == L)), None)
            if hit:
                out.append((hit, lambda n=hit: comp.picture(n)))
                continue
        for lump, path in idx.items():
            if lump[:4] == spr and (lump[4:5] == L or lump[6:7] == L):
                out.append((lump, path))
                break
    return out


def get(z, src, pal):
    return src() if callable(src) else picture(z, src, pal)


def classes(text):
    """[(class name, block text)] for every actor/class in a DECORATE or ZScript file."""
    heads = list(re.finditer(r"(?im)^\s*(?:actor|class)\s+(\w+)\s*(?::\s*(\w+))?[^\n]*", text))
    return [(m.group(1), m.group(2), text[m.start():heads[i + 1].start() if i + 1 < len(heads) else len(text)])
            for i, m in enumerate(heads)]


def state_frames(block, label):
    """The sprite frames of a state's first lines, past any TNT1 placeholders: [(sprite, letters)]."""
    m = re.search(r"(?im)^\s*" + label + r":\s*\n", block)
    if not m:
        return []
    out = []
    for ln in block[m.end():].splitlines():
        s = ln.strip()
        if not s or s.startswith("//"):
            continue
        if re.match(r"^\w+:", s) or s.lower().startswith(("goto", "stop", "loop", "wait", "}")):
            if out:
                break
            continue
        f = re.match(r'^"?(\w{4})"?\s+"?([A-Z\[\]\\#]+)"?\s', s + " ")
        if f and f.group(1).upper() not in SKIP_SPRITES:
            out.append((f.group(1).upper(), f.group(2)))
            break
    return out


def all_frames(block):
    seen = []
    for f in re.finditer(r'(?m)^\s*"?(\w{4})"?\s+"?([A-Z]+)"?\s+-?\d', block):
        k = (f.group(1).upper(), f.group(2))
        if k[0] not in SKIP_SPRITES and k not in seen:
            seen.append(k)
    return seen


def save(im, path):
    im.save(path)
    im.resize((im.width * BIG, im.height * BIG), Image.NEAREST).save(path[:-4] + f"_x{BIG}.png")


def safe(s):
    return re.sub(r'[<>:"/\\|?*]+', "-", s).strip(" .") or "unnamed"


def main(res, out):
    count = 0
    for game, pk in GAMES:
        z = zipfile.ZipFile(os.path.join(res, pk))
        pal = palette(z)
        idx = sprite_index(z)
        comp = Composites(z, idx, pal)
        words = language(z)
        for wf in sorted(n for n in z.namelist() if n.lower().startswith("actors/weapons/") and n.endswith(".txt")):
            text = z.read(wf).decode("latin-1")
            cls = classes(text)
            weapons = {c for c, parent, _ in cls if parent and parent.lower() == "weapon"}
            weapons |= {c for c, parent, _ in cls if parent in weapons}
            for c, parent, block in cls:
                if c not in weapons or c.lower() in NOT_WEAPONS:
                    continue
                tag = re.search(r'(?im)^\s*Tag\s+"([^"]+)"', block)
                name = tag.group(1) if tag else c
                name = words.get(name.upper(), c) if name.startswith("$") else name
                folder = os.path.join(out, safe(game), safe(os.path.splitext(wf.split("/")[-1])[0]),
                                      safe(f"{name} ({c})"))
                os.makedirs(os.path.join(folder, "frames"), exist_ok=True)
                wanted = [("pickup", state_frames(block, "Spawn")),
                          ("hand", state_frames(block, "LoadedReady") or state_frames(block, "Ready"))]
                icon = re.search(r'(?im)^\s*Inventory\.Icon\s+"(\w+)"', block)
                for kind, fr in wanted:
                    for spr, letters in fr:
                        for lump, src in frames_of(spr, letters[:1], idx, comp):
                            im = get(z, src, pal)
                            if im:
                                save(im, os.path.join(folder, f"{kind}_{lump}.png"))
                                count += 1
                if icon:
                    ic = icon.group(1).upper()
                    im = comp.picture(ic) if ic in comp else (picture(z, idx[ic], pal) if ic in idx else None)
                    if im:
                        save(im, os.path.join(folder, f"icon_{ic}.png"))
                for spr, letters in all_frames(block):
                    for lump, src in frames_of(spr, letters, idx, comp):
                        target = os.path.join(folder, "frames", lump + ".png")
                        if not os.path.exists(target):
                            im = get(z, src, pal)
                            if im:
                                im.save(target)
                                count += 1
                print(f"{game} / {wf.split('/')[-1]} / {name} ({c})")
    with open(os.path.join(out, "READ ME.txt"), "w") as f:
        f.write(README)
    print(count, "pictures")


README = """Every weapon in the three Ashes games, as the games draw it.

One folder per game, then one per weapon, then one per version of that weapon
(a version with an attachment, like the silenced machine pistol, is its own folder).

In each version's folder:
  pickup_...  the weapon lying on the floor: a side view, the best one for Meshy
  hand_...    the weapon in your hand, at rest
  icon_...    the inventory icon
  ..._x8      the same picture 8 times bigger, sharp edges kept
  frames      every picture the game shows for it (firing, reloading, the lantern ...)

Made by ashes-2063-weapons/tools/weapon_refs.py from the installed games.
"""


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
