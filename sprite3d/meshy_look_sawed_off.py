"""The sawn-off in the Meshy guns' look, slimmer, round 1 (2026-11-16, Developer PC). A forge design.

Tefa: "change the double barrel, it's too fat and bulky ... knowing what you know now with meshy weapons, can you look
at this picture and tweak our latest sawed off accordingly, to look slimmer like those screenshots, but still blocky
and in the style of other meshy weapons." The picture: a short side-by-side coach gun with outside hammers, thin dark
barrels, a slim wooden fore-end under them, a narrow action with side plates, two triggers, a curved wooden pistol grip.

So, from the sharp sawn-off (sharp_sawed_off.py) with the same length, breech and muzzle (the game's side picture
SAWPA0 still sets them, read at run time): barrels 4.2 cubes round instead of 5 and closer together; no heavy dark rib,
tape or blue cloth; a slim fore-end; the action as wide as the barrels and half as deep, with side plates and two
hammers; a slimmer, curved grip with a steel butt cap. Painted as the Meshy-look revolver (meshy_look.py): worn steel
in big and small patches with very little rust, plank-coloured wood with its grain, every cube half its own colour and
half its 3-cube block's. Parts as the sharp one's, so make_job_sawed_off.py's poses drive it (make_job_meshy_guns.py,
with this gun's own hinge: sharp_settings.MSAWN_HINGE).
    python blender-cubekit/forge_make.py <out> <out> meshy_look_sawed_off.py
"""
import math

from forge import mix
from meshy_look import smudged, steel, wood
from sharp_kit import BORE, BRIGHT_METAL, SURF, Picture, Profile, blade, flashes, guard, shell, start
from sharp_settings import (MSAWN_AXIS_Z, MSAWN_BARREL_R, MSAWN_BARREL_Y, SAWN_BREECH_PX, SAWN_LENGTH_M,
                            SAWN_MUZZLE_PX, park_z)

NAME = "meshy_look_sawed_off"
SIDE_SPRITE = "Sprites/Weapons/SAWPA0.png"
# ---- the settings table, in main cubes (x back of the grip to the muzzle, y to the gun's left, z up) ----
BORE_R = 2.0
RIB_W = 1.4                      # half width of the top and bottom ribs in the valleys between the barrels
ACTION_DEPTH = 9.0               # the action under the barrels' bottom
ACTION_X0_PX = 15.0              # where the action meets the wrist (picture column)
AW_EXTRA = 0.3                   # the action's half width past the barrels' sides
A_ROUND = 2.0
FOREND_PX = (22.8, 36.5)         # the fore-end: from, to (picture columns)
FOREND_DROP = 3.0                # below the barrels' bottom
FOREND_ROUND = 2.0
GRIP_W_WRIST, GRIP_W_BUTT, GRIP_ROUND = 9.0, 10.5, 3.0
CAP_ROW = 12.3                   # below this row of the picture the grip is the steel butt cap
GUARD_DROP, GUARD_W, GUARD_BAR = 11.0, 3.0, 1.8
TRIGGERS_PX = (16.8, 18.4)
HAMMER_Y = 4.0                   # each hammer's middle off the centre line
STEEL_BARREL, STEEL_ACTION, STEEL_SMALL = 62, 74, 70     # dark, as the photo's blued barrels
RUST_FROM = 0.80                 # almost none
WOOD_SHADE = 0.82
FLASH_SCALE = 0.75
# the curved pistol grip, (picture column, row): along the top of the wrist to the butt, back along its belly
GRIP_PX = [(15.6, 5.0), (12.0, 5.6), (8.5, 6.6), (5.5, 7.8), (3.6, 9.0), (2.6, 10.6), (2.8, 12.0), (4.0, 12.6),
           (5.6, 12.2), (7.4, 11.0), (9.6, 9.6), (12.0, 8.8), (14.0, 8.4), (15.6, 8.3)]
HAMMER = [(0.0, 0.0), (2.4, 0.0), (1.6, 3.2), (-0.6, 6.4), (-2.6, 7.0), (-2.2, 5.6), (-0.6, 3.6), (-0.4, 0.0)]


def build():
    pic = Picture(SIDE_SPRITE, SAWN_LENGTH_M)
    X, Z = pic.X, pic.Z
    m = start(NAME)
    BR, BY, ZC = MSAWN_BARREL_R, MSAWN_BARREL_Y, MSAWN_AXIS_Z
    BX0, MZ = X(SAWN_BREECH_PX), X(SAWN_MUZZLE_PX)
    A_TOP, A_BOT = ZC + BR, ZC - BR - ACTION_DEPTH
    AW = BY + BR + AW_EXTRA                                          # the action's half width
    barrel_c = smudged(steel(STEEL_BARREL, RUST_FROM, 131))
    action_c = smudged(steel(STEEL_ACTION, RUST_FROM, 141, scuffs=0.7))
    small_c = smudged(steel(STEEL_SMALL, 0.8, 151))

    def in_barrels(x, y, z, grow=0.0):
        return any(math.hypot(y - yc, z - ZC) < BR + grow for yc in (-BY, BY))

    # --- barrels: two thin tubes side by side, hollow, the sawn muzzles worn bright
    m.part = "barrels"

    def bcol(x, y, z):
        if any(math.hypot(y - yc, z - ZC) < BORE_R + 0.8 for yc in (-BY, BY)):
            return BORE
        c = barrel_c(x, y, z)
        return mix(c, BRIGHT_METAL, 0.45) if x > MZ - 0.6 else c
    for yc in (-BY, BY):
        m.cyl(BX0, MZ, yc, ZC, BR, bcol, hollow=BORE_R, edge=SURF, keep=True)

    # --- the ribs in the valleys above and below, a small steel bead at the muzzle
    m.part = "rib"
    m.box(BX0, MZ - 0.5, -RIB_W, RIB_W, ZC, ZC + BR - 0.5, barrel_c, size=SURF, keep=True)
    m.part = "lug"
    m.box(BX0, MZ - 0.5, -RIB_W, RIB_W, ZC - BR + 0.5, ZC, barrel_c, size=SURF, keep=True)
    m.part = "bead"
    m.box(MZ - 2.5, MZ - 1.0, -0.75, 0.75, ZC + BR - 0.5, ZC + BR + 1.0, mix(BRIGHT_METAL, (200, 200, 196), 0.5),
          size=SURF)

    # --- fore-end: slim wood under the barrels, rounded, its front cut on a slant
    m.part = "forend"
    fx0, fx1 = X(FOREND_PX[0]), X(FOREND_PX[1])
    fbot = ZC - BR - FOREND_DROP
    fp = Profile([(fx0, ZC - 0.5), (fx1, ZC - 0.5), (fx1 + 2.0, ZC - BR), (fx1 - 1.0, fbot), (fx0 + 1.0, fbot),
                  (fx0, fbot + 1.0)])
    fsolid = fp.solid(lambda x: AW - 0.6, FOREND_ROUND)
    fwood = smudged(wood(91, along=(1.0, 0.0), shade=WOOD_SHADE))
    m.fill(lambda x, y, z: fsolid(x, y, z) and not in_barrels(x, y, z, 0.01), fp.bounds(AW), fwood, size=1.0,
           edge=SURF, keep=True)

    # --- action: as wide as the barrels, half as deep as the sharp one's, side plates with two screws each
    m.part = "action"
    ax0 = X(ACTION_X0_PX)
    act = Profile([(ax0, A_TOP - 3.0), (ax0 + 3.0, A_TOP), (BX0, A_TOP), (BX0, A_BOT + 2.0), (BX0 - 2.0, A_BOT),
                   (ax0 + 1.0, A_BOT), (ax0 - 1.0, A_BOT + 3.0)])
    m.fill(act.solid(lambda x: AW, A_ROUND), act.bounds(AW), action_c, size=1.0, edge=SURF)
    plate_c = smudged(steel(STEEL_ACTION + 22, RUST_FROM, 143, scuffs=0.66))
    for side in (-1, 1):
        y0, y1 = (AW - 0.5, AW + 0.5) if side > 0 else (-AW - 0.5, -AW + 0.5)
        m.box(ax0 + 1.5, BX0 - 3.0, y0, y1, A_BOT + 2.5, A_TOP - 3.0, plate_c, size=SURF, keep=True)
        for sx, sz in ((ax0 + 4.0, A_BOT + 5.0), (BX0 - 6.0, A_TOP - 5.5)):
            m.box(sx - 0.5, sx + 0.5, side * (AW + 0.5) - 0.5, side * (AW + 0.5) + 0.5, sz - 0.5, sz + 0.5,
                  (150, 148, 144), size=SURF)
    # two outside hammers, standing on the action's back top, their spurs back toward the thumb
    hp = Profile([(ax0 + 4.0 + dx, A_TOP - 1.0 + dz) for dx, dz in HAMMER])
    hsolid = hp.solid(lambda x: 1.0, 0.4)
    for yc in (-HAMMER_Y, HAMMER_Y):
        m.fill(lambda x, y, z, yc=yc: hsolid(x, y - yc, z), (ax0 - 1.0, ax0 + 8.0, yc - 1.5, yc + 1.5, A_TOP - 2.0,
               A_TOP + 7.0), small_c, size=SURF, keep=True)

    # --- top lever between the hammers (swings aside when the gun breaks open)
    m.part = "lever"
    m.box(ax0 + 7.0, BX0 - 4.0, -1.5, 1.5, A_TOP - 1.0, A_TOP + 1.0, small_c, size=SURF)
    m.box(ax0 + 6.0, ax0 + 8.0, -2.0, 2.0, A_TOP, A_TOP + 1.5, small_c, size=SURF)

    # --- trigger guard and two triggers
    guard(m, ax0 + 0.5, X(20.6), A_BOT, A_BOT - GUARD_DROP, small_c, w=GUARD_W, bar=GUARD_BAR)
    for px in TRIGGERS_PX:
        blade(m, X(px), A_BOT, A_BOT - GUARD_DROP + GUARD_BAR + 0.8, mix((96, 98, 104), BRIGHT_METAL, 0.35),
              lean=0.35)

    # --- grip: a slim curved wooden pistol grip, its grain along the wrist, a steel butt cap
    m.part = "grip"
    gp = Profile([(X(c), Z(r)) for c, r in GRIP_PX])

    def hw(x):
        t = min(max((x - X(2.8)) / (X(12.0) - X(2.8)), 0.0), 1.0)
        return (GRIP_W_BUTT + (GRIP_W_WRIST - GRIP_W_BUTT) * t) / 2
    gwood = smudged(wood(97, along=(-0.55, -0.83), shade=WOOD_SHADE, grime_from=0.7))
    cap_z = Z(CAP_ROW)

    def grip_col(x, y, z):
        return small_c(x, y, z) if z < cap_z else gwood(x, y, z)
    m.fill(gp.solid(hw, GRIP_ROUND), gp.bounds(GRIP_W_BUTT / 2), grip_col, size=1.0, edge=SURF, keep=True)

    # --- shells (hidden unless a reload frame shows them), one per chamber, each built parked above it
    shell(m, "shell_r", BX0, -BY, ZC + park_z(1), False)
    shell(m, "shell_l", BX0, BY, ZC + park_z(2), False)

    # --- muzzle flashes, two per barrel
    flashes(m, MZ + 0.5, ZC, my=-BY, scale=FLASH_SCALE, names=("flash_ra", "flash_rb"), first=0)
    flashes(m, MZ + 0.5, ZC, my=BY, scale=FLASH_SCALE, names=("flash_la", "flash_lb"), first=2)
    return m
