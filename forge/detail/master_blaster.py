# Ashes 2063: the Master Blaster flamethrower, DETAILED (2026-11-02). Gun only: the body rig's hand docks onto the grip.
#
# Game look (in-hand NAPALM1-4, pickup LAUPA0): a black barrel with a mottled rag-wrapped stretch and a red ring, a
# silver nozzle, a dark curved wooden body, a black block with a cap, a big gauge facing the player (brass rim, white
# face, red-yellow-green arc), a red valve wheel, a copper tank underneath, braided hose.
# Real-life detail (refs/master_blaster.md; M2 / ROKS flamethrower photos, a WIKA pressure gauge, 2-litre PET bottles):
# igniter housing at the muzzle with its pilot jet, valve lever trigger, brass hose fittings with hex nuts, hose
# clamps, gauge bezel and stem, tick marks, a needle with its hub, filler cap with a chain.
# Wasteland layer (Tefa's example): one fuel tank is a used soda bottle, strapped on with hose clamps, wire and duct
# tape, its label faded and peeling, murky fuel in the bottom; rag wrap on the barrel, rust on the hoops and the copper
# tank, soot round the nozzle, a welded patch plate on the body, scratches.
import math

from _common import Model, fp, wl, BLACK, STEEL, STEEL_HI, DARK, WOOD_DK, BRASS, SCREW, COPPER, mul, mix

WOOD_BROWN = (98, 62, 40)
VALVE_RED = (190, 30, 26)
HOSE_RED = (150, 30, 40)
GAUGE_FACE = (230, 226, 214)
SILVER = (196, 198, 200)
Z = 12.0                       # the body's axis
BODY = (30.0, 82.0, 9.0)       # x0, x1, radius
BARREL = (82.0, 146.0, 3.2)
NOZZLE = (140.0, 156.0)
BOTTLE_X0 = 34.0               # the soda bottle under the body, base at the back
TANK_Y = (-5.0, 5.0)           # copper tank on the right (-y), bottle on the left (+y)


def build():
    m = Model("ashes_master_blaster_detail")
    m.pivot = (40, 0, 0)

    # ---------------------------------------------------------------- the wooden body with iron hoops
    m.part = 'body'
    bx0, bx1, br = BODY
    m.cyl(bx0, bx1, 0, Z, br, fp.wood(WOOD_BROWN, mul(WOOD_DK, 0.8)), edge=0.5)
    m.cyl(bx0 - 0.5, bx0, 0, Z, br - 1.0, fp.metal(BLACK), size=0.25, edge=0.25)
    m.cyl(bx1, bx1 + 2.0, 0, Z, br - 2.5, fp.metal(BLACK), edge=0.25)                     # front cap
    m.part = 'hoops'
    for x in (32.0, 55.0, 78.5):
        m.cyl(x, x + 2.5, 0, Z, br + 0.5, fp.metal(BLACK), size=0.5, edge=0.5)
        for side in ('+y', '-y'):
            m.screw(x + 1.25, Z, side, mul(STEEL, 0.8), kind='rivet')
    m.part = 'body'
    for side in ('+y', '-y'):                                  # wood grain cracks and a burn mark
        m.crack(44 + (6 if side == '-y' else 0), Z + 4, side, 8, 201 if side == '+y' else 202, heading=0.05)
    wl.plate(m, '-y', 60, 72, Z - 4, Z + 3, fp.metal(mul(STEEL, 0.75)), rivets=False, weld=True, seed=203)  # patch

    # ---------------------------------------------------------------- the black receiver block on top, filler cap
    m.part = 'receiver'
    m.cbox(40, 66, 6.0, Z + 7, Z + 12, fp.metal(BLACK), bevel=1.0, edge=0.25)
    for x in range(42, 64, 3):
        m.box(x, x + 0.5, -3.25, 3.25, Z + 10, Z + 11.5, None, size=0.25, carve=True)       # cooling grooves
    m.part = 'filler_cap'
    m.cyl(Z + 12, Z + 14.0, 62, 0, 2.2, fp.metal(BRASS), axis='z', size=0.25, edge=0.25)
    for k in range(8):
        a = k * math.tau / 8
        m.box(62 + math.cos(a) * 2.2 - 0.25, 62 + math.cos(a) * 2.2 + 0.25, math.sin(a) * 2.2 - 0.25,
              math.sin(a) * 2.2 + 0.25, Z + 12, Z + 14.25, mul(BRASS, 0.7), size=0.25)       # knurled edge
    m.part = 'chain'
    for i in range(14):                                                                    # its little chain
        t = i / 13
        m.put(59.5 - t * 6, 2.75 + 0.25 * (i % 2), Z + 13 - math.sin(t * math.pi) * 3 - t * 1.5,
              fp.metal(STEEL_HI), 0.25)

    # ---------------------------------------------------------------- barrel: rag wrap, red ring, igniter, nozzle
    m.part = 'barrel'
    x0, x1, r = BARREL
    m.cyl(x0, x1, 0, Z + 2, r, fp.metal(BLACK), edge=0.25)
    m.cyl(x0, x0 + 3, 0, Z + 2, r + 1.0, fp.metal(mul(BLACK, 1.2)), size=0.25, edge=0.25)  # collar into the body
    for k in range(6):                                                                     # collar's hex nuts
        a = k * math.tau / 6
        m.box(x0 + 0.75, x0 + 2.25, math.cos(a) * (r + 1.0) - 0.4, math.cos(a) * (r + 1.0) + 0.4,
              Z + 2 + math.sin(a) * (r + 1.0) - 0.4, Z + 2 + math.sin(a) * (r + 1.0) + 0.4, fp.metal(STEEL), size=0.25)
    m.part = 'red_ring'
    m.cyl(98, 100.5, 0, Z + 2, r + 0.5, VALVE_RED, size=0.25, edge=0.25)
    wl.cloth(m, 'x', 104, 128, (103, 129, -r - 1, r + 1, Z + 2 - r - 1, Z + 2 + r + 1), col=(126, 86, 52),
             seed=204, part='rag', layers=2, tail=(127.5, -1.0, Z + 2 - r - 0.5, 4.5, 1.0))
    wl.wire_wrap(m, 104.5, 108.0, 0, Z + 2, r + 0.5, pitch=0.9, col=wl.WIRE_STEEL, part='rag')
    wl.wire_wrap(m, 124.5, 128.0, 0, Z + 2, r + 0.5, pitch=0.9, col=wl.WIRE_STEEL, part='rag')
    m.part = 'gas_line'
    m.cyl(60, 140, 0, Z + 9.0, 1.4, fp.metal(BLACK), edge=0.25)
    for x in (90.0, 118.0, 134.0):
        m.cbox(x, x + 2.5, 3.0, Z + 2 + r - 0.5, Z + 9.5, fp.metal(mul(BLACK, 1.15)), size=0.5, edge=0.25)
        m.screw(x + 1.25, Z + 7.5, '+y', mul(STEEL, 0.8), kind='hex')
    m.part = 'nozzle'
    n0, n1 = NOZZLE
    m.cyl(n0, n1, 0, Z + 2, 4.0, fp.metal(SILVER), edge=0.25)
    for x in (n0 + 2, n0 + 5, n0 + 8, n0 + 11):                                            # cooling fins
        m.cyl(x, x + 1, 0, Z + 2, 4.6, fp.metal(mul(SILVER, 1.05)), size=0.25, edge=0.25)
    m.cyl(n1 - 0.75, n1 + 0.1, 0, Z + 2, 2.6, None, size=0.25, edge=0.25, carve=True)
    m.cyl(n1 - 4.0, n1 - 0.75, 0, Z + 2, 1.2, None, size=0.25, edge=0.25, carve=True)       # the jet
    m.cyl(n1 - 4.25, n1 - 4.0, 0, Z + 2, 1.2, (40, 30, 24), size=0.25, edge=0.25)
    m.part = 'pilot'
    m.cyl(n0 - 4, n1 - 2, 0, Z - 3.2, 1.0, fp.metal(BRASS), size=0.25, edge=0.25)           # pilot tube
    m.cyl(n1 - 2, n1 - 0.5, 0, Z - 3.2, 1.3, fp.metal(mul(BRASS, 0.8)), size=0.25, edge=0.25)
    m.ball(n1 - 0.25, 0, Z - 3.2, 0.9, (255, 168, 60), size=0.25, edge=0.25)               # its little flame
    m.box(n0 - 6, n0 - 3, -1.0, 1.0, Z - 4.5, Z - 2.0, fp.metal(STEEL), size=0.25)           # igniter box
    m.screw(n0 - 4.5, Z - 3.25, '+y', SCREW, kind='cross')

    # ---------------------------------------------------------------- under the body: copper tank and THE BOTTLE
    m.part = 'tank'
    ty = TANK_Y[0]
    m.cyl(36, 84, ty, Z - 12.5, 4.4, fp.rusty(COPPER, amount=0.25, seed=205), edge=0.25)
    for x in (36, 84):
        m.ball(x, ty, Z - 12.5, 4.4, fp.rusty(COPPER, amount=0.25, seed=206), edge=0.25)
    for x in (48, 74):
        m.cyl(x, x + 1.5, ty, Z - 12.5, 4.8, fp.metal(BLACK), size=0.25, edge=0.25)
        m.box(x, x + 1.5, ty - 0.5, ty + 0.5, Z - 8, Z - 6, fp.metal(BLACK), size=0.25)       # strap up to the body
    m.decal(["###.#.#.###", "#...#.#..#.", "###.#.#..#.", "#.#.#.#..#.", "###.###..#."], 52, Z - 10.5, '-y',
            (220, 200, 80), mode='paint')                                                   # a faded stencil
    m.part = 'bottle'
    cap_end = wl.bottle(m, BOTTLE_X0, TANK_Y[1], Z - 12.5, length=44.0, r=4.6, part='bottle', seed=207)
    for x in (BOTTLE_X0 + 10.0, BOTTLE_X0 + 26.0):                                          # hose clamps holding it
        wl.hose_clamp(m, x, TANK_Y[1], Z - 12.5, 4.6, part='bottle')
        m.box(x, x + 0.75, TANK_Y[1] - 0.25, TANK_Y[1] + 0.25, Z - 8, Z - 3, fp.metal(STEEL), size=0.25,
              part='bottle')
    wl.tape(m, 'x', BOTTLE_X0 + 15.0, BOTTLE_X0 + 19.0,
            (BOTTLE_X0 + 14, BOTTLE_X0 + 20, -10.5, 10.5, Z - 18, Z - 7.5), col=wl.DUCT, seed=208, part='tape')
    wl.hose_clamp(m, cap_end - 1.5, TANK_Y[1], Z - 12.5, 1.6, part='bottle')
    m.part = 'valve'
    for k in range(28):                                         # the red valve wheel, on a brass stem
        a = k * math.tau / 28
        m.box(62 + math.cos(a) * 4, 62.75 + math.cos(a) * 4, -13.0, -12.25, Z - 4 + math.sin(a) * 4,
              Z - 3.25 + math.sin(a) * 4, VALVE_RED, size=0.25)
    for k in range(5):
        a = k * math.tau / 5 + 0.3
        for t in range(8):
            rr = t * 0.5
            m.box(62 + math.cos(a) * rr, 62.5 + math.cos(a) * rr, -12.75, -12.25, Z - 4 + math.sin(a) * rr,
                  Z - 3.5 + math.sin(a) * rr, mul(VALVE_RED, 0.85), size=0.25)
    m.box(61.5, 63.0, -12.25, -8.5, Z - 4.5, Z - 3.0, fp.metal(BRASS), size=0.25)
    m.box(61.75, 62.75, -13.25, -12.75, Z - 4.25, Z - 3.25, fp.metal(BRASS), size=0.25)      # nut in the middle
    # ---------------------------------------------------------------- the fuel lines (Tefa, 2026-11-02): from both
    # tanks, along the RIGHT side of the gun, joined by a duct-taped Y splitter into one hose that runs into the barrel
    m.part = 'hose'
    ty, by = TANK_Y
    tank_out = (89.6, ty, Z - 12.5)                                 # the copper tank's front outlet
    m.cyl(88.4, 90.4, ty, Z - 12.5, 1.6, fp.metal(BRASS), size=0.25, edge=0.25)
    m.cyl(89.2, 90.0, ty, Z - 12.5, 2.0, fp.metal(mul(BRASS, 0.8)), size=0.25, edge=0.25)
    split = (95.0, -10.5, Z - 11.0)
    # from the bottle's cap: down under the front of the body and across to the right side
    wl.hose(m, [(cap_end + 0.6, by, Z - 12.5), (cap_end + 3.5, by - 1.0, Z - 16.0), (82.0, -2.0, Z - 18.0),
                (88.0, -9.5, Z - 15.5), (split[0] - 3.2, split[1], split[2] - 1.2)], 1.3, STEEL, braided=True)
    # from the copper tank: out to the right and forward (red rubber, as the game's red hose)
    wl.hose(m, [tank_out, (91.5, -8.0, Z - 12.0), (split[0] - 3.2, split[1], split[2] + 1.2)], 1.4, HOSE_RED,
            braided=False, seed=221)
    wl.y_splitter(m, split[0], split[1], split[2], 1.5, col=fp.metal(BRASS)(0, 0, 0), part='hose')
    wl.tape(m, 'x', split[0] - 3.5, split[0] + 1.0,
            (split[0] - 4.5, split[0] + 2.0, split[1] - 3.5, split[1] + 3.5, split[2] - 4.0, split[2] + 4.0),
            col=wl.DUCT, seed=222, part='tape')
    # the one hose, up along the right side into a fitting on the barrel's underside
    entry = (102.5, -3.0, Z - 0.5)          # just in front of the red ring, before the rag
    wl.hose(m, [(split[0] + 3.5, split[1], split[2]), (100.0, -10.0, Z - 7.5), (101.0, -7.0, Z - 3.5),
                (entry[0] - 1.5, entry[1] - 1.0, entry[2] - 0.5)], 1.7, STEEL, braided=True, seed=223)
    m.cyl(entry[0] - 1.5, entry[0] + 1.0, entry[1], entry[2], 2.0, fp.metal(BRASS), size=0.25, edge=0.25)
    m.box(entry[0] - 1.0, entry[0] + 0.5, -3.0, -1.5, Z - 1.0, Z + 1.0, fp.metal(BRASS), size=0.25)   # into the barrel
    wl.hose_clamp(m, split[0] + 4.0, split[1], split[2], 1.7, part='hose')

    # ---------------------------------------------------------------- grips, trigger lever
    m.part = 'grip'
    m.cprism([(36, 4), (30, -4), (26, -18), (34, -20.5), (40, -8), (44, 4)], 7.0,
             fp.wood(mul(WOOD_BROWN, 0.85), mul(WOOD_DK, 0.7), along='z'), bevel=1.5, edge=0.25)
    for side in ('+y', '-y'):
        fp.checker(m, (28, 39, -17, -3), side, mul(WOOD_BROWN, 0.85), mul(WOOD_DK, 0.6))
        m.screw(35.5, -10, side, mul(STEEL, 0.85), kind='slot')
    wl.tape(m, 'z', -17.5, -13.5, (25, 41, -4.5, 4.5, -18, -13), col=wl.DUCT_BLACK, seed=209, part='tape')
    m.part = 'guard'
    fp.guard(m, 40, 54, -8, 2, fp.metal(BLACK))
    m.part = 'trigger'
    m.cprism([(47, 3), (46, -2), (47.5, -6), (49, -6), (48.5, -2), (49.5, 3)], 1.5, fp.metal(STEEL_HI), size=0.25)
    m.part = 'front_grip'
    m.cprism([(96, Z - 3), (95, Z - 10), (94, Z - 16), (99, Z - 16.5), (100, Z - 10), (101, Z - 3)], 5.0,
             fp.wood(WOOD_BROWN, WOOD_DK, along='z'), bevel=1.0, edge=0.25)
    wl.cloth(m, 'z', Z - 15, Z - 7, (93, 102, -3.5, 3.5, Z - 15.5, Z - 6.5), col=wl.CLOTH_GREY, seed=210,
             part='rag', layers=1)

    # ---------------------------------------------------------------- the gauge at the back, facing the player
    m.part = 'gauge'
    gz = Z + 4
    m.cyl(26.5, 30, 0, gz, 1.4, fp.metal(BRASS), size=0.25, edge=0.25)                      # brass stem
    m.cyl(25.75, 26.75, 0, gz, 1.9, fp.metal(BRASS), size=0.25, edge=0.25)                   # its hex
    m.cyl(18, 25.75, 0, gz, 7.5, fp.metal((30, 30, 32)), edge=0.25)                          # black case
    m.cyl(17.25, 18.25, 0, gz, 7.8, fp.metal(BRASS), size=0.25, edge=0.25)                   # brass bezel
    m.cyl(17.25, 18.0, 0, gz, 6.6, None, size=0.25, edge=0.25, carve=True)
    m.cyl(18.0, 18.25, 0, gz, 6.6, GAUGE_FACE, size=0.25, edge=0.25)                         # the face
    for k in range(30):                                                                     # ticks and the arc
        a = math.pi * 1.25 - k * (math.pi * 1.5) / 29
        col = (200, 40, 30) if k < 8 else ((220, 190, 40) if k < 18 else (60, 170, 60))
        rr = 5.4
        m.box(17.75, 18.0, math.cos(a) * rr - 0.25, math.cos(a) * rr + 0.25, gz + math.sin(a) * rr - 0.25,
              gz + math.sin(a) * rr + 0.25, col, size=0.25)
        if k % 3 == 0:
            m.box(17.75, 18.0, math.cos(a) * 4.5 - 0.125, math.cos(a) * 4.5 + 0.125, gz + math.sin(a) * 4.5 - 0.125,
                  gz + math.sin(a) * 4.5 + 0.125, DARK, size=0.25)
    for t in range(14):                                                                     # the needle, in the red
        m.box(17.5, 17.75, -t * 0.32 - 0.125, -t * 0.32 + 0.125, gz + t * 0.22 - 0.125, gz + t * 0.22 + 0.125,
              (20, 20, 22), size=0.25)
    m.box(17.5, 17.75, -0.5, 0.5, gz - 0.5, gz + 0.5, (180, 30, 26), size=0.25)               # needle hub
    m.box(17.75, 18.0, 1.0, 3.5, gz - 3.5, gz - 2.5, (30, 30, 32), size=0.25)                 # "bar" printed small

    # ---------------------------------------------------------------- the wasteland layer
    wl.soot(m, (n0 - 2, n1 + 1, -5, 5, Z - 5, Z + 7), amount=0.75, seed=212)
    wl.soot(m, (n0 - 8, n0, -2, 2, Z - 5, Z - 1), amount=0.5, seed=213)
    wl.rust(m, (30, 84, -11, 11, Z - 2, Z + 11), amount=0.3, seed=214, pits=0.03,
            region=lambda x, y, z: abs(math.hypot(y, z - Z) - BODY[2] - 0.5) < 0.8)       # the hoops
    wl.rust(m, (82, 140, -5, 5, Z - 3, Z + 7), amount=0.18, seed=215, pits=0.02)
    for side in ('+y', '-y'):
        m.scratches(side, (82, 140, Z, Z + 5), 6, 216 if side == '+y' else 217, lighten=1.25, length=(2.0, 5.0))
        wl.chips(m, side, (40, 66, Z + 7.5, Z + 11.5), 10, 218 if side == '+y' else 219, under=mul(STEEL, 1.1))
    wl.cavity(m)
    m.wear_edges(0.15, (200, 180, 150))
    m.grime(0.22, 220)
    wl.simplify(m, step=14, block=1.5)
    return m
