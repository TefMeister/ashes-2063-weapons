"""The JackHammer in the smudge-cube look, round 2 (2026-11-07, home PC). A forge design: forge_make.py builds it.

Tefa on round 1 (smudge_jackhammer.py, kept), beside the shotgun: "the jackhammer needs to be 4x as wide". The engine,
its base and the front housing go WIDEN x wider (88 and 80 main cubes, about 30 and 27 cm); the parts on their sides
(cover plates, vents, starter cover, screws, seam) follow the new sides; the round parts (rod, collar, pipe, hoop,
D-handle) keep their size.

Round 1's own note:

Tefa, after the shotgun's round 8 settled the look: "ok the jackhammer next, please make it look like a bulky 3d
chainsaw first, in the colouring and style of this shotgun for all going forward". The SHAPE is the sharp JackHammer's
(sharp_jackhammer.py, kept: Tefa 2026-11-05, "a thick and bulky body like a chainsaw and the tip needs to be a thick
iron blunt rod to repel enemies"): a ribbed engine at the back with a vented side cover, a rope-wrapped hoop handle over
it, a base with hazard stripes, a front housing with a round starter cover, seam and screws, a D-handle on top (the
right hand), a pipe under it on two brackets, and a thick blunt iron rod out of a collar. The LOOK is the shotgun's
(smudge_kit.py): the game picture (JHAMA0, 40 x 23, read at run time) on every cube, half smudged; robust edges (the
body roundings smaller than the sharp one's), square-cut round parts in quarter cubes, carved scratches, matte.
Against the sharp one also: the rod ends in a flat-faced striking head (no mushroom curve), cut square like the
shotgun's muzzle.
Moving parts (as make_job_jackhammer.py): the rod ("chisel") hammers out and back, the throttle lever ("trigger").
"""
import math

from sharp_kit import Profile, SURF, body, darken, plates, screws, seam, start
from sharp_settings import JCK_S
from smudge_kit import SCRATCH_LEN_WOOD, Smudge, carve_scratches, round_fill

NAME = "smudge_jackhammer_v2"
SIDE_SPRITE = "Sprites/Weapons/JHAMA0.png"
WIDEN = 4.0                            # Tefa: "4x as wide"
ENG_W, HOUSE_W = 22.0 * WIDEN, 20.0 * WIDEN   # main cubes wide (round 1: the sharp one's 22 and 20)
ENG_ROUND, BASE_ROUND, HOUSE_ROUND = 1.5, 1.5, 2.0   # edge roundings (sharp one: 2.5, 2.0, 4.5: too soft for this look)
ROD_R = 4.5
HEAD_R, HEAD_LEN = 5.5, 4.0            # the flat-faced striking head on the rod
METAL = ("engine", "housing", "pipe", "chisel")


def build():
    sm = Smudge(SIDE_SPRITE, JCK_S)
    X, Z, pc = sm.X, sm.Z, sm.pc
    m = start(NAME)
    HZ = Z(14.4)                                     # the housing's (and rod's) axis

    # --- engine: ribbed at the back (cut cooling fins), a vented cover on each side further forward
    body(m, "engine", [(X(0.4), Z(6.2)), (X(6.8), Z(5.8)), (X(12.0), Z(6.2)), (X(12.0), Z(17.2)), (X(0.4), Z(17.2))],
         ENG_W / 2, ENG_ROUND, pc)
    for k in range(int((Z(6.6) - Z(16.6)) / 2.5)):
        z = Z(16.6) + 1.5 + k * 2.5
        m.box(X(0.4) - 1, X(6.6), -ENG_W, ENG_W, z, z + 1.0, None, size=SURF, carve=True)
    darken(m, lambda x, y, z: x < X(6.6) and (int(math.floor((z - Z(16.6) - 1.5) * 2)) % 5) in (0, 1), 0.7)
    plates(m, X(6.8), X(11.6), Z(15.8), Z(7.2), ENG_W / 2, pc)
    for k in range(4):
        z = Z(14.8) + k * 3.5
        for side in (-1, 1):
            y0, y1 = (ENG_W / 2 - 0.5, ENG_W / 2 + 1) if side > 0 else (-ENG_W / 2 - 1, -ENG_W / 2 + 0.5)
            m.box(X(7.6), X(10.8), y0, y1, z, z + 1.0, None, size=SURF, carve=True)
    m.part = "engine"
    screws(m, [(X(7.2), Z(7.6)), (X(11.2), Z(7.6)), (X(7.2), Z(15.4)), (X(11.2), Z(15.4))], ENG_W / 2 + 0.5, pc)

    # --- base under the engine (its hazard stripes come from the picture)
    body(m, "engine", [(X(1.0), Z(17.2)), (X(13.0), Z(17.2)), (X(13.0), Z(22.0)), (X(12.0), Z(22.6)),
                       (X(2.0), Z(22.6)), (X(1.0), Z(21.6))], ENG_W / 2, BASE_ROUND, pc, keep=True)

    # --- hoop handle over the engine, rope-wrapped: a round bar along a half ellipse, in quarter cubes
    cx, cz, rx, rz, tr = X(6.8), Z(6.0), X(4.4), X(5.4), 1.8
    m.part = "handle"
    for d in range(0, 181, 3):
        a = math.radians(d)
        px_, pz_ = cx + rx * math.cos(a), cz + rz * math.sin(a)
        round_fill(m.fill, lambda x, y, z, px_=px_, pz_=pz_: (x - px_) ** 2 + y * y + (z - pz_) ** 2 < tr * tr,
                   (px_ - tr - 0.5, px_ + tr + 0.5, -tr - 0.5, tr + 0.5, pz_ - tr - 0.5, pz_ + tr + 0.5), pc,
                   size=1.0, keep=True)

    # --- front housing: seams and screws; a round starter cover on the right side, vents in the left
    body(m, "housing", [(X(12.0), Z(9.6)), (X(35.0), Z(9.6)), (X(37.6), Z(11.4)), (X(37.6), Z(17.4)),
                        (X(36.0), Z(18.8)), (X(12.0), Z(18.8))], HOUSE_W / 2, HOUSE_ROUND, pc, keep=True)
    m.part = "housing"
    scx, scz, sr = X(28.0), Z(14.2), 8.0
    round_fill(m.fill, lambda x, y, z: (x - scx) ** 2 + (z - scz) ** 2 < sr * sr
               and -HOUSE_W / 2 - 1.5 <= y < -HOUSE_W / 2 + 1.0,
               (scx - sr - 1, scx + sr + 1, -HOUSE_W / 2 - 2, -HOUSE_W / 2 + 1, scz - sr - 1, scz + sr + 1), pc,
               size=1.0)
    for k in range(5):
        x = scx - 6.0 + k * 3.0
        m.box(x, x + 1.0, -HOUSE_W / 2 - 2, -HOUSE_W / 2 - 0.5, scz - 5.0, scz + 5.0, None, size=SURF, carve=True)
    for k in range(6):
        x = X(29.0) + k * 2.5
        m.box(x, x + 1.0, HOUSE_W / 2 - 1.0, HOUSE_W / 2 + 1, Z(16.8), Z(11.6), None, size=SURF, carve=True)
    seam(m, X(13.0), X(36.5), Z(17.4), HOUSE_W / 2)
    m.part = "housing"
    screws(m, [(X(14.0 + 4 * k), Z(10.8)) for k in range(5)], HOUSE_W / 2, pc)
    m.part = "housing"
    round_fill(m.cyl, X(37.6), X(38.8), 0.0, HZ, ROD_R + 2.0, pc)                # the collar
    # the pipe under it, on two brackets
    m.part = "pipe"
    round_fill(m.cyl, X(13.0), X(37.0), 0.0, Z(20.4), 3.0, pc)
    for x in (X(16.0), X(33.0)):
        m.box(x, x + 2.0, -2.0, 2.0, Z(20.4), Z(18.8), pc, size=SURF)

    # --- D-handle on top (the right hand holds it: part "grip"); the throttle lever inside
    m.part = "grip"
    hout = Profile([(X(20.0), Z(11.6)), (X(27.2), Z(11.6)), (X(27.2), Z(4.6)), (X(22.0), Z(4.6)), (X(20.0), Z(6.5))])
    hole = Profile([(X(21.6), Z(11.6)), (X(25.6), Z(11.6)), (X(25.6), Z(6.2)), (X(22.6), Z(6.2)), (X(21.6), Z(7.4))])
    hs = hout.solid(lambda x: 2.5, 1.0)
    round_fill(m.fill, lambda x, y, z: hs(x, y, z) and hole.sd(x, z) <= 0, hout.bounds(3.0), pc, size=1.0, keep=True)
    m.part = "trigger"
    m.box(X(24.6), X(25.6), -1.0, 1.0, Z(9.4), Z(6.6), pc, size=SURF)

    # --- the rod (moves): a thick blunt iron bar out of the collar, ending in a flat-faced striking head
    m.part = "chisel"
    round_fill(m.cyl, X(35.0), X(41.4), 0.0, HZ, ROD_R, pc)
    round_fill(m.cyl, X(41.4), X(41.4) + HEAD_LEN, 0.0, HZ, HEAD_R, pc)

    # --- carved scratches, the floor in the cut cube's own colour
    for side, seed in (("+y", 201), ("-y", 202)):
        carve_scratches(m, side, (X(0.8), X(12.0), Z(17.0), Z(6.6)), 6, seed, ("engine",))
        carve_scratches(m, side, (X(12.5), X(37.0), Z(18.4), Z(10.0)), 12, seed + 10, ("housing",))
        carve_scratches(m, side, (X(13.0), X(37.0), Z(20.4) - 2.0, Z(20.4) + 2.0), 3, seed + 20, ("pipe",),
                        along=0.15)
        carve_scratches(m, side, (cx - rx, cx + rx, cz - 1.0, cz + rz), 4, seed + 30, ("handle",),
                        length=SCRATCH_LEN_WOOD, along=1.5)
    carve_scratches(m, "+z", (X(12.5), X(35.0), -HOUSE_W / 2 + 1, HOUSE_W / 2 - 1), 8, 241, ("housing", "engine"),
                    along=0.4)
    carve_scratches(m, "+z", (X(35.0), X(41.4), -ROD_R, ROD_R), 3, 251, ("chisel",), along=0.15)
    return m
