# The left hand is recognised in the game

Order: 2
From: mod-ideas `games/ashes-2063.md` (<https://github.com/TefMeister/mod-ideas/blob/main/games/ashes-2063.md>), copied 2026-09-23

`[considered]` · `[looks doable]` — *built 2026-09-17 in our own copy of the VR program, and it WORKS in the headset: the lantern follows the left hand and lights the world*

> "somehow get the left hand recognized, even if it means changing the vr program - if it does we contact whoever
> is needed if we can't just start tweaking it on our own."

Right now only the weapon hand exists for the game; the left controller does nothing a mod can see.

**What it'd take:** a change to **GZDoomVR itself**, not just a mod. Reading its code on 2026-09-17 showed the engine
hands mods the weapon hand's position and aim, but **nothing about the off hand**. It only uses the left controller
internally, to steer walking. `[inferred-static]` The good news is that GZDoomVR is **open source** (hh79/gzdoomvr), so
there are two honest routes:
- **Tweak it ourselves:** a small engine change that passes the left hand's position and angle to mods, then the lantern
  (or a second gun) can follow it. We would build and ship our own copy of the engine.
- **Ask upstream:** propose that change to hh79, the author, so everyone's mods get it. Slower, but no fork to maintain.

⚠️ **Not checked against a build.** Nobody has compiled GZDoomVR yet, so how big "small" really is remains unknown.
Related, already in the weapons notes: a left-hand lantern that follows the controller needs exactly this.
