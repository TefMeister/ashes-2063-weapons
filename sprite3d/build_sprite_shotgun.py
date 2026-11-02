"""Sprite-faced shotgun (2026-11-03, dev PC, built with Tefa; Tefa: "can we try idea 1 on the shotgun and see how it
looks in vr", then "can you do step 2 as well amd send it to mega transfer so home pc can put it in the game").

Idea (Tefa, 2026-11-03): weapons that still look like the game's sprites but are 3D, not voxel. Route 1 of four.
Step 1: the gun's shape is cut from the game's own side picture (the pickup sprite GRZPA0, 60 x 21 pixels), each part
given its own thickness, the picture's pixels painted on both sides, sharp. From the side it IS the sprite.
Step 2: the top is painted from the held picture (GRIZA, 190 x 150, the gun seen from behind and above), following its
bright top ridge: the barrel from the muzzle to the body, then the body. Skin (the hands) is skipped; there the side
picture's edge colour stays. The barrel and tube get rounded edges.

Run inside Blender:  exec(open(<this file>).read())  or  blender --python <this file>.
It reads both pictures from the game at run time and never stores them here: the game's pictures are never committed.
Axes as every forge gun (x right, y forward along the barrel, z up), under the empty "sprite_pump_root", so
brutal-doom-3d-guns/tools/gz_forge_export.py exports it; the grip part is "sprite_pump_grip".
"""
import zipfile, math, bpy, bmesh

GAME_PK3 = r"D:/ashes2063vr/Ashes 2063 VR/Resources/Ashes2063Enriched2_23.pk3"
HOME_PK3 = r"C:/NonSteam/Ashes 2063 VR/Resources/Ashes2063Enriched2_23.pk3"
SIDE_SPRITE = "Sprites/Weapons/GRZPA0.png"
HELD_SPRITE = "Graphics/Shotgun/GRIZA.png"
GUN = "sprite_pump"
GUN_LENGTH_M = 1.0                     # the 60-pixel side picture spans about one metre
SOLID_ALPHA = 0.5
ROUND_PARTS = ("barrel", "tube")       # step 2: these get rounded edges
ROUND_WIDTH_PX = 0.45                  # how far the rounding reaches in, in side-picture pixels
ROUND_SEGMENTS = 2

# Each part: (name, which side-picture pixels belong to it, thickness in side-picture pixels). First match wins.
# Read from the 60 x 21 picture: barrel on top (rows <= 6) from column 31, wooden pump rows 7-9 columns 34-51,
# magazine tube under the barrel, receiver columns 12-30, trigger guard row 12 and below, the stock with its pistol grip
# left of column 12 (named "grip": the hand docks there).
PARTS = [
    ("barrel",   lambda x, y: y <= 6 and x >= 31, 1.8),
    ("pump",     lambda x, y: 7 <= y <= 9 and 34 <= x <= 51, 3.4),
    ("tube",     lambda x, y: y >= 7 and x >= 30, 2.0),
    ("receiver", lambda x, y: x >= 12 and y <= 11 and x < 31, 3.0),
    ("guard",    lambda x, y: y >= 12 and x >= 12, 1.0),
    ("grip",     lambda x, y: x < 12, 2.6),
]

# Step 2, the top ridge in the held picture (pixel coordinates read off a gridded close-up, 2026-11-03):
# side-picture column -> held-picture point on the ridge, and how wide the top is there (half, in held pixels).
# Muzzle (column 58) at (97, 48); barrel meets body (column 31) at (101, 63); body's back (column 12) at (122, 108).
RIDGE = [(58, (97.0, 48.0), 4.0), (31, (101.0, 63.0), 6.0), (12, (122.0, 108.0), 12.0)]
SKIN_RED_OVER_GREEN = 0.16             # a pixel this much redder than green is skin or wood under the hands


def picture(name):
    for pk3 in (GAME_PK3, HOME_PK3):
        try:
            data = zipfile.ZipFile(pk3).read(name)
            break
        except (FileNotFoundError, KeyError):
            continue
    path = bpy.app.tempdir + name.rsplit("/", 1)[-1]
    open(path, "wb").write(data)
    img = bpy.data.images.load(path)
    img.pack()
    return img


def sprite_material(name, img):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image, tex.interpolation = img, "Closest"
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.8
    return mat


def ridge_at(col):
    """Where the top ridge of side-picture column `col` sits in the held picture, its direction and half-width."""
    col = min(max(col, RIDGE[-1][0]), RIDGE[0][0])     # the grip end and the muzzle keep the nearest ridge point
    for (c0, p0, w0), (c1, p1, w1) in zip(RIDGE, RIDGE[1:]):
        if c1 <= col <= c0:
            t = (col - c0) / (c1 - c0)
            p = (p0[0] + t * (p1[0] - p0[0]), p0[1] + t * (p1[1] - p0[1]))
            d = (p0[0] - p1[0], p0[1] - p1[1])             # towards the muzzle
            n = math.hypot(*d)
            return p, (d[0] / n, d[1] / n), w0 + t * (w1 - w0)


def build():
    side, held = picture(SIDE_SPRITE), picture(HELD_SPRITE)
    W, H = side.size
    HW, HH = held.size
    spx, hpx = list(side.pixels), list(held.pixels)
    PX = GUN_LENGTH_M / W

    def alpha(x, y):
        return spx[((H - 1 - y) * W + x) * 4 + 3]

    def held_rgba(x, y):
        x, y = int(x), int(y)
        if not (0 <= x < HW and 0 <= y < HH):
            return None
        return hpx[((HH - 1 - y) * HW + x) * 4:((HH - 1 - y) * HW + x) * 4 + 4]

    solid = {(x, y) for y in range(H) for x in range(W) if alpha(x, y) > SOLID_ALPHA}
    owner = {}
    for c in solid:
        for name, test, _ in PARTS:
            if test(*c):
                owner[c] = name
                break
    thick = {n: t for n, _, t in PARTS}
    width = {c: thick[owner[c]] for c in solid}
    m_side, m_top = sprite_material("sprite_side", side), sprite_material("sprite_top", held)

    def uv_side(x, y, full=True):
        if full:
            return [(x / W, 1 - (y + 1) / H), ((x + 1) / W, 1 - (y + 1) / H),
                    ((x + 1) / W, 1 - y / H), (x / W, 1 - y / H)]
        return [((x + .5) / W, 1 - (y + .5) / H)] * 4

    def uv_top(x, s):
        """The held-picture pixel for the top of side column x, across-offset s (-1 gun's right .. +1 gun's left);
        None where it is skin, empty, or off the picture."""
        (px, py), (dx, dy), half = ridge_at(x + 0.5)
        right = (-dy, dx)                               # screen direction of the gun's right side
        hx, hy = px - s * half * right[0], py - s * half * right[1]
        c = held_rgba(hx, hy)
        if c is None or c[3] < SOLID_ALPHA or c[0] - c[1] > SKIN_RED_OVER_GREEN:
            return None
        return [((int(hx) + .5) / HW, 1 - (int(hy) + .5) / HH)] * 4

    root = bpy.data.objects.new(GUN + "_root", None)
    bpy.context.scene.collection.objects.link(root)
    painted = 0
    for name, _, _ in PARTS:
        bm = bmesh.new()
        uvl = bm.loops.layers.uv.new()

        def quad(vs, uvs, mat=0):
            f = bm.faces.new([bm.verts.new(v) for v in vs])
            f.material_index = mat
            for loop, uv in zip(f.loops, uvs):
                loop[uvl].uv = uv

        for (x, y) in [c for c in solid if owner[c] == name]:
            h = width[(x, y)] * PX / 2
            X0, X1, Z0, Z1 = x * PX, (x + 1) * PX, -(y + 1) * PX, -y * PX
            quad([(X0, -h, Z0), (X1, -h, Z0), (X1, -h, Z1), (X0, -h, Z1)], uv_side(x, y))
            quad([(X1, h, Z0), (X0, h, Z0), (X0, h, Z1), (X1, h, Z1)], [uv_side(x, y)[i] for i in (1, 0, 3, 2)])
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                hn = width[n] * PX / 2 if n in solid else 0.0
                if hn >= h:
                    continue
                edge = {(1, 0): [(X1, Z0), (X1, Z1)], (-1, 0): [(X0, Z1), (X0, Z0)],
                        (0, 1): [(X0, Z0), (X1, Z0)], (0, -1): [(X1, Z1), (X0, Z1)]}[(dx, dy)]
                (ax, az), (bx, bz) = edge
                for sgn in (-1, 1):
                    a, b = sgn * hn, sgn * h
                    vs = [(ax, a, az), (bx, a, bz), (bx, b, bz), (ax, b, az)]
                    uv, mat = uv_side(x, y, False), 0
                    if (dx, dy) == (0, -1):          # a top face: paint it from the held picture
                        # model -Y is the gun's right side (looking at the picture, muzzle right, top up)
                        top = uv_top(x, (a + b) / 2 / max(h, 1e-9))
                        if top:
                            uv, mat = top, 1
                            painted += 1
                    quad(vs[::-1] if sgn < 0 else vs, uv, mat)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        me = bpy.data.meshes.new(f"{GUN}_{name}")
        bm.to_mesh(me)
        bm.free()
        me.materials.append(m_side)
        me.materials.append(m_top)
        ob = bpy.data.objects.new(f"{GUN}_{name}", me)
        ob["part"] = name
        ob.parent = root
        # picture frame (x along the gun, -y the gun's right) -> forge axes (y forward, +x the gun's right)
        ob.rotation_euler = (0.0, 0.0, math.pi / 2)
        bpy.context.scene.collection.objects.link(ob)
        if name in ROUND_PARTS:
            bv = ob.modifiers.new("round", "BEVEL")
            bv.width, bv.segments, bv.limit_method = ROUND_WIDTH_PX * PX, ROUND_SEGMENTS, "ANGLE"
    print(f"{GUN}: {len(solid)} side pixels in {len(PARTS)} parts, {painted} top faces painted from the held picture")
    return root


if __name__ == "__main__":
    build()
