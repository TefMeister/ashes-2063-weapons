# Weapons that are the sprite from the front and 3D from the side

Order: 1
From: the ideas repo, `games/ashes-2063.md` (<https://github.com/TefMeister/mod-ideas/blob/main/games/ashes-2063.md>), copied 2026-11-03

`[raw]` · `[looks doable]` — *not checked against GZDoom VR or our CubeKit; nothing built*

> "is there a way to have 3d sprite weapons for ashes, not voxel but somehow still look like sprites but also be 3d somehow"

Verbatim record: [`inbox/2026-11-03-ashes-3d-sprite-weapons-not-voxel.md`](../inbox/2026-11-03-ashes-3d-sprite-weapons-not-voxel.md).
Asked as a question (2026-11-03). A different look from the cube-pixel guns above and from the fine-detail rebuild of
2026-11-02, so it is Tefa's choice which look Ashes keeps.

**Routes, closest to the idea first. None tried.**

1. **Sprite-faced model:** a simple 3D shape built from the sprite's own outline (front and side), with the sprite's
   pixels painted on it as seen from where the gun is held, sharp pixels, no smoothing. From the usual view it IS the
   sprite; turned, it has depth. The unseen sides are filled from the sprite's own colours.
2. **Thick cut-out:** the sprite pushed out a few centimetres, its edge pixels running round the sides. Cheapest, but
   from the side it reads as a cardboard cut-out.
3. **Sprite with a depth map:** a flat card whose shader fakes depth pixel by pixel. Sprite-perfect head-on; needs a
   custom shader in GZDoom VR, and it breaks at steep angles.
4. **A 3D model drawn through a pixel filter:** real 3D, shown at sprite resolution. Risk: the pixels crawl as the
   gun moves, and differ between the eyes in VR.

**What it'd take:** route 1 in Blender (the CubeKit pipeline already pixel-snaps colours), one gun first, worn in the
headset; route 2 as a one-evening test beside it to compare.
