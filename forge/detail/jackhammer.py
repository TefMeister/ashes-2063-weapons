# Ashes 2063: the JackHammer, DETAILED (2026-11-02). Gun only: the body rig's hands dock onto the grip and the handle.
#
# Game look (in-hand hamm1-4, pickup JHAMA): a petrol-engine gun: a red finned engine block at the back under a
# silver shroud with vent slots, a yellow two-character label on a black plate, a black tubular roll cage with a taped
# carry handle over it, a fuel cap, and in front a long black six-barrel drum on a frame.
# Real-life detail (refs/jackhammer.md; Wacker Neuson BH petrol breaker, demolition hammers, a site compressor): the
# engine's finned cylinder with the spark plug, its boot and lead, a muffler under a holed heat shield with the exhaust
# outlet, pull-start with a red T handle, fuel cap with a breather, choke lever, air filter cover with a clip,
# throttle cable from the trigger, warning stickers, bolts everywhere.
# Wasteland layer: the drum is driven by a bicycle chain from the engine, under a bent sheet guard held by wire; a
# clear fuel line patched with tape, soot round the exhaust, rust and oil stains, the carry handle wrapped in rag.
import math

from _common import Model, fp, wl, BLACK, STEEL, STEEL_HI, DARK, mul, mix

ENGINE_RED = (160, 46, 32)
ENGINE_DK = (96, 26, 18)
SHROUD = (196, 194, 188)
LABEL = (200, 170, 40)
ALU = (150, 150, 150)
Z_AXIS = 14.0


def tube_path(m, pts, r, col, y=0.0):
    for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
        n = int(max(abs(x1 - x0), abs(z1 - z0)) * 2) + 1
        for i in range(n + 1):
            t = i / n
            m.ball(x0 + (x1 - x0) * t, y, z0 + (z1 - z0) * t, r, col, size=0.25, edge=0.25)


def build():
    m = Model("ashes_jackhammer_detail")
    m.pivot = (40, 0, 0)

    # ---------------------------------------------------------------- engine block, fins, shroud
    m.part = 'engine'
    m.cbox(0, 52, 22.0, -4, 26, fp.metal(ENGINE_RED), bevel=3.0, bevel_x=1.5, edge=0.5)
    for x in range(3, 50, 3):                                                              # cooling fins
        for side in ('+y', '-y'):
            m.groove([(x, -2), (x, 18)], side, depth=3, width=2, dark=0.42)
    m.recolour(lambda x, y, z: z < 2, ENGINE_DK)
    m.part = 'shroud'
    m.cbox(4, 48, 18.0, 20, 30, fp.metal(SHROUD), bevel=2.0, edge=0.25)
    for x in range(10, 44, 5):
        for y in (-6, 2):
            m.groove([(x, y), (x + 3, y)], '+z', depth=2, width=4, dark=0.3)
    for side in ('+y', '-y'):
        for x in (6.0, 46.0):
            m.screw(x, 25.0, side, mul(STEEL, 0.8), kind='hex')
    m.part = 'label'
    m.box(12, 40, 11, 11.5, 6, 15, fp.metal(DARK), size=0.25)
    glyph = ["#######", "#.....#", "#######", "#.....#", "#######", "..#.#..", "##...##"]
    m.decal(glyph, 16, 14, '+y', LABEL, dot=2, mode='raise')
    m.decal(glyph, 27, 14, '+y', LABEL, dot=2, mode='raise')
    m.part = 'warning'                                                                    # a faded warning sticker
    m.box(14, 22, -11.25, -11.0, 8, 13, (200, 176, 60), size=0.25)
    m.box(16, 20, -11.5, -11.25, 9.5, 11.5, (40, 36, 30), size=0.25)

    # ---------------------------------------------------------------- the engine's parts: plug, muffler, starter
    m.part = 'spark_plug'
    m.cyl(-13.5, -11.0, 18, 16, 1.0, fp.metal((230, 226, 214)), axis='y', size=0.25, edge=0.25)   # white insulator
    m.cyl(-16.0, -13.5, 18, 16, 1.6, fp.metal(BLACK), axis='y', size=0.25, edge=0.25)             # its rubber boot
    tube_path(m, [(18, 17.5), (14, 21), (8, 22)], 0.5, (30, 30, 30), y=-15.5)                     # the lead
    m.part = 'muffler'
    m.box(14, 40, -14.5, -11.0, -3.0, 6.0, fp.metal((70, 66, 60)), size=0.5, edge=0.25)     # muffler body
    m.box(13, 41, -15.25, -14.5, -3.5, 6.5, fp.metal(ALU), size=0.25)                        # heat shield
    for x in range(15, 40, 3):
        for z in (-1.5, 2.0, 5.0):
            m.box(x, x + 1, -15.5, -14.25, z, z + 1, None, size=0.25, carve=True)          # its holes
    m.cyl(40, 44, -13.0, 1.5, 1.1, fp.metal((60, 54, 48)), size=0.25, edge=0.25)            # exhaust outlet
    m.cyl(43.5, 44.1, -13.0, 1.5, 0.7, None, size=0.25, edge=0.25, carve=True)
    m.part = 'starter'
    m.cyl(-4, 0, 0, 12, 4.0, fp.metal(BLACK), edge=0.25)
    for k in range(8):                                                                    # recoil cover ribs
        a = k * math.tau / 8
        m.box(-4.25, -4.0, math.cos(a) * 3 - 0.25, math.cos(a) * 3 + 0.25, 12 + math.sin(a) * 3 - 0.25,
              12 + math.sin(a) * 3 + 0.25, mul(BLACK, 1.6), size=0.25)
    m.cbox(-7, -4.5, 6.0, 10.5, 13.5, fp.metal((170, 34, 28)), size=0.25)                   # red T handle
    m.box(-5.0, -4.0, -0.25, 0.25, 11.75, 12.25, (210, 200, 180), size=0.25)                 # the rope
    m.part = 'fuel_cap'
    m.cyl(-4, -1, 30, 0, 2.6, fp.metal(DARK), axis='z', size=0.25, edge=0.25)
    for k in range(10):
        a = k * math.tau / 10
        m.box(30 + math.cos(a) * 2.6 - 0.25, 30 + math.cos(a) * 2.6 + 0.25, math.sin(a) * 2.6 - 0.25,
              math.sin(a) * 2.6 + 0.25, -4, -1.25, mul(DARK, 1.8), size=0.25)
    m.box(29.75, 30.25, -0.25, 0.25, -4.25, -4.0, (10, 10, 10), size=0.25)                    # breather hole
    m.part = 'air_filter'
    m.box(2, 12, 11.0, 15.0, 0.0, 14.0, fp.metal((40, 42, 44)), size=0.5, edge=0.25)
    m.box(6.5, 7.5, 15.0, 15.5, 5.0, 9.0, fp.metal(STEEL), size=0.25)                        # clip
    m.box(11.5, 13.5, 13.0, 15.5, 15.0, 16.0, fp.metal((190, 40, 30)), size=0.25)            # choke lever

    # ---------------------------------------------------------------- roll cage and carry handle
    m.part = 'cage'
    tube_path(m, [(-2, -2), (-4, 30), (4, 40), (44, 40), (54, 30), (54, 20)], 1.6, fp.metal(BLACK))
    for y in (-11.5, 11.5):
        for i in range(53):
            m.ball(i, y, -3, 1.4, fp.metal(BLACK), size=0.25, edge=0.25)
    for x in (4.0, 44.0):                                                                 # welds where tubes meet
        for y in (-1.0, 1.0):
            m.ball(x, y, 40.0, 1.9, fp.metal((60, 56, 50)), size=0.25, edge=0.25)
    m.part = 'handle'
    m.cyl(10, 38, 0, 40, 2.4, fp.metal((110, 80, 60)), edge=0.25)
    wl.cloth(m, 'x', 11.0, 37.0, (9, 39, -4, 4, 36, 44), col=wl.CLOTH_GREY, seed=801, part='handle', layers=2,
             tail=(36.5, 2.5, 38.5, 5.0, 1.0))

    # ---------------------------------------------------------------- drum frame, drum, the chain drive
    m.part = 'frame'
    m.cbox(52, 66, 14.0, 2, 26, fp.metal(BLACK), bevel=2.0, edge=0.25)
    for side in ('+y', '-y'):
        for x, z in ((56, 6), (62, 22), (56, 22), (62, 6)):
            m.bolt(x, z, side, mul(STEEL, 0.75))
    m.part = 'drum'
    for k in range(6):
        a = k * math.pi / 3
        yc, zc = math.cos(a) * 4.5, Z_AXIS + math.sin(a) * 4.5
        m.cyl(66, 150, yc, zc, 1.7, fp.metal(mul(BLACK, 1.2)), edge=0.25)
        m.cyl(146, 151, yc, zc, 0.9, None, size=0.25, edge=0.25, carve=True)
    for x in (80, 112, 144):
        m.cyl(x, x + 3, 0, Z_AXIS, 7.0, fp.metal(BLACK), size=0.5, edge=0.25)
        for k in range(6):                                                                 # bolts on the plates
            a = k * math.pi / 3 + math.pi / 6
            m.box(x + 2.75, x + 3.25, math.cos(a) * 6.2 - 0.4, math.cos(a) * 6.2 + 0.4,
                  Z_AXIS + math.sin(a) * 6.2 - 0.4, Z_AXIS + math.sin(a) * 6.2 + 0.4, fp.metal(STEEL), size=0.25)
    m.cyl(66, 150, 0, Z_AXIS, 2.0, fp.metal(STEEL), edge=0.25)
    m.part = 'chain'
    for x in (50.0, 70.0):                                                                 # sprockets
        m.cyl(-8.5, -7.5, x, 6.0 if x < 60 else Z_AXIS, 3.0 if x < 60 else 4.0, fp.metal(STEEL), axis='y',
              size=0.25, edge=0.25)
    for i in range(60):                                                                    # the bicycle chain
        t = i / 59
        x = 50 + t * 20
        z1 = 6.0 + 3.0 + (Z_AXIS + 4.0 - 9.0) * t
        z0 = 6.0 - 3.0 + (Z_AXIS - 4.0 - 3.0) * t
        c = fp.metal(mul(STEEL, 0.7 if i % 2 else 0.95))(x, 0, 0)
        m.put(x, -8.75, z1, c, 0.25, 'chain')
        m.put(x, -8.75, z0, c, 0.25, 'chain')
    m.part = 'chain_guard'
    m.prism([(48, 0), (48, 10), (72, Z_AXIS + 6), (74, Z_AXIS - 6), (52, 1)], -10.5, -10.0,
            fp.metal((96, 100, 96)), size=0.25)                                           # bent sheet guard
    wl.wire_wrap(m, 60.0, 62.0, -9.0, 9.0, 1.2, pitch=0.6, col=wl.WIRE_STEEL, part='chain_guard')

    # ---------------------------------------------------------------- grip, trigger, throttle cable, fuel line
    m.part = 'grip'
    m.cprism([(36, -4), (30, -10), (28, -26), (38, -28), (42, -14), (48, -4)], 8.0, fp.metal(BLACK), bevel=1.5,
             edge=0.25)
    wl.tape(m, 'z', -22.0, -15.0, (26, 44, -5, 5, -22.5, -14.5), col=wl.DUCT, seed=802, part='tape')
    m.part = 'trigger'
    fp.trigger(m, 46, -4, fp.metal((190, 40, 30)), length=8, curve=1.0)
    m.part = 'throttle_cable'
    tube_path(m, [(47, -5), (50, -1), (52, 4), (50, 10)], 0.5, (24, 24, 26), y=4.5)
    m.part = 'fuel_line'
    tube_path(m, [(30, -3.5), (24, -6), (14, -6), (8, -2)], 0.7, (190, 170, 110), y=6.0)    # clear, fuel inside
    wl.tape(m, 'x', 18.0, 20.0, (17, 21, 4.5, 7.5, -7.5, -4.5), col=wl.DUCT_BLACK, seed=803, part='tape')

    # ---------------------------------------------------------------- the wasteland layer
    wl.soot(m, (38, 46, -16, -10, -2, 5), amount=0.75, seed=804)
    wl.soot(m, (146, 151, -7, 7, Z_AXIS - 7, Z_AXIS + 7), amount=0.6, seed=805)
    wl.rust(m, (52, 151, -9, 9, Z_AXIS - 9, Z_AXIS + 9), amount=0.25, seed=806, pits=0.03)
    wl.rust(m, (-4, 56, -14, 14, -5, 42), amount=0.15, seed=807,
            region=lambda x, y, z: abs(y) > 10 or z > 38)                                 # on the cage
    m.recolour(lambda x, y, z: z < 0 and 18 < x < 40 and abs(y) < 11 and (int(x * 2) + int(y * 2)) % 7 == 0,
               (30, 24, 18))                                                               # oil drips
    for side in ('+y', '-y'):
        m.scratches(side, (0, 52, -2, 24), 6, 808 if side == '+y' else 809, lighten=1.2, length=(2.0, 5.0))
    m.crack(20, 4, '-y', 10, 810, heading=0.6)
    wl.cavity(m)
    m.wear_edges(0.15, (220, 200, 180))
    m.grime(0.25, 811, col=(40, 30, 20))
    wl.simplify(m, step=14, block=1.5)
    return m
