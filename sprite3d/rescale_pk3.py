# rescale_pk3.py -- a copy of a gun pk3 at another size, without going back through Blender.
#   python sprite3d/rescale_pk3.py <in.pk3> <out.pk3> <factor>
# Only the "Scale x y z" lines of the pk3's modeldef files change (multiplied by the factor); the
# models are copied as they are. The engine scales a model about its own origin, which the
# exporter puts at the grip, so the gun stays in the hand. The original pk3 is never touched.
import sys, re, zipfile

def rescale(src, dst, factor):
    changed = 0
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            if info.filename.lower().startswith("modeldef"):
                def bigger(m):
                    nonlocal changed
                    changed += 1
                    nums = [float(v) * factor for v in m.group(2).split()]
                    return m.group(1) + " ".join("%.4f" % v for v in nums)
                text = data.decode("utf-8")
                text = re.sub(r"(?im)^(\s*Scale\s+)([-\d.]+\s+[-\d.]+\s+[-\d.]+)", bigger, text)
                data = text.encode("utf-8")
            zout.writestr(info, data)
    return changed

if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit(__doc__ or "usage: rescale_pk3.py <in.pk3> <out.pk3> <factor>")
    n = rescale(sys.argv[1], sys.argv[2], float(sys.argv[3]))
    print("Scale lines changed:", n)
    raise SystemExit(0 if n else 1)
