"""The pipe bomb in sharp cubes (2026-11-04, home PC). A forge design: forge_make.py builds it.

Tefa, after the sharp sawn-off: "please carry on with all the rest in this style". Same look (sharp_kit.py). It
follows the game's side pickup picture (ROCKA0, 30 x 17, read at run time): a grey steel pipe with threaded end caps
and two bands of brown tape, a timer box taped to the front cap with a red light and a strip of blue tape, a black
wire looping up out of the box and back in, a fuse sticking up from the cap.
Moving parts (make_job_pipebomb.py): sparks at the fuse once it is lit; the whole bomb leaves the hand when thrown
and a new one comes back.
"""
import math

from forge import hash01, mix
from sharp_kit import BRIGHT_METAL, GUNMETAL, SURF, Picture, finish, flashes, start, toned

NAME = "sharp_pipebomb"
SIDE_SPRITE = "Sprites/Weapons/ROCKA0.png"
PIPE = [(66, 66, 72), (92, 92, 98), (124, 124, 130)]
TAPE_BROWN = [(66, 30, 26), (90, 44, 36), (112, 60, 48)]
BOX = [(26, 28, 30), (40, 44, 46), (60, 66, 66)]
BLUE = (40, 52, 110)
LED = (230, 30, 24)
FUSE = (150, 112, 52)
FUSE_TIP_PX = (19.4, 4.2)
LENGTH_M = 0.25                 # the 30-pixel picture spans a quarter metre


def tube(m, part, pts, r, col):
    m.part = part
    for (ax, az), (bx, bz) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(bx - ax, bz - az) / 0.4))
        for k in range(n + 1):
            cx, cz = ax + (bx - ax) * k / n, az + (bz - az) * k / n
            m.fill(lambda x, y, z, cx=cx, cz=cz: (x - cx) ** 2 + y * y + (z - cz) ** 2 < r * r,
                   (cx - r - 0.5, cx + r + 0.5, -r - 0.5, r + 0.5, cz - r - 0.5, cz + r + 0.5), col, size=SURF,
                   keep=True)


def build():
    pic = Picture(SIDE_SPRITE, LENGTH_M)
    X, Z = pic.X, pic.Z
    m = start(NAME)
    PZ, PR = Z(10.4), 6.6

    # --- the pipe (the hand holds it: part "grip"), threaded caps, brown tape bands
    m.part = "grip"
    m.cyl(X(1.2), X(17.8), 0.0, PZ, PR, toned(pic, PIPE, pic.thresholds(1, 17, 8, 12), 21, rust=0.2), edge=SURF)
    m.part = "caps"
    cap = toned(pic, PIPE, (0.25, 0.4), 23, rust=0.25)
    for x0, x1 in ((X(0.0), X(1.2)), (X(17.8), X(19.2))):
        m.fill(lambda x, y, z, x0=x0, x1=x1: x0 <= x < x1 and abs(y) < PR + 0.75 and abs(z - PZ) < PR + 0.75
               and abs(y) + abs(z - PZ) < (PR + 0.75) * 1.4, (x0, x1, -PR - 2, PR + 2, PZ - PR - 2, PZ + PR + 2), cap,
               size=SURF)
    for x in (X(1.6), X(16.8)):                                             # the threads showing past the caps
        m.cyl(x, x + 0.5, 0.0, PZ, PR + 0.25, mix(PIPE[1], BRIGHT_METAL, 0.3), edge=SURF)
    m.part = "tape"
    for x0, x1 in ((X(5.6), X(7.4)), (X(15.0), X(16.6))):
        m.cyl(x0, x1, 0.0, PZ, PR + 0.5, lambda x, y, z: TAPE_BROWN[0 if int(math.floor(x * 2)) % 4 == 0 else
                                                                    1 if hash01(int(x * 2), int(y * 2), int(z * 2), 3) < 0.7 else 2],
              edge=SURF)

    # --- the timer box on the front cap: a red light and blue tape on its right side, a panel
    m.part = "box"
    bcol = toned(pic, BOX, pic.thresholds(19, 27, 6, 13), 31)
    m.box(X(19.2), X(27.4), -5.0, 5.0, Z(13.6), Z(6.2), bcol, size=1.0, edge=SURF)
    m.box(X(23.6), X(24.4), -5.5, -4.5, Z(11.0), Z(10.2), LED, size=SURF)
    m.box(X(20.0), X(23.0), -5.5, 5.5, Z(13.6), Z(12.8), BLUE, size=SURF)
    m.box(X(20.0), X(23.0), -5.5, -4.5, Z(10.8), Z(8.0), mix(BOX[2], (60, 90, 70), 0.5), size=SURF)

    # --- the black wire looping up out of the box and back in; the fuse up from the cap
    wire = [(X(22.5), Z(6.2)), (X(24.5), Z(2.5)), (X(27.2), Z(0.4)), (X(28.6), Z(1.2)), (X(29.4), Z(3.5)),
            (X(29.4), Z(8.0)), (X(27.4), Z(8.8))]
    tube(m, "wire", wire, 0.75, (18, 18, 20))
    tube(m, "fuse", [(X(18.8), Z(6.6)), (X(FUSE_TIP_PX[0]), Z(FUSE_TIP_PX[1]))], 0.9, FUSE)

    # --- sparks at the fuse tip (move; hidden until it is lit)
    flashes(m, X(FUSE_TIP_PX[0]) - 1.0, Z(FUSE_TIP_PX[1]) + 1.0, scale=0.22, names=("spark_a", "spark_b"))
    finish(m, ["grip", "caps", "box"], [])
    return m
