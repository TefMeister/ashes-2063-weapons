"""The Master Blaster flamethrower in sharp cubes (2026-11-04, home PC). A forge design: forge_make.py builds it.

Tefa, after the sharp sawn-off: "please carry on with all the rest in this style". Same look (sharp_kit.py). It
follows the game's side pickup picture (LAUPA0, 56 x 18, read at run time) and Tefa's correction on the detailed one
(2026-11-02): both copper tanks ride along the right side and feed a duct-taped Y splitter, one hose goes into the
barrel, none to the gauge. A thick black barrel with a bright ring nozzle and an igniter tube with a small pilot
flame, a red valve wheel on the upper tank, a pressure gauge at the back facing the player, a wooden block at the
back, a black body with a top spine, a red hose looping round the back, a rubber pistol grip.
Moving parts (make_job_blaster.py): the flame at the nozzle (three shapes), the valve wheel turning and the gauge's
needle rising on a reload, the trigger.
"""
import math

from forge import hash01, mix
from sharp_kit import (BRASS, BRIGHT_METAL, GUNMETAL, STOCK_WOOD, SURF, Picture, barrel, blade, body, finish,
                       flashes, guard, seam, start, toned)
from sharp_settings import BLS_GAUGE_PX, BLS_LENGTH_M, BLS_TANK_Y, BLS_VALVE_PX

NAME = "sharp_blaster"
SIDE_SPRITE = "Sprites/Weapons/LAUPA0.png"
TANK_R = 6.5
BLACK = [(20, 20, 22), (30, 30, 33), (44, 44, 48)]
COPPER = [(100, 46, 24), (150, 74, 38), (198, 110, 62)]
RED = [(110, 20, 18), (160, 34, 26), (200, 58, 42)]
HOSE_RED = [(70, 14, 14), (100, 22, 20), (130, 34, 28)]
TAPE = [(92, 92, 96), (120, 120, 124), (150, 150, 154)]


def hose(m, part, pts, r, col):
    """A hose through the points, as overlapping balls (half cubes)."""
    m.part = part
    for (ax, ay, az), (bx, by, bz) in zip(pts, pts[1:]):
        n = max(1, int(math.dist((ax, ay, az), (bx, by, bz)) / 0.75))
        for k in range(n + 1):
            t = k / n
            cx, cy, cz = ax + (bx - ax) * t, ay + (by - ay) * t, az + (bz - az) * t
            m.fill(lambda x, y, z, cx=cx, cy=cy, cz=cz: (x - cx) ** 2 + (y - cy) ** 2 + (z - cz) ** 2 < r * r,
                   (cx - r - 0.5, cx + r + 0.5, cy - r - 0.5, cy + r + 0.5, cz - r - 0.5, cz + r + 0.5), col,
                   size=SURF, keep=True)


def build():
    pic = Picture(SIDE_SPRITE, BLS_LENGTH_M)
    X, Z = pic.X, pic.Z
    m = start(NAME)
    G = lambda row: Z(13.4) + (Z(row) - Z(13.4)) * 1.7  # noqa: E731  (the grip, longer than the picture's stub)
    black = toned(pic, BLACK, pic.thresholds(14, 40, 10, 13), 21, rust=0.06)
    BZ, MZ = Z(8.6), X(48.4)
    TY = BLS_TANK_Y

    # --- body: black, a spine along the top, seams
    body(m, "body", [(X(13.5), Z(10.6)), (X(40.0), Z(10.6)), (X(40.0), Z(13.6)), (X(14.0), Z(13.6))], 6.0, 1.5, black)
    body(m, "body", [(X(11.0), Z(6.4)), (X(39.0), Z(6.4)), (X(39.0), Z(4.6)), (X(11.0), Z(4.6))], 3.0, 1.0, black)
    m.part = "body"
    for x in (X(18.0), X(38.0)):                                            # posts from the spine to the body
        m.box(x, x + 3.0, -2.0, 2.0, Z(10.6), Z(6.4), black, size=1.0, edge=SURF, keep=True)
    seam(m, X(14.5), X(39.5), Z(12.0), 6.0)

    # --- barrel: thick and black, hollow, a bright ring nozzle; the igniter tube on top with a pilot flame
    barrel(m, "barrel", X(36.0), MZ, 0.0, BZ, 4.6, 2.6, black)
    m.part = "barrel"
    m.fill(lambda x, y, z: MZ - 1.5 <= x < MZ and 4.0 <= math.hypot(y, z - BZ) < 5.4,
           (MZ - 2, MZ, -6, 6, BZ - 6, BZ + 6), mix(GUNMETAL[2], BRIGHT_METAL, 0.6), size=SURF)
    for x in (X(41.0), X(44.5)):
        m.fill(lambda x_, y, z, x=x: x <= x_ < x + 1.0 and 4.4 <= math.hypot(y, z - BZ) < 5.0,
               (x, x + 1, -6, 6, BZ - 6, BZ + 6), mix(GUNMETAL[1], BRIGHT_METAL, 0.3), size=SURF)
    IZ = BZ + 4.6 + 2.0                       # the igniter rides on the barrel
    barrel(m, "barrel", X(41.0), X(48.6), 0.0, IZ, 1.8, 0.8, toned(pic, GUNMETAL, pic.thresholds(43, 48, 3, 5), 23))
    m.box(X(42.0), X(43.0), -1.0, 1.0, IZ - 4.0, IZ - 1.5, black, size=SURF)
    for k in range(10):                                                     # the pilot flame: blue core, orange tip
        r = lambda j: hash01(k, j, 77)  # noqa: E731
        x = X(48.6) + 0.25 + r(1) * 1.5
        m.put(x, (r(2) - 0.5) * 1.0, IZ + (r(3) - 0.5) * 1.0, (80, 140, 255) if x < X(48.6) + 1.0 else (255, 170, 60),
              size=0.25, part="barrel")

    # --- two copper tanks along the right side, brass bands, domed ends
    for tz in (Z(7.0), Z(10.3)):
        m.part = "tanks"
        cc = toned(pic, COPPER, pic.thresholds(19, 38, 6, 11), 31 + int(tz))
        m.cyl(X(19.5), X(37.5), TY, tz, TANK_R, cc, edge=SURF)
        for x0, x1, r in ((X(19.0), X(19.5), TANK_R - 1.5), (X(18.6), X(19.0), TANK_R - 3.5),
                          (X(37.5), X(38.0), TANK_R - 1.5), (X(38.0), X(38.4), TANK_R - 3.5)):
            m.cyl(x0, x1, TY, tz, r, cc, edge=SURF)
        for x in (X(23.0), X(33.0)):
            m.cyl(x, x + 1.0, TY, tz, TANK_R + 0.5, mix(BRASS, (90, 70, 30), 0.3), edge=SURF, keep=False)
    # the tanks hang off the body on two straps
    m.part = "tanks"
    for x in (X(22.0), X(34.0)):
        m.box(x, x + 1.5, TY + TANK_R - 1.0, -5.5, Z(11.6), Z(6.0), black, size=SURF, keep=True)

    # --- hoses: from each tank's front into a duct-taped Y splitter, one hose on into the barrel
    yx = X(40.6)
    hcol = toned(pic, BLACK, (0.2, 0.3), 41)
    hose(m, "hoses", [(X(38.4), TY, Z(7.0)), (X(39.6), TY, Z(7.6)), (yx, TY + 0.5, BZ)], 1.2, hcol)
    hose(m, "hoses", [(X(38.4), TY, Z(10.3)), (X(39.6), TY, Z(9.6)), (yx, TY + 0.5, BZ)], 1.2, hcol)
    hose(m, "hoses", [(yx, TY + 0.5, BZ), (yx + 3.0, -5.0, BZ), (X(41.6), -4.0, BZ)], 1.4, hcol)
    m.part = "hoses"
    m.box(yx - 2.0, yx + 2.0, TY - 1.5, TY + 2.5, BZ - 2.0, BZ + 2.0, toned(pic, TAPE, (0.2, 0.3), 43), size=SURF)

    # --- red valve wheel (moves) on a stem over the upper tank
    vx, vz = X(BLS_VALVE_PX[0]), Z(BLS_VALVE_PX[1])
    m.part = "tanks"
    m.box(vx - 0.75, vx + 0.75, TY - 0.75, TY + 0.75, Z(7.0) + TANK_R - 0.5, vz, mix(BRASS, (90, 70, 30), 0.3), size=SURF)
    m.part = "valve"
    rc = toned(pic, RED, (0.2, 0.3), 45)
    m.fill(lambda x, y, z: vz <= z < vz + 1.0 and (3.8 <= math.hypot(x - vx, y - TY) < 5.0
                                                   or (math.hypot(x - vx, y - TY) < 5.0
                                                       and (abs(x - vx) < 0.5 or abs(y - TY) < 0.5))),
           (vx - 6, vx + 6, TY - 6, TY + 6, vz, vz + 1), rc, size=SURF)

    # --- pressure gauge facing the player at the back, its needle (moves)
    gx, gz = X(BLS_GAUGE_PX[0]), Z(BLS_GAUGE_PX[1])
    m.part = "body"
    m.box(gx + 0.5, gx + 2.0, -0.75, 0.75, Z(4.6), gz - 2.0, black, size=SURF)
    m.cyl(gx, gx + 2.0, 0.0, gz, 3.8, mix(BRASS, (90, 70, 30), 0.2), edge=SURF)
    m.cyl(gx - 0.5, gx, 0.0, gz, 3.2, (214, 206, 180), edge=SURF)
    for k in range(5):                                                      # dial marks
        a = math.radians(-120 + k * 60)
        m.box(gx - 1.0, gx - 0.5, 1.8 * math.sin(a) - 0.25, 1.8 * math.sin(a) + 0.25, gz + 1.8 * math.cos(a) - 0.25,
              gz + 1.8 * math.cos(a) + 0.25, (30, 30, 30), size=0.25)
    m.part = "needle"
    for k in range(6):
        m.box(gx - 1.25, gx - 0.75, -0.25 + k * 0.25 - 0.75, k * 0.25 - 0.75, gz - 0.25, gz + 0.25, (200, 30, 24),
              size=0.25)

    # --- wooden block at the back, the red hose looping round behind it
    body(m, "stock", [(X(12.0), Z(7.8)), (X(18.5), Z(7.8)), (X(18.5), Z(11.0)), (X(12.4), Z(11.4))], 5.0, 2.0,
         toned(pic, STOCK_WOOD, pic.thresholds(12, 17, 8, 11), 71))
    cx, cz, R = X(10.4), Z(9.2), X(10.4) - X(6.4)
    loop = [(cx + R * math.sin(a), 0.0, cz + R * math.cos(a)) for a in [math.radians(d) for d in range(30, 331, 15)]]
    hose(m, "hoses", [(X(11.5), 0.0, Z(5.4))] + loop[::-1] + [(X(13.0), 0.0, Z(13.0))], 1.6,
         toned(pic, HOSE_RED, (0.2, 0.3), 47))

    # --- pistol grip, guard, trigger
    body(m, "grip", [(X(14.5), Z(13.4)), (X(19.0), Z(13.4)), (X(18.4), G(16.2)), (X(14.8), G(16.2))], 4.5, 2.0,
         toned(pic, BLACK, pic.thresholds(13, 19, 12, 14), 51), keep=True)
    for k in range(3):
        seam(m, X(14.5), X(19.0), G(15.6) + k * 3.5, 4.5)
    guard(m, X(19.2), X(24.6), Z(13.6), G(15.4), black, w=3.5, bar=1.8)
    blade(m, X(20.8), Z(13.6), G(14.9), mix(GUNMETAL[2], BRIGHT_METAL, 0.4), lean=0.3)

    # --- the flame (moves): three shapes at the nozzle
    flashes(m, MZ + 0.5, BZ, scale=1.25)
    finish(m, ["body", "barrel", "tanks", "guard"], ["stock"])
    return m
