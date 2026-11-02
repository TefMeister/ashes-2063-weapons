# Ashes 2063: the Battle Rifle (FAL), DETAILED (2026-11-02). Gun only: the body rig's hands dock onto grip and handguard.
#
# Game look (in-hand FAL1*, pickup FALPA / FICOA): light tan wood stock, pistol grip and handguard over a black
# receiver, a box magazine, a slotted flash hider, a tall box sight on top with a round lens and a red no-entry sticker.
# Real-life detail (refs/battle_rifle.md; FN FAL / L1A1 photos and an Argentine FAL drawing): dust cover over the
# receiver, folding carry handle with grip ridges, charging handle on the left front, rear peep sight, gas block with
# front sight post between ears and the gas regulator, handguard with three oval vents, long slotted flash hider and a
# bayonet lug, ribbed 20-round magazine with its release behind, selector and takedown lever on the left, pivot pin of
# the hinged lower, sling swivels, butt plate.
# The eyepiece lens stays its own part, 'glass': the live scope picture is drawn on it (../../scope/).
# Wasteland layer: cracked stock bound with wire, cloth wrap on the handguard, the sticker scuffed, rust on the flash
# hider, chipped paint on the receiver, a spare magazine taped to the one in the gun (jungle style), scratches.
import math

from _common import Model, fp, wl, BLACK, STEEL, STEEL_HI, DARK, BRASS, mul, mix

TAN = (176, 116, 62)
TAN_DK = (112, 66, 30)
PARK = (46, 48, 48)
STICKER = (200, 30, 30)
Z_BORE = 12.0
RX0, RX1, RZ0, RZ1, RW = 60.0, 136.0, 2.0, 18.0, 9.0
STOCK = [(0, -14), (0, 14), (6, 16), (60, 16), (60, 6), (36, -2), (8, -16)]
GRIP = [(80, 2), (70, 2), (62, -14), (60, -24), (70, -26), (76, -16), (86, 0)]
HX0, HX1, HZ0, HZ1, HW = 136.0, 196.0, 1.5, 16.5, 10.0
BX1, BR, BORE = 270.0, 2.0, 1.0
MAG = [(110, 2), (108, -24), (124, -26), (128, 2)]


def mag(m, dx, dz, seed):
    m.cprism([(p[0] + dx, p[1] + dz) for p in MAG], 7.5, fp.metal(PARK), bevel=0.75, edge=0.25)
    for z in (-6, -11, -16, -21):
        for side in ('+y', '-y'):
            m.groove([(110 + dx, z + dz), (125 + dx, z + dz)], side, depth=1, width=2, dark=0.5)
    m.cprism([(107 + dx, -24 + dz), (107 + dx, -26.5 + dz), (125 + dx, -27.5 + dz), (125 + dx, -25 + dz)], 8.0,
             fp.metal(mul(PARK, 0.8)), size=0.25)                                     # floor plate


def build():
    m = Model("ashes_battle_rifle_detail")
    m.pivot = (72, 0, 0)
    wood = fp.wood(TAN, TAN_DK)
    blk = fp.metal(PARK, speck=0.06)

    # ---------------------------------------------------------------- receiver
    m.part = 'receiver'
    m.cbox(RX0, RX1, RW, RZ0, RZ1, blk, bevel=0.75, edge=0.25)
    m.part = 'dust_cover'
    m.cbox(RX0 + 4, RX1 - 8, RW - 2.5, RZ1, RZ1 + 1.75, fp.metal(mul(PARK, 0.9)), bevel=0.5, size=0.25)
    for x in range(int(RX0 + 8), int(RX1 - 12), 3):                                       # pressed ribs on it
        m.box(x, x + 0.5, -2.75, 2.75, RZ1 + 1.5, RZ1 + 1.75, mul(PARK, 1.3), size=0.25)
    m.part = 'receiver'
    m.box(96, 120, -RW / 2 - 0.5, -RW / 2 + 1.5, 10, 15, None, size=0.25, carve=True)        # ejection port
    m.part = 'bolt'
    m.box(96, 120, -RW / 2 + 1.5, -RW / 2 + 1.75, 10, 15, fp.metal(STEEL), size=0.25)
    m.cyl(101, 106.5, -2.5, 12.5, 1.2, BRASS, size=0.25, edge=0.25)
    m.part = 'charge'
    m.box(124, 129, RW / 2, RW / 2 + 0.75, 12.0, 14.0, fp.metal(STEEL_HI), size=0.25)
    m.box(126.5, 129, RW / 2 + 0.75, RW / 2 + 3.0, 12.25, 13.75, fp.metal(STEEL_HI), size=0.25)   # folding knob
    m.part = 'carry_handle'
    for x in (119.0, 131.0):                                                              # its two posts
        m.box(x, x + 1.5, -0.5, 0.5, RZ1 + 1.75, RZ1 + 6.0, blk, size=0.25)
    m.box(119, 132.5, -1.25, 1.25, RZ1 + 5.0, RZ1 + 6.5, blk, size=0.25)
    for x in range(121, 131, 2):
        m.box(x, x + 1, -1.25, 1.25, RZ1 + 6.5, RZ1 + 7.0, blk, size=0.25)                 # grip ridges
    m.part = 'rear_sight'
    m.box(62, 66, -1.5, 1.5, RZ1, RZ1 + 3.0, blk, size=0.25)
    m.box(61.5, 66.5, -0.4, 0.4, RZ1 + 1.6, RZ1 + 2.4, None, size=0.25, carve=True)           # the peep hole
    m.part = 'controls'
    m.box(74, 79, RW / 2, RW / 2 + 0.5, 6.0, 7.5, fp.metal(STEEL), size=0.25)                 # selector
    m.box(66, 70, RW / 2, RW / 2 + 0.5, 9.0, 10.0, fp.metal(STEEL), size=0.25)                # takedown lever
    m.box(128, 131, RW / 2, RW / 2 + 0.25, 3.0, 5.0, fp.metal(STEEL), size=0.25)              # mag release
    for k in range(3):                                                                  # S R A marks
        m.box(76 + k * 1.5, 76.5 + k * 1.5, RW / 2, RW / 2 + 0.25, 8.5, 9.0, (220, 210, 190), size=0.25)
    for side in ('+y', '-y'):
        m.screw(64, 10, side, mul(STEEL, 0.7), kind='slot')
        m.screw(132, 4, side, mul(STEEL, 0.7), kind='rivet')                               # lower pivot pin
        m.groove([(RX0 + 2, 6), (RX1 - 2, 6)], side, depth=1, dark=0.45)

    # ---------------------------------------------------------------- stock, grip, handguard
    m.part = 'stock'
    m.cprism(STOCK, 9.0, wood, bevel=2.0, edge=0.25)
    m.part = 'butt_plate'
    m.cbox(-2, 0, 9.5, -15, 15, fp.metal(DARK), size=0.5)
    for z in range(-13, 14, 2):
        m.box(-2.25, -2.0, -4.0, 4.0, z, z + 0.5, mul(DARK, 1.6), size=0.25)
    m.part = 'swivel'
    for k in range(10):
        a = k * math.tau / 10
        m.box(14 + math.cos(a) * 1.3, 14.25 + math.cos(a) * 1.3, -0.25, 0.25, -12.5 + math.sin(a) * 1.3,
              -12.25 + math.sin(a) * 1.3, fp.metal(STEEL), size=0.25)
    m.part = 'grip'
    m.cprism(GRIP, 8.0, wood, bevel=2.0, edge=0.25)
    for side in ('+y', '-y'):
        for z in range(-22, -4, 2):
            m.groove([(63 + (z + 22) * 0.35, z), (74 + (z + 22) * 0.35, z)], side, depth=1, dark=0.55)
    m.part = 'handguard'
    m.cbox(HX0, HX1, HW, HZ0, HZ1, wood, bevel=2.5, edge=0.25)
    for x in (152.0, 162.0, 172.0):                                                        # three oval vents
        for side in ('+y', '-y'):
            m.groove([(x, 9.5), (x + 5, 9.5)], side, depth=3, width=5, dark=0.22)
    m.part = 'guard'
    fp.guard(m, 80, 100, -8, RZ0, blk)
    m.part = 'trigger'
    fp.trigger(m, 88, RZ0, fp.metal(STEEL_HI), length=6)

    # ---------------------------------------------------------------- barrel, gas block, front sight, flash hider
    m.part = 'barrel'
    fp.barrel(m, HX0, BX1, Z_BORE, BR, blk, bore=BORE, edge=0.5)
    m.part = 'gas_block'
    m.cbox(HX1, HX1 + 10, 5.0, Z_BORE - 3, Z_BORE + 8, blk, bevel=0.75, size=0.5, edge=0.25)
    m.cyl(HX1 + 10, HX1 + 12, 0, Z_BORE + 5, 1.6, fp.metal(STEEL), size=0.25, edge=0.25)      # regulator
    for k in range(8):
        a = k * math.tau / 8
        m.box(HX1 + 10.5, HX1 + 11.5, math.cos(a) * 1.7 - 0.2, math.cos(a) * 1.7 + 0.2, Z_BORE + 5 + math.sin(a) * 1.7
              - 0.2, Z_BORE + 5 + math.sin(a) * 1.7 + 0.2, fp.metal(mul(STEEL, 0.7)), size=0.25)
    m.part = 'front_sight'
    for y in (-2.0, 1.25):
        m.box(HX1 + 3, HX1 + 7, y, y + 0.75, Z_BORE + 8, Z_BORE + 12, blk, size=0.25)     # ears
    m.box(HX1 + 4.5, HX1 + 5.5, -0.4, 0.4, Z_BORE + 8, Z_BORE + 11, fp.metal(STEEL_HI), size=0.25)
    m.part = 'bayonet_lug'
    m.box(HX1 + 12, HX1 + 18, -0.75, 0.75, Z_BORE - 3.5, Z_BORE - 2.0, blk, size=0.25)
    m.part = 'flash_hider'
    m.cyl(BX1 - 14, BX1, 0, Z_BORE, 2.6, fp.metal(mul(PARK, 0.85)), size=0.25, edge=0.25)
    for x in range(int(BX1) - 12, int(BX1) - 1, 3):                                        # the slots
        for a in range(4):
            ang = a * math.pi / 2 + math.pi / 4
            y, z = math.cos(ang) * 2.6, Z_BORE + math.sin(ang) * 2.6
            m.box(x, x + 2, y - 0.4, y + 0.4, z - 0.4, z + 0.4, None, size=0.25, carve=True)
    m.cyl(BX1 - 0.5, BX1 + 0.1, 0, Z_BORE, 1.6, None, size=0.25, edge=0.25, carve=True)

    # ---------------------------------------------------------------- magazine (and the taped spare)
    m.part = 'mag'
    mag(m, 0, 0, 1)
    m.part = 'spare_mag'                       # a second magazine taped beside it, upside down, jungle style
    m.prism([(110, -26), (108, 0), (124, 2), (128, -26)], 3.75, 11.25, fp.metal(mul(PARK, 1.05)), bevel=0.75,
            edge=0.25)
    wl.tape(m, 'z', -12.0, -8.0, (106, 130, -4.5, 12.5, -12.5, -7.5), col=wl.DUCT, seed=714, part='tape')

    # ---------------------------------------------------------------- the box sight with its lens and sticker
    m.part = 'sight'
    m.cbox(96, 116, 10.0, RZ1 + 1.5, RZ1 + 15, fp.metal(DARK), bevel=1.0, edge=0.25)
    m.cbox(95, 117, 6.0, RZ1 + 4, RZ1 + 12, None, size=0.5, carve=True)
    for side in ('+y', '-y'):
        m.screw(98.0, RZ1 + 13.5, side, mul(STEEL, 0.6), kind='hex')
        m.screw(114.0, RZ1 + 13.5, side, mul(STEEL, 0.6), kind='hex')
        m.screw(106.0, RZ1 + 2.75, side, mul(STEEL, 0.6), kind='slot')                   # mount screws
    m.box(118, 120, -1.0, 1.0, RZ1 + 7, RZ1 + 9, fp.metal(mul(DARK, 1.4)), size=0.25)      # adjustment turret
    m.part = 'glass'                # the eyepiece lens on its own: the live scope view is drawn on it (../../scope/)
    m.cyl(98, 99, 0, RZ1 + 8, 3.0, (60, 90, 110), size=0.25, edge=0.25)
    m.part = 'sight'
    m.box(97.5, 98, -0.25, 0.25, RZ1 + 7.75, RZ1 + 8.25, (255, 40, 30), size=0.25)
    m.cyl(113, 114, 0, RZ1 + 8, 3.0, (90, 130, 150), size=0.25, edge=0.25)
    m.decal(["..###..", ".#####.", "#######", "#.....#", "#######", ".#####.", "..###.."], 102, RZ1 + 12, '+y',
            STICKER, dot=2, mode='paint')

    # ---------------------------------------------------------------- the wasteland layer
    for side in ('+y', '-y'):
        m.crack(30, 6, side, 16, 701 if side == '+y' else 702, heading=0.2)
    wl.tape(m, 'x', 28.0, 33.0, (27, 34, -6, 6, -10, 17), col=wl.DUCT_BLACK, seed=703, part='tape')
    wl.cloth(m, 'x', 140.0, 150.0, (139, 151, -7, 7, 0, 18), col=wl.CLOTH_KHAKI, seed=704, part='cloth', layers=2,
             tail=(145.0, -6.0, 1.0, 5.0, 1.0))
    m.paint_line([(102, RZ1 + 10), (108, RZ1 + 8)], '+y', lambda c: mix(c, (220, 220, 210), 0.5))   # scuffed sticker
    wl.rust(m, (BX1 - 15, BX1 + 1, -4, 4, Z_BORE - 4, Z_BORE + 4), amount=0.35, seed=705, pits=0.03)
    wl.rust(m, (RX0, RX1, -RW, RW, RZ0, RZ1 + 2), amount=0.12, seed=706)
    wl.soot(m, (BX1 - 3, BX1 + 0.5, -4, 4, Z_BORE - 4, Z_BORE + 4), amount=0.55, seed=707)
    for side in ('+y', '-y'):
        wl.chips(m, side, (RX0 + 2, RX1 - 2, RZ0 + 1, RZ1), 10, 708 if side == '+y' else 709, under=mul(STEEL, 1.2))
        m.scratches(side, (RX0, RX1, RZ0, RZ1), 6, 710 if side == '+y' else 711, lighten=1.2, length=(1.5, 4.5))
    m.crack(160, 10, '-y', 12, 712, heading=3.1)
    wl.cavity(m)
    m.wear_edges(0.15, (200, 190, 170))
    m.grime(0.18, 713)
    wl.simplify(m)
    return m
