"""The pump-action shotgun, Meshy 2026-11-27 (bird's-head grip, short barrel), in the cube look. A forge design
(m2_kit.py). Measured with m2_probe.py and the gridded side views: receiver x 40-100 (14 cubes wide, z -18 to -39),
barrel y -0.5 z -23.5 r 4.5 to the muzzle at 197, magazine tube under it (z -33.5, r 4.5), wooden pump x 121-176.
- Shell port on the RIGHT only (Tefa, every gun): Meshy painted a port window on both sides of a solid receiver; the
  right one becomes a pocket 3 cubes deep with the shell guard set in it, which slides back the port's length as the
  pump comes back (Tefa: "shell guard on the shotgun"); the painted window on the left is painted over with the
  receiver's own colour.
- The barrel is bored right through from the receiver to the muzzle.
- The pump slides back its stroke on the game's Pump states; the magazine tube's core stays on the body.
"""
import math

from forge import mul
from m2_anim import Rig
from m2_kit import cut_scratches, fill_box, flashes, load, set_part, bore, cells_in   # noqa: F401
from meshy_kit import big_shell
from smudge_kit import blocky_steel

NAME = "m2_pump_shotgun"
FILE = "pump action shotgun"
LENGTH_M = 0.67                          # a real short pump gun (Mossberg Shockwave class)
BARREL = (-0.5, -23.5, 4.5)              # y, z, outer radius
BORE_R, BORE_X0, MUZZLE_X = 2.7, 100, 197.2
TUBE = (-0.5, -33.5, 4.6)                # the magazine tube's axis and radius, inside the pump
PUMP_X = (120, 177)
PUMP_TOP_Z = -28.5
PORT = (72, 95, -29, -20)                # x0, x1, z0, z1 of the shell port window (both sides)
WALL_Y = -7                              # the receiver's right wall (cell y); the left wall is +6
POCKET_BACK_Y = -4                       # the pocket's back wall: cells -7, -6, -5 go
GUARD_Y = -6                             # the guard plate's cell (one in from the wall)
STROKE = 23                              # the pump's travel = the port's length, so the guard clears the port
TRIGGER = (44, 51, -1.5, 1.5, -49, -40.5)
GRIP = (0, 30, -75, -36)                 # x0, x1, z0, z1: the bird's-head grip (the hand's middle)
SHELL_K = 1.0                            # 12 gauge at real size (big_shell: 5.9 cubes across, 20.5 long)

CLASSES = {"ep1": ("Shotgun.txt", ["pumpaction"]), "afterglow": ("Shotgun.txt", ["pumpaction"])}
RIG = Rig(cycle={"pump": STROKE, "bolt": STROKE}, trigger="trigger", trigger_back=1.5,
          rounds={"shell": (0.0, 0.0, -14.0)}, cycle_in_reload=True)


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    x0, x1, z0, z1 = PORT

    def clean(x, y, z):                  # the receiver's own colour from behind the port, same height
        return g.col(x - 30, y, z)

    # the left window: paint the receiver's colour over it
    for c, v in cells_in(m, (x0, x1, 3, 9, z0, z1)):
        v[0] = clean(*c)
    # the right port: a pocket, the guard plate in it
    m.box(x0, x1, WALL_Y - 2, POCKET_BACK_Y, z0, z1, None, size=1.0, carve=True)
    for c, v in cells_in(m, (x0 - 1, x1 + 1, WALL_Y - 2, POCKET_BACK_Y + 1, z0 - 1, z1 + 1)):
        v[0] = mul(clean(*c), 0.35)
    m.part = "bolt"
    m.box(x0, x1, GUARD_Y, GUARD_Y + 1, z0, z1, blocky_steel(4.0), size=1.0)

    # the barrel, hollow
    bore(m, BORE_X0, MUZZLE_X, BARREL[0], BARREL[1], BORE_R)

    # moving parts
    ty, tz, tr = TUBE
    px0, px1 = PUMP_X
    set_part(m, lambda x, y, z: px0 <= x < px1 and z < PUMP_TOP_Z and math.hypot(y - ty, z - tz) >= tr, "pump")
    a0, a1, b0, b1, c0, c1 = TRIGGER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "trigger")
    set_part(m, lambda x, y, z: GRIP[0] <= x < GRIP[1] and GRIP[2] <= z < GRIP[3], "grip")

    cut_scratches(m, 11, 22, sides=("+y", "-y", "+z"), parts={"body", "pump", "grip"})

    # the shell pushed up into the loading port under the receiver on a reload (hidden until then; built just under
    # the receiver so it overlaps nothing), and the flashes
    big_shell(m, "shell", 62.0, -0.5, -43.0, SHELL_K)
    flashes(m, MUZZLE_X, BARREL[1], BARREL[0], scale=0.6)
    return m
