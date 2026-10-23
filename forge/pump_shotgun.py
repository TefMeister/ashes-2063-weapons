# Ashes 2063: the pump-action shotgun ("Pump-action shotgun", pickup GRZPA, in hand GRIZ*), forge cube version.
# From the game's pictures: a black receiver with its ejection port on the right, the barrel over a magazine tube, a
# ribbed orange wooden pump, a short wooden pistol-grip stock with blue tape round the wrist.
from _common import Model, fp, BLACK, STEEL, STEEL_HI, DARK, WOOD, WOOD_DK, TAPE, TAPE_BLUE, BRASS, RED_SHELL, \
    CUT, SCREW, mul

Z_BARREL, Z_TUBE = 11.0, 3.5
RECEIVER = (40, 104, -4, 16)          # x0, x1, z0, z1
WIDTH = 8.0
BARREL = (104, 262, 2.6, 1.5)         # x0, x1, radius, bore
TUBE = (104, 240, 2.4)
PUMP = (130, 190, -2.5, 8.5, 9.0)     # x0, x1, z0, z1, width
PORT = (64, 88, 8, 13.5)              # ejection port on the right side
GRIP = [(46, -4), (38, -4), (30, -14), (22, -28), (20, -34), (31, -36), (35, -30), (44, -12), (52, -4)]
STOCK_CAP = [(18, -32), (16, -38), (19, -42), (33, -42), (34, -36)]


def build():
    m = Model("ashes_pump_shotgun")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (40, 0, 0)
    blk = fp.metal(BLACK)
    # receiver: a box with bevelled long edges, the top a little narrower, the rear sloping into the grip
    x0, x1, z0, z1 = RECEIVER
    m.cbox(x0, x1, WIDTH, z0, z1, blk, bevel=1.0, edge=0.5)
    m.cbox(x0 - 6, x0, WIDTH - 1, 4, z1 - 1, blk, bevel=1.0, edge=0.5)          # the tang sloping to the grip
    m.cbox(x0 + 2, x1 - 2, WIDTH - 3, z1, z1 + 1, mul(BLACK, 1.1), size=0.5)    # top rib
    # ejection port on the right (-y): cut in, a red shell inside
    px0, px1, pz0, pz1 = PORT
    m.box(px0, px1, -WIDTH / 2 - 1, -WIDTH / 2 + 1.5, pz0, pz1, None, size=0.25, carve=True)
    m.box(px0, px1, -WIDTH / 2 + 1.5, -WIDTH / 2 + 2, pz0, pz1, DARK, size=0.5)
    m.cyl(px0 + 6, px0 + 16, -1.5, (pz0 + pz1) / 2, 2.0, RED_SHELL, edge=0.25)
    m.cyl(px0 + 3, px0 + 6, -1.5, (pz0 + pz1) / 2, 2.0, BRASS, edge=0.25)
    # loading port underneath, a dark slot
    m.cbox(60, 96, 4, z0, z0 + 1, None, size=0.25, carve=True)
    m.part = 'barrel'
    # barrel and magazine tube, joined at the front by a clamp
    bx0, bx1, br, bb = BARREL
    fp.barrel(m, bx0, bx1, Z_BARREL, br, fp.metal(mul(BLACK, 1.15)), bore=bb, muzzle_ring=(br + 0.25, 2, STEEL))
    tx0, tx1, tr = TUBE
    m.part = 'tube'
    m.cyl(tx0, tx1, 0, Z_TUBE, tr, blk)
    m.cyl(tx1, tx1 + 2, 0, Z_TUBE, tr - 0.5, STEEL, edge=0.25)                  # tube cap
    m.cbox(tx1 - 6, tx1 - 2, 5.5, Z_TUBE - 2, Z_BARREL + 2, fp.metal(STEEL), bevel=1, edge=0.25)   # barrel clamp
    m.part = 'sight'
    m.box(255, 257, -0.5, 0.5, Z_BARREL + 2, Z_BARREL + 3.5, STEEL_HI, size=0.25)   # front bead
    # the pump: orange wood, ribbed all round
    ux0, ux1, uz0, uz1, uw = PUMP
    m.part = 'pump'
    m.cbox(ux0, ux1, uw, uz0, uz1, fp.wood(WOOD, WOOD_DK), bevel=2.0, bevel_x=1.0, edge=0.5)
    m.part = 'body'
    for x in range(int(ux0) + 5, int(ux1) - 4, 4):                              # ribs: grooves round it
        for side in ('+y', '-y'):
            m.groove([(x, uz0 + 1), (x, uz1 - 1)], side, depth=2, width=2, dark=0.4)
        m.groove([(x, -2.5), (x, 2.5)], '-z', depth=2, width=2, dark=0.4)
    m.part = 'grip'
    # pistol grip: black, wrapped in tape with a blue band; a wooden butt cap below
    m.cprism(GRIP, 6.0, fp.flat(TAPE), bevel=1.5, edge=0.5)
    m.cprism(STOCK_CAP, 6.5, fp.wood(WOOD, WOOD_DK, along='z'), bevel=1.0, edge=0.5)
    m.recolour(lambda x, y, z: -20 <= z <= -15 and x < 40, TAPE_BLUE)
    for z in (-8, -11, -24, -27, -30):                                           # tape turns
        for side in ('+y', '-y'):
            m.groove([(20, z), (50, z + 3)], side, depth=1, width=1, dark=0.6)
    m.part = 'guard'
    # trigger guard and trigger
    fp.guard(m, 44, 62, -12, -4, blk)
    fp.trigger(m, 54, -4, STEEL)
    # pins and screws on both sides of the receiver
    for side in ('+y', '-y'):
        m.screw(50, 0, side, SCREW, kind='slot')
        m.screw(70, -1, side, SCREW, kind='slot')
        m.screw(96, 6, side, SCREW, kind='cross')
        m.screw(46, 12, side, SCREW, kind='rivet')
        m.groove([(42, 2), (102, 2)], side, depth=1, dark=0.5)                  # panel line along the receiver
    # wear: chipped edges, scratches, a long crack in the pump's wood
    m.wear_edges(0.4, (150, 150, 150), only=None)
    m.scratches('+y', (44, 100, -2, 14), 18, 11)
    m.scratches('-y', (44, 100, -2, 14), 14, 12)
    m.crack(150, 6, '+y', 18, 5, heading=0.1)
    m.crack(170, 0, '-y', 12, 6, heading=3.0)
    m.grime(0.22, 4)
    return m
