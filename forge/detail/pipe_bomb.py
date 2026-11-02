# Ashes 2063: the pipe bomb, DETAILED (2026-11-02). A thrown item: the body rig's hand holds it.
#
# Game look (in-hand pipe*, pickup PIPEA / ROCKA): a dark steel pipe with threaded end caps, grey clamps, a red light,
# wires, a black fuse hooked out of the top cap that sparks once lit.
# Real-life detail (refs/pipe_bomb.md; threaded pipe and cast cap pictures): a galvanised pipe with its seam line,
# exposed threads between pipe and caps, cast end caps with ribs round them, a hole for the fuse, a green hobby fuse,
# a 9-volt battery with its snap, twisted wires.
# Wasteland layer: duct tape round the middle, two hose clamps, a skull label, a red LED, rust and grime.
import math

from _common import Model, fp, wl, BLACK, STEEL, STEEL_HI, DARK, mul, hash01

PIPE = (112, 114, 118)
LABEL_RED = (176, 28, 24)
FUSE = (52, 110, 60)


def build():
    m = Model("ashes_pipe_bomb_detail")
    m.pivot = (24, 0, 0)

    m.part = 'pipe'
    m.cyl(0, 48, 0, 0, 5.0, fp.rusty(PIPE, (110, 60, 30), 0.25), edge=0.25)
    m.groove([(1, 4.5), (47, 4.5)], '+y', depth=1, dark=0.6)                              # its seam
    for x0 in (3.5, 42.0):                                                              # threads showing
        for k in range(5):
            m.cyl(x0 + k * 0.5, x0 + k * 0.5 + 0.25, 0, 0, 5.1, fp.metal(mul(PIPE, 0.7)), size=0.25, edge=0.25)
    m.part = 'caps'
    for x0, x1 in ((-6, 3.5), (44.5, 54)):
        m.cyl(x0, x1, 0, 0, 6.2, fp.metal(mul(PIPE, 0.8)), size=0.5, edge=0.25)
        for k in range(8):                                                              # cast ribs round each cap
            a = k * math.tau / 8
            m.box(x0 + 0.5, x1 - 0.5, math.cos(a) * 6.3 - 0.4, math.cos(a) * 6.3 + 0.4, math.sin(a) * 6.3 - 0.4,
                  math.sin(a) * 6.3 + 0.4, fp.metal(mul(PIPE, 0.9)), size=0.25)
    m.cyl(-6.5, -5.75, 0, 0, 1.0, None, size=0.25, edge=0.25, carve=True)                 # the fuse hole
    m.part = 'tape'
    wl.tape(m, 'x', 16.0, 34.0, (15, 35, -7, 7, -7, 7), col=wl.DUCT, seed=1101, part='tape')
    m.decal(["..####..", ".######.", "##.##.##", "########", ".#.##.#.", "..####.."], 22, 3.5, '+y', LABEL_RED,
            dot=2, mode='paint')
    m.part = 'clamps'
    for x in (8.0, 38.0):
        wl.hose_clamp(m, x, 0, 0, 5.0, part='clamps')
    m.part = 'fuse'
    for i in range(48):
        t = i / 47
        m.ball(-6.5 - math.sin(t * 2.4) * 8, math.sin(t * 5) * 1.5, t * 14, 0.6, FUSE if i % 3 else mul(FUSE, 0.7),
               size=0.25, edge=0.25)
    m.ball(-6.5 - math.sin(2.4) * 8, math.sin(5) * 1.5, 14.5, 0.8, (255, 170, 60), size=0.25, edge=0.25)
    m.part = 'battery'
    m.cbox(6, 16, 5.0, 5.25, 9.5, fp.metal((40, 40, 46)), size=0.25)                       # a 9 V battery
    m.box(6.25, 15.75, -2.5, 2.5, 7.0, 7.5, (200, 170, 40), size=0.25)                      # its label band
    m.box(15.75, 17.0, -1.5, 1.5, 6.25, 8.5, (24, 24, 26), size=0.25)                       # the snap
    m.part = 'wires'
    for k in range(60):                                                                   # two twisted wires
        x = 17.0 + k * 0.4
        for j, col in enumerate(((190, 40, 30), (30, 30, 34))):
            a = k * 0.8 + j * math.pi
            m.put(x, math.cos(a) * 0.4, 5.5 + abs(math.sin(a)) * 0.25, col, 0.25, "wires")
    m.part = 'led'
    m.ball(42.0, 0, 5.75, 0.8, (255, 40, 30), size=0.25, edge=0.25)
    m.box(41.5, 42.5, -0.25, 0.25, 5.0, 5.5, (30, 30, 30), size=0.25)
    wl.rust(m, (-7, 55, -7, 7, -7, 7), amount=0.22, seed=1102, pits=0.04)
    m.scratches('-y', (0, 48, -4, 4), 6, 1103, lighten=1.2)
    wl.cavity(m)
    m.wear_edges(0.15, (190, 190, 190))
    m.grime(0.28, 1104)
    wl.simplify(m)
    return m
