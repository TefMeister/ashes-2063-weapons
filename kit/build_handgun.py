# Ashes 2063 handgun model. +Y is the muzzle, +Z up, +X the gun's right side.
# Moving parts are separate objects so the shoot/reload files can animate them:
# HG_Slide, HG_Hammer, HG_Trigger, HG_Mag, HG_MuzzleFlash, HG_FlashLight, HG_Casing.
import math
exec(open(r"C:\Users\TD3KX\github-backups\ashes-2063-weapons\kit\pixel_kit.py").read())

OUT = r"C:\Users\TD3KX\github-backups\ashes-2063-weapons\handgun\Ashes_2063_EP1_handgun_model.blend"

# ---- dimensions (metres) --------------------------------------------------
SLIDE_Y = (-0.078, 0.125)
SLIDE_Z = (0.030, 0.063)
SLIDE_W = 0.031
FRAME_Z = (0.010, 0.030)
FRAME_W = 0.029
GRIP_TILT = math.radians(-17)      # bottom of the grip leans back
GRIP_TOP = (0.0, -0.040, 0.012)
GRIP_SIZE = (0.030, 0.050, 0.105)
MAG_SIZE = (0.022, 0.036, 0.104)
BORE_R = 0.0052
BARREL_R = 0.0090
CASING = (0.0046, 0.018)            # radius, length

reset_scene()
setup_scene("Handgun_Model")
C = collection("HANDGUN")

# ---- materials -------------------------------------------------------------
STEEL = [(0.0, (0.30, 0.30, 0.31)), (0.35, (0.42, 0.42, 0.43)), (0.75, (0.55, 0.55, 0.56))]
RED = [(0.0, (0.30, 0.02, 0.02)), (0.4, (0.45, 0.04, 0.03)), (0.8, (0.58, 0.08, 0.05))]
m_slide = pixel_mat("HG_SlideSteel", STEEL, metal=0.8, rough=0.45, paint=RED,
                    paint_cover=0.5, paint_scale=24, paint_seed=2.0)
m_frame = pixel_mat("HG_FrameGunmetal",
                    [(0.0, (0.07, 0.07, 0.08)), (0.4, (0.12, 0.12, 0.13)), (0.8, (0.18, 0.18, 0.19))],
                    metal=0.7, rough=0.5, paint=RED, paint_cover=0.45, paint_scale=22, paint_seed=3.0)
m_dark = pixel_mat("HG_DarkSteel", [(0.0, (0.02, 0.02, 0.02)), (0.5, (0.05, 0.05, 0.055))],
                   metal=0.6, rough=0.6, wear=0.3)
m_rubber = pixel_mat("HG_GripRubber", [(0.0, (0.03, 0.03, 0.03)), (0.5, (0.07, 0.07, 0.07)),
                                        (0.85, (0.13, 0.12, 0.12))],
                     metal=0.0, rough=0.9, wear=0.6, stripes=(2, 0.009, 0.34))
m_brass = pixel_mat("HG_Brass", [(0.0, (0.45, 0.30, 0.06)), (0.5, (0.70, 0.52, 0.12)),
                                  (0.85, (0.90, 0.75, 0.30))], metal=1.0, rough=0.35, wear=0.25)
m_chrome = pixel_mat("HG_BrightSteel", [(0.0, (0.55, 0.55, 0.56)), (0.5, (0.75, 0.75, 0.76))],
                     metal=1.0, rough=0.3, wear=0.5)
m_flash = pixel_mat("HG_Flash", [(0.0, (0.9, 0.08, 0.0)), (0.35, (1.0, 0.35, 0.02)),
                                  (0.7, (1.0, 0.75, 0.2)), (0.92, (1.0, 1.0, 0.8))],
                    metal=0.0, rough=1.0, wear=0.0, emit=1.6, block=0.005)

root = empty("HG_Root", coll=C, size=0.05)

# ---- frame, grip, trigger guard (static) ----------------------------------
p = Part()
fy0, fy1 = SLIDE_Y[0] + 0.004, SLIDE_Y[1] - 0.012
p.box((FRAME_W, fy1 - fy0, FRAME_Z[1] - FRAME_Z[0]), (0, (fy0 + fy1) / 2, sum(FRAME_Z) / 2), 0)
# accessory rail slots under the dust cover
for i in range(3):
    p.box((FRAME_W + 0.001, 0.004, 0.004), (0, 0.078 + i * 0.011, FRAME_Z[0] + 0.001), 2)
# beavertail over the web of the hand
p.box((0.024, 0.022, 0.010), (0, SLIDE_Y[0] - 0.006, 0.022), 0, rot=(math.radians(-12), 0, 0))
# grip core (tilted), with the magazine well open at the bottom
gx, gy, gz = GRIP_SIZE
gc = Vector(GRIP_TOP) + Euler((GRIP_TILT, 0, 0)).to_matrix() @ Vector((0, 0, -gz / 2))
p.box((gx - 0.004, gy, gz), gc, 0, rot=(GRIP_TILT, 0, 0))
# grip panels (rubber, checkered) and a front strap
for sx in (1, -1):
    pc = Vector(GRIP_TOP) + Euler((GRIP_TILT, 0, 0)).to_matrix() @ Vector((sx * (gx / 2 - 0.001), -0.002, -gz / 2 - 0.004))
    p.box((0.004, gy - 0.010, gz - 0.018), pc, 1, rot=(GRIP_TILT, 0, 0))
    # grip screw
    sc_ = Vector(GRIP_TOP) + Euler((GRIP_TILT, 0, 0)).to_matrix() @ Vector((sx * (gx / 2 + 0.001), 0.0, -0.022))
    p.cyl(0.003, 0.003, sc_, 4, rot=(0, math.pi / 2, 0), segs=6)
# trigger guard: a bent flat band
tg = [(0, 0.052, FRAME_Z[0] + 0.002), (0, 0.056, -0.004), (0, 0.050, -0.020), (0, 0.034, -0.025),
      (0, 0.012, -0.024), (0, -0.002, -0.014)]
p.tube(tg, 0.0045, 0, sides=4, twist=math.pi / 4, flat=[1.8] * len(tg))
# slide stop and safety levers (left side)
p.box((0.003, 0.018, 0.005), (-FRAME_W / 2 - 0.0015, 0.030, 0.027), 2)
p.box((0.003, 0.010, 0.007), (-FRAME_W / 2 - 0.0015, -0.062, 0.033), 2)
frame = p.build("HG_Frame", [m_frame, m_rubber, m_dark, m_chrome, m_chrome], parent=root, coll=C)

# ---- barrel (static; the slide moves over it) ------------------------------
p = Part()
p.cyl(BARREL_R, 0.016, (0, SLIDE_Y[1] - 0.004, 0.046), 0, rot=(math.pi / 2, 0, 0), segs=8)
p.cyl(BORE_R, 0.0162, (0, SLIDE_Y[1] - 0.0038, 0.046), 1, rot=(math.pi / 2, 0, 0), segs=8)
p.build("HG_Barrel", [m_chrome, m_dark], parent=root, coll=C)

# ---- slide -----------------------------------------------------------------
p = Part()
sy0, sy1 = SLIDE_Y
sz0, sz1 = SLIDE_Z
p.box((SLIDE_W, sy1 - sy0, sz1 - sz0), (0, (sy0 + sy1) / 2, (sz0 + sz1) / 2), 0, top_scale=(0.82, 1.0))
p.box((0.012, sy1 - sy0 - 0.02, 0.004), (0, (sy0 + sy1) / 2, sz1 + 0.0015), 0)        # top rib
# rear serrations, both sides
for i in range(7):
    y = sy0 + 0.008 + i * 0.0065
    for sx in (1, -1):
        p.box((0.0012, 0.0028, 0.022), (sx * (SLIDE_W / 2 - 0.0002), y, (sz0 + sz1) / 2), 1)
# ejection port, right side
p.box((0.002, 0.034, 0.013), (SLIDE_W / 2 - 0.0005, 0.040, 0.052), 1)
# front sight post; rear sight with a notch
p.box((0.004, 0.009, 0.007), (0, sy1 - 0.010, sz1 + 0.006), 1)
p.box((0.004, 0.001, 0.0015), (0, sy1 - 0.0145, sz1 + 0.0085), 2)
for sx in (1, -1):
    p.box((0.007, 0.009, 0.008), (sx * 0.0065, sy0 + 0.010, sz1 + 0.006), 1)
    p.box((0.0015, 0.001, 0.0015), (sx * 0.0045, sy0 + 0.0145, sz1 + 0.0085), 2)
# muzzle bushing ring
p.box((SLIDE_W - 0.004, 0.004, sz1 - sz0 - 0.004), (0, sy1 + 0.0005, (sz0 + sz1) / 2), 1)
slide = p.build("HG_Slide", [m_slide, m_dark, m_brass], pivot=(0, 0.0, 0.046), parent=root, coll=C)

# ---- hammer: round ring hammer at the back ---------------------------------
p = Part()
hp = (0, sy0 - 0.003, 0.040)
ring = [(0, sy0 - 0.004 - 0.007 * math.sin(a), 0.056 + 0.007 * math.cos(a))
        for a in [i * math.pi * 2 / 8 for i in range(9)]]
p.tube(ring, 0.0022, 0, sides=4, caps=False, twist=math.pi / 4)
p.box((0.005, 0.005, 0.012), (0, sy0 - 0.004, 0.045), 0)
p.build("HG_Hammer", [m_chrome], pivot=hp, parent=root, coll=C)

# ---- trigger -----------------------------------------------------------------
p = Part()
p.tube([(0, 0.030, 0.010), (0, 0.031, 0.0), (0, 0.027, -0.010), (0, 0.021, -0.014)],
       0.0028, 0, sides=4, twist=math.pi / 4, flat=[1.6] * 4)
p.build("HG_Trigger", [m_chrome], pivot=(0, 0.030, 0.010), parent=root, coll=C)

# ---- magazine: origin at its top so it slides out along the grip axis ------
p = Part()
mx, my, mz = MAG_SIZE
mtop = Vector(GRIP_TOP) + Euler((GRIP_TILT, 0, 0)).to_matrix() @ Vector((0, 0.004, -0.004))
R = Euler((GRIP_TILT, 0, 0)).to_matrix()


def at(v):
    return mtop + R @ Vector(v)


p.box((mx, my, mz), at((0, 0, -mz / 2)), 0, rot=(GRIP_TILT, 0, 0))
p.box((0.003, 0.010, mz * 0.7), at((mx / 2 + 0.0002, -0.006, -mz / 2 - 0.004)), 2, rot=(GRIP_TILT, 0, 0))
p.box((GRIP_SIZE[0] + 0.002, GRIP_SIZE[1] + 0.004, 0.009), at((0, -0.002, -mz - 0.004)), 1,
      rot=(GRIP_TILT, 0, 0))
# two staggered rounds peeking out of the feed lips
for i, (sx, dz) in enumerate(((0.004, 0.004), (-0.004, -0.004))):
    c = at((sx, 0.0, dz))
    p.cyl(0.0046, 0.020, c, 3, rot=(-math.pi / 2 + GRIP_TILT, 0, 0), segs=6)
    tip = at((sx, 0.014, dz))
    p.cyl(0.0046, 0.009, tip, 3, rot=(-math.pi / 2 + GRIP_TILT, 0, 0), segs=6, r2=0.0018)
mag = p.build("HG_Mag", [m_frame, m_dark, m_dark, m_brass], pivot=tuple(mtop), parent=root, coll=C)

# ---- effects: muzzle flash, its light, the spent casing --------------------
FX = collection("HANDGUN_FX", C)
p = Part()
fc = Vector((0, SLIDE_Y[1] + 0.030, 0.046))
ball = bmesh.ops.create_uvsphere(p.bm, u_segments=7, v_segments=5, radius=0.024)["verts"]
p._place(ball, fc + Vector((0, 0.012, 0)), (0, 0, 0), 0)
for i in range(6):
    a = i * math.pi / 3 + 0.3
    d = Vector((math.cos(a), 0, math.sin(a)))
    p.tube([fc + Vector((0, -0.015, 0)), fc + d * 0.028 + Vector((0, 0.004, 0)), fc + d * 0.045 + Vector((0, 0.012, 0))],
           [0.010, 0.007, 0.002], 0, sides=4)
p.tube([fc, fc + Vector((0, 0.055, 0))], [0.012, 0.002], 0, sides=5)
flash = p.build("HG_MuzzleFlash", [m_flash], pivot=tuple(fc), parent=root, coll=FX)
fl = bpy.data.lights.new("HG_FlashLight", 'POINT'); fl.energy = 4.0; fl.color = (1.0, 0.55, 0.2)
fl.shadow_soft_size = 0.02
flo = bpy.data.objects.new("HG_FlashLight", fl); FX.objects.link(flo)
flo.parent = root; flo.location = fc
flash.hide_viewport = flash.hide_render = True
flo.hide_viewport = flo.hide_render = True

p = Part()
p.cyl(CASING[0], CASING[1], (0, 0, 0), 0, rot=(math.pi / 2, 0, 0), segs=6)
p.cyl(CASING[0] * 0.6, CASING[1] + 0.0004, (0, 0, 0), 1, rot=(math.pi / 2, 0, 0), segs=6)
casing = p.build("HG_Casing", [m_brass, m_dark], pivot=(0, 0, 0), parent=root, coll=FX)
casing.location = (0.012, 0.040, 0.052)
casing.hide_viewport = casing.hide_render = True

studio(target=(0, 0.02, 0.0), dist=0.55, name="HG_ModelCam")
look_through(bpy.context.scene.camera)
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("saved", OUT)
