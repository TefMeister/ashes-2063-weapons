"""The heavy MQ11, step 2 (2026-11-16, Developer PC): the Meshy heavy machine gun's parts built onto the MQ11's plan.

Tefa: "take the MQ11 as a reference for it and build the parts into it so it looks like a heavy model of the
submachine gun, parts like the barrel, body, grip, trigger and guard, sights and the stock (which is way too short and
wide) can hopefully still be usable". Step 1 (meshy_heavy_parts.py) cut the heavy gun into parts; Tefa then chose:
- the magazine as on the MQ11: the heavy gun's angled pistol grip out, the MQ11's grip with its magazine in;
- the heavy stock kept, 1.6 times longer and 0.6 times as wide, lifted level with the body;
- (the silenced MQ11 gets the heavy suppressor, a bit darker: meshy_mq11_silenced.py).
The heavy gun is built at HEAVY_M (its receiver then as long as the MQ11's) and turned level (Meshy made it 10 degrees
nose-up). Everything is rebuilt from the two Meshy models through meshy_kit.transplant, in mixed cubes.
Measured numbers below are in the step-1 model's cubes ("h", 0.74 m), scaled here by K.
    python blender-cubekit/forge_make.py <out> <out> meshy_heavy_mq11.py
"""
import os

from meshy_kit import Meshy, fill_between, transplant
import sharp_kit

HERE = os.path.dirname(os.path.abspath(__file__))
HEAVY_GLB = os.path.join(HERE, "meshy", "heavy_mg_meshy_2026-11-15.glb")
MQ11_GLB = os.path.join(HERE, "meshy", "mq11_meshy_2026-11-15.glb")
NAME = "meshy_heavy_mq11"
H_M, HEAVY_M, MQ11_M = 0.74, 0.85, 0.59
K = HEAVY_M / H_M                # step-1 cubes to this model's
TILT_DEG = 10.0
TOP = -17.0                      # every Meshy gun's top (meshy_kit.TOP_M in cubes); scaling keeps it


def hx(x):
    return x * K


def hz(z):
    return TOP + (z - TOP) * K


# the heavy gun (step-1 cubes)
STOCK_X1, STOCK_Z1, STOCK_REAR_X1 = 42, -62, 21          # the stock: behind 42 and below -62, or behind 21
STOCK_LONG, STOCK_NARROW = 1.6, 0.6
STOCK_LIFT = hz(-40) - hz(-79)   # its middle (z -79) up to the bore line (z -40)
GRIP_X = (64, 104)               # the heavy pistol grip, left out ...
HINGE_X = (42, 64)               # the old stock hinge hanging under the body behind the grip: left out too (the stock
                                 # moved up, it would hang there on its own)
STOCK_OVERLAP = 4.0              # the stretched stock reaches this far further forward, so it meets the body
GRIP_Z1 = -63                    # ... below the body
SHIFT = hx(STOCK_X1) * (STOCK_LONG - 1)    # everything in front of the stock moves back by what the stock grew
# the MQ11 (its own cubes at MQ11_M): grip and magazine, under its body
MQ_GRIP_X, MQ_BODY_BOTTOM = (88, 117), -49
MQ_GRIP_DEST_X1 = hx(104) + SHIFT + 16       # its front at the heavy trigger guard's back post (the guard's
                                             # region starts 18 cubes ahead of the post: first try left a gap)
MQ_DX = MQ_GRIP_DEST_X1 - MQ_GRIP_X[1]
MQ_DZ = hz(-64) - MQ_BODY_BOTTOM             # its top on the heavy body's underside


def build():
    gh = Meshy(HEAVY_GLB, HEAVY_M, tilt_deg=TILT_DEG)
    gq = Meshy(MQ11_GLB, MQ11_M)
    m = sharp_kit.start(NAME)
    lo, hi = gh.lo, gh.hi
    ybox = (lo.y - 2, hi.y + 2)

    def is_stock(x, y, z):
        return (x < hx(STOCK_X1) and z < hz(STOCK_Z1)) or x < hx(STOCK_REAR_X1)

    def is_heavy_grip(x, y, z):
        return (hx(GRIP_X[0]) <= x < hx(GRIP_X[1]) or hx(HINGE_X[0]) <= x < hx(HINGE_X[1])) and z < hz(GRIP_Z1)

    # the body, barrel, suppressor, sights, trigger guard: the heavy gun moved back by SHIFT
    transplant(m, gh, (SHIFT - 1, hi.x + SHIFT + 1, *ybox, lo.z - 1, hi.z + 1),
               lambda x, y, z: (x - SHIFT, y, z),
               region=lambda x, y, z: not is_stock(x, y, z) and not is_heavy_grip(x, y, z), part="body")
    # the stock: longer, slimmer, lifted
    transplant(m, gh, (STOCK_OVERLAP - 1, hx(STOCK_X1) * STOCK_LONG + STOCK_OVERLAP + 1, ybox[0] * STOCK_NARROW,
                       ybox[1] * STOCK_NARROW, lo.z + STOCK_LIFT - 1, hi.z + 1),
               lambda x, y, z: ((x - STOCK_OVERLAP) / STOCK_LONG, y / STOCK_NARROW, z - STOCK_LIFT), region=is_stock,
               part="stock")
    # the MQ11's grip with its magazine, under the heavy body
    ql, qh = gq.lo, gq.hi
    transplant(m, gq, (MQ_GRIP_X[0] + MQ_DX - 1, MQ_GRIP_X[1] + MQ_DX + 1, ql.y - 1, qh.y + 1, ql.z + MQ_DZ - 1,
                       MQ_BODY_BOTTOM + MQ_DZ + 1),
               lambda x, y, z: (x - MQ_DX, y, z - MQ_DZ),
               region=lambda x, y, z: MQ_GRIP_X[0] <= x < MQ_GRIP_X[1] and z < MQ_BODY_BOTTOM, part="grip")
    box = (-2, int(hi.x + SHIFT) + 3, int(lo.y) - 2, int(hi.y) + 3, int(ql.z + MQ_DZ) - 2, int(hi.z) + 3)
    for axis in (1, 2):
        fill_between(m, box, axis=axis, max_gap=3)
    return m
