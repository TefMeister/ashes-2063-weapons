# Ashes 2063: the 9mm Autoloader, DETAILED (2026-11-02). Gun only: the body rig's hand docks onto the grip.
#
# Game look (in-hand Glock*, pickup GLOKA): a Glock-like service pistol, dark grey polymer frame, a lighter slide worn
# through to red-brown rust and old blood, big squared sights, a red-brown magazine base.
# Real-life detail (refs/handgun.md; Glock 17 / 19 photos): rear slide serrations, ejection port with the barrel hood
# and a case showing, extractor behind the port, rolled slide text, front-slanted slide nose, recoil spring guide under
# the muzzle, accessory rail on the dust cover, takedown lever and slide stop lever, locking block and trigger pins,
# square guard with a serrated hook, trigger with its safety blade, magazine release, finger grooves, square grip
# texture with a logo panel, beavertail, magazine base plate.
# Wasteland layer: rust bloom on the slide and in the serrations, chipped paint, black electrical tape on the grip, a
# cheap torch strapped under the rail with a hose clamp and duct tape, scratches.
import math

from _common import Model, fp, wl, STEEL, DARK, BRASS, mul, mix, hash01

SLIDE_GREY = (100, 98, 96)
FRAME_GREY = (64, 64, 66)
BLOOD = (98, 30, 20)
DOT = (235, 235, 228)
TORCH_RED = (150, 36, 30)
Z_BORE = 9.0
SX0, SX1, SZ0, SZ1, SW = 0.0, 58.0, 4.0, 15.0, 7.5
FRAME = [(1, 4.25), (54, 4.25), (54, 1), (40, 0), (22, 0), (14, -4), (4, -4), (0, 1)]
GRIP_BACK = [(15, 2), (1.5, 3.0), (-1.5, 1.5), (-6, -20), (-6.5, -27)]
GRIP_FRONT = [(7.5, -27), (9.5, -22.5), (8.5, -20.5), (10.5, -17), (9.5, -15), (12, -11), (11, -9), (13.5, -5),
              (17, -2)]


def build():
    m = Model("ashes_handgun_detail")
    m.pivot = (6, 0, 0)

    # ---------------------------------------------------------------- slide
    m.part = 'slide'
    m.cbox(SX0, SX1, SW, SZ0, SZ1, fp.metal(SLIDE_GREY), bevel=1.25, bevel_x=0.5, edge=0.25)
    m.prism([(SX1 - 4, SZ1), (SX1, SZ1 - 3), (SX1, SZ1 + 1), (SX1 - 4, SZ1 + 1)], -SW, SW, None, size=0.25, carve=True)
    m.cbox(SX1 - 0.5, SX1 + 0.1, 3.5, Z_BORE - 1.75, Z_BORE + 1.75, None, size=0.25, carve=True)        # muzzle face
    m.cyl(SX1 - 0.75, SX1 - 0.25, 0, Z_BORE, 1.6, fp.metal(mul(STEEL, 0.6)), size=0.25, edge=0.25)
    m.cyl(SX1 - 1.0, SX1 + 0.2, 0, Z_BORE, 0.9, None, size=0.25, edge=0.25, carve=True)
    m.cyl(SX1 - 1.25, SX1 - 1.0, 0, Z_BORE, 0.9, DARK, size=0.25, edge=0.25)
    for side in ('+y', '-y'):                                                    # rear serrations
        for i in range(8):
            x = 2.5 + i * 1.25
            m.groove([(x, SZ0 + 1.5), (x, SZ1 - 1.25)], side, depth=2, dark=0.4)
    m.box(SX0 - 0.25, SX0 + 0.25, -2.0, 2.0, SZ0 + 2, SZ1 - 2, fp.metal(mul(FRAME_GREY, 1.2)), size=0.25)   # back plate
    m.box(SX0 - 0.3, SX0 + 0.1, -0.4, 0.4, Z_BORE - 0.4, Z_BORE + 0.4, DARK, size=0.25)                   # pin hole
    # ejection port on the right with the barrel hood and a spent case
    m.box(30, 43, -SW / 2 - 0.5, 0.75, 11.5, SZ1 + 0.5, None, size=0.25, carve=True)
    m.box(30, 43, -1.75, 1.75, 10.5, 13.75, fp.metal(mul(STEEL, 0.85)), size=0.25)
    m.box(30.5, 36, -1.75, 1.75, 13.5, 13.75, fp.metal(mul(STEEL, 1.1)), size=0.25)
    m.cyl(36.5, 41.0, -0.5, 12.75, 1.0, BRASS, size=0.25, edge=0.25)
    m.part = 'extractor'
    m.box(25, 30, -SW / 2 - 0.25, -SW / 2, 11.75, 12.75, fp.metal(mul(STEEL, 0.8)), size=0.25)
    m.part = 'slide'
    m.decal(["#.###...###.#.#..#.###", "#...#...#.#.#.#.##.#.#", "#..#....###..#..#..###", "#.#.......#.#.#.#....#",
             "#.#.....###.#.#.#..###"], 20, 11.5, '+y', mul(SLIDE_GREY, 0.45), mode='carve')   # "17  9X19"
    m.part = 'sights'
    m.box(SX1 - 4.5, SX1 - 3.0, -0.75, 0.75, SZ1, SZ1 + 2.0, fp.metal(DARK), size=0.25)
    m.box(SX1 - 4.75, SX1 - 4.5, -0.5, 0.5, SZ1 + 1.0, SZ1 + 1.75, DOT, size=0.25)
    m.box(1.5, 4.0, -2.25, 2.25, SZ1, SZ1 + 2.25, fp.metal(DARK), size=0.25)
    m.box(1.25, 4.25, -0.75, 0.75, SZ1 + 0.75, SZ1 + 2.5, None, size=0.25, carve=True)
    for y in (-1.5, 0.75):                                                         # the U-notch outline
        m.box(3.75, 4.0, y, y + 0.75, SZ1 + 0.75, SZ1 + 2.0, DOT, size=0.25)

    # ---------------------------------------------------------------- frame, rail, levers, pins
    m.part = 'frame'
    m.cprism(FRAME, 7.0, fp.metal(FRAME_GREY, speck=0.08), bevel=0.75, edge=0.25)
    m.cyl(SX1 - 4.0, SX1 - 0.25, 0, Z_BORE - 4.0, 0.9, fp.metal(mul(STEEL, 0.7)), size=0.25, edge=0.25)  # spring guide
    for x in (41.0, 45.0, 49.0):                                                   # rail slots
        m.box(x, x + 1.25, -3.75, 3.75, 0.75, 1.75, None, size=0.25, carve=True)
    for side, sgn in (('+y', 1), ('-y', -1)):
        m.groove([(SX0, SZ0 + 0.25), (54, SZ0 + 0.25)], side, depth=1, dark=0.35)  # slide / frame line
        m.screw(22.0, 2.5, side, mul(STEEL, 0.6), kind='rivet')                     # trigger pin
        m.screw(30.0, 2.5, side, mul(STEEL, 0.6), kind='rivet')                     # locking block pin
        m.screw(6.0, -1.0, side, mul(STEEL, 0.6), kind='rivet')                     # trigger housing pin
    m.part = 'takedown'
    for y in (3.5, -3.75):                                                          # takedown lever, both sides
        m.box(33.5, 36.0, y, y + 0.25, 1.75, 3.25, fp.metal(mul(STEEL, 0.55)), size=0.25)
    m.part = 'slide_stop'
    m.box(16.0, 27.0, 3.5, 3.75, 2.5, 3.25, fp.metal(mul(STEEL, 0.55)), size=0.25)
    m.box(16.0, 18.5, 3.5, 4.0, 2.5, 3.5, fp.metal(mul(STEEL, 0.6)), size=0.25)
    m.part = 'mag_release'
    m.box(14.0, 16.5, 3.25, 3.75, -3.25, -1.0, fp.metal(mul(FRAME_GREY, 0.8)), size=0.25)

    m.part = 'guard'

    def guard_in(x, y, z):
        return abs(y) < 1.0 and 18 <= x <= 37 and -8 <= z <= 0 and not (19.5 < x < 35.5 and -6.5 < z)
    m.fill(guard_in, (18, 37, -1, 1, -8, 0), fp.metal(FRAME_GREY), 0.25)
    for k in range(5):                                                               # serrated front hook
        m.box(36.75, 37.0, -1.0, 1.0, -7.5 + k * 1.25, -7.0 + k * 1.25, None, size=0.25, carve=True)
    m.part = 'trigger'
    fp.trigger(m, 26, 0, fp.metal(DARK), length=5.0, curve=1.5)
    m.box(26.25, 26.75, -0.25, 0.25, -4.0, -0.5, fp.metal(mul(STEEL, 0.8)), size=0.25)   # safety blade

    # ---------------------------------------------------------------- grip
    m.part = 'grip'
    m.cprism(GRIP_BACK + GRIP_FRONT, 7.5, fp.metal(FRAME_GREY, speck=0.1), bevel=1.25, edge=0.25)
    m.cprism([(1.5, 3.0), (-3.0, 2.5), (-4.0, 1.0), (0.0, 1.0)], 6.5, fp.metal(FRAME_GREY), size=0.25)   # beavertail
    for side in ('+y', '-y'):
        wl.stipple(m, side, (-5, 9, -24, -6), 31 if side == '+y' else 32, depth_share=0.45, dark=0.62)
        m.box(-1.5, 3.5, (3.75 if side == '+y' else -4.0), (4.0 if side == '+y' else -3.75), -6.0, -2.5,
              fp.metal(mul(FRAME_GREY, 0.85)), size=0.25)                            # logo panel
        m.decal(["###.#...###.###.#.#", "#...#...#.#.#...##.", "#.#.#...#.#.#...#.#", "###.###.###.###.#.#"], -1.0,
                -3.0, side, mul(FRAME_GREY, 1.6), mode='paint')
    m.part = 'mag'
    m.cbox(-6.5, 7.5, 6.5, -28.0, -26.5, fp.metal(mul(BLOOD, 1.1)), size=0.25)
    m.box(-7.0, -6.5, -2.0, 2.0, -28.0, -27.0, fp.metal(mul(BLOOD, 0.9)), size=0.25)   # base plate tab

    # ---------------------------------------------------------------- the wasteland layer: a torch strapped under
    m.part = 'torch'
    m.cyl(39.5, 56.0, 0, -1.0, 2.0, fp.metal(TORCH_RED), edge=0.25)
    m.cyl(56.0, 58.5, 0, -1.0, 2.5, fp.metal(mul(STEEL, 0.9)), size=0.25, edge=0.25)  # its head
    m.cyl(58.25, 58.75, 0, -1.0, 1.9, (238, 232, 190), size=0.25, edge=0.25)           # the lens
    m.box(44.0, 45.5, -0.5, 0.5, -3.25, -2.75, (30, 30, 30), size=0.25)                    # its button
    wl.hose_clamp(m, 42.0, 0, -1.0, 2.0, part='torch')
    wl.tape(m, 'x', 49.0, 52.5, (48.5, 53, -3, 3, -3.5, 2.5), col=wl.DUCT, seed=301, part='tape')
    wl.tape(m, 'z', -21.0, -17.5, (-7.5, 12, -4.5, 4.5, -21.5, -17), col=wl.DUCT_BLACK, seed=302, part='tape')

    wl.rust(m, (SX0, SX1, -SW, SW, SZ0, SZ1 + 1), amount=0.3, seed=303, pits=0.04)
    wl.rust(m, (1, 14, -SW, SW, SZ0 + 1, SZ1), amount=0.45, seed=304, pits=0.02)       # in the serrations
    m.recolour(lambda x, y, z: z > SZ0 and hash01(int(x // 1.25), int(z // 1.25), int(y > 0), 305)
               * hash01(int(x // 4), int(z // 4), 313) > 0.62,
               lambda x, y, z: mix(BLOOD, (60, 18, 12), hash01(int(x), int(z), 306)))   # old blood, as the sprite
    for side in ('+y', '-y'):
        wl.chips(m, side, (12, 56, SZ0 + 1, SZ1 - 0.5), 8, 307 if side == '+y' else 308, under=mul(STEEL, 1.15))
        m.scratches(side, (0, 56, 4, 15), 5, 309 if side == '+y' else 310, lighten=1.2, length=(1.5, 4.0))
    m.crack(4, -14, '-y', 6, 311, heading=1.3)
    wl.cavity(m)
    m.wear_edges(0.18, (186, 184, 180))
    m.grime(0.15, 312)
    wl.simplify(m)
    return m
