# Ashes 2063: the sawed-off shotgun, DETAILED (2026-11-02). Gun only: the body rig's hand docks onto the grip.
#
# Game look (in-hand SAWN*, pickup SAWPA / SAWFA): a dark side-by-side double barrel cut short, a top lever, the stock
# cut down to a wooden pistol grip, red shells showing when broken open.
# Real-life detail (refs/sawed_off.md; boxlock side-by-side photos): tapered matted top rib and a bottom rib between
# the barrels, a brass bead, a boxlock action with scroll engraving worn smooth on the high spots, the hinge knuckle,
# the spade top lever with checkering, a safety slide on the tang marked S, double triggers, guard tang screws, a
# splinter fore-end with its release latch, checkering on the grip.
# Wasteland layer: a ragged hacksaw cut with file marks at the muzzles, rust on the barrels, the cracked fore-end held
# with black electrical tape, the grip wrapped in blue cloth with a loose tail, a dented brass butt cap, chips.
# 2026-11-02, BULKIER (Tefa, after the shotgun: bodies bigger, bulky, worn and dangerous; rounder edges; the handle part
# of the body; a bigger trigger and guard): the action 26 -> 46 long, 11 -> 15 wide, 14.5 -> 22 tall; barrels thicker
# and starting where the bigger action ends; the half-moon guard now a solid block with a finger hole cut up into the
# action; bigger triggers. Every detail kept, moved onto the new body.
import math

from _common import Model, fp, wl, BLACK, STEEL, STEEL_HI, WOOD, WOOD_DK, TAPE_BLUE, BRASS, mul, mix, hash01

BLUED = (52, 54, 58)
ENGRAVE = (150, 150, 146)
Z_BORE = 11.0
BX0, BX1, BR, BORE = 50.0, 130.0, 3.6, 2.4
GAP = 3.6
AX0, AX1, AZ0, AZ1, AW = 6.0, 52.0, -5.0, 15.5, 15.0
# 2026-11-02 (Tefa: "more like doom super shotgun - the part where the barrels come apart when reloading - that has to
# neatly blend into the build and blend into the handle"): the action is a full-width front (the barrels and the hinge
# they break open on) whose top slopes down into a narrower wrist that runs into the grip
ACTION_FRONT = [(30, -5), (30, 15.5), (47, 15.5), (50.5, 14.5), (52, 12.5), (52, 1), (48, -2), (42, -5)]
# (Tefa, the same evening: "roud the guard and the receiver as well to match the curve of the barrels going into it")
GUARD = [(12, -3), (11, -7), (14, -11), (19, -13.5), (37, -13.5), (42, -11), (44, -6), (43, -2)]
ACTION_WRIST = [(2, 1), (8, 5), (20, 11), (34, 15.5), (34, -5), (16, -5), (8, -3)]
FOREND = [(52, 0), (52, 7), (90, 7.5), (94, 5), (92, 0), (56, -1)]
GRIP = [(20, 2), (8, 4), (-4, -2), (-14, -12), (-20, -22), (-8, -26), (2, -14), (14, -4), (24, -1)]


def build():
    m = Model("ashes_sawed_off_detail")
    m.pivot = (12, 0, 0)

    # ---------------------------------------------------------------- barrels, ribs, bead, the hacksaw cut
    m.part = 'barrels'
    for y in (-GAP, GAP):
        fp.barrel(m, BX0, BX1, Z_BORE, BR, fp.metal(BLUED), bore=BORE, yc=y, edge=0.25)
        m.cyl(BX1 - 0.25, BX1 + 0.1, y, Z_BORE, BR - 0.25, None, size=0.25, edge=0.25, carve=True)  # thin walls
    m.part = 'rib'
    m.prism([(BX0, Z_BORE + 2.2), (BX1 - 1, Z_BORE + 2.2), (BX1 - 1, Z_BORE + 3.45), (BX0, Z_BORE + 4.2)], -1.0, 1.0,
            fp.metal(mul(BLUED, 1.1)), size=0.25)
    for x in range(int(BX0) * 2, int(BX1 - 1) * 2):                                  # matted top: fine cross lines
        if x % 2 == 0:
            m.box(x / 2, x / 2 + 0.25, -0.75, 0.75, Z_BORE + 3.2, Z_BORE + 4.2, mul(BLUED, 0.75), size=0.25)
    m.cbox(BX0, BX1 - 3, 3.5, Z_BORE - 4.2, Z_BORE - 2.6, fp.metal(BLUED), size=0.5)       # bottom rib
    m.part = 'bead'
    m.ball(BX1 - 2.5, 0, Z_BORE + 3.95, 0.7, fp.metal(BRASS), size=0.25, edge=0.25)
    m.part = 'barrels'
    for i in range(14):                                                               # ragged cut
        y = -GAP - 2.75 + i * 0.85
        z = Z_BORE + (2.4 if i % 3 else -2.8) + (hash01(i, 501) - 0.5)
        m.box(BX1 - 0.5, BX1, y, y + 0.5, z, z + 0.5, None, size=0.25, carve=True)
    for side, y in (('+y', GAP), ('-y', -GAP)):                                       # file marks
        for k in range(6):
            x = BX1 - 3.0 + k * 0.5
            m.paint_line([(x, Z_BORE - 2), (x + 0.25, Z_BORE + 2)], side, lambda c: mul(c, 1.5))

    # ---------------------------------------------------------------- the action
    m.part = 'action'
    m.cprism(ACTION_FRONT, AW, fp.metal(mul(STEEL, 0.95)), bevel=5.5, edge=0.25)      # round like the barrels
    m.cprism(ACTION_WRIST, AW - 4, fp.metal(mul(STEEL, 0.95)), bevel=4.0, edge=0.25)
    m.cyl(-AW / 2 + 0.5, AW / 2 - 0.5, AX1 - 2.0, 0.5, 2.6, fp.metal(STEEL), axis='y', size=0.25,
          edge=0.25)                                                                    # hinge knuckle
    for side in ('+y', '-y'):                                                          # scroll engraving
        for k in range(26):
            t = k / 25
            a, b = 33 + t * 15, 7.0 + 4.0 * math.sin(t * math.tau * 1.5)
            m.paint_line([(a, b), (a + 0.6, b + 0.4 * math.cos(t * 9))], side, lambda c: mix(c, ENGRAVE, 0.6))
            if k % 4 == 0:
                for r in range(6):
                    ang = r * 1.1
                    m.paint_line([(a + math.cos(ang) * 1.1, b + math.sin(ang) * 1.1),
                                  (a + math.cos(ang + 1.1) * 1.1, b + math.sin(ang + 1.1) * 1.1)], side,
                                 lambda c: mix(c, ENGRAVE, 0.5))
        m.groove([(32, AZ1 - 3), (AX1 - 2, AZ1 - 3)], side, depth=1, dark=0.5)
        m.screw(20, 0, side, mul(STEEL, 0.75), kind='slot')
        m.screw(44, -1.5, side, mul(STEEL, 0.75), kind='cross')
    m.part = 'top_lever'
    m.box(36, 46, -3.5, 1.0, AZ1, AZ1 + 1.0, fp.metal(STEEL_HI), size=0.25, edge=0.25, bevel_x=0.5)
    for k in range(5):
        m.box(36.5 + k * 0.6, 36.75 + k * 0.6, -3.25, -1.0, AZ1 + 0.75, AZ1 + 1.0, mul(STEEL_HI, 0.6), size=0.25)
    m.part = 'safety'
    m.box(30.0, 34.0, -1.0, 1.0, AZ1 - 0.75, AZ1 + 0.25, fp.metal(STEEL_HI), size=0.25)
    m.box(34.5, 35.5, -0.5, 0.5, AZ1 - 0.25, AZ1, (230, 220, 200), size=0.25)            # the S, a white dot

    # ---------------------------------------------------------------- fore-end, grip, guard, triggers
    m.part = 'foreend'
    m.cprism(FOREND, 11.0, fp.wood(WOOD, WOOD_DK), bevel=3.0, edge=0.25)
    m.box(88.0, 91.0, -0.75, 0.75, -1.25, -0.25, fp.metal(STEEL), size=0.25)               # release latch
    for side in ('+y', '-y'):
        fp.checker(m, (60, 84, 1.5, 6.5), side, WOOD, WOOD_DK)
    wl.tape(m, 'x', 70.0, 74.0, (69, 75, -6.0, 6.0, -1.5, 8.5), col=wl.DUCT_BLACK, seed=502, part='tape')
    m.part = 'grip'
    m.cprism(GRIP, 9.0, fp.wood(mul(WOOD, 0.85), WOOD_DK, along='z'), bevel=3.0, edge=0.25)
    m.part = 'butt_cap'
    m.ball(-14, 0, -23, 5.0, fp.metal(BRASS), ry=4.5, rz=4.0, edge=0.25)
    for k in range(3):                                                                  # dents in the cap
        m.ball(-17 + k * 3, 4.3 if k % 2 else -4.3, -24 + k, 0.8, None, size=0.25, edge=0.25, carve=True)
    m.part = 'guard'   # 2026-11-02: part of the action, the finger hole cut up into it
    m.cprism(GUARD, AW - 3, fp.metal(BLUED), bevel=3.5, edge=0.25)
    m.cbox(18, 37, AW + 2, -10.5, -2.0, None, size=0.25, carve=True)
    for side in ('+y', '-y'):
        m.groove([(19.5, -13.0), (36.5, -13.0)], side, depth=1, dark=0.45)
    m.part = 'triggers'
    fp.trigger(m, 24, -2, fp.metal(STEEL_HI), length=7, curve=3)
    fp.trigger(m, 30, -2, fp.metal(STEEL_HI), length=7, curve=3)
    m.screw(22.0, 0.0, '-z', mul(STEEL, 0.7), kind='slot')                              # guard tang screws
    m.screw(34.0, 0.0, '-z', mul(STEEL, 0.7), kind='slot')
    # (Tefa: "please make the tape on the handle narrower and criss cross and color dark red")
    wl.crisscross(m, (-19, 6, -6, 6, -22, 0), along=(-40, -24), period=4.5, width=1.0, col=(105, 22, 20), seed=503,
                  part='tape')

    # ---------------------------------------------------------------- the wasteland layer
    # (Tefa: "make the rust patches randomly placed and shaped")
    wl.rust_patches(m, (BX0, BX1 + 1, -8, 8, Z_BORE - 5, Z_BORE + 5), count=9, seed=504, rmin=1.5, rmax=6.5, pits=0.05)
    wl.rust_patches(m, (AX0, AX1, -AW, AW, AZ0, AZ1 + 1), count=5, seed=505, rmin=1.5, rmax=4.5)
    wl.soot(m, (BX1 - 2, BX1 + 0.5, -7, 7, Z_BORE - 4, Z_BORE + 4), amount=0.5, seed=506)
    for side in ('+y', '-y'):
        wl.chips(m, side, (BX0, BX1 - 4, Z_BORE - 2, Z_BORE + 2), 8, 507 if side == '+y' else 508, under=mul(STEEL, 1.2))
        wl.wear_lines(m, side, (55, 125, Z_BORE - 1.5, Z_BORE + 1.5), 6, 509 if side == '+y' else 510)
    m.crack(72, 3, '+y', 10, 511, heading=0.0)
    wl.cavity(m)
    m.wear_edges(0.15, (180, 176, 168))
    m.grime(0.22, 512)
    wl.simplify(m)
    return m
