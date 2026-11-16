"""The revolver in the Meshy guns' look, with no Meshy model, round 1 (2026-11-16, Keeper PC). A forge design.

Tefa: "can you please make the ashes 2063 revolver in the style of the meshy weapons we did yesterday", then, as no
Meshy model of it exists: "can you do it without the meshy picture and see what you can come up with?" So the shape is
built here by rule, to a real revolver's proportions (the heavy six-shot the game's is drawn from: forge/detail/refs/
revolver.md: full-length underlug, vented top rib, fat fluted cylinder, spur hammer, orange front-sight insert), and the
Meshy texture's look is painted by rule (meshy_look.py). Size as the sharp revolver (sharp_settings.REV_LENGTH_M), the
top where every Meshy gun's top sits. Parts: frame, barrel, cylinder, hammer, trigger, guard, grip. Not in the game yet.
    python blender-cubekit/forge_make.py <out> <out> meshy_look_revolver.py
"""
import math

from sharp_kit import BORE, BRIGHT_METAL, SURF, Profile, barrel, blade, body, darken, guard, screws, start
from forge import mix
from meshy_kit import TOP_M
from meshy_look import smudged, steel, wood
from sharp_settings import CUBE_M, REV_LENGTH_M

NAME = "meshy_look_revolver"
# ---- the settings table, in main cubes: x from the back of the grip to the muzzle, y to the gun's left, z up
LEN = REV_LENGTH_M / CUBE_M                  # 132: the whole gun
TOP = TOP_M / CUBE_M                         # -17: the top strap
BZ, BR, BORE_R = TOP - 6.0, 4.6, 2.0         # the barrel: axis height, radius, bore
RING = 5.0                                   # the chambers' distance from the cylinder's axis
CZ, CR = BZ - RING, 8.5                      # the cylinder: axis height (the top chamber meets the barrel), radius
CX0, CX1 = 48.0, 68.5                        # the cylinder: back and front
CHAMBER_R, FLUTE_R, FLUTE_OUT, FLUTE_X0 = 2.0, 2.5, 1.1, 55.0
NOTCH = (50.5, 52.5, 1.0)                    # the cylinder stop notches: from x, to x, depth
WIN = (47.5, 69.0, CZ - CR - 0.5, CZ + CR + 0.5)     # the frame's window the cylinder sits in (x0, x1, z0, z1)
SHIELD = (44.5, 47.5, 7.6)                   # the recoil shield behind the cylinder (x0, x1, radius)
FRAME_W, FRAME_RND = 5.5, 2.0                # half width, edge rounding
FX1 = 73.5                                   # the frame's front face, where the barrel starts
FRAME_BOT = -41.0
LUG_BOT, LUG_W = -33.5, 3.3                  # the underlug: its underside, half width
RIB_TOP, RIB_W = TOP + 0.5, 1.6
VENT = (78.0, 118.0, 6.0, 3.5)               # the rib's vents: from x, to x, one every, each this long
SIGHT = (121.0, 129.0, 3.5, 0.6)             # front sight ramp: from x, to x, height, rise per cube
SIGHT_INSERT_X = 126.0                       # the orange insert: the ramp's back face from here
REAR_SIGHT = (35.0, 41.0, 3.0, 2.0)          # from x, to x, half width, height
GUARD = (45.0, 64.0, FRAME_BOT, -53.0)       # trigger guard: from x, to x, top, bottom
GUARD_UP = 2.0
TRIGGER_X = 53.0
GRIP_W, GRIP_RND = 6.0, 4.0
GRIP_SCREW = (22.0, -62.0)
GRIP_SQUASH = 0.72                           # round 2: the grip below the frame was ~24 cm; this brings it to ~17
STEEL_FRAME, STEEL_BARREL, STEEL_CYL, STEEL_SMALL = 78, 84, 92, 70   # round 2: darker, as the Meshy guns
RUST_FROM = 0.625                            # round 2: rust in fewer, smaller patches
WOOD_SHADE = 0.72
LATCH = (37.5, 43.0, -30.5, -27.0)           # the cylinder latch on the left side (x0, x1, z0, z1)
ORANGE = (236, 104, 30)
SIGHT_BLACK = (30, 31, 34)
SOOT = 0.55                                  # the cylinder gap and its faces, blackened by powder

FRAME_POLY = [(34, TOP - 0.5), (72, TOP), (FX1, TOP - 3), (FX1, -36), (70, -40), (64, FRAME_BOT), (46, FRAME_BOT),
              (44, -46), (38, -47), (30, -45), (25, -40), (26, -32), (30, -25), (33, -20)]
HAMMER_POLY = [(34.5, -27), (36, -20), (32, TOP + 1.5), (25.5, TOP + 3.5), (24, TOP + 2), (29.5, TOP - 1.5),
               (30, -27)]
GRIP_POLY = [(46, -42), (43.5, -52), (41, -56), (40.5, -62), (37, -66), (36, -72), (32.5, -76), (31, -84), (27, -87),
             (8, -86), (3, -82), (3, -74), (8, -62), (15, -50), (22, -41), (26, -36), (34, -38)]
LUG_POLY = [(FX1, BZ), (LEN - 2, BZ), (LEN - 2, LUG_BOT + 3), (LEN - 5, LUG_BOT), (FX1 + 3, LUG_BOT),
            (FX1, LUG_BOT - 2.5)]


def chambers():
    """The six chamber axes (y, z from the cylinder's axis), one at the top in line with the barrel."""
    return [(RING * math.sin(k * math.pi / 3), RING * math.cos(k * math.pi / 3)) for k in range(6)]


def build():
    m = start(NAME)
    low = lambda x, y, z: 0.10 * max(0.0, min(1.0, (BZ - z) / 20.0))  # noqa: E731  more rust lower on the gun
    frame_c = smudged(steel(STEEL_FRAME, RUST_FROM, 21, more_rust=low))
    barrel_c = smudged(steel(STEEL_BARREL, RUST_FROM + 0.01, 31, more_rust=low))
    small_c = smudged(steel(STEEL_SMALL, 0.70, 61))

    # --- frame, with the window the cylinder sits in, the recoil shield behind it, the rear sight
    wx0, wx1, wz0, wz1 = WIN
    window = lambda x, y, z: wx0 <= x < wx1 and wz0 < z < wz1  # noqa: E731
    body(m, "frame", FRAME_POLY, FRAME_W, FRAME_RND, frame_c, exclude=window)
    m.cyl(SHIELD[0], SHIELD[1], 0.0, CZ, SHIELD[2], frame_c, edge=SURF, keep=True, part="frame")
    rx0, rx1, rw, rh = REAR_SIGHT
    m.box(rx0, rx1, -rw, rw, TOP - 0.5, TOP + rh, SIGHT_BLACK, size=SURF, keep=True, part="frame")
    m.box(rx0 - 0.5, rx1 + 0.5, -0.75, 0.75, TOP + rh - 1.0, TOP + rh + 0.5, None, size=SURF, carve=True)
    lx0, lx1, lz0, lz1 = LATCH
    m.box(lx0, lx1, FRAME_W - 0.5, FRAME_W + 1.0, lz0, lz1, small_c, size=SURF, keep=True, part="frame")
    screws(m, [(40.0, -42.5), (60.0, -39.0), (33.0, -30.0)], FRAME_W - 0.5, col=(150, 148, 144))

    # --- barrel: round, on a full-length underlug, a vented rib with a ramp front sight on top
    barrel(m, "barrel", FX1, LEN, 0.0, BZ, BR, BORE_R, barrel_c)
    body(m, "barrel", LUG_POLY, LUG_W, 2.0, barrel_c, keep=True,
         exclude=lambda x, y, z: math.hypot(y, z - BZ) < BR)
    m.box(FX1, LEN - 2.0, -RIB_W, RIB_W, BZ + BR - 1.0, RIB_TOP, barrel_c, size=SURF, keep=True, part="barrel")
    v0, v1, every, vlen = VENT
    x = v0
    while x + vlen <= v1:
        m.box(x, x + vlen, -RIB_W - 0.5, RIB_W + 0.5, BZ + BR, RIB_TOP - 1.0, None, size=SURF, carve=True)
        x += every
    sx0, sx1, sh, rise = SIGHT

    def sight(x, y, z):
        return sx0 <= x < sx1 and abs(y) < 1.0 and RIB_TOP - 0.5 <= z < RIB_TOP + min(sh, (x - sx0) * rise)
    m.fill(sight, (sx0, sx1, -1.5, 1.5, RIB_TOP - 1, RIB_TOP + sh + 1),
           lambda x, y, z: ORANGE if x >= SIGHT_INSERT_X and z >= RIB_TOP + 1.0 else SIGHT_BLACK, size=SURF,
           part="barrel", keep=True)

    # --- cylinder (its own part): fluted between the chambers, stop notches, chamber mouths at the front
    cyl_c = smudged(steel(STEEL_CYL, RUST_FROM + 0.03, 41,
                          more_rust=lambda x, y, z: 0.05 if math.hypot(y, z - CZ) < CR - 1.2 else 0.0))
    ch = chambers()

    def cyl_in(x, y, z):
        r = math.hypot(y, z - CZ)
        if not (CX0 <= x < CX1) or r >= CR:
            return False
        for k in range(6):
            a = (k + 0.5) * math.pi / 3                              # a flute between two chambers
            if x >= FLUTE_X0 and math.hypot(y - (CR + FLUTE_OUT) * math.sin(a),
                                            z - CZ - (CR + FLUTE_OUT) * math.cos(a)) < FLUTE_R:
                return False
            b = k * math.pi / 3                                      # a stop notch over each chamber
            if NOTCH[0] <= x < NOTCH[1] and r > CR - NOTCH[2] and \
                    math.hypot(y - CR * math.sin(b), z - CZ - CR * math.cos(b)) < 1.3:
                return False
        return True
    m.fill(cyl_in, (CX0, CX1, -CR - 1, CR + 1, CZ - CR - 1, CZ + CR + 1), cyl_c, size=1.0, edge=SURF,
           part="cylinder", keep=True)
    for cy, cz in ch:
        m.cyl(CX1 - 2.0, CX1 + 0.5, cy, CZ + cz, CHAMBER_R, None, carve=True, edge=None, size=SURF)
    darken(m, lambda x, y, z: CX1 - 2.5 <= x < FX1 + 0.5 and wz0 < z < wz1, SOOT)

    # --- hammer, trigger guard, trigger
    body(m, "hammer", HAMMER_POLY, 1.5, 0.5, small_c, keep=True)
    gx0, gx1, gtop, gbot = GUARD
    guard(m, gx0, gx1, gtop, gbot, small_c, w=3.5, bar=1.8, up=GUARD_UP)
    blade(m, TRIGGER_X, gtop, gbot + 3.5, mix((96, 98, 104), BRIGHT_METAL, 0.4), lean=0.4, up=GUARD_UP)

    # --- grip: wood with finger swells, on a steel grip frame that shows along the front and back
    sq = lambda z: z if z >= FRAME_BOT else FRAME_BOT + (z - FRAME_BOT) * GRIP_SQUASH  # noqa: E731
    gp = Profile([(x, sq(z)) for x, z in GRIP_POLY])
    wood_c = smudged(wood(71, along=(-0.42, -0.91), shade=WOOD_SHADE, grime_from=0.72))
    strap_c = smudged(steel(STEEL_SMALL, 0.66, 73))

    def grip_col(x, y, z):
        return strap_c(x, y, z) if abs(y) < 1.6 and gp.sd(x, z) < 1.4 else wood_c(x, y, z)
    m.fill(gp.solid(lambda x: GRIP_W, GRIP_RND), gp.bounds(GRIP_W), grip_col, size=1.0, edge=SURF, part="grip",
           keep=True)
    screws(m, [(GRIP_SCREW[0], sq(GRIP_SCREW[1]))], GRIP_W - 0.5, col=(150, 148, 144))

    # the bore, dark to its end
    m.cyl(LEN - 3.0, LEN + 0.5, 0.0, BZ, BORE_R, None, carve=True, edge=None, size=SURF)
    assert BORE
    return m
