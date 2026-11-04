"""Numbers the sharp cube shotgun's design (sharp_cube_pump.py, runs in Blender) and its export job (make_job_sharp.py,
runs anywhere) must agree on. No Blender imports here, so both can read it.
"""
CUBE_M = 0.0034                        # cube_size.VOXEL_M: one main cube, in metres

# Tefa, 2026-11-04, after watching it in Blender: "shell guard on the right side needs to match the shell length,
# handle needs to travel the whole length". So the ejection port is one shell long, and the pump travels exactly the
# port's length, so a full stroke opens it all the way and the bolt closes it all the way.
SHELL_LEN = 20.5                       # main cubes, rim to crimp (brass 4 + rim 0.5 + hull 16)
PORT_CLEAR = 1.0                       # main cubes of room round the shell in the port
PORT_LEN = SHELL_LEN + PORT_CLEAR      # 21.5 main cubes, 73 mm
PUMP_STROKE_M = PORT_LEN * CUBE_M      # the pump's full travel, metres

# "needs to be a little darker in colour" (same day): every colour of the gun times this; the flash keeps its own.
DARKEN = 0.8

# "it has to kick a little ... that look right!": metres back and degrees nose up round the hand, per game frame
# (kind letter: F = the shot, P = the pump state's recoil frames). Nothing else moves the whole gun.
KICK = {("F", "A"): (0.012, 2.5), ("F", "B"): (0.008, 1.5), ("F", "C"): (0.004, 0.8), ("P", "C"): (0.002, 0.4)}

# Moving parts that would overlap another moving part (the flashes of one muzzle, a shell in its chamber) are built
# apart, each in its own spot this many main cubes above where it is shown, and the job moves it down in the frames
# that show it: a model holds one part per cube, so overlapping parts overwrote each other's cubes.
PARK_STEP = 60.0


def park_z(k):
    """Main cubes above its shown place that the k-th parked part is built (k = 0 is built in place)."""
    return k * PARK_STEP

# ---------------------------------------------------------------------------------------------- the sawn-off
# (sharp_sawed_off.py builds it, make_job_sawed_off.py animates it.) Its side picture SAWPA0 is 54 pixels wide; the
# gun spans 47 of them, about 0.70 m: a short, heavy boomstick next to the 1.0 m pump.
SAWN_PIC_W = 54
SAWN_LENGTH_M = 0.80                   # the whole picture's width
SAWN_S = SAWN_LENGTH_M / SAWN_PIC_W / CUBE_M   # main cubes per picture pixel (4.36)
SAWN_HINGE_PX = (21.6, 11.0)           # the hinge pin the barrels break open on (picture column, row)
SAWN_OPEN_DEG = 30.0                   # barrels fully open, muzzles down
SAWN_BARREL_Y = 5.2                    # main cubes from the middle to each barrel's axis (right = minus)
SAWN_TOP_PX = 4.2                      # picture row of the barrels' top
SAWN_BARREL_R = 5.0
SAWN_BREECH_PX = 22.5                  # picture column where the barrels meet the action
SAWN_MUZZLE_PX = 50.5

# ---------------------------------------------------------------------------------------------- the revolver
# (sharp_revolver.py, make_job_revolver.py) Side picture REVPA0, 34 pixels wide; the gun spans 27 of them, about 0.36 m.
REV_PIC_W = 34
REV_LENGTH_M = 0.45
REV_S = REV_LENGTH_M / REV_PIC_W / CUBE_M      # main cubes per picture pixel (3.9)
REV_CYL_PX = (11.6, 18.9, 6.4)         # the cylinder: from column, to column, axis row
REV_CYL_R, REV_CHAMBER_RING = 6.8, 4.0  # main cubes: cylinder radius, chambers' distance from its axis
REV_CRANE = (5.0, -6.5)                # the crane it swings out on: main cubes left of and below the cylinder's axis
REV_SWING_DEG = -110.0                 # swung out to the gun's left, round the axis along the barrel

# ---------------------------------------------------------------------------------------------- the 9mm (Glock)
# (sharp_handgun.py, make_job_handgun.py) Side picture GLPPA0, 34 pixels wide; the gun spans 26, about 0.24 m.
GLK_PIC_W = 34
GLK_LENGTH_M = 0.31
GLK_S = GLK_LENGTH_M / GLK_PIC_W / CUBE_M      # main cubes per picture pixel (2.7)
GLK_SLIDE_STROKE = 7.0                 # main cubes the slide runs back
GLK_MAG_AXIS = (-0.216, -0.976)        # the magazine slides out along the (stretched) grip: (x, z) per main cube

# ---------------------------------------------------------------------------------------------- the Ingram (3 builds)
# (sharp_ingram.py + sharp_ingram1/2/3.py, make_job_ingram.py) Side pictures MPIPA0 / MP2PA0 / MP3PA0, 46 pixels wide =
# 0.40 m: the bare gun spans 31 of them (0.27 m), the silenced builds with the folded stock 44 (0.38 m).
ING_PIC_W = 46
ING_LENGTH_M = 0.40
ING_S = ING_LENGTH_M / ING_PIC_W / CUBE_M      # main cubes per picture pixel (2.6)
ING_BOLT_STROKE = 6.0                  # main cubes the cocking knob runs back

# ---------------------------------------------------------------------------------------------- the FAL
# (sharp_fal.py, make_job_fal.py) Side picture FWEPA0, 88 pixels wide; the rifle spans 72 of them, about 1.05 m.
FAL_PIC_W = 88
FAL_LENGTH_M = 1.28
FAL_S = FAL_LENGTH_M / FAL_PIC_W / CUBE_M      # main cubes per picture pixel (4.3)
FAL_HANDLE_STROKE = 18.0               # main cubes the charging handle runs back

# ---------------------------------------------------------------------------------------------- the Junker Musket
# (sharp_musket.py, make_job_musket.py) Side picture MKTPA0, 69 pixels wide; the rifle spans 64 of them, about 1.10 m.
MSK_PIC_W = 69
MSK_LENGTH_M = 1.19
MSK_S = MSK_LENGTH_M / MSK_PIC_W / CUBE_M      # main cubes per picture pixel (5.1)
MSK_BOLT_ROW = 9.2                     # picture row of the bolt's axis (it turns on it)
MSK_BOLT_LIFT_DEG = -70.0              # the handle lifted up, round the bolt's axis
MSK_BOLT_STROKE = 16.0                 # main cubes the bolt runs back

# ---------------------------------------------------------------------------------------------- the Master Blaster
# (sharp_blaster.py, make_job_blaster.py) Side picture LAUPA0, 56 pixels wide; the flamethrower spans 43, about 0.9 m.
BLS_PIC_W = 56
BLS_LENGTH_M = 1.17
BLS_S = BLS_LENGTH_M / BLS_PIC_W / CUBE_M      # main cubes per picture pixel (6.1)
BLS_VALVE_PX = (24.5, 4.2)             # the red valve wheel on the upper tank (column, row), off to the right
BLS_TANK_Y = -10.5                     # main cubes: both tanks ride the right side
BLS_GAUGE_PX = (20.0, 3.4)             # the pressure gauge facing the player (column, row)

# ---------------------------------------------------------------------------------------------- the JackHammer
# (sharp_jackhammer.py, make_job_jackhammer.py) Side picture JHAMA0, 40 pixels wide = 0.80 m.
JCK_PIC_W = 40
JCK_LENGTH_M = 0.80
JCK_S = JCK_LENGTH_M / JCK_PIC_W / CUBE_M      # main cubes per picture pixel (5.9)
JCK_CHISEL_STROKE = 8.0                # main cubes the chisel hammers out
