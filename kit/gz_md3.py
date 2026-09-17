# Minimal MD3 writer (Quake 3 vertex-animation model, read by GZDoom).
# Every frame stores every vertex; parts hidden in a frame are collapsed to a point.
import math, struct

MAX_SURFACE_VERTS = 4000


def _normal_bytes(n):
    x, y, z = n
    polar = math.acos(max(-1.0, min(1.0, z)))
    azim = math.atan2(y, x)
    lng = int(round(polar * 255.0 / (2 * math.pi))) & 0xFF
    lat = int(round(azim * 255.0 / (2 * math.pi))) & 0xFF
    return struct.pack("<H", (lat << 8) | lng)


def write_md3(path, name, frames, tris_uv, shader):
    """frames: list of per-frame lists of (pos xyz, normal xyz), one entry per vertex.
    tris_uv: (triangles [(a,b,c)], uvs [(s,t)]) over the same vertex indices."""
    tris, uvs = tris_uv
    nv = len(uvs)
    # split into surfaces of <= MAX_SURFACE_VERTS; triangles never share vertices
    # across the split because every triangle owns its three corners.
    surfaces = []
    cur_t, cur_v = [], []
    for t in tris:
        if len(cur_v) + 3 > MAX_SURFACE_VERTS:
            surfaces.append((cur_t, cur_v)); cur_t, cur_v = [], []
        base = len(cur_v)
        cur_v += list(t)
        cur_t.append((base, base + 1, base + 2))
    if cur_t:
        surfaces.append((cur_t, cur_v))

    nf = len(frames)
    HDR = 108
    FRAME = 56
    ofs_frames = HDR
    ofs_surf = ofs_frames + nf * FRAME
    body = b""
    for si, (st, sv) in enumerate(surfaces):
        n = len(sv)
        SURF_HDR = 108
        ofs_shaders = SURF_HDR
        ofs_tris = ofs_shaders + 68
        ofs_st = ofs_tris + 12 * len(st)
        ofs_xyz = ofs_st + 8 * n
        ofs_end = ofs_xyz + 8 * n * nf
        s = struct.pack("<4s64siiiiiiiiii", b"IDP3", f"{name}_{si}".encode(), 0, nf, 1, n, len(st),
                        ofs_tris, ofs_shaders, ofs_st, ofs_xyz, ofs_end)
        s += struct.pack("<64si", shader.encode(), 0)
        s += b"".join(struct.pack("<3i", *t) for t in st)
        s += b"".join(struct.pack("<2f", uvs[v][0], 1.0 - uvs[v][1]) for v in sv)
        for fr in frames:
            for v in sv:
                p, nrm = fr[v]
                q = [max(-32768, min(32767, int(round(c * 64.0)))) for c in p]
                s += struct.pack("<3h", *q) + _normal_bytes(nrm)
        assert len(s) == ofs_end
        body += s
    head_frames = b""
    for i, fr in enumerate(frames):
        pts = [p for p, _ in fr]
        mn = [min(p[k] for p in pts) for k in range(3)]
        mx = [max(p[k] for p in pts) for k in range(3)]
        r = max(math.sqrt(sum(c * c for c in p)) for p in pts)
        head_frames += struct.pack("<3f3f3ff16s", *mn, *mx, 0.0, 0.0, 0.0, r, f"f{i}".encode())
    ofs_end = ofs_surf + len(body)
    head = struct.pack("<4si64s9i", b"IDP3", 15, name.encode(), 0, nf, 0, len(surfaces), 0,
                       ofs_frames, ofs_surf, ofs_surf, ofs_end)
    assert len(head) == HDR
    with open(path, "wb") as f:
        f.write(head + head_frames + body)
    return len(surfaces), nv, len(tris)
