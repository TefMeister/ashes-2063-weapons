# Read the greedy-meshed palette model into per-cube faces. Shared by the analysis and build steps.
import bpy, math, collections
from mathutils import Vector
def dir_of(n):
    ax=max(range(3),key=lambda i:abs(n[i])); d=[0,0,0]; d[ax]=1 if n[ax]>0 else -1; return tuple(d)
def read(ob, v, off, img):
    W,H=img.size; px=list(img.pixels); me=ob.data; uv=me.uv_layers.active.data
    faces={}
    for p in me.polygons:
        d=dir_of(p.normal); ax=[i for i in range(3) if d[i]][0]; ua,va=[i for i in range(3) if i!=ax]
        g=[[ (me.vertices[i].co[k])/v-off[k] for k in range(3)] for i in p.vertices]
        plane=round(g[0][ax]); cellax=plane-1 if d[ax]>0 else plane
        u0=round(min(x[ua] for x in g)); u1=round(max(x[ua] for x in g))
        w0=round(min(x[va] for x in g)); w1=round(max(x[va] for x in g))
        us=[uv[l].uv for l in p.loop_indices]; cu=sum(a.x for a in us)/len(us); cv=sum(a.y for a in us)/len(us)
        x=min(W-1,int(cu*W)); y=min(H-1,int(cv*H)); i=(y*W+x)*4
        col=tuple(px[i+k] for k in range(3))
        for a in range(u0,u1):
            for b in range(w0,w1):
                c=[0,0,0]; c[ax]=cellax; c[ua]=a; c[va]=b
                faces[(tuple(c),d)]=col
    return faces
def flood(faces):
    cs=[c for c,_ in faces]; lo=[min(c[i] for c in cs)-1 for i in range(3)]; hi=[max(c[i] for c in cs)+1 for i in range(3)]
    walls=set()
    for (c,d) in faces:
        walls.add((c,d)); walls.add(((c[0]+d[0],c[1]+d[1],c[2]+d[2]),(-d[0],-d[1],-d[2])))
    DIRS=((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))
    start=tuple(lo); air={start}; st=[start]
    while st:
        a=st.pop()
        for d in DIRS:
            b=(a[0]+d[0],a[1]+d[1],a[2]+d[2])
            if b in air or any(b[i]<lo[i] or b[i]>hi[i] for i in range(3)) or (a,d) in walls: continue
            air.add(b); st.append(b)
    cells=set()
    for x in range(lo[0],hi[0]+1):
        for y in range(lo[1],hi[1]+1):
            for z in range(lo[2],hi[2]+1):
                if (x,y,z) not in air: cells.add((x,y,z))
    return cells
