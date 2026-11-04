"""The sawn-off in sharp cubes (2026-11-04, home PC). A forge design: forge_make.py builds it.

Tefa, after the sharp cube shotgun: "it looks pretty damn great, can you please do all the episode 1 weapons like you
did that? because this look, even if needs tweaks, looks really good." Same look (sharp_kit.py): half-cube surfaces,
flat palettes picked by the game's side picture, gaps and ridges cut or added as cubes, round hollow barrels with flat
muzzles, the flash in the smallest cubes.

The gun follows the game's side pickup picture (SAWPA0, 54 x 16, read at run time, never stored here) and its in-hand
frames: a side-by-side double barrel cut short, a wooden fore-end round the barrels held with black tape, a heavy
dark rib under them, a boxlock action with copper side plates and a hinge knuckle, a top lever, two triggers in a
guard, a short wooden pistol grip wrapped in blue cloth with a dented butt cap.
Moving parts (make_job_sawed_off.py maps the game's frames): the barrels with their fore-end and ribs break open on the
hinge, the top lever swings aside, two shells come out and two go in, the triggers, and a flash at each muzzle.
"""
import math

from forge import hash01, mix, mul
from sharp_kit import (BLUED, BORE, BRASS, BRIGHT_METAL, GUNMETAL, PUMP_WOOD, STOCK_WOOD, SURF, Picture, Profile,
                       blade, darken, finish, flashes, grooved, guard, shell, start, toned)
from sharp_settings import (SAWN_BARREL_R, SAWN_BARREL_Y, SAWN_BREECH_PX, SAWN_HINGE_PX, SAWN_LENGTH_M,
                            SAWN_MUZZLE_PX, SAWN_TOP_PX, park_z)

NAME = "sharp_sawed_off"
SIDE_SPRITE = "Sprites/Weapons/SAWPA0.png"

BLUE_CLOTH = [(34, 44, 74), (52, 66, 104), (80, 96, 136)]
COPPER = [(104, 48, 26), (146, 70, 34), (184, 100, 52)]
TAPE = [(16, 16, 18), (28, 28, 31), (42, 42, 46)]
DARK_RIB = [(26, 27, 31), (38, 40, 46), (56, 58, 66)]
SCREW = (164, 162, 158)

AW, A_ROUND = 22.0, 3.0                # action width and rounding (main cubes)
GRIP_W_WRIST, GRIP_W_BUTT, GRIP_ROUND = 12.0, 13.5, 4.0
FOREND_ROUND, LUG_W, LUG_ROUND = 4.0, 9.0, 2.5
GUARD_W, GUARD_BAR = 4.0, 2.2


def build():
    pic = Picture(SIDE_SPRITE, SAWN_LENGTH_M)
    X, Z = pic.X, pic.Z
    m = start(NAME)
    BR, BY = SAWN_BARREL_R, SAWN_BARREL_Y
    TOP = Z(SAWN_TOP_PX)
    ZC = TOP - BR
    BX0, MZ = X(SAWN_BREECH_PX), X(SAWN_MUZZLE_PX)
    HX, HZ = X(SAWN_HINGE_PX[0]), Z(SAWN_HINGE_PX[1])
    A_BOT = Z(12.3)

    def in_barrels(x, y, z, grow=0.0):
        return any(math.hypot(y - yc, z - ZC) < BR + grow for yc in (-BY, BY))

    # --- barrels: two round tubes side by side, hollow, flat sawn muzzles worn bright, a ragged hacksaw edge
    m.part = "barrels"
    bcol = toned(pic, BLUED, pic.thresholds(23, 49, 4, 7), 31, rust=0.14)

    def barrel_col(x, y, z):
        if any(math.hypot(y - yc, z - ZC) < 3.0 + 0.8 for yc in (-BY, BY)):
            return BORE
        if x > MZ - 0.6:
            return mix(bcol(x, y, z), BRIGHT_METAL, 0.5)
        return bcol(x, y, z)
    for yc in (-BY, BY):
        m.cyl(BX0, MZ, yc, ZC, BR, barrel_col, hollow=3.0, edge=SURF, keep=True)
    for i in range(10):                                   # the hacksaw cut: a few nicks out of the muzzle rims
        a = hash01(i, 501) * 2 * math.pi
        yc = (-BY, BY)[i % 2]
        m.box(MZ - 0.5, MZ + 0.5, yc + math.cos(a) * (BR - 0.5) - 0.5, yc + math.cos(a) * (BR - 0.5),
              ZC + math.sin(a) * (BR - 0.5) - 0.5, ZC + math.sin(a) * (BR - 0.5), None, size=SURF, carve=True)

    # --- top rib in the valley between the barrels, matted with cut cross lines, a brass bead at the muzzle
    m.part = "rib"
    m.box(BX0, MZ - 1.0, -2.5, 2.5, ZC, TOP + 0.5, toned(pic, BLUED, (0.2, 0.35), 33), size=SURF, keep=True)
    for k in range(int((MZ - 1.0 - BX0) / 2.0)):
        x = BX0 + 1.0 + k * 2.0
        m.box(x, x + 0.5, -1.5, 1.5, TOP, TOP + 1.0, None, size=SURF, carve=True)
    m.part = "bead"
    m.box(MZ - 3.0, MZ - 1.5, -1.0, 1.0, TOP + 0.5, TOP + 2.0, BRASS, size=SURF)

    # --- the heavy dark rib under the barrels, to the muzzle (the black lower half of the picture)
    m.part = "lug"
    lug = Profile([(BX0, Z(6.3)), (MZ, Z(6.3)), (MZ, Z(10.6)), (MZ - 3.0, Z(11.0)), (BX0 + 4.0, Z(11.0)),
                   (BX0, Z(10.2))])
    lsolid = lug.solid(lambda x: LUG_W / 2, LUG_ROUND)
    m.fill(lambda x, y, z: lsolid(x, y, z) and not in_barrels(x, y, z), lug.bounds(LUG_W / 2),
           toned(pic, DARK_RIB, pic.thresholds(40, 50, 8, 11), 35, rust=0.08), size=1.0, edge=SURF)
    m.box(MZ - 0.5, MZ + 0.5, -2.0, 2.0, Z(10.2), Z(7.0), None, size=SURF, carve=True)   # a slot in its sawn face

    # --- fore-end: wood round the lower half of the barrels and the rib, cut grooves, one band of black tape
    m.part = "forend"
    fpoly = [(X(23.0), Z(5.6)), (X(39.5), Z(5.6)), (X(40.5), Z(7.2)), (X(40.0), Z(10.6)), (X(38.5), Z(11.6)),
             (X(24.5), Z(11.6)), (X(23.0), Z(10.5))]
    fp = Profile(fpoly)
    FW = BY + BR + 1.5
    fout = fp.solid(lambda x: FW, FOREND_ROUND)
    fin = fp.solid(lambda x: FW, FOREND_ROUND, grow=-1.0)
    bands = [(X(26.0), X(26.0) + 1.5), (X(36.5), X(36.5) + 1.5)]
    fg = grooved(fout, fin, bands)
    m.fill(lambda x, y, z: fg(x, y, z) and not in_barrels(x, y, z, 0.01), fp.bounds(FW),
           toned(pic, PUMP_WOOD, pic.thresholds(26, 38, 6, 8), 81), size=1.0, edge=SURF, keep=True)
    fdeep = fp.solid(lambda x: FW, FOREND_ROUND, grow=-1.5)
    darken(m, lambda x, y, z: any(a <= x < b for a, b in bands) and fin(x, y, z) and not fdeep(x, y, z), 0.62)
    tape = fp.solid(lambda x: FW, FOREND_ROUND, grow=0.5)
    tx0, tx1 = X(30.5), X(33.0)

    def tape_col(x, y, z):
        c = TAPE[1 if hash01(math.floor(x * 2), math.floor(y * 2), math.floor(z * 2), 77) < 0.7 else 2]
        return TAPE[0] if abs(x - tx0 - 1.5) < 0.5 else c                 # the overlap of the wrap, darker
    m.fill(lambda x, y, z: tx0 <= x < tx1 and tape(x, y, z) and not fout(x, y, z) and not in_barrels(x, y, z),
           (tx0, tx1, -FW - 1, FW + 1, Z(12), Z(5)), tape_col, size=SURF)
    m.box(X(38.0), X(39.6), -1.5, 1.5, Z(11.6) - 1.0, Z(11.6), mix(GUNMETAL[2], BRIGHT_METAL, 0.4), size=SURF)

    # --- action: a rounded boxlock from the picture's outline; copper side plates with screws, a hinge knuckle
    m.part = "action"
    apoly = [(X(13.0), Z(6.4)), (X(15.0), Z(4.9)), (X(17.0), Z(4.4)), (BX0, Z(4.4)), (BX0, Z(11.4)),
             (X(21.3), A_BOT), (X(14.2), A_BOT), (X(13.0), Z(11.4))]
    act = Profile(apoly)
    m.fill(act.solid(lambda x: AW / 2, A_ROUND), act.bounds(AW / 2),
           toned(pic, GUNMETAL, pic.thresholds(13, 22, 5, 12), 21, rust=0.16), size=1.0, edge=SURF)
    for side in (-1, 1):
        y0, y1 = (AW / 2 - 0.5, AW / 2 + 0.5) if side > 0 else (-AW / 2 - 0.5, -AW / 2 + 0.5)
        m.box(X(15.4), X(19.3), y0, y1, Z(8.8), Z(6.6), toned(pic, COPPER, pic.thresholds(15, 19, 6, 8), 23),
              size=SURF, keep=True)
        for sx, sz in ((X(16.0), Z(7.2)), (X(18.6), Z(8.2))):
            yc = side * (AW / 2 + 0.5)
            m.box(sx - 0.5, sx + 0.5, yc - 0.5, yc + 0.5, sz - 0.5, sz + 0.5, SCREW, size=SURF)
        m.box(X(13.6), X(21.6), y0 - side * 0.5, y1 - side * 0.5, Z(10.0), Z(9.8), None, size=SURF, carve=True)
    kr = 2.6
    m.fill(lambda x, y, z: math.hypot(x - HX, z - HZ) < kr and abs(y) < AW / 2 + 0.5,
           (HX - kr - 1, HX + kr + 1, -AW / 2 - 1, AW / 2 + 1, HZ - kr - 1, HZ + kr + 1),
           lambda x, y, z: mix(GUNMETAL[2], BRIGHT_METAL, 0.55 if abs(y) > AW / 2 - 0.6 else 0.2), size=SURF)
    m.box(X(12.0), X(13.2), -1.0, 1.0, Z(6.3), Z(6.3) + 1.0, mix(GUNMETAL[2], BRIGHT_METAL, 0.5), size=SURF)  # safety

    # --- top lever (moves aside when the gun breaks open): a bar on the action with a checkered thumb spade
    m.part = "lever"
    lz0 = Z(4.4) + 0.5
    # sunk one cube into the action, so it never floats; swung aside it leaves its slot showing
    m.box(X(14.6), X(18.4), -2.2, 2.2, lz0 - 1.5, lz0 + 2.0, mix(GUNMETAL[2], BRIGHT_METAL, 0.35), size=SURF)
    m.box(X(12.8), X(14.6), -3.0, 3.0, lz0 + 0.5, lz0 + 2.0, mix(GUNMETAL[2], BRIGHT_METAL, 0.35), size=SURF)
    for i in range(5):
        for j in range(5):
            if (i + j) % 2:
                m.box(X(12.8) + i * 0.5 + 0.5, X(12.8) + i * 0.5 + 1.0, -2.5 + j, -2.0 + j, lz0 + 1.5, lz0 + 2.0,
                      None, size=SURF, carve=True)

    # --- trigger guard, its finger hole carried up into the action (2026-11-05); two triggers (move) hang from there
    gx0, gx1, gbot = X(15.0), X(21.4), Z(14.4)
    guard(m, gx0, gx1, A_BOT, gbot, toned(pic, GUNMETAL, (0.2, 0.3), 61, rust=0.1), w=GUARD_W, bar=GUARD_BAR)
    for tx in (X(16.8), X(18.6)):
        blade(m, tx, A_BOT, gbot + GUARD_BAR + 0.5, mix(GUNMETAL[2], BRIGHT_METAL, 0.4), lean=0.3)

    # --- grip: wood from the picture's outline, the wrist wrapped in blue cloth with a loose tail, a dented butt cap
    m.part = "grip"
    gpoly = [(X(13.5), Z(6.4)), (X(11.0), Z(6.9)), (X(8.0), Z(7.6)), (X(5.5), Z(8.8)), (X(3.5), Z(10.2)),
             (X(2.8), Z(12.0)), (X(3.0), Z(14.8)), (X(4.0), Z(15.9)), (X(6.8), Z(15.9)), (X(8.2), Z(14.5)),
             (X(9.3), Z(12.8)), (X(11.5), A_BOT), (X(13.5), A_BOT)]
    gp = Profile(gpoly)

    def hw(x):
        t = min(max((x - X(3.0)) / (X(12.0) - X(3.0)), 0.0), 1.0)
        return (GRIP_W_BUTT + (GRIP_W_WRIST - GRIP_W_BUTT) * t) / 2
    wood = toned(pic, STOCK_WOOD, pic.thresholds(3, 9, 9, 15), 71)
    cap_z = Z(15.2)

    def grip_col(x, y, z):
        if z < cap_z:
            dent = hash01(math.floor(x), math.floor(y), 5) < 0.25
            return mul(mix(BRASS, (70, 56, 30), 0.55), 0.8 if dent else 1.0)
        return wood(x, y, z)
    m.fill(gp.solid(hw, GRIP_ROUND), gp.bounds(GRIP_W_BUTT / 2), grip_col, size=1.0, edge=SURF, keep=True)
    m.box(X(2.0), X(9.0), -8, 8, cap_z - 0.25, cap_z + 0.25, None, size=SURF, carve=True)   # the cap's seam
    wrap = gp.solid(hw, GRIP_ROUND, grow=0.5)
    inner = gp.solid(hw, GRIP_ROUND)
    wx0, wx1 = X(8.3), X(12.8)

    def cloth(x, y, z):
        a = (x - wx0) + 0.5 * (z - Z(9.0))                                 # wound on a slant
        if int(math.floor(a / 1.5)) % 3 == 0:
            return BLUE_CLOTH[0]                                          # the edge of each turn, in shadow
        return BLUE_CLOTH[1 if hash01(math.floor(x * 2), math.floor(y * 2), math.floor(z * 2), 88) < 0.75 else 2]
    m.fill(lambda x, y, z: wx0 <= x + 0.5 * (z - Z(9.0)) < wx1 and wrap(x, y, z) and not inner(x, y, z),
           (wx0 - 12, wx1 + 6, -GRIP_W_BUTT, GRIP_W_BUTT, A_BOT - 2, Z(5.5)), cloth, size=SURF)
    m.box(X(9.6), X(10.4), -GRIP_W_WRIST / 2 - 1.0, -GRIP_W_WRIST / 2 - 0.5, A_BOT - 9.0, A_BOT - 1.0,
          BLUE_CLOTH[1], size=SURF)                                       # the loose tail, on the right side

    # --- shells (move; hidden unless a reload frame shows them): one per chamber, each built parked above it
    shell(m, "shell_r", BX0, -BY, ZC + park_z(1), False)
    shell(m, "shell_l", BX0, BY, ZC + park_z(2), False)

    # --- muzzle flashes (move; hidden unless a firing frame shows them), two per barrel, all in the smallest cubes
    flashes(m, MZ + 0.5, ZC, my=-BY, scale=0.9, names=("flash_ra", "flash_rb"), first=0)
    flashes(m, MZ + 0.5, ZC, my=BY, scale=0.9, names=("flash_la", "flash_lb"), first=2)

    finish(m, ["action", "barrels", "rib", "lug", "guard", "lever"], ["grip", "forend"])
    return m
