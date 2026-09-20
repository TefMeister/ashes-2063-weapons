# Ashes 2063 crowbar model. Runs along +Y from the flat chisel end to the
# hooked claw; +Z is the side the hook curls toward. Origin is where the hand holds it.
import math
exec(open(r"C:\Users\TD3KX\github-backups\ashes-2063-weapons\kit\pixel_kit.py").read())

OUT = r"C:\Users\TD3KX\github-backups\ashes-2063-weapons\crowbar\Ashes_2063_EP1_crowbar_model.blend"

# ---- dimensions (metres) --------------------------------------------------
SHAFT_R = 0.0115              # hex bar "radius"
SHAFT_END = 0.50              # where the bend starts
HOOK_R = 0.048                # bend radius of the goose neck
PAINT_UNTIL_DEG = 25          # red paint runs this far round the bend
HOOK_END_DEG = 135
GRIP_Y = 0.17                 # hand position (object origin)

reset_scene()
setup_scene("Crowbar_Model")
C = collection("CROWBAR")

STEEL = [(0.0, (0.10, 0.10, 0.11)), (0.4, (0.20, 0.20, 0.21)), (0.8, (0.38, 0.38, 0.39))]
RED = [(0.0, (0.30, 0.01, 0.01)), (0.35, (0.48, 0.03, 0.02)), (0.75, (0.62, 0.06, 0.04))]
m_red = pixel_mat("CB_RedPaint", STEEL, metal=0.5, rough=0.45, paint=RED, paint_cover=0.68,
                  paint_scale=34, paint_seed=5.0, block=0.0025)
m_steel = pixel_mat("CB_DarkSteel", STEEL, metal=0.9, rough=0.4, block=0.0025)
m_notch = pixel_mat("CB_Notch", [(0.0, (0.01, 0.01, 0.01)), (0.5, (0.03, 0.03, 0.03))], metal=0.3,
                    rough=0.8, wear=0.0)

root = empty("CB_Root", loc=(0, GRIP_Y, 0), coll=C, size=0.05)


def bend(a_deg):
    a = math.radians(a_deg)
    return (0.0, SHAFT_END + HOOK_R * math.cos(a), HOOK_R + HOOK_R * math.sin(a))


p = Part()
# red painted shaft running into the start of the bend
pts = [(0, 0.015, 0), (0, 0.2, 0), (0, SHAFT_END - 0.02, 0)] + [bend(a) for a in range(-90, PAINT_UNTIL_DEG + 1, 23)]
p.tube(pts, SHAFT_R, 0, sides=6)
# chisel end: flattens into a blade and kinks slightly
chisel = [(0, 0.03, 0), (0, -0.01, 0), (0, -0.035, -0.004), (0, -0.058, -0.012), (0, -0.075, -0.019)]
p.tube(chisel, [SHAFT_R, SHAFT_R, 0.0115, 0.013, 0.014], 1, sides=6, flat=[1.0, 1.0, 0.7, 0.4, 0.14])
# claw end: steel, widening and flattening as it curls round
angles = list(range(PAINT_UNTIL_DEG - 10, HOOK_END_DEG + 1, 15))
claw = [bend(a) for a in angles]
n = len(claw)
radii = [SHAFT_R + 0.010 * i / (n - 1) for i in range(n)]
flat = [1.0 - 0.72 * (i / (n - 1)) ** 1.5 for i in range(n)]
p.tube(claw, radii, 1, sides=6, flat=flat, squash='b')
# the split in the claw
tip = Vector(bend(HOOK_END_DEG)); prev = Vector(bend(HOOK_END_DEG - 22))
d = (tip - prev).normalized()
ang = math.atan2(d.z, d.y)
p.box((0.0045, 0.028, 0.009), tuple(tip - d * 0.011), 2, rot=(ang, 0, 0))
cb = p.build("CB_Crowbar", [m_red, m_steel, m_notch], pivot=(0, GRIP_Y, 0), parent=None, coll=C)
cb.parent = root
cb.location = (0, 0, 0)

studio(target=(0, GRIP_Y + 0.1, 0.02), dist=1.1, name="CB_ModelCam")
bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("saved", OUT)
