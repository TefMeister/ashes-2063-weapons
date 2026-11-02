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
import math

from _common import Model, fp, wl, BLACK, STEEL, STEEL_HI, WOOD, WOOD_DK, TAPE_BLUE, BRASS, mul, mix, hash01

BLUED = (52, 54, 58)
ENGRAVE = (150, 150, 146)
Z_BORE = 9.0
BX0, BX1, BR, BORE = 40.0, 128.0, 2.9, 1.9
GAP = 2.9
AX0, AX1, AZ0, AZ1, AW = 16.0, 42.0, -1.0, 13.5, 11.0
FOREND = [(42, 2), (42, 6), (80, 6.5), (84, 4), (82, 2), (46, 1)]
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
    m.prism([(BX0, Z_BORE + 1.5), (BX1 - 1, Z_BORE + 1.5), (BX1 - 1, Z_BORE + 2.75), (BX0, Z_BORE + 3.5)], -1.0, 1.0,
            fp.metal(mul(BLUED, 1.1)), size=0.25)
    for x in range(int(BX0) * 2, int(BX1 - 1) * 2):                                  # matted top: fine cross lines
        if x % 2 == 0:
            m.box(x / 2, x / 2 + 0.25, -0.75, 0.75, Z_BORE + 2.5, Z_BORE + 3.5, mul(BLUED, 0.75), size=0.25)
    m.cbox(BX0, BX1 - 3, 3.0, Z_BORE - 3.5, Z_BORE - 2, fp.metal(BLUED), size=0.5)       # bottom rib
    m.part = 'bead'
    m.ball(BX1 - 2.5, 0, Z_BORE + 3.25, 0.6, fp.metal(BRASS), size=0.25, edge=0.25)
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
    m.cbox(AX0, AX1, AW, AZ0, AZ1, fp.metal(mul(STEEL, 0.95)), bevel=2.0, bevel_x=1.0, edge=0.25)
    m.cyl(-AW / 2 + 0.5, AW / 2 - 0.5, AX1 - 1.5, AZ0 + 2.5, 2.25, fp.metal(STEEL), axis='y', size=0.25,
          edge=0.25)                                                                    # hinge knuckle
    for side in ('+y', '-y'):                                                          # scroll engraving
        for k in range(26):
            t = k / 25
            a, b = AX0 + 3 + t * 20, 6.5 + 3.5 * math.sin(t * math.tau * 1.5)
            m.paint_line([(a, b), (a + 0.6, b + 0.4 * math.cos(t * 9))], side, lambda c: mix(c, ENGRAVE, 0.6))
            if k % 4 == 0:
                for r in range(6):
                    ang = r * 1.1
                    m.paint_line([(a + math.cos(ang) * 1.1, b + math.sin(ang) * 1.1),
                                  (a + math.cos(ang + 1.1) * 1.1, b + math.sin(ang + 1.1) * 1.1)], side,
                                 lambda c: mix(c, ENGRAVE, 0.5))
        m.groove([(AX0 + 2, AZ1 - 3), (AX1 - 2, AZ1 - 3)], side, depth=1, dark=0.5)
        m.screw(22, 3, side, mul(STEEL, 0.75), kind='slot')
        m.screw(36, 1.5, side, mul(STEEL, 0.75), kind='cross')
    m.part = 'top_lever'
    m.box(24, 34, -3.5, 1.0, AZ1, AZ1 + 1.0, fp.metal(STEEL_HI), size=0.25, edge=0.25, bevel_x=0.5)
    for k in range(5):
        m.box(24.5 + k * 0.6, 24.75 + k * 0.6, -3.25, -1.0, AZ1 + 0.75, AZ1 + 1.0, mul(STEEL_HI, 0.6), size=0.25)
    m.part = 'safety'
    m.box(17.0, 21.0, -1.0, 1.0, AZ1 - 0.5, AZ1 + 0.5, fp.metal(STEEL_HI), size=0.25)
    m.box(21.5, 22.5, -0.5, 0.5, AZ1, AZ1 + 0.25, (230, 220, 200), size=0.25)            # the S, a white dot

    # ---------------------------------------------------------------- fore-end, grip, guard, triggers
    m.part = 'foreend'
    m.cprism(FOREND, 9.0, fp.wood(WOOD, WOOD_DK), bevel=2.0, edge=0.25)
    m.box(78.0, 81.0, -0.75, 0.75, 0.75, 1.75, fp.metal(STEEL), size=0.25)               # release latch
    for side in ('+y', '-y'):
        fp.checker(m, (52, 74, 2.5, 6.0), side, WOOD, WOOD_DK)
    wl.tape(m, 'x', 60.0, 64.0, (59, 65, -5.5, 5.5, 0, 7.5), col=wl.DUCT_BLACK, seed=502, part='tape')
    m.part = 'grip'
    m.cprism(GRIP, 8.0, fp.wood(mul(WOOD, 0.85), WOOD_DK, along='z'), bevel=2.0, edge=0.25)
    m.part = 'butt_cap'
    m.ball(-14, 0, -23, 5.0, fp.metal(BRASS), ry=4.5, rz=4.0, edge=0.25)
    for k in range(3):                                                                  # dents in the cap
        m.ball(-17 + k * 3, 4.3 if k % 2 else -4.3, -24 + k, 0.8, None, size=0.25, edge=0.25, carve=True)
    m.part = 'guard'
    fp.guard(m, 18, 32, -8, -1, fp.metal(BLUED))
    m.part = 'triggers'
    fp.trigger(m, 23, -1, fp.metal(STEEL_HI), length=5)
    fp.trigger(m, 28, -1, fp.metal(STEEL_HI), length=5)
    m.screw(19.0, 0.0, '-z', mul(STEEL, 0.7), kind='slot')                              # guard tang screws
    m.screw(31.0, 0.0, '-z', mul(STEEL, 0.7), kind='slot')
    wl.cloth(m, 'z', -16.0, -3.0, (-18, 18, -5, 5, -16.5, -2.5), col=TAPE_BLUE, seed=503, part='cloth', layers=2,
             tail=(-6.0, -4.75, -9.0, 6.0, 1.0))

    # ---------------------------------------------------------------- the wasteland layer
    wl.rust(m, (BX0, BX1 + 1, -7, 7, Z_BORE - 4, Z_BORE + 4), amount=0.32, seed=504, pits=0.04)
    wl.rust(m, (AX0, AX1, -AW, AW, AZ0, AZ1 + 1), amount=0.15, seed=505)
    wl.soot(m, (BX1 - 2, BX1 + 0.5, -7, 7, Z_BORE - 4, Z_BORE + 4), amount=0.5, seed=506)
    for side in ('+y', '-y'):
        wl.chips(m, side, (BX0, BX1 - 4, Z_BORE - 2, Z_BORE + 2), 8, 507 if side == '+y' else 508, under=mul(STEEL, 1.2))
        wl.wear_lines(m, side, (45, 120, Z_BORE - 1.5, Z_BORE + 1.5), 6, 509 if side == '+y' else 510)
    m.crack(62, 4, '+y', 10, 511, heading=0.0)
    wl.cavity(m)
    m.wear_edges(0.15, (180, 176, 168))
    m.grime(0.22, 512)
    wl.simplify(m)
    return m
