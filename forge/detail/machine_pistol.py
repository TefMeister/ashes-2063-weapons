# Ashes 2063: the Machine Pistol (Ingram), DETAILED (2026-11-02). Gun only: the body rig's hand docks onto the grip.
#
# Game look (in-hand SINGRA* / Ingram*, pickup INGPA / MPIPA): a grey-black stamped box receiver, the magazine running
# down through the grip, a cocking knob on top, a long dark suppressor (the upgraded builds).
# Real-life detail (refs/machine_pistol.md; Cobray M11 / SOCOM M11 photos): threaded barrel stub, front sight post
# between guard ears, rear peep sight, cocking slot along the top with its knob, ejection port with the bolt face,
# selector lever over the trigger, guard with a sling loop, receiver pins and rivets, holes in the back plate, magazine
# with a base plate and its release at the heel of the grip.
# Wasteland layer: the suppressor is home-made, a steel tube held on with hose clamps, wire and red tape, holes drilled
# in its end; paracord sling through the back loop, black tape on the grip, rust, chips, scratches.
import math

from _common import Model, fp, wl, STEEL, STEEL_HI, DARK, BRASS, mul, mix, hash01

GREY = (74, 74, 78)
GREY_DK = (58, 58, 62)
SUPP = (62, 66, 68)
TAPE_RED = (150, 32, 28)
Z_BORE = 12.0
RX0, RX1, RZ0, RZ1, RW = 0.0, 70.0, 2.0, 20.0, 10.0
GRIP = [(38, 2), (24, 2), (24, -30), (38, -30)]
SX0, SX1, SR = 76.0, 146.0, 4.2


def build():
    m = Model("ashes_machine_pistol_detail")
    m.pivot = (31, 0, 0)
    g = fp.metal(GREY, speck=0.06)

    # ---------------------------------------------------------------- receiver
    m.part = 'receiver'
    m.cbox(RX0, RX1, RW, RZ0, RZ1, g, bevel=0.75, bevel_x=0.5, edge=0.25)
    m.box(RX0 + 8, RX1 - 6, -0.75, 0.75, RZ1 - 0.75, RZ1 + 0.1, None, size=0.25, carve=True)    # cocking slot
    m.box(RX0 + 8, RX1 - 6, -0.5, 0.5, RZ1 - 1.0, RZ1 - 0.75, DARK, size=0.25)
    for side in ('+y', '-y'):
        m.groove([(RX0 + 1, RZ0 + 2.0), (RX1 - 1, RZ0 + 2.0)], side, depth=1, dark=0.45)     # upper / lower seam
        m.screw(RX1 - 4.0, RZ0 + 3.5, side, mul(GREY, 0.75), kind='rivet')                   # front pin
        m.screw(RX0 + 3.5, RZ0 + 3.5, side, mul(GREY, 0.75), kind='rivet')                   # rear pin
        for x in (12.0, 44.0, 58.0):
            m.screw(x, RZ1 - 2.0, side, mul(GREY, 0.85), kind='rivet')
    for (y, z) in ((-2.5, 8.0), (2.5, 8.0), (0.0, 14.0), (-2.5, 14.0)):                    # holes in the back plate
        m.box(RX0 - 0.1, RX0 + 0.5, y - 0.5, y + 0.5, z - 0.5, z + 0.5, None, size=0.25, carve=True)
    m.part = 'bolt'
    m.box(36, 50, -RW / 2 - 0.5, -RW / 2 + 1.25, 12.0, 16.0, None, size=0.25, carve=True)       # ejection port
    m.box(36, 50, -RW / 2 + 1.25, -RW / 2 + 1.5, 12.0, 16.0, fp.metal(STEEL_HI), size=0.25)
    m.box(46, 50, -RW / 2 + 1.0, -RW / 2 + 1.25, 13.0, 15.0, fp.metal(STEEL), size=0.25)
    m.part = 'cocking_knob'
    m.cyl(RZ1, RZ1 + 2.5, 52.0, 0, 1.4, fp.metal(STEEL), axis='z', size=0.25, edge=0.25)
    m.cyl(RZ1 + 2.0, RZ1 + 3.0, 52.0, 0, 1.9, fp.metal(mul(STEEL, 0.8)), axis='z', size=0.25, edge=0.25)
    m.box(51.75, 52.25, -1.5, 1.5, RZ1 + 2.75, RZ1 + 3.0, mul(STEEL, 0.5), size=0.25)          # slot in the knob
    m.part = 'sights'
    for y in (-2.25, 1.25):                                                                 # front guard ears
        m.box(RX1 - 4.0, RX1 - 1.0, y, y + 1.0, RZ1, RZ1 + 3.0, g, size=0.25)
    m.box(RX1 - 3.0, RX1 - 2.0, -0.5, 0.5, RZ1, RZ1 + 2.5, fp.metal(DARK), size=0.25)         # front post
    for k in range(16):                                                                     # rear peep ring
        a = k * math.tau / 16
        m.box(2.0, 3.0, math.cos(a) * 1.5 - 0.25, math.cos(a) * 1.5 + 0.25, RZ1 + 2.5 + math.sin(a) * 1.5 - 0.25,
              RZ1 + 2.5 + math.sin(a) * 1.5 + 0.25, fp.metal(GREY_DK), size=0.25)
    m.box(2.0, 3.0, -1.0, 1.0, RZ1, RZ1 + 1.0, fp.metal(GREY_DK), size=0.25)
    m.part = 'barrel'
    m.cyl(RX1, RX1 + 6.0, 0, Z_BORE, 1.8, fp.metal(STEEL), size=0.25, edge=0.25)
    for k in range(10):                                                                     # thread
        m.cyl(RX1 + 1 + k * 0.5, RX1 + 1.25 + k * 0.5, 0, Z_BORE, 2.0, fp.metal(mul(STEEL, 0.75)), size=0.25,
              edge=0.25)

    # ---------------------------------------------------------------- grip, magazine, guard, trigger, selector
    m.part = 'grip'
    m.cprism(GRIP, 7.5, fp.metal(GREY_DK), bevel=0.75, edge=0.25)
    m.part = 'mag'
    m.cbox(25.5, 36.5, 5.5, -40.0, -30.0, fp.metal(mul(GREY_DK, 0.9)), size=0.5, edge=0.25)
    m.cbox(25.0, 37.0, 6.5, -41.0, -40.0, fp.metal(mul(GREY_DK, 0.75)), size=0.25)            # base plate
    m.box(23.5, 24.5, -1.0, 1.0, -30.0, -27.5, fp.metal(STEEL), size=0.25)                     # heel release
    m.part = 'guard'
    m.fill(lambda x, y, z: abs(y) < 0.75 and 38 <= x <= 56 and -8 <= z <= 2 and not (39.5 < x < 54.5 and -6.5 < z),
           (38, 56, -1, 1, -8, 2), g, 0.25)
    for k in range(10):                                                                     # sling loop at its front
        a = k * math.tau / 10
        m.box(56.5 + math.cos(a) * 1.2, 56.75 + math.cos(a) * 1.2, -0.25, 0.25, -6.0 + math.sin(a) * 1.2,
              -5.75 + math.sin(a) * 1.2, fp.metal(STEEL), size=0.25)
    m.part = 'trigger'
    fp.trigger(m, 45, 2, fp.metal(DARK), length=5.5, curve=1.5)
    m.part = 'selector'
    m.box(42.0, 49.0, RW / 2, RW / 2 + 0.5, 4.0, 5.0, fp.metal(STEEL), size=0.25)
    m.box(48.0, 49.5, RW / 2, RW / 2 + 0.75, 4.0, 6.0, fp.metal(STEEL_HI), size=0.25)

    # ---------------------------------------------------------------- the home-made suppressor
    m.part = 'suppressor'
    m.cyl(SX0, SX1, 0, Z_BORE, SR, fp.metal(SUPP), edge=0.5)
    m.cyl(SX0 - 2.0, SX0 + 1.0, 0, Z_BORE, SR - 0.75, fp.metal(STEEL), size=0.25, edge=0.25)   # coupler onto the thread
    m.cyl(SX1 - 0.25, SX1 + 0.1, 0, Z_BORE, SR - 0.5, None, size=0.25, edge=0.25, carve=True)
    m.cyl(SX1 - 1.0, SX1 + 0.2, 0, Z_BORE, 1.2, None, size=0.25, edge=0.25, carve=True)
    for k in range(6):                                                                      # drilled vent holes
        a = k * math.tau / 6
        m.box(SX1 - 0.5, SX1 + 0.1, math.cos(a) * 2.6 - 0.3, math.cos(a) * 2.6 + 0.3, Z_BORE + math.sin(a) * 2.6 - 0.3,
              Z_BORE + math.sin(a) * 2.6 + 0.3, None, size=0.25, carve=True)
    m.groove([(SX0 + 30, Z_BORE - SR), (SX0 + 30, Z_BORE + SR)], '+y', depth=1, dark=0.4)     # its weld seam
    for x in (SX0 + 3.0, SX0 + 40.0):
        wl.hose_clamp(m, x, 0, Z_BORE, SR, part='suppressor')
    wl.tape(m, 'x', SX1 - 22.0, SX1 - 12.0, (SX1 - 23, SX1 - 11, -6, 6, Z_BORE - 6, Z_BORE + 6), col=TAPE_RED,
            seed=601, part='tape')
    wl.wire_wrap(m, SX0 + 12.0, SX0 + 16.0, 0, Z_BORE, SR, pitch=0.8, col=wl.WIRE_COPPER, part='suppressor')

    # ---------------------------------------------------------------- the wasteland layer
    m.part = 'sling'
    for k in range(12):                                                                     # a loop on the back plate
        a = k * math.tau / 12
        m.box(-1.0 + math.cos(a) * 1.1, -0.75 + math.cos(a) * 1.1, -0.25, 0.25, 17.0 + math.sin(a) * 1.1,
              17.25 + math.sin(a) * 1.1, fp.metal(STEEL), size=0.25)
    for i in range(48):                                                                     # paracord from it to the grip
        t = i / 47
        x = -1.0 + 24.5 * t - math.sin(t * math.pi) * 6.0
        z = 16.0 - 36.0 * t
        m.put(x, -0.25 + 0.25 * (i % 2), z, wl.PARACORD if i % 5 else mul(wl.PARACORD, 0.7), 0.25, 'sling')
    wl.tape(m, 'z', -18.0, -12.0, (22, 40, -5, 5, -18.5, -11.5), col=wl.DUCT_BLACK, seed=602, part='tape')
    wl.rust(m, (RX0, RX1, -RW, RW, RZ0, RZ1 + 1), amount=0.18, seed=603, pits=0.03)
    wl.rust(m, (SX0, SX1, -6, 6, Z_BORE - 6, Z_BORE + 6), amount=0.25, seed=604, pits=0.03)
    wl.soot(m, (SX1 - 2, SX1 + 0.5, -5, 5, Z_BORE - 5, Z_BORE + 5), amount=0.6, seed=605)
    wl.soot(m, (36, 50, -RW, -2, 11, 17), amount=0.45, seed=606)
    for side in ('+y', '-y'):
        wl.chips(m, side, (RX0 + 2, RX1 - 2, RZ0 + 1, RZ1 - 1), 10, 607 if side == '+y' else 608, under=mul(STEEL, 1.2))
        m.scratches(side, (RX0, RX1, RZ0, RZ1), 6, 609 if side == '+y' else 610, lighten=1.2, length=(1.5, 4.5))
    wl.cavity(m)
    m.wear_edges(0.15, (180, 180, 184))
    m.grime(0.18, 611)
    wl.simplify(m)
    return m
