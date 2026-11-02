# Ashes 2063: the pump-action shotgun, DETAILED (2026-11-02). Gun only: the body rig's hands dock onto the grip and pump.
#
# Game look (in-hand GRIZ* / GR2*, pickup GRZPA / SHOTA): a dark blued receiver with a red shell in the port, barrel
# over a magazine tube, a ribbed orange wooden pump, a short pistol-grip with blue and black tape and a wooden cap.
# Real-life detail (refs/pump_shotgun.md; Remington 870 photos): grooved receiver top, ejection port with the bolt and
# extractor, loading port with the shell lifter, separate trigger plate with two pins, action bar lock and cross-bolt
# safety, barrel ring and clamp to the tube, knurled magazine cap with a sling loop, brass front bead, action bars
# from the pump to the receiver, corn-cob grooves all round the pump.
# Wasteland layer: a side saddle of four red shells on an elastic cloth band, a hose clamp and wire holding barrel to
# tube near the muzzle, rust at the muzzle and on the clamp, soot at the port and muzzle, cracked pump wood, chips.
# 2026-11-02, BULKIER (Tefa: "leave the ashes 2063 designs as they are, but make the weapon bodies, the main chunky part
# that houses ammo, please make these bigger ... the body is really small and the part where the pump handle is and the
# barrel is very long and skinny. they must look bulky, worn and dangerous, realism is not the main thing"): the receiver
# 64 -> 96 long, 20 -> 28 tall, 8 -> 12 wide; barrel and tube about 1.3 times as thick; the pump bigger; the barrel now
# starts where the bigger receiver ends, so the gun is barely longer. Every detail kept, moved onto the new body.
import math

from _common import Model, fp, wl, BLACK, STEEL, STEEL_HI, DARK, WOOD, WOOD_DK, TAPE, TAPE_BLUE, BRASS, RED_SHELL, mul

BLUED = (44, 48, 50)
Z_BARREL, Z_TUBE = 15.0, 4.0
RX0, RX1, RZ0, RZ1, W = 40.0, 136.0, -8.0, 20.0, 12.0
BARREL = (136.0, 268.0, 3.4, 2.0)
TUBE = (136.0, 246.0, 3.2)
PUMP = (152.0, 210.0, -4.0, 12.0, 12.0)
PORT = (74.0, 108.0, 10.0, 17.5)
GRIP = [(46, -8), (38, -8), (30, -18), (22, -32), (20, -38), (31, -40), (35, -34), (44, -16), (52, -8)]
STOCK_CAP = [(18, -36), (16, -42), (19, -46), (33, -46), (34, -40)]


def build():
    m = Model("ashes_pump_shotgun_detail")
    m.pivot = (40, 0, 0)
    blk = fp.metal(BLUED, speck=0.05)

    # ---------------------------------------------------------------- receiver
    m.part = 'receiver'
    m.cbox(RX0, RX1, W, RZ0, RZ1, blk, bevel=1.0, edge=0.25)
    m.cbox(RX0 - 6, RX0, W - 1, 4, RZ1 - 1, blk, bevel=1.0, edge=0.25)
    m.cbox(RX0 + 2, RX1 - 2, W - 3, RZ1, RZ1 + 1, fp.metal(mul(BLUED, 1.1)), size=0.5, edge=0.25)
    for y in (-1.25, -0.25, 0.75):                                              # anti-glare grooves along the top
        m.box(RX0 + 3, RX1 - 3, y, y + 0.5, RZ1 + 0.75, RZ1 + 1.0, None, size=0.25, carve=True)
    px0, px1, pz0, pz1 = PORT
    m.box(px0, px1, -W / 2 - 1, -W / 2 + 1.5, pz0, pz1, None, size=0.25, carve=True)
    m.box(px0, px1, -W / 2 + 1.5, -W / 2 + 1.75, pz0, pz1, DARK, size=0.25)
    m.part = 'bolt'
    m.box(px0 - 0.5, px0 + 6, -W / 2 + 1.0, -W / 2 + 1.75, pz0 + 0.5, pz1 - 0.5, fp.metal(STEEL_HI), size=0.25)
    m.box(px0 + 4.5, px0 + 6, -W / 2 + 0.75, -W / 2 + 1.0, pz1 - 2.0, pz1 - 1.0, fp.metal(STEEL), size=0.25)  # extractor
    m.part = 'shell'
    m.cyl(px0 + 9, px0 + 19, -1.5, (pz0 + pz1) / 2, 2.0, fp.metal(RED_SHELL, speck=0.04), edge=0.25)
    m.cyl(px0 + 6, px0 + 9, -1.5, (pz0 + pz1) / 2, 2.1, fp.metal(BRASS), size=0.25, edge=0.25)
    m.box(px0 + 5.75, px0 + 6, -2.0, -1.0, (pz0 + pz1) / 2 - 0.5, (pz0 + pz1) / 2 + 0.5, (220, 200, 150), size=0.25)
    m.part = 'receiver'
    m.cbox(72, 126, 6.5, RZ0, RZ0 + 1.5, None, size=0.25, carve=True)                 # loading port
    m.part = 'lifter'
    m.cbox(74, 124, 5.5, RZ0 + 1.25, RZ0 + 1.5, fp.metal(mul(STEEL, 0.75)), size=0.25)
    m.part = 'trigger_plate'
    m.cprism([(42, -8), (42, -10), (68, -10), (70, -8)], W - 1.0, fp.metal(mul(BLUED, 0.85)), size=0.25)
    for side in ('+y', '-y'):
        m.screw(46, -5.0, side, mul(STEEL, 0.7), kind='rivet')                         # trigger plate pins
        m.screw(66, -5.0, side, mul(STEEL, 0.7), kind='rivet')
        m.groove([(42, -7.75), (70, -7.75)], side, depth=1, dark=0.4)
        m.groove([(RX0 + 1, 2), (RX1 - 1, 2)], side, depth=1, dark=0.45)
        m.screw(128, 9, side, mul(STEEL, 0.7), kind='slot')
    m.part = 'safety'
    m.cyl(-W / 2 - 0.5, W / 2 + 0.5, 64.5, -12.0, 0.75, fp.metal(STEEL), axis='y', size=0.25, edge=0.25)
    m.box(64.0, 65.0, -W / 2 - 0.75, -W / 2 - 0.5, -12.5, -11.5, (200, 30, 26), size=0.25)    # the red ring: off
    m.part = 'action_lock'
    m.box(44.5, 46.5, W / 2 - 0.5, W / 2 + 0.25, -13.0, -11.5, fp.metal(mul(STEEL, 0.6)), size=0.25)
    m.decal(["###.###.###", "#.#...#.#.#", "###..#..#.#", "#.#.#...#.#", "###.#...###"], 96, 4.0, '+y',
            mul(BLUED, 1.6), mode='carve')                                               # "870"

    # ---------------------------------------------------------------- barrel, tube, clamp, sights
    m.part = 'barrel'
    bx0, bx1, br, bb = BARREL
    m.cyl(bx0, bx0 + 4, 0, Z_BARREL, br + 0.75, blk, size=0.25, edge=0.25)               # barrel ring
    fp.barrel(m, bx0, bx1, Z_BARREL, br, fp.metal(mul(BLUED, 1.15)), bore=bb, edge=0.5)
    m.cyl(bx1 - 0.25, bx1 + 0.1, 0, Z_BARREL, br - 0.5, None, size=0.25, edge=0.25, carve=True)
    m.part = 'sight'
    m.ball(bx1 - 3.0, 0, Z_BARREL + br + 0.5, 0.6, fp.metal(BRASS), size=0.25, edge=0.25)  # brass bead
    m.part = 'tube'
    tx0, tx1, tr = TUBE
    m.cyl(tx0, tx1, 0, Z_TUBE, tr, blk, edge=0.5)
    m.part = 'mag_cap'
    m.cyl(tx1, tx1 + 4, 0, Z_TUBE, tr + 0.25, fp.metal(mul(BLUED, 1.2)), size=0.25, edge=0.25)
    for k in range(16):
        a = k * math.tau / 16
        m.box(tx1 + 0.5, tx1 + 3.5, math.cos(a) * (tr + 0.4) - 0.125, math.cos(a) * (tr + 0.4) + 0.125,
              Z_TUBE + math.sin(a) * (tr + 0.4) - 0.125, Z_TUBE + math.sin(a) * (tr + 0.4) + 0.125,
              fp.metal(mul(BLUED, 0.7)), size=0.25)                                       # knurling
    for k in range(14):                                                                 # the sling loop on its end
        a = k * math.tau / 14
        m.box(tx1 + 4 + math.cos(a) * 1.5, tx1 + 4.25 + math.cos(a) * 1.5, -0.25, 0.25, Z_TUBE - 3 + math.sin(a) * 1.5,
              Z_TUBE - 2.75 + math.sin(a) * 1.5, fp.metal(STEEL), size=0.25)
    m.part = 'clamp'
    m.cbox(tx1 - 6, tx1 - 2, 5.5, Z_TUBE - 2, Z_BARREL + 2, fp.metal(STEEL), bevel=1, edge=0.25)
    m.screw(tx1 - 4, Z_TUBE + 3.5, '-y', mul(STEEL, 0.8), kind='hex')

    # ---------------------------------------------------------------- the pump and its action bars
    m.part = 'pump'
    ux0, ux1, uz0, uz1, uw = PUMP
    m.cbox(ux0, ux1, uw, uz0, uz1, fp.wood(WOOD, WOOD_DK), bevel=2.0, bevel_x=1.0, edge=0.5)
    for i in range(int((ux1 - ux0 - 7) / 2.5)):                                         # corn-cob grooves all round
        x = ux0 + 4 + i * 2.5
        for side in ('+y', '-y'):
            m.groove([(x, uz0 + 1), (x, uz1 - 1)], side, depth=2, width=3, dark=0.38)
        m.groove([(x, -4.5), (x, 4.5)], '-z', depth=2, width=3, dark=0.38)
    m.box(ux1, ux1 + 1.0, -uw / 2 + 0.5, uw / 2 - 0.5, uz0 + 0.5, uz1 - 0.5, fp.metal(BLUED), size=0.25)   # end cap
    m.part = 'action_bars'
    for y in (-2.25, 2.0):
        m.box(RX1 - 1, ux0 + 1, y, y + 0.25, Z_TUBE - 0.25, Z_TUBE + 0.75, fp.metal(STEEL_HI), size=0.25)

    # ---------------------------------------------------------------- grip: tape and the wooden cap
    m.part = 'grip'
    m.cprism(GRIP, 6.0, fp.metal(TAPE, speck=0.1), bevel=1.5, edge=0.25)
    m.part = 'grip_cap'
    m.cprism(STOCK_CAP, 6.5, fp.wood(WOOD, WOOD_DK, along='z'), bevel=1.0, edge=0.25)
    m.part = 'guard'
    fp.guard(m, 44, 66, -16, -8, blk)
    m.part = 'trigger'
    fp.trigger(m, 56, -8, fp.metal(STEEL))
    wl.tape(m, 'z', -24.0, -19.0, (15, 50, -4.5, 4.5, -24.5, -18.5), col=TAPE_BLUE, seed=401, part='tape')
    wl.tape(m, 'z', -33.0, -28.0, (15, 50, -4.5, 4.5, -33.5, -27.5), col=wl.DUCT_BLACK, seed=402, part='tape')
    for side in ('+y', '-y'):
        m.screw(26, -42.5, side, mul(STEEL, 0.75), kind='slot')

    # ---------------------------------------------------------------- the wasteland layer
    m.part = 'side_saddle'
    wl.plate(m, '+y', 78, 110, 0.5, 9.0, fp.metal((40, 40, 38)), rivets=True, seed=403)      # the carrier plate
    for i in range(4):                                                                     # four red shells on it
        x = 82.0 + i * 7.0
        m.box(x - 1.5, x + 1.5, W / 2 + 0.5, W / 2 + 3.5, 0.75, 7.75, fp.metal(RED_SHELL, speck=0.05), size=0.25)
        m.box(x - 1.5, x + 1.5, W / 2 + 0.5, W / 2 + 3.5, -1.0, 0.75, fp.metal(BRASS), size=0.25)
        m.box(x - 0.5, x + 0.5, W / 2 + 3.5, W / 2 + 3.75, -0.75, 0.25, (220, 200, 150), size=0.25)   # primer
    wl.cloth(m, 'x', 78.5, 110.0, (77.5, 111, W / 2, W / 2 + 4.5, 3.0, 5.5), col=wl.CLOTH_GREY, seed=404,
             part='side_saddle', layers=1)                                                 # the elastic band
    wl.hose_clamp(m, 236.0, 0, Z_BARREL, br, part='clamp')
    wl.wire_wrap(m, 228.0, 232.0, 0, (Z_BARREL + Z_TUBE) / 2, 4.6, pitch=0.8, col=wl.WIRE_STEEL, part='clamp')
    wl.rust(m, (231, 269, -5, 5, 0, 19), amount=0.35, seed=405, pits=0.04)
    wl.rust(m, (RX0, RX1, -W, W, RZ0, RZ1 + 1), amount=0.12, seed=406)
    wl.soot(m, (px0, px1 + 2, -W, -1, pz0 - 1, pz1 + 1), amount=0.45, seed=407)
    wl.soot(m, (bx1 - 3, bx1 + 0.5, -3.5, 3.5, Z_BARREL - 3.5, Z_BARREL + 3.5), amount=0.6, seed=408)
    for side in ('+y', '-y'):
        wl.chips(m, side, (RX0 + 2, RX1 - 2, RZ0 + 1, RZ1), 9, 409 if side == '+y' else 410, under=mul(STEEL, 1.2))
        wl.wear_lines(m, side, (152, 226, 10, 17), 8, 411 if side == '+y' else 412)
    m.crack(168, 8, '+y', 16, 413, heading=0.1)
    m.crack(192, 2, '-y', 10, 414, heading=3.0)
    wl.cavity(m)
    m.wear_edges(0.15, (150, 150, 150))
    m.grime(0.2, 415)
    wl.simplify(m)
    return m
