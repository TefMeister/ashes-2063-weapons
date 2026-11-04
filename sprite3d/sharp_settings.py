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
