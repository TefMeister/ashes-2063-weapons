# Shared helpers for the Ashes 2063 weapon models: scene setup, blocky pixel
# materials, and simple mesh builders (boxes, cylinders, swept tubes).
# Run inside Blender with exec(open(path).read()).
import bpy, bmesh, math
from mathutils import Vector, Matrix, Euler

# ---- settings -------------------------------------------------------------
RENDER_W, RENDER_H = 320, 240      # same as the lantern: low-res, crunchy
FPS = 35                           # one frame = one GZDoom tic (lantern assumption)
BLOCK = 0.003                      # texture pixel size in metres
WEAR_BLOCK = 0.0025                # wear pattern pixel size
BG_COLOR = (0.02, 0.02, 0.022, 1.0)
GRIME_COLOR = (0.03, 0.028, 0.025, 1.0)
RUST_COLOR = (0.22, 0.09, 0.035, 1.0)
SCRATCH_COLOR = (0.62, 0.62, 0.6, 1.0)


def reset_scene():
    bpy.ops.wm.read_homefile(use_empty=True)


def setup_scene(name, frame_end=1):
    sc = bpy.context.scene
    sc.name = name
    try:
        sc.render.engine = 'BLENDER_EEVEE'
    except TypeError:
        pass
    sc.render.resolution_x, sc.render.resolution_y = RENDER_W, RENDER_H
    sc.render.fps = FPS
    sc.render.filter_size = 0.0
    try:
        sc.view_settings.view_transform = 'Standard'   # punchy, retro colours
    except TypeError:
        pass
    sc.frame_start, sc.frame_end = 1, frame_end
    w = bpy.data.worlds.new("W_Dark")
    try:
        w.use_nodes = True
    except Exception:
        pass
    bg = next(n for n in w.node_tree.nodes if n.type == 'BACKGROUND')
    bg.inputs[0].default_value = BG_COLOR
    bg.inputs[1].default_value = 1.0
    sc.world = w
    return sc


def collection(name, parent=None):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    p = parent or bpy.context.scene.collection
    if c.name not in p.children:
        p.children.link(c)
    return c


# ---- materials ------------------------------------------------------------
def _ramp(nt, stops):
    r = nt.nodes.new('ShaderNodeValToRGB')
    r.color_ramp.interpolation = 'CONSTANT'
    els = r.color_ramp.elements
    while len(els) > 1:
        els.remove(els[-1])
    els[0].position = stops[0][0]
    els[0].color = (*stops[0][1], 1.0)
    for pos, col in stops[1:]:
        e = els.new(pos)
        e.color = (*col, 1.0)
    return r


def wear_group():
    ng = bpy.data.node_groups.get("G_PixelWear")
    if ng:
        return ng
    ng = bpy.data.node_groups.new("G_PixelWear", 'ShaderNodeTree')
    ng.interface.new_socket("Color", in_out='INPUT', socket_type='NodeSocketColor')
    ng.interface.new_socket("Amount", in_out='INPUT', socket_type='NodeSocketFloat')
    ng.interface.new_socket("Color", in_out='OUTPUT', socket_type='NodeSocketColor')
    ng.interface.new_socket("Grime", in_out='OUTPUT', socket_type='NodeSocketFloat')
    N, L = ng.nodes, ng.links
    gi, go = N.new('NodeGroupInput'), N.new('NodeGroupOutput')
    tc = N.new('ShaderNodeTexCoord')
    snap = N.new('ShaderNodeVectorMath'); snap.operation = 'SNAP'
    snap.inputs[1].default_value = (WEAR_BLOCK,) * 3
    L.new(tc.outputs['Object'], snap.inputs[0])

    def thresh(src, lo, hi, scale):
        mr = N.new('ShaderNodeMapRange'); mr.interpolation_type = 'STEPPED'
        mr.inputs['From Min'].default_value, mr.inputs['From Max'].default_value = lo, hi
        mr.inputs['Steps'].default_value = 3
        L.new(src, mr.inputs['Value'])
        m = N.new('ShaderNodeMath'); m.operation = 'MULTIPLY'
        L.new(mr.outputs['Result'], m.inputs[0])
        m2 = N.new('ShaderNodeMath'); m2.operation = 'MULTIPLY'
        m2.inputs[1].default_value = scale
        L.new(gi.outputs['Amount'], m2.inputs[0])
        L.new(m2.outputs[0], m.inputs[1])
        return m.outputs[0]

    def mix(fac, a, col):
        mx = N.new('ShaderNodeMix'); mx.data_type = 'RGBA'
        L.new(fac, mx.inputs['Factor'])
        L.new(a, mx.inputs['A'])
        mx.inputs['B'].default_value = col
        return mx.outputs['Result']

    grime_n = N.new('ShaderNodeTexNoise'); grime_n.inputs['Scale'].default_value = 16.0
    grime_n.inputs['Detail'].default_value = 3.0
    L.new(snap.outputs[0], grime_n.inputs['Vector'])
    grime = thresh(grime_n.outputs['Fac'], 0.52, 0.75, 0.65)

    rust_n = N.new('ShaderNodeTexNoise'); rust_n.noise_dimensions = '4D'
    rust_n.inputs['W'].default_value = 11.0; rust_n.inputs['Scale'].default_value = 45.0
    L.new(snap.outputs[0], rust_n.inputs['Vector'])
    rust = thresh(rust_n.outputs['Fac'], 0.64, 0.8, 0.7)

    vor = N.new('ShaderNodeTexVoronoi'); vor.feature = 'DISTANCE_TO_EDGE'
    vor.inputs['Scale'].default_value = 28.0
    L.new(snap.outputs[0], vor.inputs['Vector'])
    edge = N.new('ShaderNodeMath'); edge.operation = 'LESS_THAN'
    edge.inputs[1].default_value = 0.025
    L.new(vor.outputs['Distance'], edge.inputs[0])
    sc_n = N.new('ShaderNodeTexNoise'); sc_n.noise_dimensions = '4D'
    sc_n.inputs['W'].default_value = 5.0; sc_n.inputs['Scale'].default_value = 9.0
    L.new(snap.outputs[0], sc_n.inputs['Vector'])
    patch = N.new('ShaderNodeMath'); patch.operation = 'GREATER_THAN'
    patch.inputs[1].default_value = 0.55
    L.new(sc_n.outputs['Fac'], patch.inputs[0])
    sc_m = N.new('ShaderNodeMath'); sc_m.operation = 'MULTIPLY'
    L.new(edge.outputs[0], sc_m.inputs[0]); L.new(patch.outputs[0], sc_m.inputs[1])
    scratch = thresh(sc_m.outputs[0], 0.0, 1.0, 0.55)

    c = mix(grime, gi.outputs['Color'], GRIME_COLOR)
    c = mix(rust, c, RUST_COLOR)
    c = mix(scratch, c, SCRATCH_COLOR)
    L.new(c, go.inputs['Color'])
    L.new(grime, go.inputs['Grime'])
    return ng


def pixel_mat(name, stops, metal=0.3, rough=0.6, wear=1.0, block=BLOCK,
              paint=None, paint_cover=0.5, paint_scale=22.0, paint_seed=1.0,
              emit=0.0, stripes=None):
    """stops: [(pos, (r,g,b)), ...] picked per texture pixel by white noise.
    paint: second stops list laid over in blotches (worn paint).
    stripes: (axis 0/1/2, period, duty) dark bands, e.g. checkering/serrations."""
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    try:
        m.use_nodes = True
    except Exception:
        pass
    nt = m.node_tree
    nt.nodes.clear()
    N, L = nt.nodes, nt.links
    out = N.new('ShaderNodeOutputMaterial')
    bsdf = N.new('ShaderNodeBsdfPrincipled')
    L.new(bsdf.outputs[0], out.inputs['Surface'])
    tc = N.new('ShaderNodeTexCoord')
    snap = N.new('ShaderNodeVectorMath'); snap.operation = 'SNAP'
    snap.inputs[1].default_value = (block,) * 3
    L.new(tc.outputs['Object'], snap.inputs[0])
    wn = N.new('ShaderNodeTexWhiteNoise'); wn.noise_dimensions = '4D'
    wn.inputs['W'].default_value = paint_seed
    L.new(snap.outputs[0], wn.inputs['Vector'])
    base = _ramp(nt, stops)
    L.new(wn.outputs['Value'], base.inputs['Fac'])
    col = base.outputs['Color']
    if paint:
        pn = N.new('ShaderNodeTexNoise'); pn.noise_dimensions = '4D'
        pn.inputs['W'].default_value = paint_seed * 7.0
        pn.inputs['Scale'].default_value = paint_scale
        pn.inputs['Detail'].default_value = 2.0
        L.new(snap.outputs[0], pn.inputs['Vector'])
        gt = N.new('ShaderNodeMath'); gt.operation = 'GREATER_THAN'
        gt.inputs[1].default_value = 1.0 - paint_cover
        L.new(pn.outputs['Fac'], gt.inputs[0])
        pr = _ramp(nt, paint)
        L.new(wn.outputs['Value'], pr.inputs['Fac'])
        mx = N.new('ShaderNodeMix'); mx.data_type = 'RGBA'
        L.new(gt.outputs[0], mx.inputs['Factor'])
        L.new(col, mx.inputs['A']); L.new(pr.outputs['Color'], mx.inputs['B'])
        col = mx.outputs['Result']
    if stripes:
        axis, period, duty = stripes
        sep = N.new('ShaderNodeSeparateXYZ')
        L.new(snap.outputs[0], sep.inputs[0])
        md = N.new('ShaderNodeMath'); md.operation = 'FLOORED_MODULO'
        md.inputs[1].default_value = period
        L.new(sep.outputs[axis], md.inputs[0])
        lt = N.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'
        lt.inputs[1].default_value = period * duty
        L.new(md.outputs[0], lt.inputs[0])
        mx = N.new('ShaderNodeMix'); mx.data_type = 'RGBA'
        mx.inputs['Factor'].default_value = 0.0
        L.new(lt.outputs[0], mx.inputs['Factor'])
        L.new(col, mx.inputs['A']); mx.inputs['B'].default_value = (0.012, 0.012, 0.012, 1)
        col = mx.outputs['Result']
    if wear > 0:
        g = N.new('ShaderNodeGroup'); g.node_tree = wear_group()
        g.inputs['Amount'].default_value = wear
        L.new(col, g.inputs['Color'])
        col = g.outputs['Color']
        r = N.new('ShaderNodeMath'); r.operation = 'ADD'
        r.inputs[1].default_value = rough
        rm = N.new('ShaderNodeMath'); rm.operation = 'MULTIPLY'
        rm.inputs[1].default_value = 0.3
        L.new(g.outputs['Grime'], rm.inputs[0]); L.new(rm.outputs[0], r.inputs[0])
        L.new(r.outputs[0], bsdf.inputs['Roughness'])
    else:
        bsdf.inputs['Roughness'].default_value = rough
    L.new(col, bsdf.inputs['Base Color'])
    bsdf.inputs['Metallic'].default_value = metal
    if emit > 0:
        L.new(col, bsdf.inputs['Emission Color'])
        bsdf.inputs['Emission Strength'].default_value = emit
    m.diffuse_color = (*stops[len(stops) // 2][1], 1.0)
    return m


# ---- mesh building --------------------------------------------------------
def _faces_of(verts):
    return {f for v in verts for f in v.link_faces}


class Part:
    """Collects primitives into one mesh; each primitive gets a material slot index."""

    def __init__(self):
        self.bm = bmesh.new()

    def _place(self, verts, center, rot, mat):
        M = Matrix.Translation(Vector(center)) @ Euler(rot).to_matrix().to_4x4()
        bmesh.ops.transform(self.bm, matrix=M, verts=verts)
        for f in _faces_of(verts):
            f.material_index = mat

    def box(self, size, center, mat=0, rot=(0, 0, 0), top_scale=None):
        verts = bmesh.ops.create_cube(self.bm, size=1.0)['verts']
        for v in verts:
            v.co.x *= size[0]; v.co.y *= size[1]; v.co.z *= size[2]
            if top_scale and v.co.z > 0:
                v.co.x *= top_scale[0]; v.co.y *= top_scale[1]
        self._place(verts, center, rot, mat)

    def cyl(self, r, depth, center, mat=0, rot=(0, 0, 0), segs=8, r2=None):
        verts = bmesh.ops.create_cone(self.bm, cap_ends=True, cap_tris=False, segments=segs,
                                      radius1=r, radius2=r if r2 is None else r2, depth=depth)['verts']
        self._place(verts, center, rot, mat)

    def tube(self, points, radius, mat=0, sides=6, caps=True, twist=0.0, flat=1.0, squash='b'):
        """Sweep a polygon along points. radius may be a list (taper).
        flat squashes the cross-section along the frame's second axis
        (squash='b') or its first axis (squash='n')."""
        pts = [Vector(p) for p in points]
        radii = radius if isinstance(radius, (list, tuple)) else [radius] * len(pts)
        tangents = []
        for i in range(len(pts)):
            a = pts[max(i - 1, 0)]; b = pts[min(i + 1, len(pts) - 1)]
            tangents.append((b - a).normalized())
        ref = Vector((0, 0, 1)) if abs(tangents[0].z) < 0.9 else Vector((1, 0, 0))
        n = tangents[0].cross(ref).normalized()
        rings = []
        for i, p in enumerate(pts):
            t = tangents[i]
            n = (n - t * n.dot(t)).normalized()
            bnorm = t.cross(n).normalized()
            fl = flat[i] if isinstance(flat, (list, tuple)) else flat
            ring = []
            for s in range(sides):
                ang = twist + 2 * math.pi * s / sides
                fn, fb = (fl, 1.0) if squash == 'n' else (1.0, fl)
                off = n * math.cos(ang) * radii[i] * fn + bnorm * math.sin(ang) * radii[i] * fb
                ring.append(self.bm.verts.new(p + off))
            rings.append(ring)
        faces = []
        for a, b in zip(rings, rings[1:]):
            for s in range(sides):
                faces.append(self.bm.faces.new((a[s], a[(s + 1) % sides], b[(s + 1) % sides], b[s])))
        if caps:
            faces.append(self.bm.faces.new(list(reversed(rings[0]))))
            faces.append(self.bm.faces.new(rings[-1]))
        for f in faces:
            f.material_index = mat

    def build(self, name, mats, pivot=(0, 0, 0), parent=None, coll=None):
        bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces)
        bmesh.ops.translate(self.bm, vec=-Vector(pivot), verts=self.bm.verts)
        me = bpy.data.meshes.new(name)
        self.bm.to_mesh(me)
        self.bm.free()
        for p in me.polygons:
            p.use_smooth = False
        ob = bpy.data.objects.new(name, me)
        for m in mats:
            ob.data.materials.append(m)
        (coll or bpy.context.scene.collection).objects.link(ob)
        if parent:
            ob.parent = parent
        ob.location = pivot
        return ob


def empty(name, loc=(0, 0, 0), parent=None, coll=None, size=0.03):
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = size
    (coll or bpy.context.scene.collection).objects.link(e)
    e.parent = parent
    e.location = loc
    return e


def studio(target=(0, 0, 0), dist=0.5, coll=None, name="Cam"):
    """Model-viewing camera and lights."""
    c = coll or bpy.context.scene.collection
    key = bpy.data.lights.new("KeyLight", 'SUN'); key.energy = 3.0
    ko = bpy.data.objects.new("KeyLight", key); c.objects.link(ko)
    ko.rotation_euler = (math.radians(50), math.radians(10), math.radians(35))
    fill = bpy.data.lights.new("FillLight", 'SUN'); fill.energy = 0.8
    fo = bpy.data.objects.new("FillLight", fill); c.objects.link(fo)
    fo.rotation_euler = (math.radians(70), 0, math.radians(-140))
    cam = bpy.data.cameras.new(name); cam.lens = 50
    co = bpy.data.objects.new(name, cam); c.objects.link(co)
    t = Vector(target)
    co.location = t + Vector((dist * 0.85, -dist * 0.6, dist * 0.35))
    co.rotation_euler = (t - co.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = co
    return co


def key_constant(obj):
    ad = obj.animation_data
    if not ad or not ad.action:
        return
    act = ad.action
    curves = []
    if hasattr(act, "fcurves"):
        curves = list(act.fcurves)
    if not curves and hasattr(act, "layers"):
        for layer in act.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    curves += list(bag.fcurves)
    for fc in curves:
        for k in fc.keyframe_points:
            k.interpolation = 'CONSTANT'


def look_through(cam_obj):
    for area in bpy.context.screen.areas if bpy.context.screen else []:
        if area.type == 'VIEW_3D':
            sp = area.spaces.active
            sp.shading.type = 'MATERIAL'
            sp.region_3d.view_perspective = 'CAMERA'
