"""The 9mm handgun in sharp cubes (2026-11-04, home PC). A forge design: forge_make.py builds it.

Tefa, after the sharp sawn-off: "please carry on with all the rest in this style". Same look (sharp_kit.py). The gun
follows the game's side pickup picture (GLPPA0, 34 x 15, read at run time): a blocky polymer pistol with a steel
slide (serrations cut at the back, the ejection port on the right with the barrel hood showing, sights), a rail
under the frame, a trigger guard, a slanted stippled grip with finger grooves and a magazine whose floorplate shows.
Moving parts (make_job_handgun.py): the slide runs back on each shot and stays back when empty, the barrel shows in
front of it; the magazine drops out and a new one goes in; the trigger; two flashes.
"""
import math

from forge import hash01, mix
from sharp_kit import (BRASS, BRIGHT_METAL, GUNMETAL, Profile, SURF, Picture, blade, body, darken, finish, flashes,
                       guard, start, toned)
from sharp_settings import GLK_LENGTH_M

NAME = "sharp_handgun"
SIDE_SPRITE = "Sprites/Weapons/GLPPA0.png"
# 2026-11-05, Tefa: "automatic pistol nr2 is needs to be more black, have rust on it and look like a glock 19 a lot
# more": a near-black polymer frame, a black slide with rust coming through, the Glock 19's flat-topped slide with the
# bevelled nose
POLYMER = [(14, 14, 15), (21, 21, 23), (32, 32, 35)]
SLIDE_STEEL = [(18, 18, 20), (27, 27, 30), (40, 40, 44)]
RUSTY = [(84, 46, 26), (112, 62, 34)]
SLIDE_W, FRAME_W, GRIP_W, MAG_W = 10.0, 9.0, 9.5, 6.0
GRIP_STRETCH = 1.7


def build():
    pic = Picture(SIDE_SPRITE, GLK_LENGTH_M)
    X, Z = pic.X, pic.Z
    m = start(NAME)
    MZ = X(28.7)
    # the grip and magazine 1.7x longer below the frame than the picture draws them (its 6-pixel grip came out a
    # stub under the slide); sharp_settings.GLK_MAG_AXIS follows this slant
    G = lambda row: Z(7.2) + (Z(row) - Z(7.2)) * GRIP_STRETCH  # noqa: E731
    BZ, BR, BORE = Z(4.4), 2.4, 1.3
    in_barrel = lambda x, y, z: x >= X(12.0) and math.hypot(y, z - BZ) < BR  # noqa: E731

    # --- barrel (stays): inside the slide, seen in front of it when the slide runs back and through the port
    m.part = "barrel"
    bcol = lambda x, y, z: mix(GUNMETAL[2], BRIGHT_METAL, 0.35)  # noqa: E731
    m.cyl(X(12.0), MZ - 0.5, 0.0, BZ, BR, lambda x, y, z: (14, 14, 16) if math.hypot(y, z - BZ) < BORE + 0.6
          else bcol(x, y, z), hollow=BORE, edge=SURF)

    # --- slide (moves): steel, hollow round the barrel, serrations, port, sights
    scol = toned(pic, SLIDE_STEEL, pic.thresholds(6, 28, 2, 6), 21, rust=0.22, rust_cols=RUSTY)
    body(m, "slide", [(X(6.2), Z(2.1)), (MZ, Z(2.1)), (MZ, Z(7.2)), (X(6.2), Z(7.2))], SLIDE_W / 2, 1.5, scol,
         exclude=in_barrel)
    for k in range(6):                                                      # rear serrations, both sides
        x = X(6.8) + k * 1.5
        for side in (-1, 1):
            y0, y1 = (SLIDE_W / 2 - 0.5, SLIDE_W / 2 + 1) if side > 0 else (-SLIDE_W / 2 - 1, -SLIDE_W / 2 + 0.5)
            m.box(x, x + 0.5, y0, y1, Z(6.6), Z(2.8), None, size=SURF, carve=True)
    port = (X(13.8), X(19.4), -SLIDE_W / 2 - 1, -SLIDE_W / 2 + 2.0, Z(4.6), Z(2.1) + 1)
    m.box(*port, None, size=SURF, carve=True)                               # ejection port, right side, open on top
    darken(m, lambda x, y, z: port[0] <= x < port[1] and y < port[3] + 0.5 and z >= port[4] - 0.5, 0.55)
    m.box(X(6.6), X(8.0), -2.0, 2.0, Z(2.1), Z(2.1) + 1.5, mix(GUNMETAL[1], BRIGHT_METAL, 0.2), size=SURF)
    m.box(X(6.6), X(8.0), -0.5, 0.5, Z(2.1) + 0.5, Z(2.1) + 1.5, None, size=SURF, carve=True)   # rear notch
    m.box(MZ - 2.0, MZ - 0.5, -0.75, 0.75, Z(2.1), Z(2.1) + 1.5, mix(GUNMETAL[1], BRIGHT_METAL, 0.2), size=SURF)
    m.box(MZ - 1.5, MZ - 1.0, -0.25, 0.25, Z(2.1) + 1.0, Z(2.1) + 1.5, (220, 220, 200), size=SURF)  # front dot

    # --- frame: polymer, a rail under the front with cut slots
    pcol = toned(pic, POLYMER, pic.thresholds(6, 21, 6, 9), 31)
    # the slide's nose bevelled all round, as on a Glock
    for side in (-1, 1):
        m.fill(lambda x, y, z, side=side: x > MZ - 3.0 and side * y > SLIDE_W / 2 - (x - (MZ - 3.0)) * 0.6,
               (MZ - 3.5, MZ + 1, -SLIDE_W, SLIDE_W, Z(7.2), Z(2.1) + 1), None, size=SURF, carve=True)
    m.fill(lambda x, y, z: x > MZ - 3.0 and z > Z(2.1) - (x - (MZ - 3.0)) * 0.6,
           (MZ - 3.5, MZ + 1, -SLIDE_W, SLIDE_W, Z(4.0), Z(2.1) + 1), None, size=SURF, carve=True)
    body(m, "frame", [(X(6.2), Z(7.2)), (X(21.5), Z(7.2)), (X(21.5), Z(8.6)), (X(10.4), Z(8.6)), (X(6.2), Z(8.6))],
         FRAME_W / 2, 1.0, pcol)
    for k in range(3):
        x = X(17.4) + k * 2.0
        m.box(x, x + 1.0, -FRAME_W, FRAME_W, Z(8.6) - 0.5, Z(8.6) + 0.5, None, size=SURF, carve=True)

    # --- trigger guard (square at the front, polymer) and trigger
    guard(m, X(10.2), X(19.8), Z(8.6), Z(10.4), toned(pic, POLYMER, (0.15, 0.25), 33), w=3.5, bar=1.6)
    blade(m, X(12.4), Z(8.6), Z(9.9), mix(POLYMER[2], BRIGHT_METAL, 0.2), w=1.25, lean=0.25)

    # --- magazine (moves) inside the grip, its floorplate showing under it; a brass round on top
    mpoly = [(X(9.8), G(7.6)), (X(8.6), G(10.6)), (X(7.7), G(13.0)), (X(4.8), G(13.0)), (X(5.9), G(10.4)),
             (X(7.0), G(7.6))]
    mp = Profile(mpoly)
    in_mag = mp.solid(lambda x: MAG_W / 2, 0.5)
    body(m, "mag", mpoly, MAG_W / 2, 0.5, toned(pic, SLIDE_STEEL, (0.2, 0.35), 41, rust=0.3, rust_cols=RUSTY))
    body(m, "mag", [(X(8.2), G(13.0)), (X(8.0), G(13.9)), (X(3.4), G(13.9)), (X(3.8), G(13.0))], GRIP_W / 2 + 0.25,
         1.0, toned(pic, POLYMER, (0.2, 0.3), 43))
    m.part = "mag"
    m.box(X(7.2), X(9.6), -1.25, 1.25, G(7.6), G(7.6) + 1.0, BRASS, size=SURF)

    # --- grip: slanted, stippled polymer round the magazine, finger grooves cut in its front
    def stipple(x, y, z):
        c = pcol(x, y, z)
        return mix(c, (14, 14, 15), 0.5) if hash01(math.floor(x * 2), math.floor(y * 2), math.floor(z * 2), 51) < 0.25 \
            else c
    gpoly = [(X(10.8), Z(7.2)), (X(9.5), G(10.4)), (X(8.4), G(13.0)), (X(3.8), G(13.0)), (X(3.2), G(12.4)),
             (X(5.4), G(8.6)), (X(6.2), Z(7.2))]
    body(m, "grip", gpoly, GRIP_W / 2, 2.5, stipple, keep=True, exclude=in_mag)
    for k in range(3):                                                      # finger grooves across the front
        zc = G(9.6) - k * 4.0
        t = (zc - Z(7.2)) / (G(13.0) - Z(7.2))
        xf = X(10.8) + (X(8.4) - X(10.8)) * t                               # the grip's front edge at that height
        m.fill(lambda x, y, z, xf=xf, zc=zc: math.hypot(x - xf, z - zc) < 1.1, (xf - 2, xf + 2, -GRIP_W, GRIP_W,
               zc - 2, zc + 2), None, size=SURF, carve=True)

    flashes(m, MZ + 0.5, BZ, scale=0.55, names=("flash_a", "flash_b"))
    finish(m, ["slide", "barrel", "mag"], [])
    return m
