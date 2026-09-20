# Hands for the Ashes 2063 shotgun. Same space as the gun: +Y is the muzzle, +Z up,
# +X the gun's right side.
#
# Tefa's brief (2026-09-20), with the Duke-style screenshot they sent as the reference:
#   "add hands to the gun ... black gloves, the line where the wrist should start, make that
#    black leather as well and fingers showing so like half-gloves"
#
# So: fingerless leather gloves. The glove covers the back of the hand, the palm and the first
# knuckle of every finger; the middle and tip segments are bare skin. The wrist ends in a raised
# leather cuff, which is the "line where the wrist should start" - it is built a size larger than
# the wrist so it reads as a band rather than as a colour change.
#
# TWO hands, and they are NOT the same kind of object:
#   SG_HandRight  the trigger hand, parented to SG_Root. It rides the gun.
#   SG_HandLeft   the support hand, parented to SG_PUMP. It has to rack back and forward WITH
#                 the forend, or the hand slides through the wood on every shot.
#
# Everything is unlit (the standing rule), chunky, and built from boxes, so it matches the gun
# it sits on rather than looking like a smooth modern model dropped into a pixel game.

# ---- the look --------------------------------------------------------------
# Black leather, near the stock's black but flatter and a touch warmer, so glove and stock do
# not read as one lump where the hand meets the wood.
GLOVE_STOPS = [(0.0, (0.020, 0.019, 0.021)), (0.45, (0.031, 0.030, 0.033)),
               (0.82, (0.046, 0.044, 0.048))]
# The cuff is darker, not lighter: a lighter band would read as a highlight rather than leather.
CUFF_STOPS = [(0.0, (0.012, 0.011, 0.013)), (0.50, (0.022, 0.021, 0.024)),
              (0.85, (0.034, 0.032, 0.036))]
# Bare fingers. Ashes lives in a dark, dusty palette, so this is a weathered tan rather than a
# clean skin tone - bright pink fingers would be the first thing the eye lands on.
SKIN_STOPS = [(0.0, (0.196, 0.116, 0.094)), (0.42, (0.268, 0.170, 0.140)),
              (0.80, (0.340, 0.230, 0.194))]

BLOCK_HAND = 0.0032          # texture pixel size; a shade finer than the gun's 0.0045


# Past the cuff: a dark sleeve. It exists so the CUFF has something to be a line BETWEEN -- a
# black band against black leather is not a line, it is a smudge.
SLEEVE_STOPS = [(0.0, (0.026, 0.025, 0.023)), (0.48, (0.037, 0.036, 0.033)),
                (0.85, (0.050, 0.048, 0.043))]


def hand_materials():
    """The materials the hands use. Slot order matters: GLOVE, CUFF, SKIN, SLEEVE."""
    m_glove = pixel_mat("SG_GloveLeather", GLOVE_STOPS, metal=0.05, rough=0.72,
                        wear=0.22, block=BLOCK_HAND)
    m_cuff = pixel_mat("SG_GloveCuff", CUFF_STOPS, metal=0.05, rough=0.80,
                       wear=0.18, block=0.0026)
    m_skin = pixel_mat("SG_Skin", SKIN_STOPS, metal=0.0, rough=0.78,
                       wear=0.10, block=BLOCK_HAND)
    m_sleeve = pixel_mat("SG_Sleeve", SLEEVE_STOPS, metal=0.0, rough=0.9,
                         wear=0.30, block=0.0038)
    return [m_glove, m_cuff, m_skin, m_sleeve]


GLOVE, CUFF, SKIN, SLEEVE = 0, 1, 2, 3


def _finger(p, centre_xz, y, radii, thetas, seg, mats, width):
    """One finger, wrapped around a grip.

    A finger holding something round is an ARC, so it is placed as one: each segment sits at an
    angle around the grip's cross-section, tangent to it. The first version chained boxes by
    stepping and rotating each in turn, and every finger ended up standing off the top of the
    forend like a row of bricks - the drift compounds and there is nothing holding the tip near
    the wood.

    centre_xz  (x, z) of the grip's cross-section
    radii      (rx, rz) of that cross-section, already including the thickness of the finger
    thetas     one angle per segment, in degrees, measured from +X and going anticlockwise
               (so 90 is the top, 180 is the -X side, -90 is underneath)
    seg        (length, thickness) of one segment
    mats       one material per segment, base to tip
    width      how wide the finger is along the gun
    """
    cx, cz = centre_xz
    rx, rz = radii
    length, thick = seg
    for th, mat in zip(thetas, mats):
        a = math.radians(th)
        x = cx + rx * math.cos(a)
        z = cz + rz * math.sin(a)
        # Long axis along the tangent: a box whose length lies on X, turned about Y by -(th+90).
        p.box((length, width, thick), (x, y, z), mat, rot=(0, -(a + math.pi / 2), 0))


def build_hands(root, pump, coll, S):
    """Build both hands. S is the settings module's namespace (globals()), for the gun numbers."""
    MATS = hand_materials()
    MAG_Z, REC_Z = S["MAG_Z"], S["REC_Z"]
    PUMP_PIVOT = S["PUMP_PIVOT"]

    # =======================================================================
    # LEFT HAND - the support hand, wrapped around the pump.
    # Palm against the left face of the forend, fingers over the top and curling down the far
    # side, thumb lying along the left. This is the pose the reference screenshot shows.
    # =======================================================================
    FORE_HALF_W = 0.0235                 # the ribs are the widest part of the forend
    MAG_Z_R = 0.0275                     # half-height of the forend
    CY = 0.326                           # middle of the grip, along the forend

    p = Part()

    # back of the hand, flat against the left side of the wood
    p.box((0.013, 0.058, 0.040), (-(FORE_HALF_W + 0.009), CY - 0.006, MAG_Z + 0.002), GLOVE,
          rot=(0, 0.06, 0))

    # Four fingers wrapping the forend: knuckles on the left, over the top, tips curling down the
    # far side. Spacing is close to the rib pitch so they sit in the grooves.
    # Knuckle gloved, middle and tip bare - that is what makes it a half-glove.
    FORE_R = (FORE_HALF_W + 0.007, MAG_Z_R + 0.007)
    for i, fy in enumerate((CY - 0.030, CY - 0.009, CY + 0.012, CY + 0.033)):
        reach = (0, -5, -11, -18)[i]                 # little finger does not get as far round
        _finger(p, (0.0, MAG_Z), fy, FORE_R,
                (172 + reach * 0.3, 112 + reach * 0.7, 40 + reach),
                (0.022, 0.012), (GLOVE, SKIN, SKIN),
                width=(0.015, 0.015, 0.014, 0.012)[i])   # gaps between them, or it is one slab

    # thumb, lying forward along the left of the forend
    p.box((0.015, 0.032, 0.017), (-(FORE_HALF_W + 0.012), CY + 0.040, MAG_Z + 0.010),
          GLOVE, rot=(-0.30, 0, 0.10))
    p.box((0.013, 0.024, 0.015), (-(FORE_HALF_W + 0.013), CY + 0.066, MAG_Z + 0.019),
          SKIN, rot=(-0.45, 0, 0.10))

    # wrist, then the CUFF, then the forearm running off toward the player
    p.box((0.025, 0.030, 0.034), (-0.046, CY - 0.050, MAG_Z - 0.014), GLOVE,
          rot=(0.32, 0, -0.26))
    p.box((0.032, 0.015, 0.041), (-0.056, CY - 0.074, MAG_Z - 0.030), CUFF,
          rot=(0.32, 0, -0.26))                       # <-- the line where the wrist starts
    p.box((0.027, 0.085, 0.034), (-0.074, CY - 0.122, MAG_Z - 0.060), SLEEVE,
          rot=(0.32, 0, -0.26))

    # Built at the PUMP's origin and parented to it, so it racks back and forward with the wood.
    hand_l = p.build("SG_HandLeft", MATS, pivot=PUMP_PIVOT, parent=pump, coll=coll)
    hand_l.location = (0, 0, 0)

    # =======================================================================
    # RIGHT HAND - the trigger hand, wrapped around the wrist of the stock.
    # Palm on the gun's right, three fingers curling under the stock, index forward on the
    # trigger, thumb over the top.
    # =======================================================================
    GX = 0.018                           # right face of the stock wrist
    GY = -0.046                          # middle of the grip
    GZ = REC_Z - 0.004

    p = Part()

    # back of the hand
    p.box((0.013, 0.054, 0.046), (GX + 0.008, GY - 0.012, GZ + 0.002), GLOVE, rot=(0.10, -0.05, 0))

    # index finger, reaching forward to the trigger
    p.box((0.026, 0.022, 0.014), (GX + 0.002, GY + 0.055, GZ - 0.004), GLOVE, rot=(0, 0.20, 0))
    p.box((0.016, 0.026, 0.012), (GX - 0.012, GY + 0.082, GZ - 0.013), SKIN, rot=(0.20, 0.55, 0))

    # Three fingers curling under the wrist of the stock: knuckles on the right, round the
    # bottom, tips coming up the far side. Angles run negative because they go UNDER.
    GRIP_R = (0.017 + 0.007, 0.025 + 0.007)
    for i, fy in enumerate((GY + 0.028, GY + 0.006, GY - 0.016)):
        reach = (0, -7, -16)[i]
        _finger(p, (0.0, REC_Z), fy, GRIP_R,
                (-30 + reach * 0.3, -92 + reach * 0.7, -158 - reach),
                (0.022, 0.012), (GLOVE, SKIN, SKIN),
                width=(0.016, 0.015, 0.013)[i])

    # thumb over the top of the stock wrist
    p.box((0.016, 0.034, 0.017), (GX + 0.004, GY + 0.018, GZ + 0.030), GLOVE,
          rot=(0.25, 0, -0.18))
    p.box((0.014, 0.025, 0.015), (GX - 0.008, GY + 0.042, GZ + 0.036), SKIN,
          rot=(0.40, 0, -0.30))

    # wrist, CUFF, forearm
    p.box((0.027, 0.032, 0.036), (GX + 0.020, GY - 0.048, GZ - 0.018), GLOVE,
          rot=(-0.28, 0, 0.22))
    p.box((0.034, 0.016, 0.043), (GX + 0.030, GY - 0.074, GZ - 0.034), CUFF,
          rot=(-0.28, 0, 0.22))                       # <-- the line where the wrist starts
    p.box((0.029, 0.090, 0.036), (GX + 0.048, GY - 0.124, GZ - 0.064), SLEEVE,
          rot=(-0.28, 0, 0.22))

    hand_r = p.build("SG_HandRight", MATS, parent=root, coll=coll)

    return hand_l, hand_r
