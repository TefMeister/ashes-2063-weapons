# Ashes 2063: the revolver, DETAILED (2026-11-02). Gun only: the body rig's hand docks onto the grip.
#
# Game look (in-hand PISTO*, pickup REVPA): bright steel, heavy barrel with a full under-lug and a vented top rib, a
# fat fluted six-shot cylinder, a spur hammer, an orange front-sight insert, a dark finger-groove grip.
# Real-life detail (refs/revolver.md; Taurus 66/627 and S&W 686 photos): side plate on the RIGHT with its seam and
# three screws, cylinder latch with grooves on the LEFT behind the cylinder, crane seam below the cylinder front,
# cylinder stop notches with lead-in grooves over each chamber, ejector rod at the cylinder front, forcing cone and
# cylinder gap, adjustable rear sight with its elevation and windage screws, anti-glare serrations on the top strap,
# hammer and trigger pivot pins, recessed muzzle crown, grip medallion, lanyard ring.
# Wasteland layer: soot round the cylinder gap and front face, rust in the flutes and round the screws, holster-wear
# scratches, tally marks, duct tape round the grip, paracord through the lanyard ring.
import math

from _common import Model, fp, wl, STEEL_HI, DARK, BRASS, mul, mix

STEEL_R = (116, 120, 124)            # bright stainless, a touch lighter than the first pass (the sprites read chrome)
STEEL_DK = (84, 87, 91)
RUBBER = (40, 40, 42)
ORANGE = (255, 130, 26)
COPPER_TIP = (184, 112, 52)
GOLD = (190, 156, 72)

Z_BORE = 10.0
CYL_X0, CYL_X1, CYL_R = 8.5, 25.5, 5.6
CYL_Z = Z_BORE - 3.3                 # the top chamber lines up with the bore
CHAMBER_R, CHAMBER_RING = 1.1, 3.3
BARREL_X1, BARREL_R, BORE_R = 74.0, 2.3, 1.0
FRAME = [(0, 2), (0, 15), (6, 15), (30, 15), (30, 3), (24, -0.5), (8, -2)]
GRIP_BACK = [(2, 2), (-4, 0), (-12, -16), (-14, -26), (-12.5, -29)]
GRIP_FRONT = [(-2, -29.5), (4, -25), (7, -22), (5.5, -19), (7.5, -16), (6, -13), (8.5, -10), (7.5, -7), (9.5, -3),
              (10, 0)]


def build():
    m = Model("ashes_revolver_detail")
    m.pivot = (4, 0, 0)
    st = fp.metal(STEEL_R, speck=0.05)

    # ---------------------------------------------------------------- frame, with the cylinder window cut through
    m.part = 'frame'
    m.cprism(FRAME, 7.0, st, bevel=1.0, edge=0.25)
    m.box(CYL_X0 - 0.5, CYL_X1 + 0.5, -4, 4, 0.75, 14.0, None, size=0.25, carve=True)       # the window
    m.box(0, 30, -2.5, 2.5, 15, 17, fp.metal(mul(STEEL_R, 0.94)), size=0.25, edge=0.25, bevel=0.5)   # top strap
    for x in range(6 * 4, 26 * 4):                                            # anti-glare serrations across it
        if x % 2 == 0:
            m.box(x / 4, x / 4 + 0.25, -1.5, 1.5, 16.75, 17, mul(STEEL_R, 0.62), size=0.25)
    # hammer slot behind the top strap, frame tang over the grip
    m.box(-2.5, 1.0, -0.75, 0.75, 11.5, 17.5, None, size=0.25, carve=True)
    m.cprism([(-1, 1), (-4, 1), (-6, -4), (2, -4), (4, 1)], 7.5, st, size=0.5, edge=0.25)
    # forcing cone: the barrel's back end showing in the window, and the ejector rod under it
    m.cyl(CYL_X1 + 0.5, 26.5, 0, Z_BORE, 1.9, fp.metal(STEEL_DK), size=0.25, edge=0.25)
    m.part = 'ejector'
    m.cyl(CYL_X1, 27.0, 0, CYL_Z, 0.85, fp.metal(STEEL_HI), size=0.25, edge=0.25)

    # ---------------------------------------------------------------- cylinder
    m.part = 'cylinder'
    m.cyl(CYL_X0, CYL_X1, 0, CYL_Z, CYL_R, fp.metal(mul(STEEL_R, 1.08)), edge=0.25)
    m.cyl(CYL_X0, CYL_X0 + 0.75, 0, CYL_Z, CYL_R - 0.25, fp.metal(STEEL_DK), size=0.25, edge=0.25)  # chamfered back
    m.cyl(CYL_X1 - 0.5, CYL_X1, 0, CYL_Z, CYL_R, None, size=0.25, edge=0.25, carve=True)
    m.cyl(CYL_X1 - 0.5, CYL_X1, 0, CYL_Z, CYL_R - 0.5, fp.metal(mul(STEEL_R, 1.02)), size=0.25, edge=0.25)  # front bevel
    for k in range(6):
        a = math.pi / 2 + k * math.pi / 3                  # chamber angles: one straight up, under the bore
        yc, zc = math.cos(a) * CHAMBER_RING, CYL_Z + math.sin(a) * CHAMBER_RING
        # chamber mouths with the copper noses of the rounds a little way in
        m.cyl(CYL_X1 - 1.75, CYL_X1 + 0.25, yc, zc, CHAMBER_R, None, size=0.25, edge=0.25, carve=True)
        m.cyl(CYL_X1 - 2.0, CYL_X1 - 1.75, yc, zc, CHAMBER_R, COPPER_TIP, size=0.25, edge=0.25)
        m.box(CYL_X1 - 2.0, CYL_X1 - 1.75, yc - 0.25, yc + 0.25, zc - 0.25, zc + 0.25, mul(COPPER_TIP, 0.55),
              size=0.25)                                    # hollow point
        # flutes between the chambers
        b = a + math.pi / 6
        m.cyl(CYL_X0 + 3.0, CYL_X1 - 3.0, math.cos(b) * (CYL_R + 0.55), CYL_Z + math.sin(b) * (CYL_R + 0.55), 1.75,
              None, size=0.25, edge=0.25, carve=True)
        fy, fz = math.cos(b) * (CYL_R + 0.55), CYL_Z + math.sin(b) * (CYL_R + 0.55)
        m.recolour(lambda x, y, z, fy=fy, fz=fz: CYL_X0 + 2.75 <= x <= CYL_X1 - 2.75
                   and math.hypot(y - fy, z - fz) <= 2.15, fp.metal(mul(STEEL_R, 0.72)))
        # the cylinder stop notch over each chamber, with its lead-in groove
        nx = CYL_X0 + 2.0
        ny, nz = math.cos(a) * (CYL_R - 0.1), CYL_Z + math.sin(a) * (CYL_R - 0.1)
        m.box(nx, nx + 1.0, ny - 0.4, ny + 0.4, nz - 0.4, nz + 0.4, None, size=0.25, carve=True)
        for t in range(1, 6):
            aa = a - t * 0.07
            gy, gz = math.cos(aa) * (CYL_R - 0.05), CYL_Z + math.sin(aa) * (CYL_R - 0.05)
            m.box(nx + 0.25, nx + 0.75, gy - 0.15, gy + 0.15, gz - 0.15, gz + 0.15, None, size=0.25, carve=True)

    # ---------------------------------------------------------------- barrel, lug, rib, sights
    m.part = 'barrel'
    fp.barrel(m, 26.0, BARREL_X1, Z_BORE, BARREL_R, st, bore=BORE_R)
    m.cyl(BARREL_X1 - 0.25, BARREL_X1 + 0.1, 0, Z_BORE, 1.85, None, size=0.25, edge=0.25, carve=True)   # crown
    m.cyl(BARREL_X1 - 0.5, BARREL_X1 - 0.25, 0, Z_BORE, 1.85, fp.metal(mul(STEEL_R, 1.15)), size=0.25, edge=0.25)
    m.cyl(BARREL_X1 - 0.75, BARREL_X1 + 0.2, 0, Z_BORE, BORE_R, None, size=0.25, edge=0.25, carve=True)
    m.part = 'lug'
    m.cbox(26.0, BARREL_X1 - 2.0, 4.0, 4.25, Z_BORE - 1.0, st, bevel=1.0, edge=0.25)
    m.cbox(BARREL_X1 - 4.0, BARREL_X1 - 2.0, 4.0, 4.25, Z_BORE - 1.0, None, size=0.25, carve=True)
    m.prism([(BARREL_X1 - 4.0, 4.25), (BARREL_X1 - 2.0, 6.5), (BARREL_X1 - 2.0, Z_BORE - 1), (BARREL_X1 - 4.0,
             Z_BORE - 1)], -2.0, 2.0, st, size=0.25, edge=0.25)                    # rounded nose of the lug
    m.part = 'rib'
    m.cbox(26.0, BARREL_X1 - 0.5, 2.0, Z_BORE + 2.0, Z_BORE + 3.5, st, size=0.5, edge=0.25)
    for x in range(28, int(BARREL_X1) - 6, 5):
        m.box(x, x + 3, -1.25, 1.25, Z_BORE + 2.25, Z_BORE + 3.25, None, size=0.25, carve=True)      # vent ports
        m.box(x, x + 3, -0.5, 0.5, Z_BORE + 2.25, Z_BORE + 2.5, mul(STEEL_R, 0.4), size=0.25)        # dark floor
    m.part = 'front_sight'
    m.prism([(BARREL_X1 - 6.0, Z_BORE + 3.5), (BARREL_X1 - 1.5, Z_BORE + 6.5), (BARREL_X1 - 0.75, Z_BORE + 6.5),
             (BARREL_X1 - 0.75, Z_BORE + 3.5)], -0.5, 0.5, st, size=0.25)
    m.box(BARREL_X1 - 3.0, BARREL_X1 - 1.5, -0.5, 0.5, Z_BORE + 5.25, Z_BORE + 6.25, ORANGE, size=0.25)  # insert
    m.box(BARREL_X1 - 4.5, BARREL_X1 - 4.0, -0.5, 0.5, Z_BORE + 3.5, Z_BORE + 4.25, mul(STEEL_R, 0.5),
          size=0.25)                                                                  # its roll pin
    m.part = 'rear_sight'
    m.box(1.5, 5.5, -1.75, 1.75, 17.0, 18.0, fp.metal(mul(STEEL_R, 0.5)), size=0.25)          # base, blued
    m.box(1.5, 2.75, -1.75, 1.75, 18.0, 19.5, fp.metal(mul(STEEL_R, 0.45)), size=0.25)         # blade
    m.box(1.25, 3.0, -0.5, 0.5, 18.5, 19.75, None, size=0.25, carve=True)                     # notch
    m.box(2.5, 2.75, -1.0, -0.5, 18.5, 19.5, (220, 220, 210), size=0.25)                       # white outline
    m.box(2.5, 2.75, 0.5, 1.0, 18.5, 19.5, (220, 220, 210), size=0.25)
    m.box(2.5, 2.75, -1.0, 1.0, 18.25, 18.5, (220, 220, 210), size=0.25)
    m.screw(4.25, 0.0, '+z', mul(STEEL_R, 0.7), kind='slot')                                  # elevation screw
    m.screw(2.0, 18.0, '-y', mul(STEEL_R, 0.7), kind='slot')                                  # windage screw

    # ---------------------------------------------------------------- hammer, trigger, guard, pins
    m.part = 'hammer'
    m.cprism([(-0.5, 11.5), (-3.5, 16.0), (-6.5, 16.75), (-6.0, 18.0), (-2.5, 17.5), (1.0, 14.5), (0.5, 11.0)], 1.5,
             fp.metal(mul(STEEL_R, 1.05)), size=0.25, edge=0.25)
    for i in range(6):                                       # checkering on the spur
        for j in (-1, 1):
            x = -6.0 + i * 0.6
            m.box(x, x + 0.25, j * 0.25 - 0.125, j * 0.25 + 0.125, 17.75 - i * 0.1, 18.25 - i * 0.1, None, size=0.25,
                  carve=True)
    m.part = 'guard'
    fp.guard(m, 6, 22, -9, -1, st)
    m.part = 'trigger'
    fp.trigger(m, 15, -1, fp.metal(STEEL_HI), length=6.0)
    m.part = 'frame'
    for side in ('+y', '-y'):
        m.screw(0.0, 12.0, side, mul(STEEL_R, 0.8), kind='rivet')                       # hammer pin
        m.screw(14.5, -1.0, side, mul(STEEL_R, 0.8), kind='rivet')                      # trigger pin

    # ---------------------------------------------------------------- the right side: side plate, three screws
    m.groove([(0.75, 13.75), (7.5, 13.75), (7.5, 0.25), (21.5, 0.25), (21.5, -1.5), (4.0, -1.75), (0.75, 1.5),
              (0.75, 13.75)], '-y', depth=1, dark=0.45)
    m.screw(2.25, 12.25, '-y', mul(STEEL_R, 0.85), kind='slot')
    m.screw(4.0, -0.5, '-y', mul(STEEL_R, 0.85), kind='slot')
    m.screw(19.5, -0.75, '-y', mul(STEEL_R, 0.85), kind='slot')
    m.screw(28.0, 1.75, '-y', mul(STEEL_R, 0.85), kind='slot')                           # yoke screw
    m.decal(["###.###", "#.#.#..", "###.###", "..#...#", "###.###"], 34, Z_BORE - 2.25, '-y', None, mode='carve')

    # ---------------------------------------------------------------- the left side: cylinder latch, crane seam
    m.part = 'latch'
    for qx in range(0, 14):
        for qz in range(0, 10):
            if qx % 3 != 2:                                  # grooved thumb piece, two quarters proud
                q = m.surface_q('+y', 12 + qx, 32 + qz)
                if q:
                    for h in (1, 2):
                        m.put_q(q[0], q[1] + h, q[2], mul(STEEL_R, 0.9 if h == 1 else 1.05), None, 'latch')
    m.part = 'frame'
    m.screw(5.0, 10.75, '+y', mul(STEEL_R, 0.8), kind='slot')
    m.groove([(26.0, 0.5), (26.0, 4.5)], '+y', depth=1, dark=0.5)                       # crane seam
    m.groove([(23.0, 0.5), (26.0, 0.5)], '+y', depth=1, dark=0.5)
    wl.tally(m, '+y', 1.0, 3.0, 7, height=2.25)                                         # seven kills, scratched in

    # ---------------------------------------------------------------- grip: finger-groove rubber, medallion, ring
    m.part = 'grip'
    m.cprism(GRIP_BACK + GRIP_FRONT, 8.0, fp.metal(RUBBER, speck=0.1), bevel=2.0, edge=0.25)
    for side in ('+y', '-y'):
        wl.stipple(m, side, (-11.5, 5.5, -26, -4), 11 if side == '+y' else 12)
    for side, y in (('+y', 4.0), ('-y', -4.25)):
        m.box(-4.0, -1.5, y, y + 0.25, -10.25, -7.75, GOLD, size=0.25)                   # medallion
        m.box(-3.5, -2.0, y, y + 0.25, -9.75, -8.25, mul(GOLD, 0.7), size=0.25)
    m.screw(-1.0, -15.0, '+y', mul(STEEL_R, 0.8), kind='slot')                           # grip screw
    m.part = 'lanyard'
    for k in range(16):                                                                 # lanyard ring at the butt
        a = k * math.tau / 16
        m.box(-8.0 + math.cos(a) * 1.5, -7.75 + math.cos(a) * 1.5, -0.25, 0.25, -30.5 + math.sin(a) * 1.5,
              -30.25 + math.sin(a) * 1.5, fp.metal(STEEL_DK), size=0.25)

    # ---------------------------------------------------------------- the wasteland layer
    wl.tape(m, 'z', -24.0, -19.0, (-15, 11, -5, 5, -24.5, -18.5), col=wl.DUCT, seed=101, part='tape')
    m.part = 'paracord'
    for i in range(36):                                     # a paracord loop through the ring, hanging
        t = i / 35
        x = -8.0 + math.sin(t * math.pi) * 2.5
        z = -31.5 - math.sin(t * math.pi) * 5.0 - t * 1.0
        m.put(x, -0.25 + 0.25 * (i % 2), z, wl.PARACORD if i % 6 else mul(wl.PARACORD, 0.7), 0.25, 'paracord')
    wl.soot(m, (CYL_X1 - 1.0, CYL_X1 + 2.0, -CYL_R, CYL_R, CYL_Z - CYL_R, CYL_Z + CYL_R + 1), amount=0.55, seed=102)
    wl.soot(m, (24.0, 28.0, -3, 3, Z_BORE - 2.5, Z_BORE + 2.5), amount=0.7, seed=103)
    wl.soot(m, (BARREL_X1 - 1.0, BARREL_X1 + 0.5, -2.5, 2.5, Z_BORE - 2.5, Z_BORE + 2.5), amount=0.5, seed=104)
    wl.rust(m, (CYL_X0 + 2.5, CYL_X1 - 2.5, -CYL_R - 1, CYL_R + 1, CYL_Z - CYL_R - 1, CYL_Z + CYL_R + 1),
            amount=0.22, seed=105, pits=0.02)                                         # in and round the flutes
    wl.rust(m, (-1, 30, -4, 4, -2.5, 3), amount=0.3, seed=106, pits=0.05,
            region=lambda x, y, z: z < 1.5)                                            # the frame's underside
    wl.rust(m, (BARREL_X1 - 10, BARREL_X1 + 1, -3, 3, 4, 9.5), amount=0.25, seed=107)  # nose of the lug
    m.wear_edges(0.18, (200, 202, 206))
    wl.wear_lines(m, '+y', (26, 66, 6, 12.5), 14, 108)                                 # holster wear along the side
    wl.wear_lines(m, '-y', (26, 66, 6, 12.5), 12, 109)
    m.scratches('+y', (CYL_X0, CYL_X1, 2, 12), 5, 110, lighten=1.2, length=(1.5, 4.0))
    wl.cavity(m)
    m.crack(-8, -14, '+y', 6, 111, heading=-1.0)                                        # a split in the rubber
    m.grime(0.2, 112)
    wl.simplify(m)
    return m
