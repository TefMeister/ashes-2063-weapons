"""The revolver in sharp cubes (2026-11-04, home PC). A forge design: forge_make.py builds it.

Tefa, after the sharp sawn-off: "the sawn off looks epic! please carry on with all the rest in this style". Same look
(sharp_kit.py). The gun follows the game's side pickup picture (REVPA0, 34 x 15, read at run time): a heavy revolver
with a ventilated top rib, a full-length underlug, a fluted six-shot cylinder that sticks out past the frame, a hammer
spur, a trigger guard and a pinkish wooden grip with checkered panels on a metal grip frame.
Moving parts (make_job_revolver.py): the cylinder swings out to the left on its crane, six rounds are pushed out and
six go in, the trigger, two flashes.
"""
import math

from forge import hash01, mix
from sharp_kit import (BLUED, BRASS, BRIGHT_METAL, GUNMETAL, Profile, SURF, barrel, blade, body, finish, flashes,
                       guard, screws, seam, start, toned, Picture)
from sharp_settings import REV_CHAMBER_RING, REV_CYL_PX, REV_CYL_R, REV_LENGTH_M, park_z

NAME = "sharp_revolver"
SIDE_SPRITE = "Sprites/Weapons/REVPA0.png"
CYL_STEEL = [(58, 60, 68), (86, 88, 96), (120, 122, 130)]
GRIP_WOOD = [(92, 46, 34), (150, 90, 66), (204, 146, 112)]
FRAME_W = 12.0


def chambers():
    """The six chamber axes (y, z offsets from the cylinder's axis), one at the top in line with the barrel."""
    return [(REV_CHAMBER_RING * math.sin(k * math.pi / 3), REV_CHAMBER_RING * math.cos(k * math.pi / 3))
            for k in range(6)]


def build():
    pic = Picture(SIDE_SPRITE, REV_LENGTH_M)
    X, Z = pic.X, pic.Z
    m = start(NAME)
    CX0, CX1, CZ = X(REV_CYL_PX[0]), X(REV_CYL_PX[1]), Z(REV_CYL_PX[2])
    CR = REV_CYL_R
    BZ = CZ + REV_CHAMBER_RING                   # the barrel lines up with the top chamber
    BR, BORE = 4.0, 1.8
    BX0, MZ = CX1 + 0.5, X(30.5)
    TOP = BZ + BR + 1.5                          # the top strap and rib sit just over the barrel
    metal = toned(pic, BLUED, pic.thresholds(15, 30, 2, 7), 31, rust=0.10)

    # --- barrel, ventilated rib with a front sight, full-length underlug
    barrel(m, "barrel", BX0, MZ, 0.0, BZ, BR, BORE, metal)
    m.part = "barrel"
    m.box(X(15.5), MZ - 0.5, -1.5, 1.5, BZ + BR - 1.0, TOP, metal, size=SURF, keep=True)
    seam(m, BX0, MZ, BZ - BR + 0.25, 2.6)                                    # where the lug meets the barrel
    for k in range(int((MZ - BX0 - 4) / 3.0)):
        x = BX0 + 2.0 + k * 3.0
        m.box(x, x + 1.5, -2, 2, BZ + BR, TOP - 1.0, None, size=SURF, carve=True)      # the rib's vents
    m.box(MZ - 2.5, MZ - 0.5, -0.75, 0.75, TOP, TOP + 2.0, mix(GUNMETAL[2], BRIGHT_METAL, 0.3), size=SURF)
    LUG_BOT = BZ - BR - 4.5
    body(m, "barrel", [(BX0, BZ), (MZ, BZ), (MZ, LUG_BOT + 1.0), (MZ - 1.5, LUG_BOT), (BX0 + 2, LUG_BOT),
                       (BX0, LUG_BOT + 1.5)],
         2.6, 1.5, toned(pic, BLUED, pic.thresholds(20, 30, 5, 7), 33, rust=0.08), keep=True,
         exclude=lambda x, y, z: math.hypot(y, z - BZ) < BR)

    # --- frame: the outline with a window the cylinder fills; top strap with a rear sight notch; hammer spur
    in_cyl = lambda x, y, z: CX0 - 0.5 <= x < CX1 + 0.5 and math.hypot(y, z - CZ) < CR + 0.5  # noqa: E731
    fpoly = [(X(8.5), TOP), (BX0, TOP), (BX0, Z(8.8)), (X(17.0), Z(10.2)), (X(11.0), Z(10.2)), (X(10.3), Z(8.2)),
             (X(9.0), Z(6.2)), (X(8.2), Z(4.2))]
    body(m, "frame", fpoly, FRAME_W / 2, 2.0, toned(pic, GUNMETAL, pic.thresholds(8, 19, 2, 10), 21, rust=0.12),
         exclude=in_cyl)
    m.box(X(9.5), X(10.5), -1.0, 1.0, TOP - 1.0, TOP + 0.5, None, size=SURF, carve=True)
    m.box(X(7.4), X(9.2), -1.5, 1.5, TOP - 2.0, TOP + 2.5, mix(GUNMETAL[2], BRIGHT_METAL, 0.3), size=SURF)
    m.box(X(6.4), X(7.4), -1.5, 1.5, TOP + 1.0, TOP + 2.5, mix(GUNMETAL[2], BRIGHT_METAL, 0.3), size=SURF)
    screws(m, [(X(12.0), Z(9.2)), (X(16.5), Z(9.4))], FRAME_W / 2)

    # --- cylinder (moves): fluted between the chambers, chamber mouths cut into its back face
    m.part = "cylinder"
    ccol = toned(pic, CYL_STEEL, pic.thresholds(11, 19, 5, 9), 41, rust=0.04)    # polished, lighter than the frame
    ch = chambers()

    def cyl_in(x, y, z):
        if not (CX0 <= x < CX1) or math.hypot(y, z - CZ) >= CR:
            return False
        for k in range(6):                                                  # flutes between the chambers
            a = (k + 0.5) * math.pi / 3
            fy, fz = (CR + 0.6) * math.sin(a), CZ + (CR + 0.6) * math.cos(a)
            if math.hypot(y - fy, z - fz) < 1.6 and CX0 + 1.5 <= x < CX1 - 1.5:
                return False
        return True
    m.fill(cyl_in, (CX0, CX1, -CR - 1, CR + 1, CZ - CR - 1, CZ + CR + 1), ccol, size=1.0, edge=SURF)
    for cy, cz in ch:
        m.cyl(CX0 - 0.5, CX0 + 3.0, cy, CZ + cz, 1.9, None, carve=True, edge=None, size=SURF)
        m.cyl(CX1 - 1.5, CX1 + 0.5, cy, CZ + cz, 1.9, None, carve=True, edge=None, size=SURF)

    # --- trigger guard and trigger
    guard(m, X(12.4), X(18.4), Z(10.0), Z(12.2), toned(pic, GUNMETAL, (0.2, 0.3), 61, rust=0.1), w=3.5, bar=1.8)
    blade(m, X(14.6), Z(10.0), Z(11.6), mix(GUNMETAL[2], BRIGHT_METAL, 0.4), lean=0.4)

    # --- grip: wood panels on a metal grip frame (front and back straps), checkered, a screw, a metal butt
    # slanted down and back from under the frame, as a revolver grip (the picture's 4-pixel blob, given its shape)
    gpoly = [(X(11.4), Z(7.0)), (X(10.0), Z(10.0)), (X(8.2), Z(12.7)), (X(4.0), Z(12.7)), (X(3.4), Z(11.6)),
             (X(5.4), Z(8.0)), (X(7.6), Z(5.4)), (X(10.6), Z(5.2))]
    gp = Profile(gpoly)
    wood = toned(pic, GRIP_WOOD, pic.thresholds(4, 10, 6, 11), 71)
    strap = toned(pic, GUNMETAL, (0.2, 0.3), 73, rust=0.1)

    def grip_col(x, y, z):
        if z < Z(12.2) or (abs(y) < 2.0 and gp.sd(x, z) < 1.5):
            return strap(x, y, z)
        return wood(x, y, z)
    m.part = "grip"
    sol = gp.solid(lambda x: 5.5, 3.5)
    m.fill(sol, gp.bounds(5.5), grip_col, size=1.0, edge=SURF, keep=True)
    for i in range(int((X(9.0) - X(5.0)) / 1.0)):
        for j in range(int((Z(8.0) - Z(11.5)) / 1.0)):
            if (i + j) % 2:
                x, z = X(5.0) + i, Z(11.5) + j
                if sol(x + 0.25, 5.0, z + 0.25):
                    m.box(x, x + 0.5, 5.0, 6.5, z, z + 0.5, None, size=SURF, carve=True)
                if sol(x + 0.25, -5.0, z + 0.25):
                    m.box(x, x + 0.5, -6.5, -5.0, z, z + 0.5, None, size=SURF, carve=True)
    screws(m, [(X(7.0), Z(9.6))], 5.0)

    # --- rounds (move; shown with the cylinder swung out), built parked above the cylinder
    m.part = "rounds"
    pz = park_z(1)
    for cy, cz in ch:
        m.cyl(CX0 - 0.5, CX0, cy, CZ + cz + pz, 2.2, mul_b(0.85), edge=SURF)
        m.cyl(CX0, CX1 - 1.0, cy, CZ + cz + pz, 1.7, lambda x, y, z: BRASS if hash01(math.floor(x * 2), 1, 2) < 0.8
              else mix(BRASS, (120, 90, 40), 0.5), edge=SURF)
        m.box(CX0 - 0.5, CX0, cy - 0.5, cy + 0.5, CZ + cz + pz - 0.5, CZ + cz + pz + 0.5, (150, 120, 70), size=SURF)

    flashes(m, MZ + 0.5, BZ, scale=0.75, names=("flash_a", "flash_b"))
    finish(m, ["frame", "barrel", "cylinder", "guard"], ["grip"])
    return m


def mul_b(k):
    return tuple(v * k for v in BRASS)
