# Revolver pass 2 (2026-11-16, Tefa): rust off, weathered steel with carved gouges and bright scratches,
# curved trigger and a round trigger guard like the S&W 625 photo. Same 1.7 mm cubes as the rest.
#     blender -b meshy_look_revolver.blend --python meshy_look_revolver_pass2.py -- <out.blend>
# Works on the built blend (the cubes and their colour sheet), after meshy_look_revolver.py; meshy_look_vox.py reads it.
import bpy, sys, math, random, collections
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meshy_look_vox as vox
from mathutils import Vector
ARGS = sys.argv[sys.argv.index('--')+1:]
OUT = ARGS[0]
V = 0.00085; OFF = [0, 0, 1.0]
DIRS = ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))
SH = {(0,0,1):1.26,(0,0,-1):0.62,(1,0,0):1.0,(-1,0,0):1.0,(0,1,0):0.77,(0,-1,0):0.77}
GUARD = [(249,-162),(253,-174),(254,-188),(249,-201),(239,-210),(225,-214),(210,-212),(197,-205),(188,-196),(183,-186),(181,-175)]
TRIG = [(221,-160),(218,-170),(216,-179),(217,-188),(221,-194),(227,-198)]


def K(c): return (c[0]//2, c[1]//2, (c[2]-1)//2)
def units(k): return [(2*k[0]+a, 2*k[1]+b, 2*k[2]+1+e) for a in (0,1) for b in (0,1) for e in (0,1)]
def h01(*a):
    x = 0
    for i, n in enumerate(a): x ^= (n * (73856093, 19349663, 83492791, 2654435761, 97)[i % 5])
    x = (x ^ (x >> 13)) * 1274126177
    return ((x ^ (x >> 16)) & 0xFFFFFF) / float(0xFFFFFF)
def lum(c): return (c[0]+c[1]+c[2])/3
def is_rust(c): return c[0]-c[2] > 0.02 and c[0] > c[1]*1.05


img = bpy.data.images['meshy_look_revolver_palette']
obs = {o.name.split('_')[-1]: o for o in bpy.data.objects if o.type == 'MESH'}
METAL = ('barrel','cylinder','frame','hammer')
data = {}
for n, o in obs.items():
    f = vox.read(o, V, OFF, img)
    cf = {}
    for (c, d), col in f.items(): cf.setdefault((K(c), d), col)
    data[n] = {'cells': vox.flood(f), 'cf': cf}

pool = collections.defaultdict(list)
for n in ('frame','barrel','cylinder'):
    for (k, d), col in data[n]['cf'].items():
        if not is_rust(col) and 0.12 < lum(col) < 0.6: pool[d].append(col)
def steel(k, d, seed=0):
    p = pool[d]; return p[int(h01(*k, seed, 7) * len(p)) % len(p)]

# 1. rust off: copy a neighbouring colour from the same side, spreading inwards
def derust(cf, keep=lambda k, d: False, wood=False):
    test = (lambda c: c[0] > 0.45 and c[0] > c[1]*2.2) if wood else is_rust
    bad = {key for key, col in cf.items() if test(col) and not keep(*key)}
    good = {key: col for key, col in cf.items() if key not in bad}
    left = set(bad)
    for it in range(80):
        new = {}
        for (k, d) in left:
            ax = [i for i in range(3) if d[i]][0]
            nb = []
            for i in range(3):
                if i == ax: continue
                for s in (1, -1):
                    for depth in (0, 1, -1):
                        kk = list(k); kk[i] += s; kk[ax] += depth
                        col = good.get((tuple(kk), d))
                        if col: nb.append(col)
            if nb: new[(k, d)] = nb[int(h01(*k, it) * len(nb)) % len(nb)]
        if not new: break
        good.update(new); left -= set(new)
    for key in left: good[key] = steel(*key)
    print("  rust faces replaced", len(bad), "unfilled", len(left))
    return good
for n in METAL:
    data[n]['cf'] = derust(data[n]['cf'])     # the orange front sight insert too (Tefa: "remove the orange from the revolvers sight")
data['grip']['cf'] = derust(data['grip']['cf'], wood=True)

# 2. new trigger guard and trigger from a centre line (y, z in small-cell units)
def catmull(pts, steps=24):
    out = []; P = [pts[0]] + pts + [pts[-1]]
    for i in range(1, len(P)-2):
        p0, p1, p2, p3 = (Vector(P[j]) for j in (i-1, i, i+1, i+2))
        for s in range(steps):
            t = s/steps
            out.append(0.5*((2*p1) + (-p0+p2)*t + (2*p0-5*p1+4*p2-p3)*t*t + (-p0+3*p1-3*p2+p3)*t**3))
    out.append(Vector(pts[-1])); return out
def rod(pts, rp_of, rx, xs):
    line = catmull(pts); n = len(line); cubes = set()
    for ky in range(int(min(p[0] for p in pts)-8)//2, int(max(p[0] for p in pts)+8)//2+1):
        for kz in range(int(min(p[1] for p in pts)-8)//2, int(max(p[1] for p in pts)+8)//2+1):
            cy, cz = 2*ky+1, 2*kz+2
            best, bi = 1e9, 0
            for i, p in enumerate(line):
                dd = (p.x-cy)**2 + (p.y-cz)**2
                if dd < best: best, bi = dd, i
            rp = rp_of(bi/(n-1))
            for kx in xs:
                if best/rp**2 + ((2*kx+1)/rx)**2 <= 1.0: cubes.add((kx, ky, kz))
    return cubes
gc = rod(GUARD, lambda t: 4.9, 9.0, range(-4, 4))
tc = rod(TRIG, lambda t: 4.4 - 1.2*t, 7.0, range(-3, 3))
frame_cubes = {K(c) for c in data['frame']['cells']}
gc -= frame_cubes; tc -= frame_cubes; tc -= gc
screw = {c for c in data['trigger']['cells'] if c[1] < 150}     # the grip screw sits in the trigger part: kept
data['guard']['cells'] = {u for k in gc for u in units(k)}
data['trigger']['cells'] = screw | {u for k in tc for u in units(k)}
data['guard']['cf'] = {}
data['trigger']['cf'] = {key: col for key, col in data['trigger']['cf'].items() if key[0][1] < 75}
print("guard cubes", len(gc), "trigger cubes", len(tc))

# 3. weathering on the flat sides: carved gouges (cubes really taken out, 1 deep) and bright scratches
rnd = random.Random(2063)
def strokes(cubes, count, lmin, lmax, maxang):
    ys = [k[1] for k in cubes]; zs = [k[2] for k in cubes]; out = []
    for _ in range(count):
        y0 = rnd.uniform(min(ys)+2, max(ys)-2); z0 = rnd.uniform(min(zs)+2, max(zs)-2)
        a = math.radians(rnd.uniform(-maxang, maxang) + (180 if rnd.random() < .5 else 0)); L = rnd.uniform(lmin, lmax)
        bend = rnd.uniform(-0.03, 0.03); pts = []
        for s in range(int(L*2)):
            t = s/2; aa = a + bend*t
            pts.append((round(y0 + math.cos(aa)*t), round(z0 + math.sin(aa)*t)))
        out.append((rnd.choice((1, -1)), list(dict.fromkeys(pts))))
    return out
for n, gouges, scratches in (('barrel', 7, 18), ('frame', 7, 14), ('cylinder', 3, 8)):
    d = data[n]; cubes = {K(c) for c in d['cells']}
    index = collections.defaultdict(list)
    for k in cubes: index[(k[1], k[2])].append(k[0])
    removed = set()
    for sx, pts in strokes(cubes, gouges, 5, 16, 30):
        for (ky, kz) in pts:
            xs = index.get((ky, kz))
            if not xs: continue
            kx = max(xs) if sx > 0 else min(xs)
            if all((kx - sx*i, ky, kz) in cubes for i in range(1, 4)) and (kx, ky, kz+1) in cubes and (kx, ky, kz-1) in cubes:
                removed.add((kx, ky, kz))
    cubes -= removed
    for (kx, ky, kz) in removed:
        for sx in (1, -1):
            lip = ((kx - sx, ky, kz - 1), (sx, 0, 0))
            if (kx, ky, kz - 1) in cubes and (kx, ky, kz - 1) not in removed:
                key = ((kx, ky, kz - 1), (sx, 0, 0))
                if key in d['cf']: d['cf'][key] = tuple(min(0.75, x*1.3) for x in d['cf'][key])
    d['cells'] = {c for c in d['cells'] if K(c) not in removed}
    sc = 0
    for sx, pts in strokes(cubes, scratches, 4, 22, 35):
        for (ky, kz) in pts:
            xs = [x for x in index.get((ky, kz), ()) if (x, ky, kz) in cubes]
            if not xs: continue
            kx = max(xs) if sx > 0 else min(xs)
            key = ((kx, ky, kz), (sx, 0, 0))
            base = d['cf'].get(key) or steel(*key)
            b = 1.18 + 0.14*h01(kx, ky, kz, 3)
            d['cf'][key] = (min(0.7, base[0]*b), min(0.7, base[1]*b), min(0.72, base[2]*b*1.02))
            sc += 1
    for (k, dd), col in list(d['cf'].items()):        # worn top edges, here and there
        if dd == (0, 0, 1) and ((k[0]+1, k[1], k[2]) not in cubes or (k[0]-1, k[1], k[2]) not in cubes) and h01(*k, 5) < 0.55:
            d['cf'][(k, dd)] = tuple(min(0.9, x*1.22) for x in col)
    print(n, "gouge cubes", len(removed), "scratch faces", sc)

# 4. write every part back: greedy rectangles of one colour, one shared new palette
def colour_for(n, k, d):
    col = data[n]['cf'].get((k, d))
    if col: return col
    if n == 'grip':
        others = [data[n]['cf'][(k, e)] for e in DIRS if (k, e) in data[n]['cf']]
        return others[0] if others else (0.33, 0.2, 0.12)
    c = steel(k, d, 11)
    return c if n in ('guard', 'trigger') else tuple(x*0.72 for x in c)    # inside walls of a gouge: grime
cols = {}
def ci(col):
    q = tuple(round(x*255) for x in col)
    if q not in cols: cols[q] = len(cols)
    return cols[q]
built = {}
for n, d in data.items():
    cells = d['cells']; faces = collections.defaultdict(dict)
    for c in cells:
        for dd in DIRS:
            if (c[0]+dd[0], c[1]+dd[1], c[2]+dd[2]) in cells: continue
            ax = [i for i in range(3) if dd[i]][0]; ua, va = [i for i in range(3) if i != ax]
            faces[(dd, c[ax])][(c[ua], c[va])] = ci(colour_for(n, K(c), dd))
    quads = []
    for (dd, s), mask in faces.items():
        ax = [i for i in range(3) if dd[i]][0]; ua, va = [i for i in range(3) if i != ax]
        done = set()
        for (u, w) in sorted(mask, key=lambda p: (p[1], p[0])):
            if (u, w) in done: continue
            cc = mask[(u, w)]; wd = 1
            while mask.get((u+wd, w)) == cc and (u+wd, w) not in done: wd += 1
            ht = 1
            while all(mask.get((u+i, w+ht)) == cc and (u+i, w+ht) not in done for i in range(wd)): ht += 1
            for i in range(wd):
                for j in range(ht): done.add((u+i, w+j))
            plane = s + (1 if dd[ax] > 0 else 0); pts = []
            for du, dv in ((0, 0), (wd, 0), (wd, ht), (0, ht)):
                p = [0, 0, 0]; p[ax] = plane; p[ua] = u+du; p[va] = w+dv
                pts.append(Vector(((p[0]+OFF[0])*V, (p[1]+OFF[1])*V, (p[2]+OFF[2])*V)))
            if (pts[1]-pts[0]).cross(pts[2]-pts[0]).dot(Vector(dd)) < 0: pts.reverse()
            quads.append((pts, cc))
    built[n] = quads
    print(n, "faces", len(quads))
side = 1
while side*side < len(cols): side *= 2
newimg = bpy.data.images.new("meshy_look_revolver_palette_v2", side, side, alpha=False)
px = [0.0]*(side*side*4)
for q, i in cols.items():
    x, y = i % side, i // side; j = (y*side+x)*4
    px[j:j+4] = [q[0]/255, q[1]/255, q[2]/255, 1.0]
newimg.pixels.foreach_set(px)
newimg.pack()
mat = bpy.data.materials['meshy_look_revolver_cubes']
for nd in mat.node_tree.nodes:
    if nd.type == 'TEX_IMAGE': nd.image = newimg; nd.interpolation = 'Closest'
for n, quads in built.items():
    o = obs[n]; old = o.data
    verts, polys, uvs = [], [], []
    for pts, cc in quads:
        b = len(verts); verts += [tuple(p) for p in pts]; polys.append((b, b+1, b+2, b+3))
        x, y = cc % side, cc // side; uvs += [((x+.5)/side, (y+.5)/side)]*4
    me = bpy.data.meshes.new(old.name)
    me.from_pydata(verts, [], polys); me.update()
    uvl = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices: uvl.data[li].uv = uvs[me.loops[li].vertex_index]
    me.materials.append(mat)
    o.data = me; bpy.data.meshes.remove(old)
print("palette colours", len(cols), "size", side)
bpy.ops.wm.save_as_mainfile(filepath=OUT, copy=False)
