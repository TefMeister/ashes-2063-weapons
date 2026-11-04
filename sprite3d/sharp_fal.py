"""The FAL battle rifle in sharp cubes (2026-11-04, home PC). A forge design: forge_make.py builds it.

Tefa, after the sharp sawn-off: "please carry on with all the rest in this style". Same look (sharp_kit.py). The
rifle follows the game's side pickup picture (FWEPA0, 88 x 26, read at run time): a wooden stock with a rubber butt
pad, a steel receiver with the ejection port on the right, a folded-up carry handle, the charging handle on the left,
a black pistol grip, a curved magazine with ribs, a vented wooden handguard, the barrel with its front sight post and
a slotted flash hider.
Moving parts (make_job_fal.py): the magazine drops out and a new one goes in, the charging handle is pulled back
after a reload, the trigger, three flashes.
"""
import math

from forge import hash01, mix
from sharp_kit import (BRIGHT_METAL, GUNMETAL, PUMP_WOOD, RUBBER, STOCK_WOOD, SURF, Picture, Profile, barrel, blade,
                       body, darken, finish, flashes, guard, seam, start, toned)
from sharp_settings import FAL_LENGTH_M

NAME = "sharp_fal"
SIDE_SPRITE = "Sprites/Weapons/FWEPA0.png"
POLYMER = [(24, 24, 26), (34, 34, 37), (48, 48, 52)]
REC_W, GRIP_W, MAG_W, HG_W = 13.0, 10.0, 8.0, 12.0


def build():
    pic = Picture(SIDE_SPRITE, FAL_LENGTH_M)
    X, Z = pic.X, pic.Z
    m = start(NAME)
    steel = toned(pic, GUNMETAL, pic.thresholds(26, 45, 8, 14), 21, rust=0.10)
    BZ = Z(9.8)
    MZ = X(80.5)
    # grip, guard and magazine 1.7x longer below the receiver than the picture draws them (the 9mm's lesson)
    G = lambda row: Z(14.4) + (Z(row) - Z(14.4)) * 1.7  # noqa: E731

    # --- stock: wood from the outline, wider at the butt, a rubber pad with cut grooves
    spoly = [(X(8.2), Z(7.6)), (X(14.0), Z(7.8)), (X(26.0), Z(8.6)), (X(26.0), Z(13.6)), (X(19.0), Z(15.6)),
             (X(8.6), Z(15.6)), (X(8.2), Z(14.6))]
    wood = toned(pic, STOCK_WOOD, pic.thresholds(9, 25, 8, 15), 71)

    def stock_col(x, y, z):
        if x < X(9.2):
            return RUBBER
        return wood(x, y, z)

    def hw(x):
        t = min(max((x - X(9.0)) / (X(25.0) - X(9.0)), 0.0), 1.0)
        return (13.0 + (11.0 - 13.0) * t) / 2
    body(m, "stock", spoly, hw, 3.5, stock_col)
    for k in range(4):
        z = Z(14.6) + 1.5 + k * 3.5
        m.box(X(8.2) - 1, X(8.2) + 1.0, -8, 8, z, z + 1.0, None, size=SURF, carve=True)

    # --- receiver: steel, ejection port on the right, a seam, the charging handle's slot on the left
    body(m, "receiver", [(X(26.0), Z(8.2)), (X(45.5), Z(8.2)), (X(45.5), Z(13.2)), (X(44.0), Z(14.6)),
                         (X(26.0), Z(14.6))], REC_W / 2, 2.0, steel)
    port = (X(34.0), X(41.0), -REC_W / 2 - 1, -REC_W / 2 + 2.5, Z(10.8), Z(9.0))
    m.box(*port, None, size=SURF, carve=True)
    darken(m, lambda x, y, z: port[0] - 0.5 <= x < port[1] + 0.5 and y < port[3] + 0.5
           and port[4] - 0.5 <= z < port[5] + 0.5, 0.5)
    seam(m, X(26.5), X(45.0), Z(12.0), REC_W / 2)
    m.box(X(40.0), X(45.6), REC_W / 2 - 0.5, REC_W / 2 + 1, Z(10.4), Z(10.0), None, size=SURF, carve=True)
    m.part = "receiver"
    m.box(X(37.0), X(44.0), -3.0, 3.0, Z(8.2), Z(8.2) + 1.0, mix(GUNMETAL[2], BRIGHT_METAL, 0.35), size=SURF)

    # --- carry handle, folded up: a loop with a real hole
    m.part = "handle"
    hout = Profile([(X(29.6), Z(8.2)), (X(35.0), Z(8.2)), (X(35.0), Z(3.0)), (X(33.6), Z(2.8)), (X(31.5), Z(4.2)),
                    (X(29.6), Z(5.6))])
    hole = Profile([(X(30.8), Z(8.0)), (X(33.8), Z(8.0)), (X(33.8), Z(4.6)), (X(32.0), Z(5.4)), (X(30.8), Z(6.2))])
    hs = hout.solid(lambda x: 1.75, 0.75)
    m.fill(lambda x, y, z: hs(x, y, z) and hole.sd(x, z) <= 0, hout.bounds(2.0), toned(pic, POLYMER, (0.2, 0.3), 23),
           size=1.0, edge=SURF, keep=True)

    # --- charging handle (moves): a knob out of the left side
    m.part = "bolt"
    m.box(X(43.6), X(45.2), REC_W / 2 - 0.5, REC_W / 2 + 3.5, Z(10.6), Z(9.8), mix(GUNMETAL[2], BRIGHT_METAL, 0.4),
          size=SURF)
    m.box(X(43.6), X(45.2), REC_W / 2 + 2.5, REC_W / 2 + 4.0, Z(11.0), Z(9.4), mix(GUNMETAL[2], BRIGHT_METAL, 0.4),
          size=SURF)

    # --- pistol grip, guard, trigger
    def grip_col(x, y, z):
        c = toned(pic, POLYMER, pic.thresholds(24, 31, 14, 18), 31)(x, y, z)
        return mix(c, (12, 12, 13), 0.5) if hash01(int(x * 2), int(y * 2), int(z * 2), 51) < 0.2 else c
    body(m, "grip", [(X(25.5), Z(14.4)), (X(31.2), Z(14.4)), (X(30.0), G(17.0)), (X(28.8), G(18.6)),
                     (X(24.8), G(18.6)), (X(24.4), G(16.2))], GRIP_W / 2, 2.5, grip_col, keep=True)
    for k in range(3):
        seam(m, X(24.4), X(31.2), G(18.0) + k * 3.0, GRIP_W / 2)
    guard(m, X(30.6), X(36.2), Z(14.6), G(16.8), steel, w=3.5, bar=1.8)
    blade(m, X(32.2), Z(14.6), G(16.2), mix(GUNMETAL[2], BRIGHT_METAL, 0.4), lean=0.3)

    # --- magazine (moves): curved, ribbed
    mcol = toned(pic, GUNMETAL, pic.thresholds(36, 44, 14, 19), 41)
    body(m, "mag", [(X(36.6), Z(14.4)), (X(44.4), Z(14.4)), (X(44.0), G(17.4)), (X(42.4), G(19.8)),
                    (X(36.4), G(19.8)), (X(36.0), G(17.0))], MAG_W / 2, 1.0, mcol)
    m.part = "mag"
    for k in range(5):
        z = G(19.0) + k * 3.0
        for side in (-1, 1):
            m.box(X(37.2), X(43.2), side * (MAG_W / 2) - 0.5, side * (MAG_W / 2) + 0.5, z, z + 1.0,
                  mix(mcol(0, 0, 0), BRIGHT_METAL, 0.25), size=SURF, keep=True)

    # --- handguard: wood, vented with cut slots
    hgcol = toned(pic, PUMP_WOOD, pic.thresholds(46, 67, 8, 13), 81)
    body(m, "handguard", [(X(45.5), Z(7.8)), (X(67.8), Z(7.8)), (X(68.4), Z(9.0)), (X(68.4), Z(12.4)),
                          (X(67.4), Z(13.6)), (X(45.5), Z(13.6))], HG_W / 2, 4.0, hgcol)
    vents = []
    for k in range(7):
        x = X(48.0) + k * (X(66.0) - X(48.0)) / 7
        vents.append((x, x + 2.0))
        for side in (-1, 1):
            y0, y1 = (HG_W / 2 - 1.5, HG_W / 2 + 1) if side > 0 else (-HG_W / 2 - 1, -HG_W / 2 + 1.5)
            m.box(x, x + 2.0, y0, y1, Z(10.8), Z(9.6), None, size=SURF, carve=True)
    darken(m, lambda x, y, z: any(a - 0.5 <= x < b + 0.5 for a, b in vents) and abs(y) > HG_W / 2 - 2.5
           and Z(10.8) - 0.5 <= z < Z(9.6) + 0.5, 0.45)

    # --- barrel, front sight post, flash hider with slots
    barrel(m, "barrel", X(45.5), X(76.5), 0.0, BZ, 2.6, 1.4, steel)
    m.part = "barrel"
    m.box(X(69.4), X(71.4), -1.0, 1.0, BZ + 2.0, Z(7.4), steel, size=SURF)
    m.box(X(69.0), X(71.8), -2.0, 2.0, BZ - 3.0, BZ + 2.5, steel, size=SURF, keep=True)          # gas block
    barrel(m, "barrel", X(76.5), MZ, 0.0, BZ, 3.4, 1.8, toned(pic, GUNMETAL, (0.2, 0.3), 43))
    for k in range(4):                                                      # the flash hider's slots
        a = k * math.pi / 2 + math.pi / 4
        yc, zc = 3.0 * math.cos(a), BZ + 3.0 * math.sin(a)
        m.box(X(77.4), MZ - 0.5, yc - 0.5, yc + 0.5, zc - 0.5, zc + 0.5, None, size=SURF, carve=True)

    flashes(m, MZ + 0.5, BZ, scale=0.9)
    finish(m, ["receiver", "barrel", "bolt", "mag", "guard", "handle"], ["stock", "handguard"])
    return m
