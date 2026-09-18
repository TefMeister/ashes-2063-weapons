# Ashes 2063 pump-action shotgun model. +Y is the muzzle, +Z up, +X the gun's right side.
# Built by eye from Tefa's screenshots (`Ashes 2063/shotgun/`): dark blued barrel and magazine
# tube, dark green-grey receiver with a big open port, deeply ribbed warm-brown wooden pump,
# near-black worn stock with a rubber pad. Everything is deliberately darker and dirtier than the
# revolver and the lantern (Tefa, 2026-09-18).
# The port is on the gun's RIGHT, as it is in the game and on any real 12-gauge (Tefa, 2026-09-18 —
# the heavily zoomed screenshots read as left, which was our mistake, not the game's).
# Moving parts are separate objects so the shoot/reload files can animate them:
# SG_Pump (racks back and forward), SG_Trigger, SG_PortShell, SG_MuzzleFlash, SG_Casing, SG_LoadShell.
import math
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\pixel_kit.py").read())
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\shotgun_settings.py").read())

OUT = MODEL

# Weathering colours, darkened for this weapon: the revolver's bright scratches read as white
# cracks on a dark gun, which is exactly what Tefa asked us to get away from.
SCRATCH_COLOR = (0.26, 0.26, 0.255, 1.0)
RUST_COLOR = (0.115, 0.048, 0.020, 1.0)
GRIME_COLOR = (0.018, 0.017, 0.015, 1.0)

reset_scene()
setup_scene("Shotgun_Model")
C = collection("SHOTGUN")

# ---- materials: dark, tarnished, weathered ---------------------------------
m_blued = pixel_mat("SG_BluedSteel", [(0.0, (0.030, 0.032, 0.036)), (0.40, (0.042, 0.045, 0.050)),
                                      (0.80, (0.058, 0.062, 0.068))],
                    metal=0.8, rough=0.55, wear=0.30, block=BLOCK_SG)
m_recv = pixel_mat("SG_ReceiverSteel", [(0.0, (0.062, 0.070, 0.064)), (0.38, (0.085, 0.096, 0.086)),
                                        (0.78, (0.115, 0.128, 0.116))],
                   metal=0.7, rough=0.6, wear=0.38, block=BLOCK_SG,
                   paint=[(0.0, (0.105, 0.052, 0.024)), (0.5, (0.150, 0.078, 0.035))],
                   paint_cover=0.10, paint_scale=19, paint_seed=3.0)
m_wood = pixel_mat("SG_PumpWood", [(0.0, (0.105, 0.050, 0.022)), (0.40, (0.145, 0.070, 0.030)),
                                   (0.78, (0.195, 0.098, 0.044))],
                   metal=0.0, rough=0.8, wear=0.30, block=0.0035)
m_groove = pixel_mat("SG_PumpGroove", [(0.0, (0.038, 0.018, 0.008)), (0.5, (0.055, 0.027, 0.012))],
                     metal=0.0, rough=0.9, wear=0.35, block=0.003)
m_stock = pixel_mat("SG_StockBlack", [(0.0, (0.026, 0.026, 0.029)), (0.42, (0.036, 0.037, 0.041)),
                                      (0.80, (0.050, 0.052, 0.058))],
                    metal=0.4, rough=0.7, wear=0.15, block=BLOCK_SG)
m_pad = pixel_mat("SG_ButtPad", [(0.0, (0.009, 0.009, 0.010)), (0.5, (0.020, 0.020, 0.022))],
                  metal=0.0, rough=0.95, wear=0.3, block=0.003, stripes=(2, 0.010, 0.38))
m_sight = pixel_mat("SG_WornSteel", [(0.0, (0.145, 0.145, 0.150)), (0.40, (0.185, 0.185, 0.191)),
                                     (0.80, (0.235, 0.235, 0.242))],
                    metal=1.0, rough=0.45, wear=0.45, block=0.0035)
m_dark = pixel_mat("SG_Inside", [(0.0, (0.009, 0.010, 0.009)), (0.6, (0.018, 0.020, 0.018))],
                   metal=0.5, rough=0.8, wear=0.2, block=0.002)
m_hull = pixel_mat("SG_ShellRed", [(0.0, (0.225, 0.030, 0.024)), (0.5, (0.310, 0.046, 0.034)),
                                   (0.85, (0.400, 0.075, 0.052))],
                   metal=0.0, rough=0.7, wear=0.3, block=0.003)
m_brass = pixel_mat("SG_Brass", [(0.0, (0.150, 0.102, 0.020)), (0.5, (0.250, 0.176, 0.042)),
                                 (0.85, (0.355, 0.268, 0.088))],
                    metal=1.0, rough=0.5, wear=0.4, block=0.003)
m_flash = pixel_mat("SG_Flash", [(0.0, (0.9, 0.08, 0.0)), (0.35, (1.0, 0.35, 0.02)),
                                 (0.7, (1.0, 0.75, 0.2)), (0.92, (1.0, 1.0, 0.8))],
                    metal=0.0, rough=1.0, wear=0.0, emit=1.6, block=0.006)

root = empty("SG_Root", coll=C, size=0.10)
MATS = [m_blued, m_recv, m_wood, m_groove, m_stock, m_pad, m_sight, m_dark, m_hull, m_brass]
BLUE_, RECV_, WOOD_, GROOVE_, STOCK_, PAD_, SIGHT_, DARK_, HULL_, BRASS_ = range(10)
Y90 = (math.pi / 2, 0, 0)          # lay a cylinder along +Y
PORT_X = 1                         # +1 = the gun's right side (see the note at the top)


def shell(p, centre, rot=Y90, length=SHELL_L):
    """A 12-gauge shell: red hull with a brass head at its -Y end."""
    cx, cy, cz = centre
    body = length - SHELL_BRASS_L
    p.cyl(SHELL_R, body, (cx, cy + SHELL_BRASS_L / 2, cz), HULL_, rot=rot, segs=8)
    p.cyl(SHELL_R * 1.05, SHELL_BRASS_L, (cx, cy - body / 2, cz), BRASS_, rot=rot, segs=8)
    p.cyl(SHELL_R * 0.45, 0.003, (cx, cy - body / 2 - SHELL_BRASS_L / 2 + 0.0015, cz), BRASS_,
          rot=rot, segs=6)


# ---------------------------------------------------------------------------
# SG_Body: receiver, barrel, magazine tube, sights, trigger guard, stock
# ---------------------------------------------------------------------------
p = Part()

# ---- receiver: a dark core wrapped in side plates, so the port is a real hole
HALF_W, HALF_H = REC_W / 2, REC_H / 2
PLATE = 0.0055
P_Y0, P_Y1 = PORT_Y - 0.034, PORT_Y + 0.034          # port opening, front to back
P_Z0, P_Z1 = BORE_Z - 0.023, BORE_Z + 0.014          # port opening, bottom to top
CAVITY = 0.014                                       # depth of the well behind the port
p.box((REC_W - 2 * PLATE - CAVITY, REC_LEN, REC_H),
      (-PORT_X * CAVITY / 2, REC_LEN / 2, REC_Z), DARK_)
p.box((PLATE, REC_LEN, REC_H), (-PORT_X * (HALF_W - PLATE / 2), REC_LEN / 2, REC_Z), RECV_)
px = PORT_X * (HALF_W - PLATE / 2)
p.box((PLATE, P_Y0, REC_H), (px, P_Y0 / 2, REC_Z), RECV_)                       # behind the port
p.box((PLATE, REC_LEN - P_Y1, REC_H), (px, (REC_LEN + P_Y1) / 2, REC_Z), RECV_)  # in front of it
p.box((PLATE, P_Y1 - P_Y0, REC_Z + HALF_H - P_Z1), (px, PORT_Y, (P_Z1 + REC_Z + HALF_H) / 2), RECV_)
p.box((PLATE, P_Y1 - P_Y0, P_Z0 - REC_Z + HALF_H), (px, PORT_Y, (P_Z0 + REC_Z - HALF_H) / 2), RECV_)
# top and bottom skins, so the core never shows through
p.box((REC_W, REC_LEN, 0.005), (0, REC_LEN / 2, REC_Z + HALF_H - 0.0025), RECV_)
p.box((REC_W, REC_LEN, 0.005), (0, REC_LEN / 2, REC_Z - HALF_H + 0.0025), RECV_)
# sloped nose where the barrel joins, and the rounded rear where the stock starts
p.box((REC_W * 0.92, 0.030, REC_H * 0.80), (0, REC_LEN + 0.010, REC_Z + 0.004), RECV_,
      top_scale=(0.80, 0.90))
p.box((REC_W * 0.88, 0.022, REC_H * 0.94), (0, -0.010, REC_Z - 0.002), RECV_, top_scale=(0.84, 0.9))
# shallow sighting groove along the receiver top
p.box((0.013, REC_LEN * 0.80, 0.005), (0, REC_LEN * 0.50, REC_Z + HALF_H - 0.0005), DARK_)
# loading port underneath
p.box((0.026, 0.056, 0.006), (0, 0.050, REC_Z - HALF_H + 0.0015), DARK_)
# carrier lip inside the port, so the hole does not read as empty black
p.box((CAVITY, P_Y1 - P_Y0 - 0.005, 0.005), (PORT_X * 0.017, PORT_Y, P_Z0 + 0.003), RECV_)
# pivot pin heads and a row of blocky stamped marks on the outside
for sx in (1, -1):
    p.cyl(0.0060, 0.004, (sx * (HALF_W - 0.0005), 0.070, REC_Z - 0.014), SIGHT_, segs=8,
          rot=(0, math.pi / 2, 0))
    p.cyl(0.0034, 0.004, (sx * (HALF_W - 0.0005), 0.182, REC_Z - 0.018), SIGHT_, segs=6,
          rot=(0, math.pi / 2, 0))
for i in range(6):
    p.box((0.003, 0.0045, 0.0035), (-PORT_X * (HALF_W - 0.0005), 0.100 + i * 0.008, BORE_Z + 0.004),
          DARK_)

# ---- barrel ----------------------------------------------------------------
by0, by1 = BARREL_Y
p.cyl(BARREL_R * 1.26, 0.052, (0, by0 + 0.026, BORE_Z), BLUE_, rot=Y90, segs=10)   # thick breech
p.cyl(BARREL_R, by1 - by0 - 0.040, (0, by0 + 0.040 + (by1 - by0 - 0.040) / 2, BORE_Z), BLUE_,
      rot=Y90, segs=10)
p.cyl(BARREL_R * 1.12, 0.014, (0, by1 - 0.007, BORE_Z), BLUE_, rot=Y90, segs=10)   # muzzle ring
p.cyl(BORE_R, 0.030, (0, by1 - 0.014, BORE_Z), DARK_, rot=Y90, segs=10)            # the hole

# ---- magazine tube, cap and barrel band ------------------------------------
p.cyl(MAG_R, MAG_END_Y - 0.190, (0, (MAG_END_Y + 0.190) / 2, MAG_Z), BLUE_, rot=Y90, segs=8)
p.cyl(MAG_R * 1.15, 0.020, (0, MAG_END_Y + 0.010, MAG_Z), SIGHT_, rot=Y90, segs=8)   # end cap
p.cyl(MAG_R * 0.55, 0.008, (0, MAG_END_Y + 0.024, MAG_Z), SIGHT_, rot=Y90, segs=6)
p.box((0.034, 0.020, 0.060), (0, BAND_Y, BORE_Z - 0.012), SIGHT_, top_scale=(0.72, 1.0))

# ---- front sight: a blocky ramp with a blade ------------------------------
p.box((0.019, 0.030, 0.010), (0, SIGHT_Y, BORE_Z + BARREL_R + 0.004), SIGHT_, top_scale=(0.60, 0.70))
p.box((0.007, 0.009, 0.015), (0, SIGHT_Y + 0.005, BORE_Z + BARREL_R + 0.015), SIGHT_)

# ---- trigger guard ---------------------------------------------------------
guard = [(0, 0.094, REC_Z - HALF_H + 0.002), (0, 0.090, -0.019), (0, 0.072, -0.030),
         (0, 0.046, -0.033), (0, 0.024, -0.028), (0, 0.010, -0.015),
         (0, 0.006, REC_Z - HALF_H + 0.002)]
p.tube(guard, 0.0052, RECV_, sides=5)

# ---- stock: a thick wrist swelling into a deep butt ------------------------
p.box((0.034, 0.092, 0.050), (0, -0.044, REC_Z + 0.000), STOCK_, rot=(0.10, 0, 0),
      top_scale=(0.90, 1.0))                                    # wrist behind the receiver
p.box((0.042, 0.128, 0.078), (0, -0.140, REC_Z - 0.006), STOCK_, rot=(0.05, 0, 0),
      top_scale=(0.92, 1.0))                                    # stock deepening to the rear
p.box((0.046, 0.094, 0.100), (0, -0.246, REC_Z - 0.012), STOCK_, top_scale=(0.92, 1.0))
p.box((0.030, 0.215, 0.018), (0, -0.165, REC_Z + 0.032), STOCK_, top_scale=(0.62, 1.0))  # comb
p.box((0.032, 0.070, 0.034), (0, -0.048, REC_Z - 0.036), STOCK_, top_scale=(1.0, 0.72))  # belly
# recoil pad
p.box((0.048, 0.020, 0.106), (0, BUTT_Y - 0.008, REC_Z - 0.012), PAD_, top_scale=(0.9, 0.94))
p.box((0.049, 0.007, 0.108), (0, BUTT_Y + 0.005, REC_Z - 0.012), SIGHT_, top_scale=(0.9, 0.94))
# sling swivel stud under the butt
p.cyl(0.0055, 0.010, (0, BUTT_Y + 0.055, REC_Z - 0.066), SIGHT_, segs=6)

body = p.build("SG_Body", MATS, parent=root, coll=C)

# ---------------------------------------------------------------------------
# SG_Pump: the ribbed wooden forend and its action bars; slides along -Y
# ---------------------------------------------------------------------------
p = Part()
py0, py1 = PUMP_Y
plen = py1 - py0
p.box((0.041, plen, 0.049), (0, (py0 + py1) / 2, MAG_Z + 0.002), GROOVE_, top_scale=(0.80, 1.0))
p.box((0.036, 0.015, 0.048), (0, py0 - 0.007, MAG_Z + 0.002), WOOD_, top_scale=(0.86, 1.0))
p.box((0.036, 0.015, 0.048), (0, py1 + 0.007, MAG_Z + 0.002), WOOD_, top_scale=(0.86, 1.0))
for i in range(RIB_COUNT):                              # the deep grooves Tefa's shots show
    ry = py0 + 0.014 + i * RIB_PITCH
    p.box((0.047, 0.012, 0.055), (0, ry, MAG_Z + 0.002), WOOD_, top_scale=(0.80, 1.0))
for sx in (1, -1):                                      # action bars back to the receiver
    p.box((0.005, 0.098, 0.011), (sx * 0.019, py0 - 0.056, MAG_Z - 0.013), BLUE_)
pump = p.build("SG_Pump", MATS, pivot=PUMP_PIVOT, parent=root, coll=C)

# ---------------------------------------------------------------------------
# SG_Trigger
# ---------------------------------------------------------------------------
p = Part()
p.box((0.0065, 0.009, 0.026), (0, 0.058, -0.012), BLUE_, rot=(0.18, 0, 0))
trigger = p.build("SG_Trigger", MATS, pivot=(0, 0.060, 0.000), parent=root, coll=C)

# ---------------------------------------------------------------------------
# The shell showing in the port
# ---------------------------------------------------------------------------
PORT_SHELL = (PORT_X * 0.014, PORT_Y, BORE_Z - 0.010)
p = Part()
shell(p, PORT_SHELL)
port_shell = p.build("SG_PortShell", MATS, pivot=PORT_SHELL, parent=root, coll=C)

# ---------------------------------------------------------------------------
# Hidden parts the animation files switch on
# ---------------------------------------------------------------------------
FX = collection("SHOTGUN_FX", C)

p = Part()
shell(p, (0, 0, 0))
casing = p.build("SG_Casing", MATS, parent=root, coll=FX)

p = Part()
shell(p, (0, 0, 0))
loader = p.build("SG_LoadShell", MATS, parent=root, coll=FX)

p = Part()
mz = (0, BARREL_Y[1] + 0.030, BORE_Z)
for r, off in ((0.055, 0.0), (0.040, 0.035), (0.026, 0.062)):
    v = bmesh.ops.create_icosphere(p.bm, subdivisions=1, radius=r)['verts']
    p._place(v, (mz[0], mz[1] + off, mz[2]), (0, 0, 0), 0)
flash = p.build("SG_MuzzleFlash", [m_flash], pivot=mz, parent=root, coll=FX)

for ob in (casing, loader, flash):
    ob.hide_viewport = ob.hide_render = True

studio(target=(0, 0.17, 0.03), dist=0.95, name="SG_ModelCam")
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("saved", OUT)
