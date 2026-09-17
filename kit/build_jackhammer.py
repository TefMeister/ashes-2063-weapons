# Ashes 2063 jackhammer (petrol breaker) model. +Z up, the bit points down,
# the handle loop is toward the player (-Y). The hidden underside and far side
# are guessed. Moving parts: JH_Bit (hammers in and out), JH_Puff (exhaust smoke).
import math
exec(open(r"C:\Users\TD3KX\ashes-2063-weapons\kit\pixel_kit.py").read())

OUT = r"C:\Users\TD3KX\ashes-2063-weapons\jackhammer\Ashes_2063_EP1_jackhammer_model.blend"

# ---- dimensions (metres) --------------------------------------------------
BODY = (0.28, 0.24, 0.26)          # red lower body, centre at z = BODY_Z
BODY_Z = -0.03
HOOD = (0.21, 0.19, 0.075)         # white engine hood on top
HOOD_Z = 0.135
BAND = (0.25, 0.03, 0.065)         # black logo band on the player-facing side
HANDLE_R = 0.013
GRIP_HALF = 0.095                  # half-length of the wrapped grip
BIT_R = 0.024
BIT_LEN = 0.30
BLOCK_JH = 0.005                   # bigger machine, bigger texture pixels

reset_scene()
setup_scene("Jackhammer_Model")
C = collection("JACKHAMMER")

RED = [(0.0, (0.32, 0.02, 0.02)), (0.4, (0.50, 0.04, 0.03)), (0.8, (0.66, 0.10, 0.07))]
m_red = pixel_mat("JH_RedPaint", RED, metal=0.2, rough=0.5, block=BLOCK_JH, paint=[
    (0.0, (0.72, 0.62, 0.60)), (0.5, (0.85, 0.80, 0.78))], paint_cover=0.12, paint_scale=14, paint_seed=4.0)
m_white = pixel_mat("JH_WhitePlastic", [(0.0, (0.55, 0.52, 0.50)), (0.35, (0.72, 0.70, 0.68)),
                                        (0.75, (0.86, 0.85, 0.83))], metal=0.0, rough=0.7, block=BLOCK_JH)
m_black = pixel_mat("JH_BlackPlastic", [(0.0, (0.015, 0.015, 0.015)), (0.5, (0.04, 0.04, 0.045)),
                                        (0.85, (0.08, 0.08, 0.085))], metal=0.1, rough=0.7, block=BLOCK_JH)
m_tube = pixel_mat("JH_HandleSteel", [(0.0, (0.05, 0.06, 0.06)), (0.5, (0.12, 0.13, 0.13)),
                                      (0.85, (0.30, 0.31, 0.31))], metal=0.8, rough=0.45, block=BLOCK_JH)
m_grip = pixel_mat("JH_GripWrap", [(0.0, (0.18, 0.09, 0.06)), (0.5, (0.30, 0.17, 0.12)),
                                   (0.85, (0.45, 0.30, 0.24))], metal=0.0, rough=0.85, block=0.004,
                   stripes=(0, 0.012, 0.3))
m_yellow = pixel_mat("JH_LogoYellow", [(0.0, (0.55, 0.42, 0.02)), (0.6, (0.80, 0.65, 0.08))],
                     metal=0.0, rough=0.6, wear=0.5, block=0.004)
m_steel = pixel_mat("JH_BitSteel", [(0.0, (0.28, 0.28, 0.29)), (0.4, (0.42, 0.42, 0.43)),
                                    (0.8, (0.62, 0.62, 0.63))], metal=1.0, rough=0.35, block=0.004)
m_smoke = pixel_mat("JH_Smoke", [(0.0, (0.18, 0.18, 0.18)), (0.5, (0.30, 0.30, 0.30)),
                                 (0.85, (0.42, 0.42, 0.42))], metal=0.0, rough=1.0, wear=0.0, block=0.012)

root = empty("JH_Root", coll=C, size=0.08)
MATS = [m_red, m_white, m_black, m_tube, m_grip, m_yellow, m_steel]
RED_, WHITE_, BLACK_, TUBE_, GRIP_, YEL_, STEEL_ = range(7)

p = Part()
# ---- red body with vertical ribs -------------------------------------------
bx, by, bz = BODY
p.box((bx, by, bz), (0, 0, BODY_Z), RED_, top_scale=(0.92, 0.92))
p.box((bx * 0.8, by * 0.8, 0.04), (0, 0, BODY_Z - bz / 2 - 0.02), RED_, top_scale=(1.25, 1.25))
for i in range(7):
    x = -bx / 2 + 0.03 + i * (bx - 0.06) / 6
    p.box((0.014, 0.012, bz * 0.8), (x, -by / 2 - 0.003, BODY_Z - 0.01), RED_)
for sx in (1, -1):
    for i in range(4):
        y = -by / 2 + 0.04 + i * 0.055
        p.box((0.012, 0.016, bz * 0.7), (sx * (bx / 2 + 0.002), y, BODY_Z - 0.02), RED_)
# ---- engine hood with vent slots -------------------------------------------
hx, hy, hz = HOOD
p.box((hx, hy, hz), (0, 0.005, HOOD_Z), WHITE_, top_scale=(0.9, 0.85))
for col in (-1, 1):
    for i in range(6):
        p.box((0.075, 0.009, 0.006), (col * 0.048, -hy / 2 + 0.035 + i * 0.022, HOOD_Z + hz / 2 + 0.001), BLACK_)
# ---- black logo band facing the player, with two blocky yellow glyphs ------
p.box(BAND, (0, -by / 2 + 0.005, HOOD_Z - hz / 2 - 0.02), BLACK_)
GLYPH = ["1110", "1001", "1110", "1010", "1001"]     # a blocky "R"
PX = 0.0075
for gi, gx in enumerate((-0.04, 0.012)):
    for r, row in enumerate(GLYPH):
        for c, ch in enumerate(row):
            if ch == "1":
                p.box((PX, 0.004, PX), (gx + c * PX, -by / 2 - 0.012, HOOD_Z - hz / 2 - 0.002 - r * PX), YEL_)
# ---- side parts: fuel tank cylinder with a silver cap (left), fender (right)
p.cyl(0.045, 0.17, (-bx / 2 - 0.04, -0.01, 0.06), BLACK_, segs=8)
p.cyl(0.028, 0.02, (-bx / 2 - 0.04, -0.01, 0.155), STEEL_, segs=8)
p.cyl(0.014, 0.018, (-bx / 2 - 0.04, -0.01, 0.172), STEEL_, segs=6)
p.box((0.05, by * 0.9, 0.12), (bx / 2 + 0.02, 0.0, 0.03), RED_, top_scale=(0.6, 0.9))
# ---- bit collar ------------------------------------------------------------
p.cyl(0.04, 0.05, (0, 0, BODY_Z - bz / 2 - 0.065), BLACK_, segs=8)
p.cyl(0.028, 0.03, (0, 0, BODY_Z - bz / 2 - 0.10), STEEL_, segs=6)
# ---- handle loop over the top, toward the player ---------------------------
loop = [(-0.15, 0.03, 0.07), (-0.20, -0.05, 0.20), (-0.18, -0.13, 0.30), (-0.11, -0.16, 0.34),
        (0.0, -0.165, 0.345), (0.11, -0.16, 0.34), (0.18, -0.13, 0.30), (0.20, -0.05, 0.20), (0.15, 0.03, 0.07)]
p.tube(loop, HANDLE_R, TUBE_, sides=6)
# inner struts from the hood to the loop
for sx in (1, -1):
    p.tube([(sx * 0.07, -0.06, HOOD_Z + 0.02), (sx * 0.10, -0.11, 0.25), (sx * 0.12, -0.15, 0.32)],
           0.008, TUBE_, sides=5)
    p.cyl(0.02, 0.03, (sx * 0.155, 0.035, 0.06), BLACK_, segs=6)        # rubber mounts
# wrapped grip on the top bar
p.tube([(-GRIP_HALF, -0.163, 0.343), (GRIP_HALF, -0.163, 0.343)], 0.021, GRIP_, sides=8)
for sx in (1, -1):
    p.tube([(sx * (GRIP_HALF + 0.004), -0.163, 0.343), (sx * (GRIP_HALF + 0.012), -0.163, 0.343)],
           0.024, BLACK_, sides=8)
body = p.build("JH_Body", MATS, parent=root, coll=C)

# ---- chisel bit: origin at the collar so it slides straight down -----------
p = Part()
top = BODY_Z - bz / 2 - 0.10
p.cyl(BIT_R, BIT_LEN, (0, 0, top - BIT_LEN / 2), 0, segs=6)
p.cyl(BIT_R, 0.06, (0, 0, top - BIT_LEN - 0.03), 0, segs=6, r2=0.003)
p.cyl(BIT_R * 1.5, 0.012, (0, 0, top - 0.03), 0, segs=6)
bit = p.build("JH_Bit", [m_steel], pivot=(0, 0, top), parent=root, coll=C)

# ---- exhaust puff (hidden) -----------------------------------------------------
FX = collection("JACKHAMMER_FX", C)
p = Part()
pc = Vector((-bx / 2 - 0.05, -0.02, 0.25))
for off, r in (((0, 0, 0), 0.035), ((0.03, -0.01, 0.03), 0.028), ((-0.02, 0.01, 0.045), 0.022)):
    v = bmesh.ops.create_icosphere(p.bm, subdivisions=1, radius=r)['verts']
    p._place(v, pc + Vector(off), (0, 0, 0), 0)
puff = p.build("JH_Puff", [m_smoke], pivot=tuple(pc), parent=root, coll=FX)
puff.hide_viewport = puff.hide_render = True

studio(target=(0, 0, 0.0), dist=1.6, name="JH_ModelCam")
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("saved", OUT)
