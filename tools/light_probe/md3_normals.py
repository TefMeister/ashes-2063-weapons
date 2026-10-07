"""Count how many vertex normals in an md3 (inside a pk3) are real, zero, or all the same."""
import sys, zipfile, struct, math, collections, io

pk3, inner = sys.argv[1], sys.argv[2]
with zipfile.ZipFile(pk3) as z:
    data = z.read(inner)

magic, ver, name, flags, nframes, ntags, nsurf, nskins, ofs_frames, ofs_tags, ofs_surf, ofs_end = struct.unpack_from("<4si64s9i", data, 0)
print("frames", nframes, "surfaces", nsurf)
ofs = ofs_surf
for si in range(nsurf):
    (smagic, sname, sflags, snf, nsh, nv, nt, otri, osh, ost, oxyz, oend) = struct.unpack_from("<4s64siiiiiiiiii", data, ofs)
    cnt = collections.Counter()
    zero = 0
    for fi in range(min(snf, 2)):  # first two frames are enough
        base = ofs + oxyz + fi * nv * 8
        for vi in range(nv):
            x, y, zz, n = struct.unpack_from("<3hH", data, base + vi * 8)
            lat = ((n >> 8) & 0xff) * math.pi / 128
            lng = (n & 0xff) * math.pi / 128
            nx, ny, nz = math.cos(lat) * math.sin(lng), math.sin(lat) * math.sin(lng), math.cos(lng)
            cnt[(round(nx, 1), round(ny, 1), round(nz, 1))] += 1
            if n == 0:
                zero += 1
    print(f"surface {si} verts {nv} tris {nt}: packed-zero normals {zero}; distinct normals {len(cnt)}; top {cnt.most_common(8)}")
    ofs += oend
