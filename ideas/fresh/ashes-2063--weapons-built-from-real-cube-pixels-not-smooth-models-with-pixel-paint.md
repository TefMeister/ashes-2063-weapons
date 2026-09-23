# Weapons built from real cube pixels, not smooth models with pixel paint

Order: 0
From: mod-ideas `games/ashes-2063.md` (<https://github.com/TefMeister/mod-ideas/blob/main/games/ashes-2063.md>), copied 2026-09-23

`[raw]` · `[already works]` for the pistol — *built 2026-09-22 as a true cube model (no diagonal edges anywhere), put in the game and worn: "it shoots and looks so good in VR" [verified-live 2026-09-22, n=1]. The other weapons are not done yet.*

> "can these pixels be textured? so for the player is does look like the weapon is made out of 3d
> cube pixels? for instance this trigger guard has the pixelated colour on it, but it still has
> smooth diagonal edges. what i mean is, can it look like actually pixelated like i drew some boxes
> on here, so it would look old-style pixelated in the player's hand."

Verbatim record, with the two annotated screenshots described: [`inbox/2026-09-20d-ashes-weapons-made-of-real-3d-pixels.md`](../inbox/2026-09-20d-ashes-weapons-made-of-real-3d-pixels.md)

**Asked as a question, not a request to build** — *"please don't start this work"*. Nothing started.

**The heart of it is the OUTLINE.** Our weapons already have pixel-snapped colours, and that is the
part that works. A texture cannot change a silhouette, so a smooth polygon curve stays a smooth
polygon curve however blocky the paint on it is. The trigger guard in the screenshot is exactly
that: chunky colour, smooth edge.

**Four routes, cheapest first. None has been tried.**

1. **Snap the existing models onto a cube grid.** Blender's Remesh modifier has a Blocks mode that
   does precisely this, and it is one modifier and one setting per part — an hour to SEE, not a
   project. ⚠️ Two things would need watching, and both could sink it: it eats small detail (the
   trigger, the front sight, the thin barrel band are all smaller than a sensible cube), and the
   polygon count rises steeply, which matters because the game's model format stores every frame of
   every animation as its own full set of vertices.
2. **Build from cubes in the first place** — change the kit so each part is generated as a grid of
   cubes rather than as boxes and swept tubes. Most faithful to the picture Tefa drew, most control
   over what survives at small sizes, and by far the most work: it is a rewrite of the model scripts
   rather than a setting.
3. **Render the weapon at a low resolution and blow it up.** This is what actually makes old games
   look old, and it pixelates the OUTLINE and the colours together, which no amount of modelling
   does. It needs engine work — but this is a game we build our own engine for, so it is not out of
   reach. ⚠️ Entirely unexamined; it is named here because it may get closer to the wanted look for
   less work than route 2, not because it is known to be possible.
4. **A shader trick** — ruled out. Nothing drawn on a surface can change where that surface ends.

**Worth saying plainly:** the reason the gun looks wrong next to the rest of Ashes may not only be
its edges. Everything else in that game is low-resolution sprite art, and our weapon is a crisp 3D
model in the middle of it. Route 3 addresses that mismatch directly; routes 1 and 2 address only
the weapon.

---
