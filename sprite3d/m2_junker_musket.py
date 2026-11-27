"""The Junker Musket, Meshy 2026-11-27, in the cube look. A forge design (m2_kit.py).
Measured: barrel to the muzzle at 338 (Meshy made it hollow: y -3, z -62, radius 4.5 inside); the "STOP 2063" scope on
top x 80-210; the receiver x 60-140 with a cream lever on its right side (x 74-93, z -73..-50); trigger x 108-118.
Meshy left the receiver's middle open around x 85 (the inside vote found nothing between the scope mount and the
stock), so it is filled solid in the texture's colours first.
- The barrel is bored from the receiver to the muzzle.
- The bullet cover (Tefa: "bullet cover on the junker rifle"), read here as the cream lever on the receiver's right:
  it flips back on its bottom pivot on a reload and while the gun is worked, and shuts again; the trigger moves.
"""
from m2_anim import Rig
from m2_kit import bore, cut_scratches, fill_box, flashes, load, set_part

NAME = "m2_junker_musket"
FILE = "Junker musket"
LENGTH_M = 1.15
BORE = (-3.0, -62.0, 4.0, 200, 338.2)
GAP = (60, 102, -7, 6, -76, -52)         # the receiver's open middle, filled
COVER = (73, 94, -20, -3.5, -74, -49)    # x0, x1, y0, y1, z0, z1: the lever's cubes on the right side
COVER_PIVOT = (90.0, -6.0, -72.0)
COVER_OPEN = 55.0                        # degrees: positive tips its top back toward the butt
TRIGGER = (106, 120, -2, 2, -107, -92)
GRIP = (58, 106, -104, -74)

CLASSES = {"ep1": ("Musket.txt", ["JunkerMusket"]), "afterglow": ("Musket.txt", ["JunkerMusket"])}
RIG = Rig(open_hinge={"cover": (COVER_OPEN, COVER_PIVOT, 0)}, cycle_hinge={"cover": (COVER_OPEN, COVER_PIVOT, 0)},
          trigger="trigger", trigger_back=1.5, kick=1.2)


def build():
    g, m = load(NAME, FILE, LENGTH_M)
    fill_box(m, GAP, g.col)
    bore(m, BORE[3], BORE[4], BORE[0], BORE[1], BORE[2])
    a0, a1, b0, b1, c0, c1 = COVER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "cover")
    a0, a1, b0, b1, c0, c1 = TRIGGER
    set_part(m, lambda x, y, z: a0 <= x < a1 and b0 <= y < b1 and c0 <= z < c1, "trigger")
    set_part(m, lambda x, y, z: GRIP[0] <= x < GRIP[1] and GRIP[2] <= z < GRIP[3], "grip")
    cut_scratches(m, 81, 30, parts={"body", "grip"})
    flashes(m, BORE[4], BORE[1], BORE[0], scale=0.9)
    return m
