"""Numbers the smudge-cube shotgun's design (smudge_cube_pump_v12.py, runs in Blender) and its export job
(make_job_smudge_v12.py, runs anywhere) must agree on. No Blender imports here. Round 12, 2026-11-12.

Tefa, after wearing round 11 at 0.7 size: "the guard opening still must be the size of a shell and show the actual
inside of the barrel when it goes in there. the shells going into the gun need to be twice the size".
"""
from sharp_settings import CUBE_M, PORT_CLEAR, SHELL_LEN

SHELL_K = 2.0                              # the shells shown going into the gun: twice the kit's 12 gauge
BIG_SHELL_LEN = SHELL_LEN * SHELL_K        # 41 main cubes
BIG_SHELL_R = 2.95 * SHELL_K               # 5.9 main cubes
BIG_PORT_LEN = BIG_SHELL_LEN + PORT_CLEAR  # the ejection port: one big shell long (42 main cubes)
CHAMBER_R = BIG_SHELL_R + 0.35             # the round space behind the port
CHAMBER_DROP = 3.0                         # main cubes its axis sits under the barrel's (so the receiver keeps a roof)
REC_W = 21.0                               # the receiver's width (round 11)
SHELL2_OUT = 8.0                           # main cubes from the receiver's right side to the port shell's axis, as built
# the port shell ends on the gun's middle line, in the chamber
SHELL2_IN_M = (REC_W / 2 + SHELL2_OUT) * CUBE_M
BOLT_STROKE_M = BIG_PORT_LEN * CUBE_M      # the shell guard slides the whole port open; the pump keeps its own stroke
LOAD_DROP = 7.0                            # main cubes under the receiver the loading shell's axis is built
