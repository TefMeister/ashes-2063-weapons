"""Sprite-faced shotgun, step 1 (2026-11-03, dev PC, built with Tefa in Blender).

Idea (Tefa, 2026-11-03): weapons that still look like the game's sprites but are 3D, not voxel.
Route 1 of four: the gun's shape is cut from the game's own side picture (the pickup sprite GRZPA0,
60 x 21 pixels), each part given its own thickness, and the picture's pixels painted on both sides,
sharp (Closest filtering). From the side it IS the sprite; turned, it has depth.

Run inside Blender (MCP execute or Text editor). It reads the picture from the game at run time and
never stores it here: the game's pictures are never committed.

Step 2 (not done): paint the top and back from the held picture (GRIZA), seen from where the gun is
held; round the barrel and tube. Step 3: export to md3 for GZDoom and wear it.
"""
import zipfile, io, bpy, bmesh

GAME_PK3 = r"D:/ashes2063vr/Ashes 2063 VR/Resources/Ashes2063Enriched2_23.pk3"
SIDE_SPRITE = "Sprites/Weapons/GRZPA0.png"
GUN_LENGTH_M = 1.0                     # the 60-pixel picture spans about one metre
SOLID_ALPHA = 0.5

# Each part: (name, which pixels belong to it, thickness in sprite pixels). First match wins.
# Pixel rows/columns read from the 60 x 21 picture: barrel on top (rows <= 6), wooden pump rows 7-9
# from column 34 to 51, magazine tube under the barrel, receiver columns 12-30, trigger guard row 12+,
# stock left of column 12.
PARTS = [
    ("barrel",   lambda x, y: y <= 6 and x >= 31, 1.8),
    ("pump",     lambda x, y: 7 <= y <= 9 and 34 <= x <= 51, 3.4),
    ("tube",     lambda x, y: y >= 7 and x >= 30, 2.0),
    ("receiver", lambda x, y: x >= 12 and y <= 11 and x < 31, 3.0),
    ("guard",    lambda x, y: y >= 12 and x >= 12, 1.0),
    ("stock",    lambda x, y: x < 12, 2.6),
]


def load_side_picture():
    data = zipfile.ZipFile(GAME_PK3).read(SIDE_SPRITE)
    path = bpy.app.tempdir + "GRZPA0.png"
    open(path, "wb").write(data)
    img = bpy.data.images.load(path)
    img.pack()
    return img


def build(img):
    W, H = img.size
    px = list(img.pixels)
    PX = GUN_LENGTH_M / W

    def alpha(x, y):
        return px[((H - 1 - y) * W + x) * 4 + 3]

    solid = {(x, y) for y in range(H) for x in range(W) if alpha(x, y) > SOLID_ALPHA}
    owner = {}
    for c in solid:
        for name, test, _ in PARTS:
            if test(*c):
                owner[c] = name
                break
    thick = {n: t for n, _, t in PARTS}
    width = {c: thick[owner[c]] for c in solid}

    mat = bpy.data.materials.new("sprite_side")
    mat.use_nodes = True
    nt = mat.node_tree
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image, tex.interpolation = img, "Closest"
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.8

    def uvpix(x, y, full=True):
        if full:
            return [(x / W, 1 - (y + 1) / H), ((x + 1) / W, 1 - (y + 1) / H),
                    ((x + 1) / W, 1 - y / H), (x / W, 1 - y / H)]
        u, v = (x + .5) / W, 1 - (y + .5) / H
        return [(u, v)] * 4

    for name, _, _ in PARTS:
        bm = bmesh.new()
        uvl = bm.loops.layers.uv.new()

        def quad(vs, uvs):
            f = bm.faces.new([bm.verts.new(v) for v in vs])
            for loop, uv in zip(f.loops, uvs):
                loop[uvl].uv = uv

        for (x, y) in [c for c in solid if owner[c] == name]:
            h = width[(x, y)] * PX / 2
            X0, X1, Z0, Z1 = x * PX, (x + 1) * PX, -(y + 1) * PX, -y * PX
            quad([(X0, -h, Z0), (X1, -h, Z0), (X1, -h, Z1), (X0, -h, Z1)], uvpix(x, y))
            quad([(X1, h, Z0), (X0, h, Z0), (X0, h, Z1), (X1, h, Z1)],
                 [uvpix(x, y)[i] for i in (1, 0, 3, 2)])
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                hn = width[n] * PX / 2 if n in solid else 0.0
                if hn >= h:
                    continue
                edge = {(1, 0): [(X1, Z0), (X1, Z1)], (-1, 0): [(X0, Z1), (X0, Z0)],
                        (0, 1): [(X0, Z0), (X1, Z0)], (0, -1): [(X1, Z1), (X0, Z1)]}[(dx, dy)]
                (ax, az), (bx, bz) = edge
                for s in (-1, 1):
                    a, b = s * hn, s * h
                    vs = [(ax, a, az), (bx, a, bz), (bx, b, bz), (ax, b, az)]
                    quad(vs[::-1] if s < 0 else vs, uvpix(x, y, False))
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        me = bpy.data.meshes.new("sg_" + name)
        bm.to_mesh(me)
        bm.free()
        me.materials.append(mat)
        ob = bpy.data.objects.new("sg_" + name, me)
        ob["part"] = name
        bpy.context.scene.collection.objects.link(ob)


if __name__ == "__main__":
    build(load_side_picture())
