# Ashes Afterglow (episode 2): the Killer P.I.G. (pickup PBFGA, in hand p*g*), forge cube version.
# From the pictures: a heavy, rust-orange shell cannon: a fat body wrapped in rusty bands, a big six-hole revolving
# drum, a pale bone-coloured perforated guard arching over the top, brass gears and a chain of studs down the side, a
# magazine under it in black-and-orange hazard stripes, a short fat muzzle and a fold-down leg at the front.
import math

from _common import Model, fp, BLACK, STEEL, STEEL_HI, DARK, BRASS, SCREW, RUST, COPPER, mul, mix, hash01

ORANGE_RUST = (160, 82, 40)
BONE = (196, 186, 150)
HAZARD = (210, 120, 30)
Z_AXIS = 16.0


def build():
    m = Model("ashes_killer_pig")
    m.pivot = (52, 0, 0)
    rust = fp.rusty(ORANGE_RUST, mul(RUST, 0.7), 0.5, seed=141)
    # the body: a fat rounded box, banded
    m.cbox(20, 120, 22.0, 2, 30, rust, bevel=4.0, bevel_x=2.0, edge=0.5)
    for x in (26, 50, 92, 114):
        m.cbox(x, x + 3, 23.0, 1, 31, fp.metal(BLACK), bevel=4.0, edge=0.25)
    # the revolving drum on the right side of the body: six big holes, a hub
    m.part = 'drum'
    m.cyl(-17, -11, 72, Z_AXIS, 13.0, fp.metal(STEEL), axis='y', edge=0.25)
    for k in range(6):
        a = k * math.pi / 3
        m.cyl(-18, -10, 72 + math.cos(a) * 8, Z_AXIS + math.sin(a) * 8, 3.2, None, axis='y', edge=0.25, carve=True)
        m.cyl(-14, -13, 72 + math.cos(a) * 8, Z_AXIS + math.sin(a) * 8, 3.2, fp.metal(BRASS), axis='y', size=0.25,
              edge=0.25)
    m.cyl(-19, -11, 72, Z_AXIS, 2.6, fp.metal(STEEL_HI), axis='y', edge=0.25)
    m.part = 'body'
    # the barrel: short and fat, with a heavy ring muzzle
    m.cyl(120, 160, 0, Z_AXIS, 7.0, fp.metal(BLACK), edge=0.5)
    m.cyl(156, 166, 0, Z_AXIS, 8.5, fp.metal(mul(STEEL, 0.8)), edge=0.25)
    m.cyl(160, 167, 0, Z_AXIS, 5.0, None, edge=0.25, carve=True)
    m.cyl(158, 160, 0, Z_AXIS, 5.0, fp.metal(DARK), size=0.25, edge=0.25)
    # the bone-coloured guard arching over the top, full of holes
    for i in range(60):
        t = i / 59
        x = 30 + t * 70
        z = 30 + math.sin(t * math.pi) * 12
        m.box(x, x + 1.5, -9, 9, z, z + 2, BONE, size=0.5, keep=True)
    for i in range(7):
        x = 36 + i * 9
        z = 30 + math.sin((x - 30) / 70 * math.pi) * 12
        m.box(x, x + 3, -6, 6, z - 1, z + 3, None, size=0.5, carve=True)
    for x in (32, 98):
        m.cbox(x, x + 2, 18.0, 28, 33, BONE, size=0.5)
    # brass gears on the left, and a chain of studs
    for xc, r in ((40, 6.0), (54, 4.0)):
        m.cyl(11, 13, xc, 12, r, fp.metal(BRASS), axis='y', edge=0.25)
        for k in range(10):
            a = k * math.tau / 10
            m.box(xc + math.cos(a) * (r + 0.5) - 0.5, xc + math.cos(a) * (r + 0.5) + 0.5, 11, 12.5,
                  12 + math.sin(a) * (r + 0.5) - 0.5, 12 + math.sin(a) * (r + 0.5) + 0.5, fp.metal(BRASS),
                  size=0.25)
    for i in range(14):
        m.ball(64 + i * 4, 11.5, 6 + (i % 2), 1.2, fp.metal(BRASS), edge=0.25)
    # the hazard-striped magazine underneath
    m.part = 'mag'
    m.cbox(50, 76, 14.0, -24, 2, lambda x, y, z: HAZARD if int((x + z) // 3) % 2 else (24, 22, 20), bevel=1.5,
           edge=0.5)
    m.part = 'body'
    # grip and trigger at the back, a carry bar, the fold-down leg at the front
    m.cprism([(30, 4), (22, -6), (18, -24), (30, -26), (34, -10), (40, 2)], 9.0, fp.metal(BLACK), bevel=1.5,
             edge=0.5)
    fp.guard(m, 34, 50, -10, 2, fp.metal(BLACK))
    fp.trigger(m, 42, 2, fp.metal(STEEL_HI), length=7)
    m.cprism([(128, 9), (134, 9), (150, -14), (154, -14), (154, -16), (144, -16), (126, 6)], 3.0, fp.metal(STEEL),
             size=0.5, edge=0.25)
    m.cbox(0, 22, 12.0, 6, 26, rust, bevel=3.0, edge=0.5)                       # the rear cap
    m.cyl(-4, 0, 0, Z_AXIS, 5.0, fp.metal(BLACK), edge=0.25)
    for side in ('+y', '-y'):
        for x in range(28, 118, 10):
            m.screw(x, 4, side, SCREW, kind='rivet')
            m.screw(x, 28, side, SCREW, kind='rivet')
        m.decal(["###..#..###", "#.#..#..#..", "###..#..#.#", "#....#..#.#", "#....#..###"], 96, 22, side,
                (230, 210, 170), mode='paint')                              # P.I.G.
    m.wear_edges(0.45, (220, 170, 120))
    m.scratches('+y', (20, 120, 2, 30), 18, 141)
    m.crack(40, 18, '+y', 18, 142, heading=0.2)
    m.crack(100, 10, '-y', 14, 143, heading=2.8)
    m.grime(0.3, 144)
    return m
