"""The cube shotgun, sharper (2026-11-04, home PC). A forge design: forge_make.py builds it.

Tefa, after wearing the cube sprite shotgun (sprite_cube_pump.py): "the cubes are too small ... use the one measure
bigger cubes and right now the weapon is too blurry and smudgy in VR, but that type of low rez look fits it. can you
make it look sharper but instead of just using paint for gaps and ridges, please use carving and adding cubes. also
the barrel has to be nice and round barrel with a flat end and actually hollow inside. please animate it with all the
game's animations and use the smallest cubes to make the flash when shot is fired."

What changed against the cube sprite shotgun:
- Surfaces step in HALF cubes (1.7 mm), not quarter cubes; the inside stays whole cubes. Quarter cubes are used only
  for the muzzle flash.
- Colours are no longer read smoothly from the game picture (that smear was the blur). Each part has its own small
  palette of flat colours; the game picture only picks WHICH of them a cube gets (nearest picture pixel, no blending),
  so the low-res pixel pattern stays but every edge between colours is sharp.
- Gaps and ridges are geometry: grooves round the pump and the butt pad are cut, the ejection port and loading port
  are cut, the receiver seam is cut, the trim, pins, top rib, barrel band and front bead are added cubes.
- The barrel is a real round tube with a flat muzzle and an empty bore; the magazine tube is round with an end cap.
- Moving parts for the game's animations (make_job_sharp.py maps the frames): the pump and its action bars, the
  trigger, three muzzle flashes, a shell pushed into the loading port and one dropped into the ejection port.
Shape and size follow the game's side pickup picture (GRZPA0, 60 x 21), read at run time and never stored here.
"""
import math

from forge import hash01, mix, mul
from sharp_kit import (BLUED, BORE, BRASS, BRIGHT_METAL, GUNMETAL, LEATHER, LEATHER_DK, PUMP_WOOD, RUBBER, STITCH,
                       STOCK_WOOD, SURF, Picture, Profile, darken, finish, flashes, grooved, shell, start, toned)
from sharp_settings import CUBE_M, PORT_CLEAR, PORT_LEN

SIDE_SPRITE = "Sprites/Weapons/GRZPA0.png"
NAME = "sharp_cube_pump"
GUN_LENGTH_M = 1.0                     # as before: the 60-pixel picture spans one metre (Tefa settled the size at 1.0)
S = GUN_LENGTH_M / 60 / CUBE_M         # main cubes per picture pixel (4.9)


def X(px):
    return px * S


def Z(row):
    return -row * S


# ---------------------------------------------------------------------------------------------- sizes (main cubes)
BARREL_TOP = Z(4.0)
BARREL_R = 5.4                         # 37 mm across
BORE_R = 3.0                           # 20 mm bore (a 12 gauge is 18.5)
BARREL_ZC = BARREL_TOP - BARREL_R
BARREL_X0, MUZZLE_X = X(30.5), X(57.0)
TUBE_R, TUBE_ZC = 3.8, -43.0
TUBE_X0, TUBE_X1 = X(30.5), X(56.2)
CAP_R, CAP_LEN = 4.3, 2.5
REC_X0, REC_X1 = X(12.0), X(31.0)
REC_TOP, REC_BOT = Z(4.0), Z(11.9)
REC_W, REC_ROUND = 14.0, 2.0
PORT_X0, PORT_DEPTH = X(25.0), 4.0     # the port is one shell long (sharp_settings.PORT_LEN)
SHELL2_OUT = 6.0                       # main cubes from the receiver's right side to the ejection-port shell's axis
# the pump's back end sits one stroke ahead of the receiver: pulled all the way, it meets the receiver and the port is
# fully open (Tefa: "handle needs to travel the whole length")
PUMP_X0, PUMP_X1 = REC_X1 + PORT_LEN, X(51.4)
PUMP_TOP, PUMP_BOT = Z(6.9), Z(11.6)
PUMP_W, PUMP_ROUND = 16.0, 6.5
PUMP_GROOVE_W, PUMP_GROOVE_STEP, PUMP_GROOVE_DEPTH, PUMP_GROOVE_MARGIN = 2.0, 6.0, 1.0, 7.0
STOCK_W_WRIST, STOCK_W_BUTT, STOCK_ROUND = 11.0, 13.5, 4.0
PAD_LEN = 2.5                          # rubber butt pad
STRAPS, STRAP_W, STRAP_GAP, STRAP_SLANT, STRAP_RAISE = 3, 4.0, 3.0, 0.35, 0.5
GUARD_X0, GUARD_X1, GUARD_BOT, GUARD_W, GUARD_BAR = X(14.6), X(21.4), Z(13.6), 4.0, 2.5

# ---------------------------------------------------------------------------------------------- the gun
def build():
    pic = Picture(SIDE_SPRITE, GUN_LENGTH_M)
    m = start(NAME)

    # --- receiver: a rounded box from the picture's outline, with cuts and added trim
    rec_poly = [(REC_X0, Z(5.0)), (X(13.0), REC_TOP), (REC_X1, REC_TOP), (REC_X1, REC_BOT), (REC_X0, REC_BOT)]
    rec = Profile(rec_poly)
    m.part = "receiver"
    m.fill(rec.solid(lambda x: REC_W / 2, REC_ROUND), rec.bounds(REC_W / 2),
           toned(pic, GUNMETAL, pic.thresholds(12, 30, 4, 11), 21, rust=0.16), size=1.0, edge=SURF)

    # --- barrel: round, flat muzzle, hollow; magazine tube under it with an end cap; the band that ties them
    m.part = "barrel"
    bore_col = toned(pic, BLUED, pic.thresholds(31, 56, 4, 6), 31, rust=0.10)

    def barrel_col(x, y, z):
        if math.hypot(y, z - BARREL_ZC) < BORE_R + 0.8:
            return BORE
        if x > MUZZLE_X - 0.6:
            return mix(bore_col(x, y, z), BRIGHT_METAL, 0.45)        # the muzzle face, worn bright
        return bore_col(x, y, z)

    m.cyl(BARREL_X0, MUZZLE_X, 0.0, BARREL_ZC, BARREL_R, barrel_col, hollow=BORE_R, edge=SURF, keep=True)
    m.part = "tube"
    tube_col = toned(pic, BLUED, pic.thresholds(51, 56, 7, 10), 41, rust=0.12)
    m.cyl(TUBE_X0, TUBE_X1, 0.0, TUBE_ZC, TUBE_R, tube_col, edge=SURF, keep=True)
    m.cyl(TUBE_X1, TUBE_X1 + CAP_LEN, 0.0, TUBE_ZC, CAP_R, lambda x, y, z: mix(tube_col(x, y, z), BRIGHT_METAL, 0.3),
          edge=SURF, keep=True)
    m.cyl(TUBE_X1 + CAP_LEN - 0.5, TUBE_X1 + CAP_LEN + 0.5, 0.0, TUBE_ZC, 1.2, None, carve=True, edge=None, size=0.5)
    m.part = "band"
    bx0, bx1 = X(52.6), X(53.8)

    def band(x, y, z):
        if not (bx0 <= x < bx1):
            return False
        return (math.hypot(y, z - BARREL_ZC) < BARREL_R + 1.0 or math.hypot(y, z - TUBE_ZC) < TUBE_R + 1.0
                or (abs(y) < TUBE_R + 1.0 and TUBE_ZC <= z <= BARREL_ZC))
    m.fill(band, (bx0, bx1, -BARREL_R - 2, BARREL_R + 2, TUBE_ZC - TUBE_R - 2, BARREL_TOP + 2),
           toned(pic, GUNMETAL, (0.2, 0.35), 51, rust=0.2), size=1.0, edge=SURF)

    # --- top rib along receiver and barrel (added cubes), serrated on the receiver (cut notches), brass front bead
    m.part = "receiver"
    m.box(X(13.2), REC_X1, -1.5, 1.5, REC_TOP - 1.0, REC_TOP + 1.0, GUNMETAL[1], size=SURF, keep=True)
    m.part = "barrel"
    m.box(REC_X1, MUZZLE_X - 1.0, -1.0, 1.0, BARREL_TOP - 1.0, BARREL_TOP + 1.0, BLUED[1], size=SURF, keep=True)
    for k in range(int((REC_X1 - X(13.2)) / 2.5)):
        x = X(13.2) + 1.0 + k * 2.5
        m.box(x, x + 1.0, -2, 2, REC_TOP + 0.5, REC_TOP + 1.0, None, size=SURF, carve=True)
    m.box(MUZZLE_X - 3.0, MUZZLE_X - 1.0, -1.0, 1.0, BARREL_TOP + 1.0, BARREL_TOP + 2.5, BRASS, size=SURF)

    # --- receiver cuts: ejection port (right side), the seam under it, the loading port underneath
    m.part = "receiver"
    # The port is as long as the pump stroke and a deep dark pocket; the bolt fills it and rides the pump, so pulling
    # the pump opens the port (Tefa, 2026-09-24, on the first cube shotgun: "it needs the 'lid' to open when the pump
    # handle is pulled down, and close when it is pushed up").
    port = (PORT_X0, PORT_X0 + PORT_LEN, -REC_W / 2 - 1, -REC_W / 2 + PORT_DEPTH, Z(7.6), Z(5.2))
    m.box(*port, None, size=SURF, carve=True)
    darken(m, lambda x, y, z: port[0] - 0.5 <= x < port[1] + 0.5 and -REC_W / 2 <= y < port[3] + 0.5
           and port[4] - 0.5 <= z < port[5] + 0.5, 0.45)
    m.part = "bolt"
    bolt_col = toned(pic, [mul(BRIGHT_METAL, 0.7), mul(BRIGHT_METAL, 0.85), BRIGHT_METAL], (0.25, 0.45), 91)
    m.box(port[0], port[1], -REC_W / 2 + 0.5, port[3], port[4] + 0.5, port[5] - 0.5, bolt_col, size=SURF)
    m.box(port[0], port[1], -REC_W / 2, -REC_W / 2 + 1.0, (port[4] + port[5]) / 2 - 0.5,
          (port[4] + port[5]) / 2 + 0.5, None, size=SURF, carve=True)         # a groove along the bolt
    m.part = "receiver"
    for side in (-1, 1):
        y0, y1 = (side * REC_W / 2 - 0.5, side * REC_W / 2 + 1) if side > 0 else (-REC_W / 2 - 1, -REC_W / 2 + 0.5)
        m.box(X(21.0), REC_X1, y0, y1, Z(8.7), Z(8.5), None, size=SURF, carve=True)  # the seam
    loadport = (X(22.0), X(30.6), -4.0, 4.0, REC_BOT - 1, REC_BOT + 3.0)
    m.box(*loadport, None, size=SURF, carve=True)
    darken(m, lambda x, y, z: loadport[0] - 0.5 <= x < loadport[1] + 0.5 and abs(y) < 4.5
           and REC_BOT <= z < REC_BOT + 3.5, 0.6)

    # --- receiver trim (added cubes): the bright U of the picture on both sides, and two trigger-group pins
    for side in (-1, 1):
        y0, y1 = (REC_W / 2 - 0.5, REC_W / 2 + 0.5) if side > 0 else (-REC_W / 2 - 0.5, -REC_W / 2 + 0.5)
        u = [(X(14.0), Z(9.0), X(14.6), Z(10.6)), (X(14.0), Z(10.6), X(20.9), Z(10.0)),
             (X(20.3), Z(10.6), X(20.9), Z(9.0))]
        for a0, z0, a1, z1 in u:
            m.box(a0, a1, y0, y1, min(z0, z1), max(z0, z1), mix(GUNMETAL[2], BRIGHT_METAL, 0.5), size=SURF, keep=True)
        for px_ in (16.0, 23.5):
            yc = side * (REC_W / 2 + 0.25)
            m.box(X(px_) - 1.0, X(px_) + 1.0, yc - 0.75, yc + 0.75, Z(8.0) - 1.0, Z(8.0) + 1.0,
                  mix(GUNMETAL[2], BRIGHT_METAL, 0.3), size=SURF, keep=True)

    # --- trigger guard: a loop with a real finger hole
    m.part = "guard"
    gpoly = [(GUARD_X0, REC_BOT + 0.5), (GUARD_X1, REC_BOT + 0.5), (GUARD_X1, GUARD_BOT + 3.5),
             (GUARD_X1 - 3.5, GUARD_BOT), (GUARD_X0 + 3.5, GUARD_BOT), (GUARD_X0, GUARD_BOT + 3.5)]
    gout = Profile(gpoly)
    hole = Profile([(GUARD_X0 + GUARD_BAR, REC_BOT + 1), (GUARD_X1 - GUARD_BAR, REC_BOT + 1),
                    (GUARD_X1 - GUARD_BAR, GUARD_BOT + GUARD_BAR + 2.0),
                    (GUARD_X1 - GUARD_BAR - 2.0, GUARD_BOT + GUARD_BAR),
                    (GUARD_X0 + GUARD_BAR + 2.0, GUARD_BOT + GUARD_BAR),
                    (GUARD_X0 + GUARD_BAR, GUARD_BOT + GUARD_BAR + 2.0)])
    gsolid = gout.solid(lambda x: GUARD_W / 2, 1.0)
    m.fill(lambda x, y, z: gsolid(x, y, z) and hole.sd(x, z) <= 0, gout.bounds(GUARD_W / 2),
           toned(pic, GUNMETAL, (0.2, 0.3), 61, rust=0.1), size=1.0, edge=SURF, keep=True)

    # --- trigger (moves): a blade leaning forward at the bottom
    m.part = "trigger"
    tx = X(18.4)

    def trig(x, y, z):
        if not (GUARD_BOT + GUARD_BAR + 1.0 <= z < REC_BOT) or abs(y) >= 1.0:
            return False
        lean = (REC_BOT - z) * 0.35
        return tx + lean - 1.0 <= x < tx + lean + 1.0
    m.fill(trig, (tx - 2, tx + 6, -1.5, 1.5, GUARD_BOT, REC_BOT), mix(GUNMETAL[2], BRIGHT_METAL, 0.4),
           size=SURF, keep=True)

    # --- stock: wood from the picture's outline, rounded, wider at the butt; rubber pad with cut grooves; straps
    m.part = "grip"
    spoly = [(X(13.0), Z(4.3)), (X(9.0), Z(5.0)), (X(7.0), Z(6.0)), (X(5.0), Z(7.0)), (X(3.0), Z(8.0)),
             (X(1.0), Z(9.0)), (X(0.0), Z(10.0)), (X(0.0), Z(15.0)), (X(1.0), Z(16.0)), (X(4.2), Z(16.0)),
             (X(5.6), Z(14.8)), (X(6.2), Z(12.6)), (X(7.5), Z(11.9)), (REC_X0 + 0.5, REC_BOT),
             (REC_X0 + 0.5, Z(5.0))]
    st = Profile(spoly)

    def hw_stock(x):
        t = min(max(x / X(8.0), 0.0), 1.0)
        return (STOCK_W_BUTT + (STOCK_W_WRIST - STOCK_W_BUTT) * t) / 2

    wood = toned(pic, STOCK_WOOD, pic.thresholds(0, 11, 5, 15), 71)

    def stock_col(x, y, z):
        if x < PAD_LEN:
            return mul(RUBBER, 0.9 + 0.2 * hash01(math.floor(y * 2), math.floor(z * 2), 3))
        c = wood(x, y, z)
        return mul(c, 0.8) if x > X(7.0) else c                              # the wrist darker, as in the picture
    outer = st.solid(hw_stock, STOCK_ROUND)
    inner = st.solid(hw_stock, STOCK_ROUND, grow=-0.5)
    m.fill(grooved(outer, inner, [(PAD_LEN, PAD_LEN + 0.5)]), st.bounds(STOCK_W_BUTT / 2), stock_col, size=1.0,
           edge=SURF, keep=True)
    for k in range(int((Z(10.0) - Z(15.0)) / 3.0)):
        z = Z(15.0) + 1.5 + k * 3.0
        m.box(-1, 0.5, -STOCK_W_BUTT, STOCK_W_BUTT, z, z + 1.0, None, size=SURF, carve=True)

    # leather straps round the wrist, standing one half cube proud
    wx = X(9.0)
    zmid = (Z(5.0) + Z(12.0)) / 2
    span = STRAPS * STRAP_W + (STRAPS - 1) * STRAP_GAP
    swell = st.solid(hw_stock, STOCK_ROUND, grow=STRAP_RAISE)
    for k in range(STRAPS):
        c0 = wx - span / 2 + k * (STRAP_W + STRAP_GAP)

        def strap(x, y, z, c0=c0):
            a = (x - c0) + STRAP_SLANT * (z - zmid)
            return 0.0 <= a < STRAP_W and swell(x, y, z)

        def strap_col(x, y, z, c0=c0):
            a = (x - c0) + STRAP_SLANT * (z - zmid)
            if a < 0.5 or a >= STRAP_W - 0.5:
                return LEATHER_DK
            if abs(a - STRAP_W / 2) < 0.5 and int(math.floor(z * 2)) % 4 == 0:
                return STITCH
            return mix(LEATHER, LEATHER_DK, 0.3 * hash01(math.floor(x * 2), math.floor(y * 2), math.floor(z * 2)))
        m.fill(strap, (c0 - 8, c0 + STRAP_W + 8, -STOCK_W_BUTT, STOCK_W_BUTT, Z(13.0), Z(4.0)), strap_col,
               size=SURF)

    # --- pump (moves): wood sleeve round the tube with cut ring grooves, and the two action bars to the receiver
    m.part = "pump"
    ppoly = [(PUMP_X0, PUMP_TOP), (PUMP_X1, PUMP_TOP), (PUMP_X1, Z(10.2)), (X(48.5), PUMP_BOT + 1.0),
             (X(44.5), PUMP_BOT), (PUMP_X0 + 1.5, PUMP_BOT), (PUMP_X0, Z(10.6))]
    pp = Profile(ppoly)
    bands = []
    x = PUMP_X0 + PUMP_GROOVE_MARGIN
    while x + PUMP_GROOVE_W <= PUMP_X1 - PUMP_GROOVE_MARGIN:
        bands.append((x, x + PUMP_GROOVE_W))
        x += PUMP_GROOVE_STEP
    pout = pp.solid(lambda x: PUMP_W / 2, PUMP_ROUND)
    pin = pp.solid(lambda x: PUMP_W / 2, PUMP_ROUND, grow=-PUMP_GROOVE_DEPTH)
    pg = grooved(pout, pin, bands)
    pwood = toned(pic, PUMP_WOOD, pic.thresholds(34, 50, 7, 11), 81)
    m.fill(lambda x, y, z: pg(x, y, z) and math.hypot(y, z - TUBE_ZC) >= TUBE_R, pp.bounds(PUMP_W / 2), pwood,
           size=1.0, edge=SURF)
    # the groove floors in shadow (the cut is geometry; this is only the shade at its bottom)
    pdeep = pp.solid(lambda x: PUMP_W / 2, PUMP_ROUND, grow=-PUMP_GROOVE_DEPTH - 0.5)
    darken(m, lambda x, y, z: any(a <= x < b for a, b in bands) and pin(x, y, z) and not pdeep(x, y, z), 0.62)
    # the tube again where the pump sleeve meets it, so no pump cube bites into the tube (seen when the pump racks)
    m.part = "tube"
    m.cyl(PUMP_X0 - 1, PUMP_X1 + 1, 0.0, TUBE_ZC, TUBE_R, tube_col, edge=SURF)
    m.part = "pump"
    for side in (-1, 1):
        y0 = side * (TUBE_R + 0.25)
        m.box(REC_X1, PUMP_X0 + 1, min(y0, y0 + side * 1.0), max(y0, y0 + side * 1.0), TUBE_ZC - 0.5, TUBE_ZC + 0.5,
              GUNMETAL[0], size=SURF, keep=True)

    # --- shells (move; hidden unless a reload frame shows them): one under the loading port, one at the ejection port
    shell(m, "shell", loadport[0] + 2.0, 0.0, REC_BOT - 3.5, False)
    # built clear of the gun, beside the open port (SHELL2_OUT), lined up with it (it is one shell long), so no cube
    # of it is lost to the receiver; the reload frames move it in (make_job_sharp.SHELL2)
    shell(m, "shell2", port[0] + PORT_CLEAR / 2 + 0.5, -REC_W / 2 - SHELL2_OUT, (port[4] + port[5]) / 2, False)

    # --- muzzle flashes (move; hidden unless a firing frame shows them), all in the smallest cubes
    flashes(m, MUZZLE_X + 0.5, BARREL_ZC)

    # --- wear on the edges, then a little darker all over
    finish(m, ["receiver", "barrel", "tube", "band", "guard"], ["grip", "pump"])
    return m
