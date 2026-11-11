"""The smudge-cube shotgun, round 12 (2026-11-12, Developer PC). A forge design: forge_make.py builds it.

Tefa, after wearing round 11: "body is just about right now. the guard opening still must be the size of a shell and
show the actual inside of the barrel when it goes in there. the shells going into the gun need to be twice the size".
So, against round 11 (kept): the two shells that are shown going in are twice the kit's size (big_shell, SHELL_K); the
ejection port is one big shell long and as high as the shell is thick, and no longer a shallow dark pocket: it opens
onto a round chamber on the gun's middle line, whose front wall has the barrel's own bore cut through into the hollow
barrel, so with the port open you look into the barrel; the shell guard is a thin plate over it. The loading port
underneath is as long and wide as the big shell too. The pump keeps its length and its stroke; the shell guard alone
slides the whole (longer) port open (make_job_smudge_v12.py). Numbers shared with the job: smudge_settings.py.
Round 11's own note:

The smudge-cube shotgun, round 11 (2026-11-12, Developer PC).

Tefa, after wearing round 10: "ah now i see, you made the body higher not wider, please go back so that the body and
the bottom of the pump handle are on the same line, and make the body 'fatter' please". Round 10 grew height and width
together and dropped the receiver's underside a picture row; the height is what showed. Round 11: no girth scaling at
all (GIRTH 1.0, the pk3's Scale is a plain 0.7, so heights and the pump are round 8's again), the receiver's underside
on the pump's bottom line (REC_BOT = PUMP_BOT), and the receiver FAT: 21 cubes wide (round 8: 14, the pump: 16), its
edges a little rounder, the stock's wrist and butt widened to run into it. The rail stays.
Round 10's own note:

The smudge-cube shotgun, round 10 (2026-11-12, Developer PC).

Tefa, after wearing round 9: "the shotgun body didn't feel larger at all to be honest". Round 9's 5 % and one cube were
too timid to see. Round 10, against round 8: girth 1.12 (was 1.05), the receiver 16.5 cubes wide (round 8: 14) and a
full picture row deeper, the stock's wrist and butt 2 cubes wider so the body runs into it; so the receiver comes out
about a third wider than round 8 in the hand. Length, the rail and the pump's real thickness as in round 9.
Round 9's own note:

The smudge-cube shotgun, round 9 (2026-11-11, Developer PC).

Tefa, after wearing round 8 at 0.7 size: "shotgun needs to be a little bigger, 5% more, but keeping the length the
same, it just needs to have a thicker and bulkier body, the gap between the front handle and barrel has to be filled in
with a thin layer so it forms an groove the front handle can travel on. thickness of the handle must stay te same for
now". So, against round 8 (smudge_cube_pump_v8.py, kept):
- 5 % more girth, same length: done in the game's size line, not here (the pk3's Scale is length 0.7, width and height
  0.7 x GIRTH; make_job_smudge_v9.py), so every round part stays round;
- the pump keeps its real thickness: here it is built 1 / GIRTH as wide and as tall (its top still half a cube under
  the barrel), which the size line then brings back to what round 8 had;
- a bulkier body: the receiver one cube wider (REC_W 14 -> 15) and half a picture row deeper underneath;
- THE RAIL: a thin web (RAIL_W cubes wide) joins the barrel and the magazine tube along their whole length, from the
  receiver to the band, so nothing shows through between them and the pump has a rail to travel on; the pump has a slot
  for it (no pump cube sits in the rail), and the half-cube line under the barrel is closed by it.
Round 8's own note:

The smudge-cube shotgun, round 8 (2026-11-07, home PC).

Tefa on round 7: "it looks epic! the scratches, can you join all these so they are just long lines instead of like
dotted lines". The kit's line stepper (forge.Model._line_q) steps int(length x 4) times per segment, so a half-cube
segment took one step of two quarter cells and left a cell out every time: every scratch was a row of pits. Round 8
draws the scratch lines itself (_scratch_cells: at most half a quarter cell per step, every cell between joined), finds
the surface of every cell once before cutting any (so crossings do not cut deeper), then cuts. Round 7 (kept) below.

Round 7's own note:

Tefa on round 6 (a close-up of the pump's front end): "please make these edges straight cut as well". The pump's
side outline was rounded on every edge, its two ends too, so each end curled in. Now the pump is round only across
its length (top and bottom edges, pump_solid()), its front and back faces cut flat and square. Tefa also: "it looks
epic already though!". (Their other note, the glossy light, is Blender's viewport studio light with its shine; the
model itself carries no gloss; see the board.) Round 6 (kept) below.

Round 6's own note:

Tefa on round 5: "scratches to be longer, but have the underlying colour the same as where the scratches are carved
in to, so they don't show a different colour underneath. the shell guard needs to be more smudged and blocky". So:
- scratches about twice as long and two quarter cubes deep (their walls catch the light); the floor of a cut takes the very colour of the cube that was cut away (no brighter
  or darker floor), so only the cut itself shows;
- the trigger guard a half moon (Tefa, same message thread: "please curve the bottom of the trigger guard even more
  so it's a half moon shape"): its loop and finger hole are half ellipses hanging from the gun, _moon_loop();
- the shell guard: steel in blocks (BOLT_BLOCK main cubes, half a picture pixel) of their own brightness, blended
  SMUDGE of the way into their neighbours as the picture is on the rest of the gun, and built in whole cubes where it
  is flat (the kit's mixed cubes) instead of half cubes.
Round 5 (kept) below.

Round 5's own note:

Tefa on round 4: "and still please carve some scratches into it, make the shell guard have a different pattern on it
alltogether than the rest of the gun". So:
- scratches CARVED, not painted: thin wandering cuts one quarter cube deep on the receiver, barrel and top, the pump
  and the stock; on metal the floor of the cut is bare, brighter steel (SCRATCH_METAL), on wood darker (SCRATCH_WOOD).
  Only the named parts are cut (the shell guard, shells and flashes never), carve_scratches() below.
- the shell guard (the ejection-port cover) no longer shows the game picture at all: brushed steel, fine lines along
  its length in its own steel tones (BOLT_*), about as dark as round 4's cover.
Round 4 (kept) below.

Round 4's own note:

Tefa on round 3: "pump handle travel rod is also coloured like the handle close to the handle, make the shell guard a
little darker". The game picture draws the pump over the magazine tube, so the tube under it took the pump's wood
colours; the tube (and its cap) now take the tube's own grey from the picture columns just behind the pump (31-33,
ROD_PX), whatever x. The shell guard goes BOLT_MIX 0.35 -> 0.2 toward bright steel. Round 3 (kept) below.

Round 3's own note:

Tefa on round 2: "this is what i'm talking about! nice. please make the handle all same size, right now it narrows
from the front end, the shell guard needs to be a bit different shade. make the body of the gun longer and the
trigger guard closer to the grip, and rounder. close the gap between the pump handle and barrel please, but leave it
as a line that the handle travels on". So, against round 2 (smudge_cube_pump_v2.py, kept):
- the pump is one even block from end to end (no narrowing at the front), its top raised to half a cube under the
  barrel: the gap closes to a thin line the pump slides along; the pump keeps its own picture colours;
- the ejection-port cover (the bolt) a lighter steel shade than the receiver round it;
- the receiver STRETCH_PX picture pixels longer: everything in front of it moves forward, the receiver's own picture
  is stretched to fit (X() places things, pic_u() reads the picture back);
- the trigger guard moved back towards the grip, its loop round (arcs, not cut corners), in the smallest cubes.

Round 2's own note:

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
from smudge_settings import BIG_PORT_LEN, BIG_SHELL_R, CHAMBER_DROP, CHAMBER_R, LOAD_DROP, SHELL_K
import smudge_settings
import sharp_kit
import forge
from forge import FINE

SCRATCH_DEPTH = 2                      # quarter cubes deep (round 5: 1); the walls of the cut are what show it
SCRATCH_LEN = (8.0, 20.0)              # main cubes, shortest and longest scratch on metal (round 5: 3-9)
SCRATCH_LEN_WOOD = (5.0, 12.0)         # on wood (round 5: 2-6)
SCRATCH_METAL = 2.0                    # the floor of a cut in metal: this much brighter (bare steel)
SCRATCH_WOOD = 0.55                    # the floor of a cut in wood: this much darker
BOLT_BASE = (78, 80, 86)               # the shell guard's brushed steel: its middle tone
BOLT_BLOCK = 2.45                      # main cubes per block of the shell guard's pattern (half a picture pixel)
BOLT_SPREAD = 0.22                     # +- brightness from block to block

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
    u = (math.floor(pic_u(x) * 3) + 0.5) / 3
    v = (math.floor(-z / S * 3) + 0.5) / 3
    iu, iv = min(max(int(u), 0), W - 1), min(max(int(v), 0), H - 1)
    nu, nv = PIC["near"][iv][iu]
    r, g, b, _ = PIC["rows"][nv][nu]
    sharp = (r * 255, g * 255, b * 255)
    smooth = _smooth(u, v) if (nu, nv) == (iu, iv) else None
    return sharp if smooth is None else mix(sharp, smooth, SMUDGE)


def _moon_loop(x0, x1, top, bot, n=32):
    """A side outline: straight top, and under it a half ellipse from x0 round to x1 reaching down to bot."""
    xc, a, b = (x0 + x1) / 2, (x1 - x0) / 2, top - bot
    return [(x0, top), (x1, top)] + [(xc + a * math.cos(math.pi * k / n), top - b * math.sin(math.pi * k / n))
                                     for k in range(n + 1)]


def _arc_loop(x0, x1, top, bot, r, n=10):
    """A side outline: straight top, straight sides, the two bottom corners round arcs of radius r."""
    r = max(0.0, min(r, (x1 - x0) / 2, top - bot))
    pts = [(x0, top), (x1, top)]
    for k in range(n + 1):                                   # front corner, from the side down to the bottom
        a = k / n * math.pi / 2
        pts.append((x1 - r + r * math.cos(a), bot + r - r * math.sin(a)))
    for k in range(n + 1):                                   # back corner, from the bottom up to the side
        a = math.pi / 2 + k / n * math.pi / 2
        pts.append((x0 + r + r * math.cos(a), bot + r - r * math.sin(a)))
    return pts


def round_guard(m, x0, x1, top, bot, col, w, bar, r):
    """The trigger guard of round 3: a round loop (arcs at the bottom, the bar round in cross-section), its finger
    hole carried up into the gun as a dark recess (as sharp_kit.guard), in cubes down to quarter size."""
    up = sharp_kit.GUARD_UP
    m.box(x0 + bar, x1 - bar, -2.5, 2.5, top - 0.5, top + up, None, size=SURF, carve=True)
    darken(m, lambda x, y, z: x0 + bar - 0.5 <= x < x1 - bar + 0.5 and abs(y) < 3.0 and top - 1 <= z < top + up + 0.5,
           0.55)
    m.part = "guard"
    out = Profile(_moon_loop(x0, x1, top + 0.5, bot))
    hole = Profile(_moon_loop(x0 + bar, x1 - bar, top + 1.0, bot + bar))
    sol = out.solid(lambda x: w / 2, bar / 2)
    round_fill(m.fill, lambda x, y, z: sol(x, y, z) and hole.sd(x, z) <= 0, out.bounds(w / 2), col, size=1.0,
               keep=True)


def carve_scratches(m, side, region, count, seed, parts, floor, length=(3.0, 9.0), along=0.5, width=2):
    """Carve `count` thin scratches into the surface seen from `side`, inside region (a0, a1, b0, b1) in main cubes
    (the two axes other than the side's, in x, y, z order): one quarter cube deep, `width` quarter cubes wide, the floor's colour times `floor`.
    A cell is cut only when the outermost cube there belongs to one of `parts`. `along` = how far a scratch may turn
    away from the gun's length (radians either way)."""
    ax, sign = forge.SIDES[side]
    a0, a1, b0, b1 = region
    for i in range(count):
        def r(k):
            return hash01(seed, i, k)
        a = a0 + (a1 - a0) * r(1)
        b = b0 + (b1 - b0) * r(2)
        L = length[0] + (length[1] - length[0]) * r(3)
        h = (r(4) - 0.5) * 2 * along + (math.pi if r(5) > 0.5 else 0.0)
        pts = [(a, b)]
        for st in range(int(L * 2)):
            h += (r(10 + st) - 0.5) * 0.4
            a += math.cos(h) * 0.5
            b += math.sin(h) * 0.5
            pts.append((a, b))
        cells = _scratch_cells(pts, width)
        surf = [(m.surface_q(side, qa, qb), (qa, qb)) for qa, qb in cells]
        for q, _ in surf:
            if q is None:
                continue
            v = m.get_q(*q)
            if v is None or v[2] not in parts:
                continue
            qq = list(q)
            for _ in range(SCRATCH_DEPTH):
                m.clear_q(*qq)
                qq[ax] -= sign
            w = m.get_q(*qq)
            if w is not None:
                m.put_q(*qq, v[0] if floor is None else mul(w[0], floor), w[1], w[2])


def _scratch_cells(pts, width):
    """Every quarter cell (a, b) a polyline in main units passes over, joined (steps of at most half a quarter cell),
    each widened by `width` cells across b; in order, no repeats."""
    seen, out = set(), []
    for (a0, b0), (a1, b1) in zip(pts, pts[1:]):
        n = max(1, math.ceil(max(abs(a1 - a0), abs(b1 - b0)) * FINE * 2))
        for st in range(n + 1):
            t = st / n
            qa = math.floor((a0 + (a1 - a0) * t) * FINE)
            qb = math.floor((b0 + (b1 - b0) * t) * FINE)
            for w in range(width):
                c = (qa, qb + w)
                if c not in seen:
                    seen.add(c)
                    out.append(c)
    return out


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

def big_shell(m, part, x0, yc, zc, keep, k=SHELL_K):
    """sharp_kit.shell, k times the size: a 12 gauge shell lying along x, rim at x0 (brass head, red hull, crimp)."""
    m.part = part

    def hull(x, y, z):
        return sharp_kit.HULL[0 if hash01(math.floor(x), math.floor(y), math.floor(z), 9) < 0.3 else 1]
    m.cyl(x0, x0 + 4.0 * k, yc, zc, 2.95 * k, BRASS, edge=SURF, keep=keep)
    m.cyl(x0 - 0.5 * k, x0, yc, zc, 3.3 * k, mul(BRASS, 0.85), edge=SURF, keep=keep)
    m.cyl(x0 + 4.0 * k, x0 + 20.0 * k, yc, zc, 2.85 * k, hull, edge=SURF, keep=keep)
    m.cyl(x0 + 19.5 * k, x0 + 20.5 * k, yc, zc, 1.0 * k, None, carve=True, edge=None, size=0.5)


SIDE_SPRITE = "Sprites/Weapons/GRZPA0.png"
NAME = "smudge_cube_pump_v12"
GIRTH = 1.0                            # the game draws width and height this much bigger than length (round 9)
RAIL_W = 3.0                           # main cubes: the web between barrel and tube that the pump travels on
GUN_LENGTH_M = 1.0                     # as before: the 60-pixel picture spans one metre (Tefa settled the size at 1.0)
S = GUN_LENGTH_M / 60 / CUBE_M         # main cubes per picture pixel (4.9)


STRETCH_PX = 4.0                       # how many picture pixels longer the receiver is (it spans 12..31 in the picture)
REC_PX0, REC_PX1 = 12.0, 31.0


def X(px):
    """Main cubes along the gun for picture column px, with the receiver stretched and everything in front of it
    moved forward."""
    t = min(max((px - REC_PX0) / (REC_PX1 - REC_PX0), 0.0), 1.0)
    return (px + STRETCH_PX * t) * S


def pic_u(x):
    """The picture column under a point x (main cubes): the inverse of X()."""
    a = x / S
    if a <= REC_PX0:
        return a
    if a >= REC_PX1 + STRETCH_PX:
        return a - STRETCH_PX
    return REC_PX0 + (a - REC_PX0) * (REC_PX1 - REC_PX0) / (REC_PX1 - REC_PX0 + STRETCH_PX)


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
REC_TOP, REC_BOT = Z(4.0), Z(11.6)      # round 11: on the pump's bottom line (PUMP_BOT, below)
REC_W, REC_ROUND = 21.0, 3.0           # round 11: fat (round 8: 14, 2.0)
PORT_X0 = REC_X1 - 1.5 - BIG_PORT_LEN  # round 12: the port is one BIG shell long and ends just behind the barrel
SHELL2_OUT = smudge_settings.SHELL2_OUT
CH_ZC = BARREL_ZC - CHAMBER_DROP        # the chamber's axis
assert REC_W == smudge_settings.REC_W
# the pump's back end sits one stroke ahead of the receiver: pulled all the way, it meets the receiver and the port is
# fully open (Tefa: "handle needs to travel the whole length")
PUMP_X0, PUMP_X1 = REC_X1 + PORT_LEN, X(51.4)
# the pump's top half a cube under the barrel's lowest cubes (they sit on the half-cube grid): a thin line it slides on
PUMP_TOP = math.floor((BARREL_ZC - BARREL_R) * 2) / 2
PUMP_BOT = PUMP_TOP - (PUMP_TOP - Z(11.6)) / GIRTH    # round 9: built 1 / GIRTH as tall and wide, so the game
PUMP_W, PUMP_ROUND = 16.0 / GIRTH, 6.5 / GIRTH          # draws it exactly as thick as round 8
PUMP_GROOVE_W, PUMP_GROOVE_STEP, PUMP_GROOVE_DEPTH, PUMP_GROOVE_MARGIN = 2.0, 6.0, 1.0, 7.0
STOCK_W_WRIST, STOCK_W_BUTT, STOCK_ROUND = 16.0, 17.0, 4.0   # round 11 (round 8: 11, 13.5)
PAD_LEN = 2.5                          # rubber butt pad
STRAPS, STRAP_W, STRAP_GAP, STRAP_SLANT, STRAP_RAISE = 3, 4.0, 3.0, 0.35, 0.5
GUARD_LEN = 9.0 * S                    # main cubes, front to back (round 2: 9.4 picture pixels)
GUARD_X0 = X(10.4)                     # its back end, under the grip's wrist (round 2: 12.6)
GUARD_X1, GUARD_BOT, GUARD_W, GUARD_BAR = GUARD_X0 + GUARD_LEN, Z(15.0), 4.5, 2.5
GUARD_R = 7.0                          # the loop's corner radius (main cubes): round, not cut corners
TRIGGER_X = GUARD_X0 + 0.48 * GUARD_LEN
ROD_PX = 31.2                          # first picture column of the tube's own grey (31-33, just behind the pump)
BOLT_STEEL, BOLT_MIX = (150, 152, 158), 0.2   # the shell guard: the picture's colour taken this far to bright steel

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
    def tube_col(x, y, z):
        """The tube's own grey: the picture's tube columns behind the pump (ROD_PX), one of the three per pixel step."""
        return pc(X(ROD_PX + math.floor(x / S) % 3), y, z)
    round_fill(m.cyl, TUBE_X0, TUBE_X1, 0.0, TUBE_ZC, TUBE_R, tube_col, keep=True)
    round_fill(m.cyl, TUBE_X1, TUBE_X1 + CAP_LEN, 0.0, TUBE_ZC, CAP_R, tube_col, keep=True)
    m.cyl(TUBE_X1 + CAP_LEN - 0.5, TUBE_X1 + CAP_LEN + 0.5, 0.0, TUBE_ZC, 1.2, None, carve=True, edge=None, size=0.5)
    bx0, bx1 = X(52.6), X(53.8)
    # the rail (round 9): a thin web from the barrel's middle down to the tube's middle, receiver to band
    m.part = "barrel"

    def rail(x, y, z):
        return BARREL_X0 <= x < bx0 and abs(y) < RAIL_W / 2 and TUBE_ZC <= z <= BARREL_ZC
    m.box(BARREL_X0, bx0, -RAIL_W / 2, RAIL_W / 2, TUBE_ZC, BARREL_ZC, tube_col, size=SURF, keep=True)
    m.part = "band"

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
    port = (PORT_X0, PORT_X0 + BIG_PORT_LEN, -REC_W / 2 - 1, 0.0, CH_ZC - CHAMBER_R, CH_ZC + CHAMBER_R)
    m.box(*port, None, size=SURF, carve=True)                                  # from the right side to the middle
    m.cyl(port[0], port[1], 0.0, CH_ZC, CHAMBER_R, None, carve=True, edge=None, size=0.5)   # its round far side
    # the barrel's own bore, cut through the port's front wall into the hollow barrel: you look into the barrel
    m.cyl(port[1] - 1.0, BARREL_X0 + 4.0, 0.0, BARREL_ZC, BORE_R, None, carve=True, edge=None, size=0.5)
    darken(m, lambda x, y, z: port[0] - 1.0 <= x < port[1] + 1.0 and -REC_W / 2 + 2.5 <= y < CHAMBER_R + 1.0
           and port[4] - 1.0 <= z < port[5] + 1.0, 0.4)
    darken(m, lambda x, y, z: port[1] - 1.0 <= x < BARREL_X0 + 4.5 and math.hypot(y, z - BARREL_ZC) < BORE_R + 1.0,
           0.5)
    m.part = "bolt"
    def bolt_col(x, y, z):
        """Blocky, smudged steel: each BOLT_BLOCK block its own brightness, SMUDGE of the way to the smooth blend of
        the four blocks round the point."""
        def block(i, j):
            return 1.0 + BOLT_SPREAD * (hash01(i, j, 23) - 0.5) * 2
        bu, bv = x / BOLT_BLOCK, z / BOLT_BLOCK
        sharp = block(math.floor(bu), math.floor(bv))
        u0, v0 = math.floor(bu - 0.5), math.floor(bv - 0.5)
        fu, fv = bu - 0.5 - u0, bv - 0.5 - v0
        smooth = ((block(u0, v0) * (1 - fu) + block(u0 + 1, v0) * fu) * (1 - fv)
                  + (block(u0, v0 + 1) * (1 - fu) + block(u0 + 1, v0 + 1) * fu) * fv)
        return mul(BOLT_BASE, sharp + (smooth - sharp) * SMUDGE)
    m.box(port[0], port[1], -REC_W / 2 + 0.5, -REC_W / 2 + 2.5, port[4] + 0.5, port[5] - 0.5, bolt_col, size=1.0,
          edge=SURF)                                                         # round 12: a thin plate over the chamber
    m.box(port[0], port[1], -REC_W / 2, -REC_W / 2 + 1.0, (port[4] + port[5]) / 2 - 0.5,
          (port[4] + port[5]) / 2 + 0.5, None, size=SURF, carve=True)         # a groove along the bolt
    m.part = "receiver"
    for side in (-1, 1):
        y0, y1 = (side * REC_W / 2 - 0.5, side * REC_W / 2 + 1) if side > 0 else (-REC_W / 2 - 1, -REC_W / 2 + 0.5)
        m.box(X(21.0), REC_X1, y0, y1, Z(8.7), Z(8.5), None, size=SURF, carve=True)  # the seam
    loadport = (X(22.0), X(22.0) + BIG_PORT_LEN + 1.0, -BIG_SHELL_R - 0.6, BIG_SHELL_R + 0.6, REC_BOT - 1,
                REC_BOT + 2 * BIG_SHELL_R + 1.0)
    m.box(*loadport, None, size=SURF, carve=True)
    darken(m, lambda x, y, z: loadport[0] - 0.5 <= x < loadport[1] + 0.5 and abs(y) < BIG_SHELL_R + 1.2
           and REC_BOT <= z < loadport[5] + 0.5, 0.6)

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
    round_guard(m, GUARD_X0, GUARD_X1, REC_BOT, GUARD_BOT, pc, w=GUARD_W, bar=GUARD_BAR, r=GUARD_R)
    blade(m, TRIGGER_X, REC_BOT, GUARD_BOT + GUARD_BAR + 1.0, pc, w=1.0,
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
    ppoly = [(PUMP_X0, PUMP_TOP), (PUMP_X1, PUMP_TOP), (PUMP_X1, PUMP_BOT), (PUMP_X0, PUMP_BOT)]
    pp = Profile(ppoly)
    bands = []
    x = PUMP_X0 + PUMP_GROOVE_MARGIN
    while x + PUMP_GROOVE_W <= PUMP_X1 - PUMP_GROOVE_MARGIN:
        bands.append((x, x + PUMP_GROOVE_W))
        x += PUMP_GROOVE_STEP
    def pump_solid(grow=0.0):
        """The pump: square-cut ends (x0..x1 exactly), rounded only across its length (from its top and bottom)."""
        def inside(x, y, z):
            if not (PUMP_X0 <= x < PUMP_X1):
                return False
            dz = min(z - PUMP_BOT, PUMP_TOP - z) + grow
            if dz <= 0:
                return False
            t = min(dz / PUMP_ROUND, 1.0)
            return abs(y) < (PUMP_W / 2 + grow) * math.sqrt(max(0.0, 1.0 - (1.0 - t) ** 2))
        return inside

    pout = pump_solid()
    pin = pump_solid(-PUMP_GROOVE_DEPTH)
    pg = grooved(pout, pin, bands)
    pump_rows = (Z(10.8), Z(7.3))          # the pump's own rows in the picture: its raised top keeps the pump's colours

    def pwood(x, y, z):
        return pc(x, y, min(max(z, pump_rows[0]), pump_rows[1]))
    round_fill(m.fill, lambda x, y, z: pg(x, y, z) and math.hypot(y, z - TUBE_ZC) >= TUBE_R and not rail(x, y, z),
               pp.bounds(PUMP_W / 2),
               pwood, size=1.0)
    # the groove floors in shadow (the cut is geometry; this is only the shade at its bottom)
    pdeep = pump_solid(-PUMP_GROOVE_DEPTH - 0.5)
    darken(m, lambda x, y, z: any(a <= x < b for a, b in bands) and pin(x, y, z) and not pdeep(x, y, z), 0.62)
    # the tube again where the pump sleeve meets it, so no pump cube bites into the tube (seen when the pump racks)
    m.part = "tube"
    round_fill(m.cyl, PUMP_X0 - 1, PUMP_X1 + 1, 0.0, TUBE_ZC, TUBE_R, tube_col)
    m.part = "barrel"                                        # and the rail again, for the same reason
    m.box(PUMP_X0 - 1, PUMP_X1 + 1, -RAIL_W / 2, RAIL_W / 2, TUBE_ZC + TUBE_R - 0.5, BARREL_ZC - BARREL_R + 0.5,
          tube_col, size=SURF)
    m.part = "pump"
    for side in (-1, 1):
        y0 = side * (TUBE_R + 0.25)
        m.box(REC_X1, PUMP_X0 + 1, min(y0, y0 + side * 1.0), max(y0, y0 + side * 1.0), TUBE_ZC - 0.5, TUBE_ZC + 0.5,
              pc, size=SURF, keep=True)

    # --- shells (move; hidden unless a reload frame shows them): one under the loading port, one at the ejection port
    big_shell(m, "shell", loadport[0] + 1.0, 0.0, REC_BOT - LOAD_DROP, False)
    # built clear of the gun, beside the open port (SHELL2_OUT), lined up with it (it is one shell long), so no cube
    # of it is lost to the receiver; the reload frames move it in (make_job_sharp.SHELL2)
    big_shell(m, "shell2", port[0] + PORT_CLEAR / 2 + 0.5, -REC_W / 2 - SHELL2_OUT, CH_ZC, False)

    # --- muzzle flashes (move; hidden unless a firing frame shows them), all in the smallest cubes
    flashes(m, MUZZLE_X + 0.5, BARREL_ZC)

    # --- carved scratches (round 6: longer, and the floor of a cut keeps the cut cube's own colour: floor=None)
    metal = ("receiver", "barrel", "band")
    for side, seed in (("+y", 101), ("-y", 102)):
        carve_scratches(m, side, (REC_X0 + 2, REC_X1 - 2, REC_BOT + 2, REC_TOP - 1), 14, seed, metal, None,
                        length=SCRATCH_LEN)
        carve_scratches(m, side, (BARREL_X0 + 4, MUZZLE_X - 3, BARREL_ZC - 3, BARREL_TOP - 1), 7, seed + 10, metal,
                        None, length=SCRATCH_LEN, along=0.25)
        carve_scratches(m, side, (PUMP_X0 + 2, PUMP_X1 - 2, PUMP_BOT + 3, PUMP_TOP - 3), 4, seed + 20, ("pump",),
                        None, length=SCRATCH_LEN_WOOD, along=1.0)
        carve_scratches(m, side, (PAD_LEN + 2, REC_X0 - 2, Z(15.0), Z(6.0)), 5, seed + 30, ("grip",), None,
                        length=SCRATCH_LEN_WOOD, along=1.0)
    carve_scratches(m, "+z", (REC_X0 + 2, MUZZLE_X - 3, -4.0, 4.0), 10, 141, metal, None, length=SCRATCH_LEN,
                    along=0.3)
    return m
