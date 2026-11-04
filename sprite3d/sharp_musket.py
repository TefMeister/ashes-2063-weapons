"""The Junker Musket in sharp cubes (2026-11-04, home PC). A forge design: forge_make.py builds it.

Tefa, after the sharp sawn-off: "please carry on with all the rest in this style". Same look (sharp_kit.py). The
rifle follows the game's side pickup picture (MKTPA0, 69 x 23, read at run time): a long orange-brown wooden stock, a
steel receiver lashed to the barrel with red cord, a big tan scope on two black mounts with turrets, a wooden
fore-end, wire wound round the barrel, a pipe muzzle with holes, a bolt with its handle on the right.
Moving parts (make_job_musket.py): the bolt handle lifts and the bolt runs back on each shot and to reload, a round
goes in through the open action, the trigger, three flashes.
"""
import math

from forge import hash01, mix
from sharp_kit import (BRASS, BRIGHT_METAL, GUNMETAL, PUMP_WOOD, SURF, Picture, barrel, blade, body, darken, finish,
                       flashes, guard, start, toned)
from sharp_settings import MSK_BOLT_ROW, MSK_LENGTH_M, park_z

NAME = "sharp_musket"
SIDE_SPRITE = "Sprites/Weapons/MKTPA0.png"
ORANGE_WOOD = [(90, 44, 20), (136, 70, 32), (178, 104, 52)]
SCOPE_TAN = [(96, 74, 44), (142, 112, 66), (196, 162, 92)]
RED_CORD = [(90, 18, 16), (138, 30, 24), (176, 48, 36)]
WIRE = (150, 146, 136)
GLASS = (30, 40, 64)
REC_W = 11.0


def build():
    pic = Picture(SIDE_SPRITE, MSK_LENGTH_M)
    X, Z = pic.X, pic.Z
    m = start(NAME)
    steel = toned(pic, GUNMETAL, pic.thresholds(20, 35, 8, 13), 21, rust=0.18)
    BZ, BR = Z(9.8), 3.6
    MZ = X(66.6)
    BOLT_Z = Z(MSK_BOLT_ROW)

    # --- stock: long, orange-brown, a dark butt plate
    spoly = [(X(3.2), Z(10.8)), (X(14.0), Z(10.0)), (X(20.0), Z(9.8)), (X(24.6), Z(10.0)), (X(24.6), Z(14.4)),
             (X(21.5), Z(16.4)), (X(14.5), Z(16.8)), (X(10.0), Z(18.0)), (X(7.0), Z(19.4)), (X(4.4), Z(19.4)),
             (X(3.4), Z(18.5)), (X(3.0), Z(12.0))]
    wood = toned(pic, ORANGE_WOOD, pic.thresholds(4, 23, 10, 18), 71)
    body(m, "stock", spoly, lambda x: 6.5 - 0.6 * min(max((x - X(4)) / (X(22) - X(4)), 0), 1), 4.0,
         lambda x, y, z: mix(GUNMETAL[0], (30, 30, 30), 0.3) if x < X(3.9) else wood(x, y, z))

    # --- receiver: steel, the ejection port on the top right, a slot for the bolt handle
    body(m, "receiver", [(X(20.0), Z(9.0)), (X(35.5), Z(8.2)), (X(35.5), Z(12.6)), (X(34.0), Z(14.0)),
                         (X(24.6), Z(14.0)), (X(20.0), Z(12.0))], REC_W / 2, 2.0, steel, keep=True)
    port = (X(28.0), X(34.0), -REC_W / 2 - 1, 1.0, BOLT_Z - 1.5, Z(8.2) + 1)
    m.box(*port, None, size=SURF, carve=True)
    darken(m, lambda x, y, z: port[0] - 0.5 <= x < port[1] + 0.5 and y < 1.5 and z >= port[4] - 0.5, 0.5)
    m.box(X(21.0), X(27.4), -REC_W / 2 - 1, -REC_W / 2 + 1.0, BOLT_Z - 1.5, BOLT_Z + 1.5, None, size=SURF, carve=True)

    # --- bolt (moves): its rear shroud, the handle out to the right with a round knob
    m.part = "bolt"
    bcol = mix(GUNMETAL[2], BRIGHT_METAL, 0.35)
    m.cyl(X(18.6), X(21.0), 0.0, BOLT_Z, 2.6, steel, edge=SURF)
    m.box(X(25.0), X(26.4), -REC_W / 2 - 3.5, -1.0, BOLT_Z - 0.75, BOLT_Z + 0.75, bcol, size=SURF)
    m.box(X(25.0), X(26.4), -REC_W / 2 - 3.5, -REC_W / 2 - 2.0, BOLT_Z - 4.0, BOLT_Z, bcol, size=SURF)
    m.fill(lambda x, y, z: (x - X(25.7)) ** 2 + (y + REC_W / 2 + 2.75) ** 2 + (z - BOLT_Z + 4.5) ** 2 < 2.4 ** 2,
           (X(25.7) - 3, X(25.7) + 3, -REC_W / 2 - 6, -REC_W / 2, BOLT_Z - 8, BOLT_Z - 1), bcol, size=SURF)

    # --- fore-end under the barrel, the barrel, wire wound on it, the pipe muzzle with holes
    body(m, "forend", [(X(35.5), Z(9.4)), (X(52.0), Z(9.6)), (X(52.0), Z(12.0)), (X(50.5), Z(13.0)),
                       (X(35.5), Z(13.0))], 5.0, 2.5, toned(pic, PUMP_WOOD, pic.thresholds(36, 51, 10, 12), 81),
         exclude=lambda x, y, z: math.hypot(y, z - BZ) < BR)
    barrel(m, "barrel", X(35.0), X(58.0), 0.0, BZ, BR, 1.6, toned(pic, GUNMETAL, pic.thresholds(40, 58, 7, 11), 31,
                                                                    rust=0.25))
    m.part = "barrel"
    for x0 in (X(41.0), X(53.5), X(55.6)):
        m.fill(lambda x, y, z, x0=x0: x0 <= x < x0 + 2.0 and BR - 0.25 <= math.hypot(y, z - BZ) < BR + 0.75,
               (x0, x0 + 2, -BR - 1, BR + 1, BZ - BR - 1, BZ + BR + 1),
               lambda x, y, z: WIRE if int(math.floor(x * 2)) % 2 else mix(WIRE, (60, 58, 54), 0.5), size=SURF)
    barrel(m, "barrel", X(58.0), MZ, 0.0, BZ, 4.6, 2.2, toned(pic, GUNMETAL, pic.thresholds(58, 66, 7, 11), 33,
                                                                rust=0.2))
    for k in range(3):
        x = X(59.5) + k * 2.5
        for yc in (-4.6, 4.6):
            m.box(x, x + 1.0, yc - 1, yc + 1, BZ - 0.5, BZ + 0.5, None, size=SURF, carve=True)

    # --- red cord lashing: one band round the receiver's front, one round the barrel
    def cord_col(x, y, z):
        if (int(math.floor(x * 2)) + int(math.floor(z * 2))) % 3 == 0:
            return RED_CORD[0]                                              # the turns of the cord, in shadow
        return RED_CORD[1 if hash01(int(x * 2), int(y * 2), int(z * 2), 61) < 0.7 else 2]
    m.part = "cord"
    x0, x1 = X(31.4), X(33.8)
    m.fill(lambda x, y, z: x0 <= x < x1 and abs(y) < REC_W / 2 + 0.75 and Z(12.8) <= z < Z(8.4) + 0.75,
           (x0, x1, -REC_W, REC_W, Z(13.5), Z(8)), cord_col, size=SURF)
    x2, x3 = X(36.2), X(38.6)
    m.fill(lambda x, y, z: x2 <= x < x3 and BR - 0.25 <= math.hypot(y, z - BZ) < BR + 1.0,
           (x2, x3, -BR - 2, BR + 2, BZ - BR - 2, BZ + BR + 2), cord_col, size=SURF)

    # --- scope: a big tan tube with bells, glass, two black mounts, turrets
    SZ = Z(5.0)
    scol = toned(pic, SCOPE_TAN, pic.thresholds(27, 47, 3, 6), 41)
    m.part = "scope"
    m.cyl(X(30.0), X(44.0), 0.0, SZ, 4.6, scol, edge=SURF)
    m.cyl(X(27.0), X(30.0), 0.0, SZ, 5.6, scol, edge=SURF)
    m.cyl(X(44.0), X(47.6), 0.0, SZ, 6.2, scol, edge=SURF)
    m.cyl(X(27.0) - 0.5, X(27.0) + 0.5, 0.0, SZ, 4.2, GLASS, edge=SURF)
    m.cyl(X(47.6) - 0.5, X(47.6) + 0.5, 0.0, SZ, 4.8, GLASS, edge=SURF)
    for xc in (X(32.5), X(38.6)):
        m.fill(lambda x, y, z, xc=xc: math.hypot(x - xc, y) < 2.0 and SZ + 4.0 <= z < SZ + 6.5,
               (xc - 3, xc + 3, -3, 3, SZ + 3, SZ + 7), mix(SCOPE_TAN[1], BRASS, 0.3), size=SURF)
    for xc in (X(29.0), X(37.0)):
        m.box(xc - 1.5, xc + 1.5, -3.0, 3.0, Z(8.4), SZ - 3.5, toned(pic, [(18, 18, 20), (28, 28, 31), (40, 40, 44)],
                                                                    (0.2, 0.3), 43), size=1.0, edge=SURF, keep=True)
    for k in range(5):                                                      # white scribbles on the tube
        x = X(31.0) + k * 2.6
        m.box(x, x + 0.5, -4.8, -4.2, SZ - 1.0 + (k % 2), SZ + 0.5 + (k % 2), (210, 206, 190), size=SURF, keep=True)

    # --- trigger guard and trigger
    guard(m, X(24.8), X(31.0), Z(14.0), Z(17.0), steel, w=3.5, bar=1.8)
    blade(m, X(27.0), Z(14.0), Z(16.2), mix(GUNMETAL[2], BRIGHT_METAL, 0.4), lean=0.3)

    # --- the round fed into the open action, built parked above the port
    m.part = "round"
    pz = park_z(1)
    m.cyl(X(28.6), X(28.6) + 10.0, 0.0, BOLT_Z + pz, 1.5, BRASS, edge=SURF)
    m.cyl(X(28.6) + 10.0, X(28.6) + 13.0, 0.0, BOLT_Z + pz, 1.0, (150, 96, 60), edge=SURF)

    flashes(m, MZ + 0.5, BZ, scale=0.95)
    finish(m, ["receiver", "barrel", "bolt", "guard", "scope"], ["stock", "forend"])
    return m
