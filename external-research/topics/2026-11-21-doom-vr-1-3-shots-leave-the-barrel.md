# Doom VR 1.3.0: "shots leave the barrel", and the public report of how they went wrong

**Status:** 🆕 new · **Priority:** low to medium. A follow-up to the 2026-11-11 topic
(`2026-11-11-doom-vr-openxr-engine-and-modelswapper-hand-reloads.md`). It bears on one board row, "SHOTS FROM THE GUN,
NOT SEEN YET" (our `vrfixes/zscript.txt` lifts player missiles and casing spawners to the gun's height in VR), by
giving the wear a sharper checklist. Nothing here replaces our engine.

## What is public

Read online on 2026-11-21 through the GitHub viewer and API; nothing downloaded. All `[reported 2026-11-21]`.

- **GameOrDie007's Doom VR** (UZDoom-based PC VR engine with its own OpenXR layer) moved on twice since the last pass:
  **v1.3.0 (2026-11-17)** adds co-op in VR (2 to 8 players), players with different gun styles in one game, and
  Doom Infinite support; among its fixes, **"Shots leave the barrel"**: shots *"could start near your body or a few
  feet to the side. They now leave the gun you see, along its barrel"*. **v1.3.1 (2026-11-19)** only fixes a co-op door
  desync. The commit for 1.3.0 describes it as "shots from the gun on every level".
- **The report behind the fix, Doom VR issue #2** (Moondiesel, 2026-11-10, still open; confirmed by vicdanny1975 on
  2026-11-15): in Doom and Brutal Doom, projectiles left from near the player's body, not the front of the gun, so
  shots hit nearby walls and door frames; **the origin wandered and was not fixed by recentring; sometimes it was three
  or four feet to the left or right**. Most visible with Brutal Doom's tracers.
- **A side effect worth knowing** (aidangken-cell, same issue, 2026-11-16): the engine's "bullets come from gun" option
  stopped the drift, but then **the shots followed where the controller points, not where the gun model points**, so
  the gun had to be tipped up to hit straight; the poster suggests turning the model down about 10 degrees through the
  weapon-rotate setting.
- Quiet since the last pass: hh79/gzdoomvr (last release gvr4.13.2.2, 2025-01-24; last push 2025-10-18); UZDoom has
  only an automatic preview build (5.1.0-pre, 2026-11-20) after 5.0.3 (2026-09-23).

## What it means here

- These are two separate faults any Doom-engine VR build can have, and our row's wear can test both
  `[inferred-static]`: (1) **where the shot starts**: with the head turned away from the gun and after walking a
  while (the public report says the origin drifted and recentring did not help), do the casings and the napalm gun's
  fire still leave the barrel?; (2) **where the shot goes**: does a shot land where the 3D MODEL's barrel points, or
  where the controller points? If the gun model is posed with a pitch offset from the controller (our shotgun poses
  and hand fits are tuned by eye), the two differ by that offset.
- Our bullets are hitscan (no tracers, board row of 2026-10-19), so (2) is only visible from bullet puffs on a wall;
  a close wall and a single shot is the cheapest way to see it.

## Concrete next step

Add the two checks above to the "SHOTS FROM THE GUN" wear: one shot at a near wall with the head turned 45 degrees
away, then one after walking and turning; compare the puff with where the barrel points.

## Sources

- GameOrDie007, *Doom VR* releases v1.3.0 (2026-11-17) and v1.3.1 (2026-11-19) and commit list,
  <https://github.com/GameOrDie007/Doom-VR/releases> (read 2026-11-21).
- Moondiesel, vicdanny1975, aidangken-cell: *Doom VR* issue #2, "Projectiles not firing from weapon",
  <https://github.com/GameOrDie007/Doom-VR/issues/2> (read 2026-11-21).
- UZDoom releases, <https://github.com/UZDoom/UZDoom/releases>; hh79, *gzdoomvr* releases,
  <https://github.com/hh79/gzdoomvr/releases> (read 2026-11-21).
