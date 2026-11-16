"""The Meshy guns' look without a Meshy model (2026-11-16, Keeper PC). Runs in Blender, inside a forge design.

Tefa, on the revolver, with no Meshy model of it made: "can you do it without the meshy picture and see what you can
come up with?" What the Meshy guns get from their Meshy texture is painted here by rule instead: worn steel whose
brightness drifts in big and small patches, rust in a few large orange-to-brown patches with a dark rim, light scuffs,
wood with grain along the part. As on the Meshy guns (meshy_kit.Meshy.col) every cube's colour is half its own and half
that of its BLOCK-sized block, so it reads blocky, not smooth; the shape is built by the design in the kit's mixed
cubes (sharp_kit.start), as theirs is."""
import math

from sharp_kit import noise
from forge import mix
from meshy_kit import BLOCK, SMUDGE, WOOD

RUST_BRIGHT, RUST_BROWN, RUST_RIM = (150, 62, 30), (92, 44, 26), (50, 34, 28)
SCUFF = (150, 148, 144)
RUST_EDGE = 0.05                 # how far past its threshold the rust noise must go to be full rust
GRIME = (40, 30, 24)


def smudged(tex):
    """col(x, y, z) from a paint tex(x, y, z) -> (r, g, b) 0-255: half the block's colour, half the cube's own."""
    def col(x, y, z):
        bx, bz = (math.floor(x / BLOCK) + 0.5) * BLOCK, (math.floor(z / BLOCK) + 0.5) * BLOCK
        blk, own = tex(bx, y, bz), tex(x, y, z)
        return tuple(int(round(min(255.0, max(0.0, blk[i] * (1 - SMUDGE) + own[i] * SMUDGE)))) for i in range(3))
    return col


def steel(base, rust_from, seed, scuffs=0.74, more_rust=None):
    """Worn steel `base` bright (0-255). Rust where its noise passes rust_from (0.5 half the part, 0.7 almost none);
    more_rust(x, y, z) -> a number added to that noise (the underside, the flutes)."""
    def tex(x, y, z):
        big, mid = noise(x, y, z, seed, 11.0), noise(x, y, z, seed + 1, 4.0)
        lum = base * (0.72 + 0.56 * big) * (0.86 + 0.28 * mid)
        c = (lum * 0.98, lum, lum * 1.05)
        if noise(x, y, z, seed + 2, 1.6) > scuffs and mid > 0.45:
            c = mix(c, SCUFF, 0.45)
        r = 0.6 * noise(x, y, z, seed + 5, 10.0) + 0.4 * noise(x, y, z, seed + 6, 3.5)
        if more_rust:
            r += more_rust(x, y, z)
        t = (r - rust_from) / RUST_EDGE
        if t <= 0:
            return c
        rust = mix(RUST_BROWN, RUST_BRIGHT, noise(x, y, z, seed + 7, 5.0))
        if t < 0.5:
            return mix(c, RUST_RIM, t * 1.6)             # the dark rim round a patch
        return mix(RUST_RIM, rust, min(1.0, (t - 0.5) * 2.0))
    return tex


def wood(seed, along=(1.0, 0.0), shade=1.0, grime_from=0.66):
    """Wood in the shotgun's plank colours (meshy_kit.WOOD), its grain running along `along` (x, z); dark handled
    patches where the grime noise passes grime_from."""
    n = math.hypot(*along)
    ax, az = along[0] / n, along[1] / n

    def tex(x, y, z):
        u, v = x * ax + z * az, -x * az + z * ax         # along the grain, across it
        g = 0.65 * noise(u / 6.0, y, v * 1.6, seed, 1.0) + 0.35 * noise(u, y * 2, v * 3, seed + 1, 2.0)
        i = max(0.0, min(len(WOOD) - 1.001, (g - 0.2) / 0.6 * (len(WOOD) - 1)))
        a, f = int(i), i - int(i)
        c = tuple((WOOD[a][k] * (1 - f) + WOOD[a + 1][k] * f) * shade for k in range(3))
        d = (noise(x, y, z, seed + 3, 7.0) - grime_from) / 0.08
        return mix(c, GRIME, min(0.7, d)) if d > 0 else c
    return tex
