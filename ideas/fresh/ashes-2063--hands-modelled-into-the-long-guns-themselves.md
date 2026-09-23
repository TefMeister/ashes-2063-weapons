# Hands modelled into the long guns themselves

Order: 5
From: mod-ideas `games/ashes-2063.md` (<https://github.com/TefMeister/mod-ideas/blob/main/games/ashes-2063.md>), copied 2026-09-23

`[raw]` · `[looks doable]` — *not tried*

> "that should maybe make it easier, and also hands can be added to the weapon models themselves this way"

Since 2026-09-20 a long gun in Ashes is **always** held with two hands — no button, no checks (see
[Two hands on long guns](#two-hands-on-long-guns)). That fixes where both hands are relative to the
gun, so the hands can simply be **part of the gun model** instead of being tracked separately.

**Which file gets what, in Tefa's order** (their correction, 2026-09-20 — an earlier note here had it
the wrong way round):

> "the static version is the one that you build first, only the weapon moving parts move, the animated
> weapons would also have hands, just hands, no wrists, be a part of the animation, inserting shells into
> the gun and changing the mag."

1. **`_static` first.** The gun body never moves; only its own parts do — slide, shells, magazine. This
   is the base, and the version somebody else could put their own hands on.
2. **The full animation carries the hands.** Just hands, no wrists, animated as part of the reload:
   feeding shells into the shotgun, pulling a magazine out and pushing a new one in.

**What it'd take:** hand shapes in the pixel style, animated alongside each weapon's existing
animations. No engine work and no tracking work — it is modelling only, and the timings already exist,
read tic-for-tic from the game's own weapon files. Steadier-looking than free-floating hands, because
nothing can drift apart from the gun.

⚠️ Not tried. Nothing about how it looks has been checked in the headset.
