# Ashes 2063 .45 revolver model. +Y is the muzzle, +Z up, +X the gun's right side.
# Moving parts are separate objects so the shoot/reload files can animate them:
# RV_Crane (swings out left) > RV_Cylinder (turns) > RV_Ejector, RV_Casings, RV_Rounds;
# RV_Hammer, RV_Trigger, RV_MuzzleFlash, RV_FlashLight, RV_Speedloader.
import math
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\pixel_kit.py").read())
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\revolver_settings.py").read())

OUT = MODEL
BARREL_Y = (0.032, 0.140)
BARREL_R = 0.0095
BORE_R = 0.0045
GRIP_TOP = (0.0, -0.036, 0.002)
GRIP_SIZE = (0.030, 0.042, 0.095)

reset_scene()
setup_scene("Revolver_Model")
C = collection("REVOLVER")

# ---- materials -------------------------------------------------------------
m_steel = pixel_mat("RV_Stainless", [(0.0, (0.48, 0.48, 0.50)), (0.35, (0.64, 0.64, 0.66)),
                                     (0.75, (0.82, 0.82, 0.84))], metal=0.35, rough=0.4, wear=0.35)
m_dark = pixel_mat("RV_DarkSteel", [(0.0, (0.02, 0.02, 0.02)), (0.5, (0.05, 0.05, 0.055))],
                   metal=0.6, rough=0.6, wear=0.3)
m_rubber = pixel_mat("RV_GripRubber", [(0.0, (0.03, 0.03, 0.03)), (0.5, (0.07, 0.07, 0.07)),
                                        (0.85, (0.13, 0.12, 0.12))],
                     metal=0.0, rough=0.9, wear=0.6, stripes=(2, 0.009, 0.34))
m_red = pixel_mat("RV_SightRed", [(0.0, (0.6, 0.02, 0.02)), (0.5, (0.9, 0.05, 0.03))],
                  metal=0.0, rough=0.5, wear=0.0, emit=0.6)
m_brass = pixel_mat("RV_Brass", [(0.0, (0.45, 0.30, 0.06)), (0.5, (0.70, 0.52, 0.12)),
                                  (0.85, (0.90, 0.75, 0.30))], metal=1.0, rough=0.35, wear=0.25)
m_primer = pixel_mat("RV_Primer", [(0.0, (0.75, 0.40, 0.15)), (0.5, (0.90, 0.55, 0.25))],
                     metal=1.0, rough=0.4, wear=0.0)
m_lead = pixel_mat("RV_BulletLead", [(0.0, (0.25, 0.25, 0.27)), (0.5, (0.38, 0.38, 0.40))],
                   metal=0.5, rough=0.6, wear=0.2)
m_flash = pixel_mat("RV_Flash", [(0.0, (0.9, 0.08, 0.0)), (0.35, (1.0, 0.35, 0.02)),
                                  (0.7, (1.0, 0.75, 0.2)), (0.92, (1.0, 1.0, 0.8))],
                    metal=0.0, rough=1.0, wear=0.0, emit=1.6, block=0.005)

root = empty("RV_Root", coll=C, size=0.05)
X90 = (math.pi / 2, 0, 0)


def child_of(ob, pivot, parent_pivot):
    """Part.build places the pivot in the parent's space; correct it for a moved parent."""
    ob.location = Vector(pivot) - Vector(parent_pivot)
    return ob


def chamber_xz(k, r=CHAMBER_R):
    a = math.pi / 2 + k * math.pi / 3
    return r * math.cos(a), r * math.sin(a)


# ---- frame, barrel, grip, trigger guard (static) ---------------------------
p = Part()
p.box((0.030, 0.064, 0.010), (0, 0.0, 0.001), 0)                    # under the cylinder
p.box((0.024, 0.062, 0.010), (0, 0.0, CYL_Z + CYL_R + 0.005), 0)   # top strap
p.box((0.034, 0.010, 0.064), (0, -0.027, 0.027), 0)                 # recoil shield
p.box((0.028, 0.007, 0.046), (0, 0.0285, 0.035), 0)                 # front of the frame
p.box((0.003, 0.012, 0.007), (-0.0175, -0.034, 0.036), 2)          # cylinder release latch
for sx in (1, -1):                                                  # side plate screws
    p.cyl(0.0025, 0.002, (sx * 0.0155, -0.014, -0.001), 3, rot=(0, math.pi / 2, 0), segs=6)
# barrel, full underlug and vented rib
by0, by1 = BARREL_Y
bl, bc = by1 - by0, (by0 + by1) / 2
p.cyl(BARREL_R, bl, (0, bc, BORE_Z), 0, rot=X90, segs=8)
p.cyl(BORE_R, bl + 0.0004, (0, bc, BORE_Z), 2, rot=X90, segs=8)
p.box((0.016, bl - 0.004, 0.020), (0, bc - 0.002, CYL_Z - 0.004), 0)
p.box((0.010, bl, 0.007), (0, bc, BORE_Z + 0.0115), 0)
for i in range(5):                                                  # vent slots
    p.box((0.0106, 0.008, 0.003), (0, by0 + 0.014 + i * 0.019, BORE_Z + 0.011), 2)
p.box((0.004, 0.012, 0.009), (0, by1 - 0.010, BORE_Z + 0.018), 0)   # front sight ramp
p.box((0.0046, 0.003, 0.004), (0, by1 - 0.011, BORE_Z + 0.020), 1)  # red insert
for sx in (1, -1):                                                  # rear sight with a notch
    p.box((0.006, 0.008, 0.006), (sx * 0.005, -0.022, CYL_Z + CYL_R + 0.013), 2)
# grip (tilted rubber, finger grooves on the front)
t = math.radians(GRIP_TILT_DEG)
R = Euler((t, 0, 0)).to_matrix()
gx, gy, gz = GRIP_SIZE
p.box((gx, gy, gz), Vector(GRIP_TOP) + R @ Vector((0, 0, -gz / 2)), 4, rot=(t, 0, 0))
for i in range(3):
    p.box((gx - 0.006, 0.006, 0.010), Vector(GRIP_TOP) + R @ Vector((0, gy / 2 + 0.001, -0.022 - i * 0.022)),
          2, rot=(t, 0, 0))
p.box((gx + 0.002, gy + 0.002, 0.006), Vector(GRIP_TOP) + R @ Vector((0, 0, -gz)), 2, rot=(t, 0, 0))
tg = [(0, 0.022, -0.003), (0, 0.024, -0.017), (0, 0.015, -0.029), (0, -0.002, -0.029),
      (0, -0.012, -0.020), (0, -0.016, -0.006)]
p.tube(tg, 0.0045, 0, sides=4, twist=math.pi / 4, flat=[1.8] * len(tg))
p.build("RV_Frame", [m_steel, m_red, m_dark, m_steel, m_rubber], parent=root, coll=C)

# ---- hammer ------------------------------------------------------------------
HAMMER_PIVOT = (0, -0.030, 0.030)
p = Part()
p.box((0.008, 0.010, 0.024), (0, -0.036, 0.042), 0)
p.box((0.010, 0.014, 0.006), (0, -0.045, 0.055), 1, rot=(math.radians(-20), 0, 0))
p.build("RV_Hammer", [m_steel, m_dark], pivot=HAMMER_PIVOT, parent=root, coll=C)

# ---- trigger -----------------------------------------------------------------
p = Part()
p.tube([(0, 0.010, 0.004), (0, 0.011, -0.008), (0, 0.007, -0.018), (0, 0.001, -0.022)],
       0.0028, 0, sides=4, twist=math.pi / 4, flat=[1.6] * 4)
p.build("RV_Trigger", [m_steel], pivot=(0, 0.010, 0.004), parent=root, coll=C)

# ---- crane (hinge arm) -------------------------------------------------------
cy_front = CYL_L / 2
p = Part()
cp = Vector(CRANE_PIVOT)
arm = [cp, Vector((0, cy_front + 0.002, CYL_Z))]
p.tube(arm, 0.004, 0, sides=4, twist=math.pi / 4, flat=0.5, squash='n')
p.cyl(0.004, 0.012, cp, 0, rot=X90, segs=6)
crane = p.build("RV_Crane", [m_steel], pivot=CRANE_PIVOT, parent=root, coll=C)

# ---- cylinder: turns on its own axis, child of the crane --------------------
CYL_PIVOT = (0, 0, CYL_Z)
p = Part()
p.cyl(CYL_R, CYL_L, (0, 0, CYL_Z), 0, rot=X90, segs=12)
for k in range(6):
    cx, cz = chamber_xz(k)
    p.cyl(CASE_R + 0.0004, CYL_L + 0.0006, (cx, 0, CYL_Z + cz), 1, rot=X90, segs=8)   # chamber holes
    fx, fz = chamber_xz(k + 0.5, CYL_R)                                                # flutes
    p.box((0.004, CYL_L * 0.55, 0.004), (fx, 0.002, CYL_Z + fz), 1,
          rot=(0, -(math.pi / 2 + (k + 0.5) * math.pi / 3), 0))
cyl = child_of(p.build("RV_Cylinder", [m_steel, m_dark], pivot=CYL_PIVOT, parent=crane, coll=C),
               CYL_PIVOT, CRANE_PIVOT)

# ---- ejector rod and star: slide back to push the cases out -----------------
p = Part()
p.cyl(0.0028, 0.042, (0, cy_front + 0.021, CYL_Z), 0, rot=X90, segs=6)
p.cyl(0.0042, 0.006, (0, cy_front + 0.040, CYL_Z), 1, rot=X90, segs=6)
p.cyl(0.0085, 0.002, (0, -CYL_L / 2 - 0.001, CYL_Z), 0, rot=X90, segs=6)
child_of(p.build("RV_Ejector", [m_steel, m_dark], pivot=CYL_PIVOT, parent=cyl, coll=C), CYL_PIVOT, CYL_PIVOT)


def cartridges(name, bullets, primer_mat, parent, coll, pivot=CYL_PIVOT):
    """Six cases in the chamber pattern, rims flush with the cylinder's back face."""
    p = Part()
    y0 = -CYL_L / 2
    for k in range(6):
        cx, cz = chamber_xz(k)
        c = Vector((cx, 0, CYL_Z + cz))
        p.cyl(CASE_R, CASE_L, c + Vector((0, y0 + CASE_L / 2, 0)), 0, rot=X90, segs=6)
        p.cyl(CASE_R + 0.0012, 0.0015, c + Vector((0, y0 - 0.0006, 0)), 0, rot=X90, segs=6)
        p.cyl(CASE_R * 0.45, 0.0017, c + Vector((0, y0 - 0.0007, 0)), 1, rot=X90, segs=6)
        if bullets:
            p.cyl(CASE_R * 0.95, 0.010, c + Vector((0, y0 + CASE_L + 0.005, 0)), 2, rot=X90,
                  segs=6, r2=CASE_R * 0.4)
    return p.build(name, [m_brass, primer_mat, m_lead], pivot=pivot, parent=parent, coll=coll)


child_of(cartridges("RV_Rounds", False, m_primer, cyl, C), CYL_PIVOT, CYL_PIVOT)
casings = child_of(cartridges("RV_Casings", False, m_dark, cyl, C), CYL_PIVOT, CYL_PIVOT)
casings.hide_viewport = casings.hide_render = True

# ---- effects: muzzle flash, its light, the speedloader -----------------------
FX = collection("REVOLVER_FX", C)
p = Part()
fc = Vector((0, BARREL_Y[1] + 0.030, BORE_Z))
ball = bmesh.ops.create_uvsphere(p.bm, u_segments=7, v_segments=5, radius=0.026)["verts"]
p._place(ball, fc + Vector((0, 0.012, 0)), (0, 0, 0), 0)
for i in range(6):
    a = i * math.pi / 3 + 0.3
    d = Vector((math.cos(a), 0, math.sin(a)))
    p.tube([fc + Vector((0, -0.015, 0)), fc + d * 0.030 + Vector((0, 0.004, 0)), fc + d * 0.050 + Vector((0, 0.012, 0))],
           [0.011, 0.007, 0.002], 0, sides=4)
p.tube([fc, fc + Vector((0, 0.065, 0))], [0.013, 0.002], 0, sides=5)
flash = p.build("RV_MuzzleFlash", [m_flash], pivot=tuple(fc), parent=root, coll=FX)
fl = bpy.data.lights.new("RV_FlashLight", 'POINT'); fl.energy = 5.0; fl.color = (1.0, 0.55, 0.2)
fl.shadow_soft_size = 0.02
flo = bpy.data.objects.new("RV_FlashLight", fl); FX.objects.link(flo)
flo.parent = root; flo.location = fc
for o in (flash, flo):
    o.hide_viewport = o.hide_render = True

# Speedloader: origin at the centre of the cylinder's back face, so placing it
# there with the cylinder's rotation seats all six rounds.
SL_PIVOT = (0, -CYL_L / 2, CYL_Z)
sl = cartridges("RV_Speedloader", True, m_primer, root, FX, pivot=SL_PIVOT)
p = Part()
p.cyl(CYL_R * 0.95, 0.010, (0, -CYL_L / 2 - 0.006, CYL_Z), 0, rot=X90, segs=12)
p.cyl(0.006, 0.010, (0, -CYL_L / 2 - 0.015, CYL_Z), 1, rot=X90, segs=8)
body = p.build("RV_SpeedloaderBody", [m_dark, m_steel], pivot=SL_PIVOT, parent=sl, coll=FX)
body.location = (0, 0, 0)
for o in (sl, body):
    o.hide_viewport = o.hide_render = True

studio(target=(0, 0.03, 0.01), dist=0.6, name="RV_ModelCam")
look_through(bpy.context.scene.camera)
# shared UV atlas + baked texture for GZDoom (saves the .blend before baking)
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\gz_bake.py").read())
uv_save_bake(OUT, r"C:\Users\TD3KX\ashes-2063-weapons\revolver\gzdoom\revolver.png")
