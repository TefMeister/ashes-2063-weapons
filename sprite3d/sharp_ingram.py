"""The Ingram in sharp cubes, all three builds (2026-11-04, home PC); sharp_ingram1/2/3.py are the forge designs.

Tefa, after the sharp sawn-off: "please carry on with all the rest in this style". Same look (sharp_kit.py). Each
build follows its own side pickup picture (MPIPA0, MP2PA0, MP3PA0, 46 x 21, read at run time):
1 the bare gun: a boxy stamped receiver with a cocking knob in a slot on top, rear and front sights, a short threaded
  barrel, a front strap, a red-brown plate on the side, a vertical grip round a long magazine, a trigger guard
2 the same with a fat silencer and a wire stock folded along the back, a red safety on the side
3 build 2 blacked.
Moving parts (make_job_ingram.py): the cocking knob runs back on the shot and when cocked after an empty reload, the
magazine drops out and a new one goes in, the trigger, and on the bare gun three flashes (the silenced builds have
none, as in the game).
"""
from forge import hash01, mix
from sharp_kit import (BRIGHT_METAL, GUNMETAL, Profile, SURF, Picture, barrel, blade, body, darken, finish, flashes,
                       guard, plates, screws, seam, start, toned)
from sharp_settings import ING_LENGTH_M

PICS = {1: "Sprites/Weapons/MPIPA0.png", 2: "Sprites/Weapons/MP2PA0.png", 3: "Sprites/Weapons/MP3PA0.png"}
STAMPED = [(44, 46, 52), (66, 68, 76), (98, 100, 108)]
BLACKED = [(22, 22, 25), (34, 34, 38), (52, 52, 58)]
POLYMER = [(24, 24, 26), (34, 34, 37), (48, 48, 52)]
RED = [(96, 18, 16), (150, 30, 24), (196, 52, 40)]
MAROON = [(64, 26, 24), (92, 40, 34), (120, 58, 50)]
REC_W, GRIP_W, MAG_W = 13.0, 11.0, 7.0


def make(build):
    pic = Picture(PICS[build], ING_LENGTH_M)
    X, Z = pic.X, pic.Z
    m = start("sharp_ingram%d" % build)
    pal = STAMPED if build < 3 else BLACKED
    steel = toned(pic, pal, pic.thresholds(5, 31, 4, 10), 21, rust=0.10 if build < 3 else 0.03)
    TOP, BOT = Z(4.6), Z(10.6)
    BZ = Z(7.2)
    RX0, RX1 = X(5.5), X(31.0)

    # --- receiver: a stamped box, the top slot the cocking knob runs in, sights, seams and rivets
    body(m, "receiver", [(RX0, TOP), (RX1, TOP), (RX1, BOT), (RX0, BOT)], REC_W / 2, 1.0, steel)
    m.box(X(16.0), X(29.0), -0.75, 0.75, TOP - 1.0, TOP + 1, None, size=SURF, carve=True)
    darken(m, lambda x, y, z: X(16.0) - 0.5 <= x < X(29.0) + 0.5 and abs(y) < 1.25 and z >= TOP - 1.5, 0.5)
    for x0, x1 in ((X(12.6), X(15.6)), (X(29.0), X(30.6))):                 # rear and front sight ears
        for y in (-3.0, 2.0):
            m.box(x0, x1, y, y + 1.0, TOP, TOP + 2.5, steel, size=SURF)
    seam(m, RX0 + 1, RX1 - 1, Z(8.4), REC_W / 2)
    screws(m, [(X(7.0), Z(5.6)), (X(7.0), Z(9.6)), (X(29.6), Z(5.6)), (X(29.6), Z(9.6))], REC_W / 2,
           mix(pal[2], BRIGHT_METAL, 0.3))
    if build == 1:
        plates(m, X(9.0), X(12.5), Z(8.2), Z(6.8), REC_W / 2, toned(pic, MAROON, (0.2, 0.3), 23))

    # --- cocking knob (moves): on a stem in the top slot
    m.part = "bolt"
    m.box(X(27.4), X(28.6), -0.5, 0.5, TOP - 0.5, TOP + 1.0, mix(pal[1], BRIGHT_METAL, 0.3), size=SURF)
    m.cyl(X(26.8), X(29.2), 0.0, TOP + 2.0, 1.6, mix(pal[2], BRIGHT_METAL, 0.3), edge=SURF)

    # --- barrel: short and threaded on the bare gun, a fat silencer and a cap on the other two
    if build == 1:
        barrel(m, "barrel", RX1, X(36.0), 0.0, BZ, 2.6, 1.3, steel)
        for k in range(5):
            x = X(32.0) + k * 1.5
            m.box(x, x + 0.5, -3, 3, BZ + 2.1, BZ + 3, None, size=SURF, carve=True)
        mz = X(36.0)
    else:
        sil = toned(pic, POLYMER if build == 3 else BLACKED, pic.thresholds(31, 40, 5, 10), 25)
        barrel(m, "barrel", RX1 - 1, X(40.0), 0.0, BZ, 5.5, 1.3, sil)
        for k in range(4):                                                  # grip rings cut round the silencer
            x = X(32.5) + k * 2.2
            m.fill(lambda x_, y, z, x=x: x <= x_ < x + 0.5 and (y * y + (z - BZ) ** 2) ** 0.5 > 5.0,
                   (x, x + 0.5, -6, 6, BZ - 6, BZ + 6), None, size=SURF, carve=True)
        barrel(m, "barrel", X(40.0), X(43.8), 0.0, BZ, 3.4, 1.3, steel)
        mz = X(43.8)
        # the wire stock, folded along the back: two rods and a butt plate
        m.part = "stock"
        rod = mix(pal[1], BRIGHT_METAL, 0.15)
        for y in (-4.5, 4.5):
            for z in (Z(6.8), Z(10.0)):
                m.box(X(0.6), RX0 + 1, y - 0.75, y + 0.75, z - 0.75, z + 0.75, rod, size=SURF)
        m.box(X(0.0), X(1.0), -5.5, 5.5, Z(11.0), Z(6.0), toned(pic, POLYMER, (0.2, 0.3), 27), size=SURF)
        m.part = "receiver"
        plates(m, X(10.0), X(14.8), Z(11.4), Z(10.0), REC_W / 2, toned(pic, RED, (0.2, 0.3), 29))   # safety

    # --- front strap under the barrel
    body(m, "receiver", [(RX1, Z(8.6)), (mz - 0.5 if build == 1 else X(33.0), Z(8.6)),
                         (mz - 0.5 if build == 1 else X(33.0), BOT), (RX1, BOT)], 3.0, 1.0, steel)

    # --- trigger guard, trigger
    guard(m, X(15.4), X(21.2), BOT, Z(13.6), steel, w=3.5, bar=1.8)
    blade(m, X(17.0), BOT, Z(12.8), mix(pal[2], BRIGHT_METAL, 0.3), lean=0.3)

    # --- magazine (moves) inside the vertical grip, sticking out below it
    mpoly = [(X(11.8), BOT), (X(14.6), BOT), (X(14.6), Z(17.2)), (X(11.8), Z(17.2))]
    mp = Profile(mpoly)
    in_mag = mp.solid(lambda x: MAG_W / 2, 0.5)
    body(m, "mag", mpoly, MAG_W / 2, 0.5, toned(pic, GUNMETAL, (0.2, 0.35), 41))
    body(m, "mag", [(X(11.4), Z(17.2)), (X(15.0), Z(17.2)), (X(15.0), Z(17.8)), (X(11.4), Z(17.8))], MAG_W / 2 + 0.75,
         0.5, toned(pic, GUNMETAL, (0.2, 0.35), 43))

    # --- grip: polymer round the magazine, grooved
    def grip_col(x, y, z):
        c = toned(pic, POLYMER, pic.thresholds(11, 15, 11, 15), 31)(x, y, z)
        return mix(c, (12, 12, 13), 0.5) if hash01(int(x * 2), int(y * 2), int(z * 2), 51) < 0.2 else c
    body(m, "grip", [(X(11.0), BOT), (X(15.4), BOT), (X(15.2), Z(16.0)), (X(11.2), Z(16.0))], GRIP_W / 2, 2.0,
         grip_col, keep=True, exclude=in_mag)
    for k in range(4):
        z = Z(15.4) + k * 2.5
        seam(m, X(11.0), X(15.4), z, GRIP_W / 2)

    if build == 1:
        flashes(m, mz + 0.5, BZ, scale=0.6)
    finish(m, ["receiver", "barrel", "bolt", "mag", "guard", "stock"], [])
    return m
