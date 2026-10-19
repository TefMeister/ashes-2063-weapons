# Ashes 2063: the Machine Pistol, an Ingram (pickup MPIPA / MPI2A, in hand SINGRA*), forge cube version.
# From the pictures: a pale grey stamped box receiver, the magazine running down through the grip, a cocking knob on
# top, a folded wire stock along the left side, and a long black suppressor with a red band on the muzzle.
from _common import Model, fp, BLACK, STEEL, STEEL_HI, DARK, BRASS, SCREW, mul

GREY = (146, 142, 146)                 # the pictures' pale, purple-tinged grey
GREY_DK = (92, 88, 94)
SUPP_RED = (176, 24, 22)
Z_BORE = 12.0
RECEIVER = (0, 70, 2, 20, 10.0)        # x0, x1, z0, z1, width
GRIP = [(30, 2), (24, 2), (24, -30), (38, -30), (38, 2)]
SUPP = (76, 146, 4.2)                  # x0, x1, radius


def build():
    m = Model("ashes_machine_pistol")
    m.pivot = (31, 0, 0)
    rx0, rx1, rz0, rz1, rw = RECEIVER
    m.cbox(rx0, rx1, rw, rz0, rz1, fp.metal(GREY), bevel=1.0, bevel_x=0.5, edge=0.5)
    m.cbox(rx1, rx1 + 6, 4.0, Z_BORE - 2, Z_BORE + 2, fp.metal(STEEL), size=0.5, edge=0.25)   # barrel stub
    # suppressor: black tube, ribbed, a red band at its front
    sx0, sx1, sr = SUPP
    m.cyl(sx0, sx1, 0, Z_BORE, sr, fp.metal(BLACK), edge=0.25)
    m.cyl(sx0 - 1, sx0 + 2, 0, Z_BORE, sr + 0.25, fp.metal(STEEL), edge=0.25)
    m.cyl(sx1 - 22, sx1 - 10, 0, Z_BORE, sr + 0.25, fp.metal(SUPP_RED), edge=0.25)
    m.cyl(sx1 - 1, sx1 + 0.5, 0, Z_BORE, 1.2, DARK, size=0.25, edge=0.25)
    for x in range(int(sx0) + 6, int(sx1) - 26, 6):
        for side in ('+y', '-y', '+z'):
            m.groove([(x, Z_BORE - 3) if side != '+z' else (x, -3), (x, Z_BORE + 3) if side != '+z' else (x, 3)],
                     side, depth=1, dark=0.5)
    # grip with the magazine base sticking out below it
    m.cprism(GRIP, 8.0, fp.metal(GREY_DK), bevel=1.5, edge=0.5)
    m.cbox(23, 39, 8.5, -34, -30, fp.metal(BLACK), bevel=0.5, edge=0.25)
    m.cbox(22, 40, 9.0, -35, -34, fp.metal(STEEL), size=0.5)
    # trigger guard: a square loop, and the trigger
    m.cbox(38, 58, 2.0, -8, -6.5, fp.metal(GREY_DK), size=0.5)
    m.cbox(56.5, 58, 2.0, -8, rz0, fp.metal(GREY_DK), size=0.5)
    fp.trigger(m, 44, rz0, fp.metal(DARK), length=6, curve=1.5)
    # cocking knob on top, its slot along the receiver
    m.box(10, 50, -1, 1, rz1 - 0.5, rz1, None, size=0.25, carve=True)
    m.part = 'bolt'
    m.cyl(rz1 - 1, rz1 + 3, 42, 0, 1.8, fp.metal(STEEL_HI), axis='z', edge=0.25)
    m.part = 'body'
    # sights: two ears at the back and a post at the front
    for y in (-3.5, 2.0):
        m.box(2, 5, y, y + 1.5, rz1, rz1 + 3, fp.metal(GREY), size=0.5)
    m.box(64, 66, -0.75, 0.75, rz1, rz1 + 3, fp.metal(GREY), size=0.5)
    # the folded wire stock along the left side, its butt plate at the front
    for z in (6.0, 14.0):
        m.box(-4, 62, rw / 2, rw / 2 + 1, z, z + 1, fp.metal(STEEL), size=0.5)
    m.box(60, 62, rw / 2, rw / 2 + 1.5, 4, 17, fp.metal(STEEL), size=0.5)
    m.box(-6, -2, -rw / 2, rw / 2 + 1, 4, 17, fp.metal(STEEL), size=0.5, edge=0.25)
    for side in ('+y', '-y'):
        for x in (6, 20, 56, 66):
            m.screw(x, 5, side, SCREW, kind='rivet')
        m.groove([(2, 10), (68, 10)], side, depth=1, dark=0.55)
        m.decal(["#.#.###.###", "###.#.#.#..", "#.#.###.#..", "#.#.#.#.###"], 24, 17, side, mul(GREY, 0.5),
                mode='carve')                                                     # "MAC" stamped in
    m.screw(31, -15, '+y', SCREW, kind='slot')
    m.screw(31, -15, '-y', SCREW, kind='slot')
    m.wear_edges(0.4, (200, 196, 200))
    m.scratches('+y', (2, 68, 3, 19), 14, 71)
    m.scratches('-y', (2, 68, 3, 19), 12, 72)
    m.crack(30, -20, '+y', 8, 73, heading=1.4)
    m.grime(0.2, 74)
    return m
