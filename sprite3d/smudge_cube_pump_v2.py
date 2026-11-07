"""The smudge-cube shotgun, round 2 (2026-11-07, home PC). A forge design: forge_make.py builds it.

Tefa, on round 1 (smudge_cube_pump.py) in Blender: "the selected part, the handle, please still make the little ridges
on the handle like carved out. the idea is to have a solid gun shape that looks textured as it is right now. barrel
has to be nice and round, and please use the small and even smaller cubes only when you need to make something round
or sloped, otherwise use cubes as big as possible. also the gun looks round all around ... it looks 'soft'. doesn't
have the robust metallic characteristics to the look. for example the tip of the gun has to end straight like a
factory cut pipe".

So: the SHAPE of the sharp cube shotgun (sharp_cube_pump.py: a box receiver with small rounded edges, a round hollow
barrel cut square at the muzzle, the tube and its cap, carved rings round the pump, the ports, seam, rib and trim),
built in the kit's mixed cubes (chunky: big cubes inside and on flat faces, smaller only where it curves or slopes;
the barrel, tube and pump go down to quarter cubes so they come out round), and the COLOURS of round 1: every cube
shows the game's own side picture, half sharp pixel and half smudge (SMUDGE), no palettes, no added wear, rust,
straps or darkening. Only cuts are shaded (the floors of the carved rings and ports), so the carving reads.
Shape and size follow the game's side pickup picture (GRZPA0, 60 x 21), read at run time and never stored here.
"""
import math

from forge import hash01, mix, mul
from sharp_kit import (BLUED, BORE, BRASS, BRIGHT_METAL, GUNMETAL, LEATHER, LEATHER_DK, PUMP_WOOD, RUBBER, STITCH,
                       STOCK_WOOD, SURF, Picture, Profile, blade, darken, finish, flashes, grooved, guard,
                       shell, start, toned)
from sharp_settings import CUBE_M, PORT_CLEAR, PORT_LEN
import sharp_kit

SMUDGE = 0.5                           # 0 = the nearest picture pixel (hard), 1 = the full bicubic smudge of round 1
ROUND_EDGE = 0.25                      # the smallest cube, for the round parts (barrel, tube, cap, pump)
PIC = {}                               # the side picture, filled by build()


def _cubic(t):
    return (((-t + 2) * t - 1) * t / 2, ((3 * t - 5) * t * t + 2) / 2, ((-3 * t + 4) * t + 1) * t / 2,
            (t - 1) * t * t / 2)


def _picture():
    """The side picture (top row first) and, for every pixel, the nearest solid pixel (so cubes the hand-drawn shape
    puts outside the picture's own outline still take the colour next to them)."""
    W, H, rows = sharp_kit.load_sprite(SIDE_SPRITE)
    solid = [(u, v) for v in range(H) for u in range(W) if rows[v][u][3] >= 0.5]
    near = [[min(solid, key=lambda q: (q[0] - u) ** 2 + (q[1] - v) ** 2) for u in range(W)] for v in range(H)]
    PIC.update(W=W, H=H, rows=rows, near=near)


def _smooth(u, v):
    """Alpha-weighted bicubic colour at picture coordinates (u, v), 0..255, or None where it is clear."""
    W, H, rows = PIC["W"], PIC["H"], PIC["rows"]
    u0, v0 = math.floor(u - 0.5), math.floor(v - 0.5)
    wu, wv = _cubic(u - 0.5 - u0), _cubic(v - 0.5 - v0)
    acc = [0.0] * 4
    for j in range(4):
        yy = min(max(v0 - 1 + j, 0), H - 1)
        for i in range(4):
            xx = min(max(u0 - 1 + i, 0), W - 1)
            r, g, b, a = rows[yy][xx]
            w = wu[i] * wv[j]
            acc[0] += w * r * a
            acc[1] += w * g * a
            acc[2] += w * b * a
            acc[3] += w * a
    if acc[3] < 0.5:
        return None
    return tuple(min(max(c / acc[3], 0.0), 1.0) * 255 for c in acc[:3])


def pc(x, y, z):
    """A cube's colour: the picture under it (side view), on round 1's fine grid, SMUDGE of the way to smooth."""
    W, H = PIC["W"], PIC["H"]
    u = (math.floor(x / S * 3) + 0.5) / 3
    v = (math.floor(-z / S * 3) + 0.5) / 3
    iu, iv = min(max(int(u), 0), W - 1), min(max(int(v), 0), H - 1)
    nu, nv = PIC["near"][iv][iu]
    r, g, b, _ = PIC["rows"][nv][nu]
    sharp = (r * 255, g * 255, b * 255)
    smooth = _smooth(u, v) if (nu, nv) == (iu, iv) else None
    return sharp if smooth is None else mix(sharp, smooth, SMUDGE)


def toned(pic, pal, th, seed, rust=0.0):
    """Round 2 keeps the sharp design's calls, but every part shows the picture itself."""
    return pc


def round_fill(fn, *args, **kw):
    """One fill with the kit's mixed cubes going down to ROUND_EDGE (quarter cubes) on the curve."""
    old = sharp_kit.SURF
    sharp_kit.SURF = ROUND_EDGE
    try:
        kw["edge"] = ROUND_EDGE
        fn(*args, **kw)
    finally:
        sharp_kit.SURF = old

SIDE_SPRITE = "Sprites/Weapons/GRZPA0.png"
NAME = "smudge_cube_pump_v2"
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
GUARD_X0, GUARD_X1, GUARD_BOT, GUARD_W, GUARD_BAR = X(12.6), X(22.0), Z(15.0), 4.5, 2.5

# ---------------------------------------------------------------------------------------------- the gun
def build():
    pic = Picture(SIDE_SPRITE, GUN_LENGTH_M)
    _picture()
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
        return bore_col(x, y, z)

    round_fill(m.cyl, BARREL_X0, MUZZLE_X, 0.0, BARREL_ZC, BARREL_R, barrel_col, hollow=BORE_R, keep=True)
    m.part = "tube"
    tube_col = toned(pic, BLUED, pic.thresholds(51, 56, 7, 10), 41, rust=0.12)
    round_fill(m.cyl, TUBE_X0, TUBE_X1, 0.0, TUBE_ZC, TUBE_R, tube_col, keep=True)
    round_fill(m.cyl, TUBE_X1, TUBE_X1 + CAP_LEN, 0.0, TUBE_ZC, CAP_R, tube_col, keep=True)
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
    m.box(X(13.2), REC_X1, -1.5, 1.5, REC_TOP - 1.0, REC_TOP + 1.0, pc, size=SURF, keep=True)
    m.part = "barrel"
    m.box(REC_X1, MUZZLE_X - 1.0, -1.0, 1.0, BARREL_TOP - 1.0, BARREL_TOP + 1.0, pc, size=SURF, keep=True)
    for k in range(int((REC_X1 - X(13.2)) / 2.5)):
        x = X(13.2) + 1.0 + k * 2.5
        m.box(x, x + 1.0, -2, 2, REC_TOP + 0.5, REC_TOP + 1.0, None, size=SURF, carve=True)
    m.box(MUZZLE_X - 3.0, MUZZLE_X - 1.0, -1.0, 1.0, BARREL_TOP + 1.0, BARREL_TOP + 2.5, pc, size=SURF)

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
            m.box(a0, a1, y0, y1, min(z0, z1), max(z0, z1), pc, size=SURF, keep=True)
        for px_ in (16.0, 23.5):
            yc = side * (REC_W / 2 + 0.25)
            m.box(X(px_) - 1.0, X(px_) + 1.0, yc - 0.75, yc + 0.75, Z(8.0) - 1.0, Z(8.0) + 1.0,
                  pc, size=SURF, keep=True)

    # --- trigger guard and trigger (2026-11-05, Tefa: "the pump handle shotgun again needs a bigger trigger guard and
    # a trigger more built in to the grip and the receiver"): a bigger loop running back into the stock's wrist, the
    # finger hole carried up into the receiver, the trigger hanging out of that slot
    guard(m, GUARD_X0, GUARD_X1, REC_BOT, GUARD_BOT, toned(pic, GUNMETAL, (0.2, 0.3), 61, rust=0.1), w=GUARD_W,
          bar=GUARD_BAR)
    blade(m, X(17.4), REC_BOT, GUARD_BOT + GUARD_BAR + 1.0, pc, w=1.0,
          lean=0.35)

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
        return wood(x, y, z)
    outer = st.solid(hw_stock, STOCK_ROUND)
    inner = st.solid(hw_stock, STOCK_ROUND, grow=-0.5)
    m.fill(grooved(outer, inner, [(PAD_LEN, PAD_LEN + 0.5)]), st.bounds(STOCK_W_BUTT / 2), stock_col, size=1.0,
           edge=SURF, keep=True)
    for k in range(int((Z(10.0) - Z(15.0)) / 3.0)):
        z = Z(15.0) + 1.5 + k * 3.0
        m.box(-1, 0.5, -STOCK_W_BUTT, STOCK_W_BUTT, z, z + 1.0, None, size=SURF, carve=True)

    # (no added straps in round 2: the picture has its own wrap on the wrist)

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
    round_fill(m.fill, lambda x, y, z: pg(x, y, z) and math.hypot(y, z - TUBE_ZC) >= TUBE_R, pp.bounds(PUMP_W / 2),
               pwood, size=1.0)
    # the groove floors in shadow (the cut is geometry; this is only the shade at its bottom)
    pdeep = pp.solid(lambda x: PUMP_W / 2, PUMP_ROUND, grow=-PUMP_GROOVE_DEPTH - 0.5)
    darken(m, lambda x, y, z: any(a <= x < b for a, b in bands) and pin(x, y, z) and not pdeep(x, y, z), 0.62)
    # the tube again where the pump sleeve meets it, so no pump cube bites into the tube (seen when the pump racks)
    m.part = "tube"
    round_fill(m.cyl, PUMP_X0 - 1, PUMP_X1 + 1, 0.0, TUBE_ZC, TUBE_R, tube_col)
    m.part = "pump"
    for side in (-1, 1):
        y0 = side * (TUBE_R + 0.25)
        m.box(REC_X1, PUMP_X0 + 1, min(y0, y0 + side * 1.0), max(y0, y0 + side * 1.0), TUBE_ZC - 0.5, TUBE_ZC + 0.5,
              pc, size=SURF, keep=True)

    # --- shells (move; hidden unless a reload frame shows them): one under the loading port, one at the ejection port
    shell(m, "shell", loadport[0] + 2.0, 0.0, REC_BOT - 3.5, False)
    # built clear of the gun, beside the open port (SHELL2_OUT), lined up with it (it is one shell long), so no cube
    # of it is lost to the receiver; the reload frames move it in (make_job_sharp.SHELL2)
    shell(m, "shell2", port[0] + PORT_CLEAR / 2 + 0.5, -REC_W / 2 - SHELL2_OUT, (port[4] + port[5]) / 2, False)

    # --- muzzle flashes (move; hidden unless a firing frame shows them), all in the smallest cubes
    flashes(m, MUZZLE_X + 0.5, BARREL_ZC)

    # (no wear or darkening in round 2: the picture's own colours)
    return m
