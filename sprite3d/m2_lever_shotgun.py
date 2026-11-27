"""The lever-action shotgun, Hard Reset, Meshy 2026-11-27, in the cube look. A forge design (m2_kit.py).
Measured: barrel to the muzzle at 294 (Meshy hollow there: y -0.5, z -25), the magazine tube and wooden fore-end under
it; the receiver x 60-125; the lever loop x 28-69 under the wrist (pivot at its front, x 68 z -42); trigger x 69-75.
- The barrel is bored from the receiver to the muzzle.
- The lever swings down and forward on its pivot and back up over each cycle (the game's Pump states: work the lever
  after a shot, and when loading), the trigger moves on the shot. Only the lever's own metal moves (the wooden wrist
  it wraps round stays).
"""
from m2_anim import Rig
from m2_kit import bore, cut_scratches, flashes, is_wood, load, set_part

NAME = "m2_lever_shotgun"
FILE = "lever shotgun"
LENGTH_M = 1.00
BORE = (-0.5, -25.0, 2.0, 128, 294.1)
LEVER = (27, 69, -82, -42.5)             # x0, x1, z0, z1
PIVOT = (68.0, 0.0, -42.0)
SWING = 48.0                             # degrees: positive takes the loop down
TRIGGER = (69, 76, -1.5, 1.5, -57, -43)
GRIP = (34, 72, -46, -26)

CLASSES = {"hardreset": ("Shotgun.txt", ["Leveraction"])}
RIG = Rig(cycle_hinge={"lever": (SWING, PIVOT, 0)}, trigger="trigger", trigger_back=1.2, kick=1.2,
          cycle_in_reload=False)


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    bore(m, BORE[3], BORE[4], BORE[0], BORE[1], BORE[2])
    x0, x1, z0, z1 = LEVER
    set_part(m, lambda x, y, z: x0 <= x < x1 and z0 <= z < z1 and not is_wood(g.col(x, y, z)), "lever")
    a0, a1, b0, b1, c0, c1 = TRIGGER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "trigger")
    set_part(m, lambda x, y, z: GRIP[0] <= x < GRIP[1] and GRIP[2] <= z < GRIP[3], "grip")
    cut_scratches(m, 151, 28, parts={"body", "grip"})
    flashes(m, BORE[4], BORE[1], BORE[0], scale=0.7)
    return m
