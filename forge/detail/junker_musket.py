# Ashes 2063: the Junker Musket, DETAILED (2026-11-02). Gun only: the body rig's hands dock onto the wrist and fore-end.
#
# Game look (in-hand Musket*, pickup MUSKA / MKTPA): a long home-made rifle, orange-brown wood bound with brass bands
# and copper wire, a red cloth at the wrist, a steel action with a crude bolt handle, a fat black scope with white
# scribbles, a slotted muzzle cap.
# Real-life detail (refs/junker_musket.md; M1903 Springfield photos, scope and mount photos): folded ladder rear sight
# on the barrel, upper and lower bands with sling swivels and a stacking swivel, front sight blade on its band, bolt
# with a ball handle, the cocking piece with knurling and a safety flag, the magazine cut-off lever, floor plate and
# guard screws, finger grooves along the fore-end, a checkered butt plate with a trap door, a leather sling; scope
# rings with their clamp screws, turrets, a rubber eye cup.
# The scope's eyepiece is its own part, 'glass', ready for the live scope picture (../../scope/).
# Wasteland layer: copper wire coils and brass bands (game), the red rag at the wrist, duct tape on the scope, a bottle
# cap on a string as the lens cover, white tally marks scratched on the scope, rust on the barrel, a split stock.
import math

from _common import Model, fp, wl, BLACK, STEEL, STEEL_HI, DARK, WOOD, WOOD_DK, BRASS, COPPER, RED_SHELL, mul, mix

PARK = (52, 54, 56)
LEATHER = (96, 60, 34)
Z_BORE = 12.0
STOCK = [(0, -12), (0, 12), (8, 14), (40, 12), (70, 9), (70, 2), (44, -2), (24, -6), (8, -14)]
AX0, AX1, AZ0, AZ1, AW = 66.0, 108.0, 3.0, 17.0, 8.0
FOREEND = [(108, 4), (108, 13), (176, 12.5), (180, 9), (176, 5), (112, 3)]
BX0, BX1, BR, BORE = 106.0, 232.0, 2.3, 1.2
SX0, SX1, SR = 74.0, 128.0, 4.3


def ring(m, x, y, z, r, col, axis='y', n=12, part=None):
    """A small loop of quarter cubes (sling swivels and loops), its plane across `axis`."""
    for k in range(n):
        a = k * math.tau / n
        if axis == 'y':
            m.box(x + math.cos(a) * r, x + math.cos(a) * r + 0.25, y - 0.25, y + 0.25, z + math.sin(a) * r,
                  z + math.sin(a) * r + 0.25, col, size=0.25, part=part)
        else:
            m.box(x - 0.25, x + 0.25, y + math.cos(a) * r, y + math.cos(a) * r + 0.25, z + math.sin(a) * r,
                  z + math.sin(a) * r + 0.25, col, size=0.25, part=part)


def build():
    m = Model("ashes_junker_musket_detail")
    m.pivot = (76, 0, 0)
    wood = fp.wood(WOOD, WOOD_DK)

    # ---------------------------------------------------------------- stock, butt plate, the red rag
    m.part = 'stock'
    m.cprism(STOCK, 9.0, wood, bevel=2.5, edge=0.25)
    m.part = 'butt_plate'
    m.cbox(-2, 0.5, 9.5, -13, 13, fp.metal(PARK), size=0.5)
    for z in range(-12, 12, 1):                                                         # checkering
        for y in range(-4, 4):
            if (z + y) % 2 == 0:
                m.box(-2.25, -2.0, y, y + 0.5, z, z + 0.5, mul(PARK, 0.65), size=0.25)
    m.box(-2.25, -2.0, -2.5, 2.5, 2.0, 8.0, mul(PARK, 1.25), size=0.25)                  # trap door
    m.part = 'stock'
    for side in ('+y', '-y'):
        m.crack(22, 2, side, 14, 901 if side == '+y' else 902, heading=0.3)
    wl.cloth(m, 'x', 46.0, 60.0, (45, 61, -6, 6, -4, 14), col=mul(RED_SHELL, 0.95), seed=903, part='grip', layers=2,
             tail=(58.0, -5.5, -2.0, 6.0, 1.0))

    # ---------------------------------------------------------------- action, bolt, controls
    m.part = 'action'
    m.cbox(AX0, AX1, AW, AZ0, AZ1, fp.metal(STEEL), bevel=1.0, edge=0.25)
    m.box(80, 96, -AW / 2 - 0.5, -AW / 2 + 1.5, 10, 15, None, size=0.25, carve=True)        # loading port
    m.box(80, 96, -AW / 2 + 1.5, -AW / 2 + 1.75, 10, 15, fp.metal(BRASS), size=0.25)         # a cartridge showing
    m.part = 'bolt'
    m.cyl(-AW / 2 - 6, -AW / 2, 92, 14, 0.9, fp.metal(STEEL_HI), axis='y', size=0.25, edge=0.25)
    m.ball(92, -AW / 2 - 6.5, 14, 1.8, fp.metal(STEEL_HI), size=0.25, edge=0.25)
    m.cyl(AX0 - 4, AX0, 0, 13, 2.2, fp.metal(STEEL), size=0.25, edge=0.25)                    # cocking piece
    for k in range(10):
        a = k * math.tau / 10
        m.box(AX0 - 3.5, AX0 - 1.0, math.cos(a) * 2.3 - 0.15, math.cos(a) * 2.3 + 0.15,
              13 + math.sin(a) * 2.3 - 0.15, 13 + math.sin(a) * 2.3 + 0.15, mul(STEEL, 0.6), size=0.25)
    m.box(AX0 - 1.5, AX0 - 0.5, -0.25, 0.25, 15.0, 18.0, fp.metal(STEEL_HI), size=0.25)       # safety flag
    m.part = 'cutoff'
    m.box(AX0 + 2, AX0 + 8, AW / 2, AW / 2 + 0.5, 8.0, 9.0, fp.metal(STEEL), size=0.25)
    m.part = 'floor_plate'
    m.cbox(AX0 + 6, AX0 + 30, 5.0, AZ0 - 1.5, AZ0, fp.metal(PARK), size=0.25)
    m.part = 'guard'
    fp.guard(m, 66, 86, -6, AZ0, fp.metal(BRASS))
    m.screw(68, 0, '-z', mul(BRASS, 0.8), kind='slot')
    m.screw(98, 0, '-z', mul(BRASS, 0.8), kind='slot')
    m.part = 'trigger'
    fp.trigger(m, 75, AZ0, fp.metal(STEEL_HI), length=6)

    # ---------------------------------------------------------------- fore-end, barrel, bands, sights, muzzle cap
    m.part = 'foreend'
    m.cprism(FOREEND, 9.0, wood, bevel=2.0, edge=0.25)
    for side in ('+y', '-y'):
        m.groove([(116, 10.5), (150, 10.5)], side, depth=2, width=2, dark=0.45)            # finger grooves
    m.part = 'barrel'
    fp.barrel(m, BX0, BX1, Z_BORE, BR, fp.metal(PARK), bore=BORE, edge=0.5)
    m.part = 'muzzle_cap'
    m.cyl(BX1 - 10, BX1, 0, Z_BORE, 3.0, fp.metal(STEEL), size=0.5, edge=0.25)
    for x in (BX1 - 8, BX1 - 5):
        for a in range(4):
            ang = a * math.pi / 2
            y, z = math.cos(ang) * 3.0, Z_BORE + math.sin(ang) * 3.0
            m.box(x, x + 1.5, y - 0.5, y + 0.5, z - 0.5, z + 0.5, None, size=0.25, carve=True)
    m.part = 'ladder_sight'
    m.box(110, 118, -1.75, 1.75, Z_BORE + BR - 0.25, Z_BORE + BR + 0.75, fp.metal(PARK), size=0.25)
    m.box(110.5, 117.5, -1.25, 1.25, Z_BORE + BR + 0.75, Z_BORE + BR + 1.25, fp.metal(mul(PARK, 1.3)), size=0.25)
    for x in range(111, 117):
        m.box(x, x + 0.25, -1.25, 1.25, Z_BORE + BR + 1.0, Z_BORE + BR + 1.25, (210, 210, 200), size=0.25)   # marks
    m.part = 'bands'
    for x in (114, 150, 172):
        m.cyl(x, x + 3, 0, 8.5, 5.4, fp.metal(BRASS), size=0.5, edge=0.25)
    ring(m, 151.5, 0, 2.0, 1.2, fp.metal(BRASS)(0, 0, 0), part='bands')                    # sling swivel
    ring(m, 173.5, 0, 2.0, 1.0, fp.metal(BRASS)(0, 0, 0), part='bands')                    # stacking swivel
    ring(m, 14.0, 0, -12.5, 1.2, fp.metal(STEEL)(0, 0, 0), part='bands')                   # rear swivel
    m.part = 'front_sight'
    m.box(BX1 - 13, BX1 - 11, -0.4, 0.4, Z_BORE + BR, Z_BORE + BR + 3.0, fp.metal(STEEL_HI), size=0.25)
    m.cbox(BX1 - 14, BX1 - 10, 3.0, Z_BORE - 1, Z_BORE + BR + 0.5, fp.metal(PARK), size=0.25)
    m.part = 'wire'
    for x0 in (124.0, 186.0):
        for k in range(10):
            m.cyl(x0 + k * 1.0, x0 + k * 1.0 + 0.5, 0, Z_BORE if x0 > 180 else 8.5, 3.1 if x0 > 180 else 5.6,
                  fp.metal(COPPER if k % 2 == 0 else mul(COPPER, 0.7)), size=0.25, edge=0.25)
    m.part = 'sling'
    n = 600
    for i in range(n):                                                                     # leather sling, a solid strap
        t = i / (n - 1)
        x = 14 + t * 137.5
        z = -12.5 + (2.0 + 12.5) * t - math.sin(t * math.pi) * 9.0
        col = mul(LEATHER, 0.9 + 0.2 * ((i // 12) % 2))
        for w in range(6):
            m.put(x, -0.75 + w * 0.25, z, col, 0.25, 'sling')

    # ---------------------------------------------------------------- the scope
    m.part = 'scope'
    zs = AZ1 + 6
    for x in (82, 112):
        m.cbox(x, x + 3, 5.0, AZ1, zs, fp.metal(PARK), size=0.5)
        m.cyl(x - 0.5, x + 3.5, 0, zs, SR + 0.5, fp.metal(PARK), size=0.5, edge=0.25)
        for side in ('+y', '-y'):
            m.screw(x + 1.5, zs - SR - 0.5, side, mul(STEEL, 0.6), kind='hex')               # clamp screws
    m.cyl(SX0, SX1, 0, zs, SR - 1.0, fp.metal(BLACK), edge=0.5)
    m.cyl(SX0, SX0 + 10, 0, zs, SR, fp.metal(mul(BLACK, 0.7)), size=0.5, edge=0.25)           # eye cup, rubber
    m.cyl(SX1 - 12, SX1, 0, zs, SR + 0.8, fp.metal(BLACK), size=0.5, edge=0.25)               # objective bell
    m.cyl(SX1 - 1, SX1 + 0.5, 0, zs, SR - 0.5, (70, 110, 130), size=0.25, edge=0.25)
    m.cyl(-SR - 1.5, SR + 1.5, 97, zs, 1.4, fp.metal(BLACK), axis='y', size=0.25, edge=0.25)   # windage
    m.cyl(zs, zs + SR + 1.5, 97, 0, 1.4, fp.metal(BLACK), axis='z', size=0.25, edge=0.25)     # elevation
    m.part = 'glass'               # the eyepiece lens on its own: room for the live scope picture
    m.cyl(SX0 - 0.5, SX0 + 1, 0, zs, SR - 1.5, (40, 70, 90), size=0.25, edge=0.25)
    m.part = 'scope'
    for side in ('+y', '-y'):
        m.decal(["#.#.#.#", ".......", "#######"], 100, zs + 1.5, side, (220, 220, 210), mode='paint')
    wl.tally(m, '+y', 88.0, zs - 1.0, 9, height=2.0, col=(225, 225, 215))
    wl.tape(m, 'x', 104.0, 108.0, (103, 109, -6, 6, zs - 6, zs + 6), col=wl.DUCT, seed=904, part='tape')
    m.part = 'lens_cap'                                                                  # a bottle cap on a string
    m.cyl(SX1 + 2.0, SX1 + 3.0, 0, zs - 7.0, 2.2, fp.metal((170, 40, 36)), size=0.25, edge=0.25)
    for i in range(12):
        m.put(SX1 + 0.5 + i * 0.12, 0, zs - SR - 0.5 - i * 0.2, (200, 196, 180), 0.25, 'lens_cap')

    # ---------------------------------------------------------------- the wasteland layer
    wl.rust(m, (BX0, BX1 + 1, -4, 4, Z_BORE - 4, Z_BORE + 4), amount=0.32, seed=905, pits=0.04)
    wl.rust(m, (AX0, AX1, -AW, AW, AZ0, AZ1 + 1), amount=0.15, seed=906)
    wl.soot(m, (BX1 - 3, BX1 + 0.5, -4, 4, Z_BORE - 4, Z_BORE + 4), amount=0.6, seed=907)
    for side in ('+y', '-y'):
        m.scratches(side, (AX0, AX1, AZ0, AZ1), 6, 908 if side == '+y' else 909, lighten=1.2, length=(1.5, 4.5))
    m.crack(140, 9, '-y', 12, 910, heading=3.0)
    wl.cavity(m)
    m.wear_edges(0.15, (210, 190, 150))
    m.grime(0.22, 911)
    wl.simplify(m)
    return m
