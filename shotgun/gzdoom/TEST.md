# Shotgun in GZDoomVR: in-game tests

Two builds from `kit/gz_export.py -- gz_shotgun.py [flat|vr]`:
- `Ashes2063_shotgun3d_test.pk3`: **flat screen** (model space = the Blender first-person camera, eye at the origin).
- `Ashes2063_shotgun3d_VR_test.pk3`: **VR** (real size, 100 units per metre, hung off the controller),
  and it also carries the ZScript that switches **two-handed aiming** on while the shotgun is out.

Each holds one MD3 and the baked `shotgun.png`, plus `modeldef.shotgun` mapping the game's shotgun
sprite frames (GRIZ, GRIF, GRIP, GRIR) to model frames.

**Only 42 model frames are shipped, not all 194.** Sprite letters can only ever name about forty
poses, and a 194-frame MD3 of a gun this size would be tens of megabytes in the repo for frames
nothing can display. `SHOOT_FRAMES` / `RELOAD_FRAMES` in `kit/gz_shotgun.py` are that list;
`gz_export.py` refuses to build if a sprite points at a frame not in it.

## Flat test: PASSED 2026-09-19 `[verified-live 2026-09-19, n=3 launches]`
Run unattended: `python tools/shotgun_test.py <tag>` (launches windowed into MAP01, gives the gun and
ammo, selects slot 3, captures idle / one shot / a reload from dry, quits). Evidence: `evidence-2026-09-19/`.
- The 3D shotgun replaces the sprite, fires with a flash and a kick, **throws the spent shell out to the
  right**, works the pump, and plays the full dry reload with the gun tipped over.

### ⚠️ Two things went wrong first, and both are worth knowing
1. **`Model <name>` in MODELDEF is the ACTOR CLASS, not the file name.** It only looked like the file
   name for the revolver because Ashes happens to call that actor `revolver`. This gun's class is
   **`pumpaction`**. With the wrong name the game shows the flat sprite and prints **no error at all**
   (`evidence-2026-09-19/wrong-actor-name-shows-the-sprite.png`). `ACTOR_CLASS` in `kit/gz_shotgun.py`.
2. **The Blender first-person camera has to match the game's field of view, or the gun is a monster.**
   The kit's 32 mm default is about 61°, GZDoom plays at about 90°. At 32 mm the butt of a gun this long
   sits *outside* the Blender frame while the game still draws it, filling half the screen. The shotgun
   uses **18 mm** (`VIEW_LENS_SG`), so what the Blender files show is what the game shows. This does not
   apply to the revolver, which is short enough that it never showed.

**Not judged yet (needs Tefa's eye):** whether the resting pose, angle and size look right. Nothing here
is measured against the game — `REST_LOC` / `REST_ROT` were pushed around until the framing resembled
Tefa's screenshots `[hypothesis]`.

## VR test: first wear 2026-09-19 — three things wrong, all three fixed, NOT re-worn

Tefa, first wear `[reported 2026-09-19, n=1 wear]`: *"shotgun is aiming below where the red dot is
showing, i cannot put away the lantern in my left hand and i could not two hand the shotgun, how does
that work even, i just instinctively pressed LG to grip it"*.

1. **Aiming low — a real bug, found and measured.** A VR build expresses every frame relative to the
   root's **rest** pose, and the exporter took that from frame 1 of the first animation. The revolver's
   frame 1 is the gun at rest, so it was right by luck. The shotgun's frame 1 is the **shot**, already
   kicked nose-up — so the whole gun came out **8.61° nose-down** in the hand and 2 cm out of place
   `[verified-numerically 2026-09-19: rest space measured from frame 1 vs frame 30, -8.61° against 0.00°]`.
   Fixed with `REST_FRAME` in `kit/gz_shotgun.py`, which names the neutral pose. Every future weapon
   whose first animation frame is not the rest pose needs this line.
2. **The lantern could not be put away — our bug, not the game's.** The left-hand lantern handler drew
   the lantern whenever the off hand was tracked, full stop. It now follows the game's own
   `lightlit` flag, so **the lantern key puts it away and takes it out again**, and the off hand is
   free. Rebuilt `Ashes2063_lefthand_lantern_test.pk3`.
3. **There is no grip button — and Tefa asked for one, which is the right answer.** Their words, same
   wear: *"can there be a grip button LG to hold on to a forend of the weapon? just holding my hand at
   the wooden bit did nothing"*. ⚠️ **"Did nothing" is the finding to carry forward**, and that wear
   could not explain it: the gun was 8.61° nose-down, so lining the hand up with the *visible* fore-end
   lined it up with the wrong direction, and the lantern was stuck in that hand too. Both are fixed, so
   a plain re-wear is worth one minute first. The button itself is **mod-side only, no engine rebuild** —
   ZScript reads `players[n].cmd.buttons`, so `TwoHandedAim` becomes "a long gun is out, the off hand is
   tracked, **and** the grip action is held", with the grip bound to `+user2` in the VR controls menu.
   A held button is a far better signal than geometry, because it says *I am gripping it* outright; the
   two unmeasured guard numbers then stop deciding anything.

   As things stand today there is nothing to press: Nothing to press: you just bring your left hand up
   to where the fore-end is and hold the controllers as if holding a real rifle. The engine watches the
   two hands. It needs them a minimum distance apart *and* roughly in line with the way the gun points,
   or it refuses and leaves aiming exactly as it is. **The visible sign that it worked is the red laser
   dot moving** to line up with the barrel when the off hand comes up.

Desktop-folder launcher: **`Play Ashes 2063 VR (shotgun + two-handed test).bat`** in `C:\NonSteam\Ashes 2063 VR`.
It loads our engine build plus the shotgun, the revolver and the lantern, and **drops you straight into
the first level already holding the shotgun with 40 spare shells** (`+map MAP01 +give pumpaction
+give shotgunammo 40`), so there is nothing to find first. It is weapon slot 3 if you switch away.
`[verified-live 2026-09-19, n=1 flat launch: the gun is in hand at spawn and slot 3 selects it]`

In the normal game the pump shotgun is a pickup in the levels; the console route is `give pumpaction`
then `give shotgunammo 40`, which is awkward in a headset — hence the launcher doing it.

Two separate things are being tested at once, and they fail in different ways. **Watch the red dot**:
it is the only thing that shows whether the two-handed aim took, because the gun is drawn on the
weapon hand either way.

| You see | Means / fix |
| --- | --- |
| 3D shotgun in your right hand, sensible size | the model works; judge comfort and look |
| Gun too high/low/forward in the hand | `GRIP` and the `VR_NUDGE_*` numbers in `kit/gz_shotgun.py`, or MODELDEF `Offset x y z` in cm for a no-rebuild try |
| Gun huge or tiny | `UNITS_PER_M` in `kit/gz_shotgun.py` (100 = real size) |
| Flat sprite instead of the model | the pk3 was not loaded (check the `-file` path) |
| **Shots land where the barrel points when you hold it with both hands** | the two-handed aim works — then tune the two sliders |
| **Shots land where they did before** | the engine refused. Turn on Options → VR Options → "Two-handed aim: print why" and read which guard said no |
| Shots consistently high or low by a fixed amount | the pitch sign; see `engine/TWO-HANDED-AIM.md` |

The guard limits are **sliders in Options → VR Options** ("Least hand separation", "Most disagreement"),
so they can be tuned while wearing the headset — no rebuild. Both defaults (8 map units, 55°) are
guesses `[hypothesis]`.

⚠️ The VR pk3 **only works on our engine build** (`gzdoomvr-tefa`): its ZScript names `TwoHandedAim`,
which the stock engine does not have, and a missing field stops the game from starting rather than
degrading quietly. The flat pk3 has no ZScript and runs on either.
