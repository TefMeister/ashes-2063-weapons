# Ashes 2063: the Master Blaster flamethrower (pickup LAUPA, in hand NAPALM*), forge cube version.
# From the pictures: a black barrel ending in a silver ring nozzle with a pilot light, a round dark wooden body, two
# copper fuel tanks underneath with a red valve wheel, a braided hose, a big pressure gauge at the back facing the
# player (red-yellow-green dial), and a red hose looping round the back.
import math

from _common import Model, fp, BLACK, STEEL, STEEL_HI, DARK, WOOD_DK, BRASS, SCREW, COPPER, mul, mix

WOOD_BROWN = (98, 62, 40)
VALVE_RED = (190, 30, 26)
HOSE_RED = (150, 30, 40)
GAUGE_FACE = (226, 222, 210)
Z_AXIS = 12.0


def build():
    m = Model("ashes_master_blaster")
    # the pieces each have a name, so each can be picked on its own in Blender (Tefa, 2026-10-23)
    m.pivot = (40, 0, 0)
    # the wooden body: a fat round barrel-shaped piece
    m.cyl(30, 82, 0, Z_AXIS, 9.0, fp.wood(WOOD_BROWN, mul(WOOD_DK, 0.8)), edge=0.5)
    for x in (32, 56, 79):                                              # iron hoops round it
        m.cyl(x, x + 2.5, 0, Z_AXIS, 9.5, fp.metal(BLACK), edge=0.25)
    m.part = 'barrel'
    # the barrel and the nozzle
    m.cyl(82, 150, 0, Z_AXIS + 2, 3.2, fp.metal(BLACK), edge=0.25)
    m.part = 'nozzle'
    m.cyl(140, 150, 0, Z_AXIS + 2, 3.8, fp.metal(STEEL), edge=0.25)
    for x in (142, 145, 148):
        m.cyl(x, x + 1, 0, Z_AXIS + 2, 4.3, fp.metal(STEEL_HI), size=0.25, edge=0.25)
    m.cyl(150, 155, 0, Z_AXIS + 2, 2.8, fp.metal((210, 160, 90)), edge=0.25)
    m.cyl(153, 156, 0, Z_AXIS + 2, 1.6, None, edge=0.25, carve=True)
    m.cyl(146, 152, 0, Z_AXIS - 3.5, 1.2, fp.metal(BRASS), edge=0.25)                      # pilot light
    m.ball(152.5, 0, Z_AXIS - 3.5, 1.0, (255, 170, 60), edge=0.25)
    m.part = 'gas_line'
    # a black top tube from the body to the nozzle (the gas line)
    m.cyl(60, 140, 0, Z_AXIS + 8.5, 1.6, fp.metal(BLACK), edge=0.25)
    for x in (90, 120):
        m.cbox(x, x + 3, 3.0, Z_AXIS + 2, Z_AXIS + 9, fp.metal(BLACK), size=0.5)
    m.part = 'tanks'
    # two copper tanks underneath, side by side, with caps
    for y in (-4.5, 4.5):
        m.cyl(36, 86, y, Z_AXIS - 12, 4.4, fp.metal(COPPER), edge=0.5)
        m.ball(86, y, Z_AXIS - 12, 4.4, fp.metal(COPPER), edge=0.5)
        m.ball(36, y, Z_AXIS - 12, 4.4, fp.metal(COPPER), edge=0.5)
        for x in (48, 74):
            m.cyl(x, x + 1.5, y, Z_AXIS - 12, 4.8, fp.metal(BLACK), size=0.25, edge=0.25)
    m.part = 'valve'
    # the red valve wheel on the right, on a short stem
    for k in range(24):
        a = k * math.tau / 24
        m.box(62 + math.cos(a) * 4, 62 + math.cos(a) * 4 + 0.75, -12.5, -11.5, Z_AXIS - 4 + math.sin(a) * 4,
              Z_AXIS - 4 + math.sin(a) * 4 + 0.75, VALVE_RED, size=0.25)
    for k in range(4):
        a = k * math.pi / 2 + 0.4
        for t in range(8):
            r = t * 0.5
            m.box(62 + math.cos(a) * r, 62 + math.cos(a) * r + 0.5, -12.5, -12.0, Z_AXIS - 4 + math.sin(a) * r,
                  Z_AXIS - 4 + math.sin(a) * r + 0.5, VALVE_RED, size=0.25)
    m.box(61, 63, -12, -8, Z_AXIS - 5, Z_AXIS - 3, fp.metal(STEEL), size=0.5)
    m.part = 'hose'
    # the braided hose from the tanks up to the barrel, on the left
    for i in range(40):
        t = i / 39
        x, z = 84 + t * 20, Z_AXIS - 10 + math.sin(t * math.pi) * 6 + t * 10
        m.ball(x, 7.5, z, 1.6, fp.metal(mix(STEEL, (60, 60, 64), (i % 2) * 0.6)), edge=0.25)
    m.part = 'grip'
    # the pistol grip and trigger under the body, and a front handle
    m.cprism([(36, 4), (30, -4), (26, -18), (34, -20), (40, -8), (44, 4)], 7.0, fp.metal(BLACK), bevel=1.5,
             edge=0.5)
    m.part = 'guard'
    fp.guard(m, 40, 54, -8, 2, fp.metal(BLACK))
    fp.trigger(m, 47, 3, fp.metal(STEEL_HI), length=6)
    m.part = 'gauge'
    # the pressure gauge at the back, facing the player: a brass rim, a white face with a coloured arc and a needle
    m.cyl(18, 30, 0, Z_AXIS + 4, 7.5, fp.metal(BRASS), edge=0.25)
    m.cyl(17.5, 18, 0, Z_AXIS + 4, 6.5, GAUGE_FACE, size=0.25, edge=0.25)
    for k in range(18):
        a = math.pi * 1.15 - k * (math.pi * 1.3) / 17
        col = (200, 40, 30) if k < 5 else ((220, 190, 40) if k < 11 else (60, 170, 60))
        m.box(17.25, 17.5, math.cos(a) * 5.2, math.cos(a) * 5.2 + 0.5, Z_AXIS + 4 + math.sin(a) * 5.2,
              Z_AXIS + 4 + math.sin(a) * 5.2 + 0.5, col, size=0.25)
    for t in range(9):
        m.box(17.25, 17.5, -t * 0.4, -t * 0.4 + 0.25, Z_AXIS + 4 + t * 0.45, Z_AXIS + 4.25 + t * 0.45, DARK,
              size=0.25)
    m.part = 'red_hose'
    # the red hose looping round the back from the tanks to the gauge
    for i in range(60):
        a = math.pi * 0.5 + i / 59 * math.pi
        m.ball(26 + math.cos(a) * 14, -6.5, Z_AXIS - 6 + math.sin(a) * 12, 1.5, HOSE_RED, edge=0.25)
    for side in ('+y', '-y'):
        m.screw(34, Z_AXIS + 6, side, SCREW, kind='hex')
        m.screw(78, Z_AXIS + 6, side, SCREW, kind='hex')
        m.decal(["####.#..#", "#....##.#", "###..#.##", "#....#..#", "####.#..#"], 46, Z_AXIS + 3, side,
                (200, 170, 90), mode='paint')
    m.wear_edges(0.35, (200, 180, 150))
    m.scratches('+y', (82, 150, Z_AXIS, Z_AXIS + 5), 10, 91)
    m.crack(50, Z_AXIS, '+y', 14, 92, heading=0.1)
    m.grime(0.25, 93)
    return m
