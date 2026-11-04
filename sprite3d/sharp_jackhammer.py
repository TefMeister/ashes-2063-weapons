"""The JackHammer in sharp cubes (2026-11-04, home PC). A forge design: forge_make.py builds it.

Tefa, after the sharp sawn-off: "please carry on with all the rest in this style". Same look (sharp_kit.py). It
follows the game's side pickup picture (JHAMA0, 40 x 23, read at run time) and the first cube pass's reading of it:
a red ribbed engine at the back with a silver vented cover, a rope-wrapped hoop handle over it, a black base with
yellow hazard stripes, a black front housing with a D-handle on top (where the right hand holds it), a pipe under
it, and a thick blunt iron rod out of a collar at the front (Tefa, 2026-11-05: a chainsaw-bulky body, a blunt rod
to repel enemies).
Moving parts (make_job_jackhammer.py): the rod hammers out and back, the throttle lever in the D-handle.
"""
import math

from forge import hash01, mix
from sharp_kit import (BRIGHT_METAL, GUNMETAL, Profile, SURF, Picture, body, darken, finish, plates, screws, seam,
                       start, toned)
from sharp_settings import JCK_LENGTH_M

NAME = "sharp_jackhammer"
SIDE_SPRITE = "Sprites/Weapons/JHAMA0.png"
RED = [(112, 20, 18), (164, 32, 26), (206, 60, 46)]
BLACK = [(20, 20, 22), (30, 30, 33), (46, 46, 50)]
SILVER = [(96, 98, 104), (132, 134, 140), (170, 172, 176)]
YELLOW = (204, 168, 40)
ROPE = [(112, 88, 54), (150, 120, 76), (184, 154, 100)]
# 2026-11-05, Tefa: "jachammer needs to be with a thick and bulky body like a chainsaw and the tip needs to be a thick
# iron blunt rod to repel enemies, not a sharp one"
ENG_W, HOUSE_W = 22.0, 20.0
ROD_R = 4.5


def build():
    pic = Picture(SIDE_SPRITE, JCK_LENGTH_M)
    X, Z = pic.X, pic.Z
    m = start(NAME)
    black = toned(pic, BLACK, pic.thresholds(12, 37, 11, 17), 21, rust=0.05)
    HZ = Z(14.4)                                     # the housing's (and chisel's) axis

    # --- engine: red and ribbed at the back, a silver vented cover on each side further forward
    red = toned(pic, RED, pic.thresholds(0, 6, 6, 16), 23)
    body(m, "engine", [(X(0.4), Z(6.2)), (X(6.8), Z(5.8)), (X(12.0), Z(6.2)), (X(12.0), Z(17.2)), (X(0.4), Z(17.2))],
         ENG_W / 2, 2.5, lambda x, y, z: red(x, y, z) if x < X(6.6) else black(x, y, z))
    for k in range(int((Z(6.6) - Z(16.6)) / 2.5)):                          # cooling fins: cut grooves
        z = Z(16.6) + 1.5 + k * 2.5
        m.box(X(0.4) - 1, X(6.6), -ENG_W, ENG_W, z, z + 1.0, None, size=SURF, carve=True)
    darken(m, lambda x, y, z: x < X(6.6) and (int(math.floor((z - Z(16.6) - 1.5) * 2)) % 5) in (0, 1), 0.7)
    plates(m, X(6.8), X(11.6), Z(15.8), Z(7.2), ENG_W / 2, toned(pic, SILVER, (0.3, 0.5), 25))
    for k in range(4):                                                      # vents in the silver cover
        z = Z(14.8) + k * 3.5
        for side in (-1, 1):
            y0, y1 = (ENG_W / 2 - 0.5, ENG_W / 2 + 1) if side > 0 else (-ENG_W / 2 - 1, -ENG_W / 2 + 0.5)
            m.box(X(7.6), X(10.8), y0, y1, z, z + 1.0, None, size=SURF, carve=True)
    screws(m, [(X(7.2), Z(7.6)), (X(11.2), Z(7.6)), (X(7.2), Z(15.4)), (X(11.2), Z(15.4))], ENG_W / 2 + 0.5)

    # --- base under the engine: black, yellow hazard stripes
    def base_col(x, y, z):
        if X(4.0) <= x < X(9.4) and Z(20.2) <= z < Z(17.8) and abs(y) > ENG_W / 2 - 1.5:
            return YELLOW if int(math.floor((x + z) / 4.0)) % 2 else BLACK[0]
        return black(x, y, z)
    body(m, "engine", [(X(1.0), Z(17.2)), (X(13.0), Z(17.2)), (X(13.0), Z(22.0)), (X(12.0), Z(22.6)),
                       (X(2.0), Z(22.6)), (X(1.0), Z(21.6))], ENG_W / 2, 2.0, base_col, keep=True)

    # --- hoop handle over the engine, wrapped in rope
    cx, cz, rx, rz, tr = X(6.8), Z(6.0), X(4.4), X(5.4), 1.8

    def rope_col(x, y, z):
        a = math.atan2(z - cz, x - cx)
        return ROPE[0] if int(math.floor(a * 30)) % 3 == 0 else ROPE[1 if hash01(int(x * 2), int(y * 2), 3) < 0.7 else 2]
    m.part = "handle"
    for d in range(0, 181, 3):
        a = math.radians(d)
        px_, pz_ = cx + rx * math.cos(a), cz + rz * math.sin(a)
        m.fill(lambda x, y, z, px_=px_, pz_=pz_: (x - px_) ** 2 + y * y + (z - pz_) ** 2 < tr * tr,
               (px_ - tr - 0.5, px_ + tr + 0.5, -tr - 0.5, tr + 0.5, pz_ - tr - 0.5, pz_ + tr + 0.5), rope_col,
               size=SURF, keep=True)

    # --- front housing: black, seams and rivets; the collar the chisel comes out of
    body(m, "housing", [(X(12.0), Z(9.6)), (X(35.0), Z(9.6)), (X(37.6), Z(11.4)), (X(37.6), Z(17.4)),
                        (X(36.0), Z(18.8)), (X(12.0), Z(18.8))], HOUSE_W / 2, 4.5, black, keep=True)
    # a round starter cover standing out of the right side, as on a chainsaw, and vents in the left
    m.part = "housing"
    scx, scz, sr = X(28.0), Z(14.2), 8.0
    m.fill(lambda x, y, z: (x - scx) ** 2 + (z - scz) ** 2 < sr * sr and -HOUSE_W / 2 - 1.5 <= y < -HOUSE_W / 2 + 1.0,
           (scx - sr - 1, scx + sr + 1, -HOUSE_W / 2 - 2, -HOUSE_W / 2 + 1, scz - sr - 1, scz + sr + 1),
           toned(pic, SILVER, (0.3, 0.5), 29), size=1.0, edge=SURF)
    for k in range(5):
        x = scx - 6.0 + k * 3.0
        m.box(x, x + 1.0, -HOUSE_W / 2 - 2, -HOUSE_W / 2 - 0.5, scz - 5.0, scz + 5.0, None, size=SURF, carve=True)
    for k in range(6):
        x = X(29.0) + k * 2.5
        m.box(x, x + 1.0, HOUSE_W / 2 - 1.0, HOUSE_W / 2 + 1, Z(16.8), Z(11.6), None, size=SURF, carve=True)
    seam(m, X(13.0), X(36.5), Z(17.4), HOUSE_W / 2)
    screws(m, [(X(14.0 + 4 * k), Z(10.8)) for k in range(5)], HOUSE_W / 2, mix(BLACK[2], BRIGHT_METAL, 0.3))
    m.part = "housing"
    m.cyl(X(37.6), X(38.8), 0.0, HZ, ROD_R + 2.0, toned(pic, SILVER, (0.3, 0.5), 27), edge=SURF)
    # the pipe under it, on two brackets
    m.part = "pipe"
    m.cyl(X(13.0), X(37.0), 0.0, Z(20.4), 3.0, black, edge=SURF)
    for x in (X(16.0), X(33.0)):
        m.box(x, x + 2.0, -2.0, 2.0, Z(20.4), Z(18.8), black, size=SURF)

    # --- D-handle on top (the right hand holds it: part "grip"), rubber on its bar; the throttle lever inside
    m.part = "grip"
    hout = Profile([(X(20.0), Z(11.6)), (X(27.2), Z(11.6)), (X(27.2), Z(4.6)), (X(22.0), Z(4.6)), (X(20.0), Z(6.5))])
    hole = Profile([(X(21.6), Z(11.6)), (X(25.6), Z(11.6)), (X(25.6), Z(6.2)), (X(22.6), Z(6.2)), (X(21.6), Z(7.4))])
    hs = hout.solid(lambda x: 2.5, 1.0)

    def dcol(x, y, z):
        if x >= X(25.6):                                                    # the back bar: rubber, grooved
            return BLACK[0] if int(math.floor(z)) % 3 == 0 else BLACK[1]
        return black(x, y, z)
    m.fill(lambda x, y, z: hs(x, y, z) and hole.sd(x, z) <= 0, hout.bounds(3.0), dcol, size=1.0, edge=SURF, keep=True)
    m.part = "trigger"
    m.box(X(24.6), X(25.6), -1.0, 1.0, Z(9.4), Z(6.6), mix(BLACK[2], BRIGHT_METAL, 0.3), size=SURF)

    # --- the rod (moves): a thick blunt iron bar out of the collar, a rounded, mushroomed striking face
    m.part = "chisel"
    iron = toned(pic, [(54, 54, 58), (78, 78, 82), (108, 108, 112)], (0.3, 0.5), 33, rust=0.2)
    m.cyl(X(35.0), X(41.4), 0.0, HZ, ROD_R, iron, edge=SURF)

    def head(x, y, z):
        if not (X(41.4) <= x < X(41.4) + 4.0):
            return False
        t = (x - X(41.4)) / 4.0
        r = ROD_R + 1.2 - 2.2 * max(0.0, t - 0.5) ** 2 * 4                  # swells, then rounds over at the face
        return math.hypot(y, z - HZ) < r
    m.fill(head, (X(41.4), X(41.4) + 4.5, -ROD_R - 2, ROD_R + 2, HZ - ROD_R - 2, HZ + ROD_R + 2),
           lambda x, y, z: mix(iron(x, y, z), BRIGHT_METAL, 0.35 if x > X(41.4) + 3.0 else 0.1), size=SURF)

    finish(m, ["engine", "housing", "pipe", "chisel"], ["handle"])
    return m
