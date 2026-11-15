"""The silenced MQ11 (2026-11-16, Developer PC): the Meshy MQ11 (meshy_mq11.py) with the heavy gun's suppressor.

Tefa: "then for the silenced MQ11 (ingram) we can use the same suppressor just change the colour a little", and chose
"a bit darker": darker gunmetal, close to the MQ11's own body. The suppressor is the heavy machine gun's grey can
(meshy_heavy_parts.py, straightened 10 degrees), at the size it has there (0.74 m model), slid over the MQ11's barrel
from the front of its receiver.
    python blender-cubekit/forge_make.py <out> <out> meshy_mq11_silenced.py
"""
import os

import meshy_mq11
from forge import mul
from meshy_kit import Meshy, transplant

HEAVY_GLB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meshy", "heavy_mg_meshy_2026-11-15.glb")
NAME = "meshy_mq11_silenced"
HEAVY_M, TILT_DEG = 0.74, 10.0
CAN_X0, CAN_ZC = 173, -39        # the heavy gun's suppressor (its cubes at 0.74 m): from x 173 on, its middle at z -39
MQ_FRONT_X, MQ_BORE_Z = 160, -35     # where it goes on the MQ11: the receiver's front, the barrel's middle
CAN_LEN, CAN_R = 46, 12          # its length and a little over its radius, for the bounds
DARKER = 0.62                    # Tefa: "a bit darker"


def build():
    m = meshy_mq11.build()
    m.name = NAME
    gh = Meshy(HEAVY_GLB, HEAVY_M, tilt_deg=TILT_DEG)
    dx, dz = MQ_FRONT_X - CAN_X0, MQ_BORE_Z - CAN_ZC
    transplant(m, gh, (MQ_FRONT_X - 1, MQ_FRONT_X + CAN_LEN, -CAN_R, CAN_R, MQ_BORE_Z - CAN_R, MQ_BORE_Z + CAN_R),
               lambda x, y, z: (x - dx, y, z - dz), region=lambda x, y, z: x >= CAN_X0, part="suppressor",
               tint=lambda rgb: mul(rgb, DARKER))
    return m
