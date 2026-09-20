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
3. **There was nothing to press — and now there is nothing to press for a different reason.** Tefa's
   words that wear: *"can there be a grip button LG to hold on to a forend of the weapon? just holding
   my hand at the wooden bit did nothing"*. ⚠️ **"Did nothing" is the finding that mattered**, and that
   wear could not explain it: the gun was 8.61° nose-down, so lining the hand up with the *visible*
   fore-end lined it up with the wrong direction, and the lantern was stuck in that hand too.

   A grip button was built on 2026-09-20 (`+user2`, with an alias so the VR grip still runs as well),
   and then **demoted the same day**, because Tefa asked for something simpler: *"i would actually like
   … for there to be no proximity at all, that when choosing a long weapon, it automatically switches to
   two handing. that in this game there is no way to fire a long rifle or shotgun with one hand"*.

## How it works now (2026-09-20): a long gun is ALWAYS two-handed

Nothing is conditional. Pick up any two-handed weapon and the shot follows the line from the off hand
to the weapon hand, every tic, for as long as both controllers are tracked.

- **Mod side** (`kit/gz_shotgun.py`, VR pk3 only): `TwoHandedAim` is on whenever the weapon is one of
  `LONG_GUNS` and the off hand is tracked. The ten Ashes weapons on that list are matched by class
  name, so a name that does not exist in the loaded game is simply never true.
- **Engine side**: the two guards are turned off for this setup — `vr_two_handed_min_sep 0` and
  `vr_two_handed_max_disagree 180`, set both in `gzdoomvr-tefashes-vr-3dtest.ini` and on the
  launcher's command line. The engine can now only refuse if the two hands are in exactly the same
  place, which is a divide-by-zero guard, not a judgement about how you are standing.
- ⚠️ **The price, and it is the deal that was asked for:** if the off hand drops to your side, the shot
  follows *that* line. There is no one-handed shot with a long gun.
- **The grip button is still there and does nothing** until `tefa_grip_required 1` is set, which makes
  two-handing deliberate again. The VR off-hand grip (`LShoulder`) is bound to `+tefagrip`, an alias
  that runs **and** grips, so nothing was taken away.
- **`tefa_grip_debug 1`** says where things stand the moment it is switched on, and then only when it
  changes: `two-handed aim: ON`, or `off (not a two-handed weapon)` / `off (off hand not tracked)` /
  `off (grip not held)`.

**Checked flat, on the real build, 2026-09-20** `[verified-live 2026-09-20, n=4 launches]`: the engine
starts with the new ZScript, both settings read back their new defaults, the pump shotgun is recognised
as a long gun, and the only thing left between it and two-handed aiming is a second tracked hand —
which is exactly what the headset adds. The probe is `tools/grip_test.py`, and it also proves the
button path end to end (`grip: HELD` / `grip: let go`). ⚠️ **The aim itself is still unworn.**

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
| **Shots land where they did before** | the override never ran. Turn on `tefa_grip_debug 1` — it names what is missing — and Options → VR Options → "Two-handed aim: print why" for the engine's side |
| Shots consistently high or low by a fixed amount | the pitch sign; see `engine/TWO-HANDED-AIM.md` |

The guard limits are still **sliders in Options → VR Options** ("Least hand separation", "Most
disagreement"), but they are set out of the way (0 and 180) so they decide nothing. Turning them back up
is how you would re-introduce a "your hands must look like a rifle hold" rule, if the unconditional
version ever feels wrong.

⚠️ The VR pk3 **only works on our engine build** (`gzdoomvr-tefa`): its ZScript names `TwoHandedAim`,
which the stock engine does not have, and a missing field stops the game from starting rather than
degrading quietly. The flat pk3 has no ZScript and runs on either.

## Wear 2, 2026-09-20 — the GUN does not turn. That is the next job.

Tefa, wearing the always-two-handed build `[reported 2026-09-20, n=1 wear]`:

> "the gun still only follows the right hand, left hand is not steering the front of the shotgun while
> the right hand is the anchor."

⚠️ **This is not a bug in what was built — it is the half that was never built.** Everything so far
changes only **where the shot goes**. The gun MODEL is still drawn hanging off the weapon controller,
exactly as it always was, so it looks one-handed however the shot behaves. `TWO-HANDED-AIM.md` says as
much ("the red dot is the only visible sign"), and that was the wrong thing to ship first: what a person
sees in a headset is the gun, not the bullet.

**What is still unknown:** whether the shots themselves followed the hand line. Nobody was watching the
red dot, and there is no reason to ask for another wear just to find out — the visible fix below makes
it obvious either way.

**What the next change is, in one line:** the weapon model must be *drawn* along the line from the off
hand to the weapon hand, with the weapon hand as the anchor — i.e. the same maths that already decides
the shot, applied to the render pose as well.

Where it goes, for whoever picks this up: `gl_openvr.cpp` → `OpenVRMode::GetWeaponTransform()` (line
~1089), which today is just the weapon controller's own matrix (`GetHandTransformEx`). It needs the same
`tha::decide()` result the aim block at ~1687 already computes: keep the translation (the grip stays in
the trigger hand), replace the forward axis with the hand-to-hand direction, and keep roll about that
axis so the gun does not spin. ⚠️ Both are rebuilds of the engine, so this is home-PC work, but it needs
no headset until it is built.

⚠️ A second thing to decide when it is built: the model's own rest pose points along its local forward,
and the current VR fit (`GRIP`, `VR_NUDGE_*` in `kit/gz_shotgun.py`) was tuned against the controller's
tilt. Turning the gun to the hand line may want those re-tuned `[hypothesis]`.

---

## Built 2026-09-20 late — the gun IS now drawn along the hand line. Not worn.

The change above is done. Tefa confirmed the shape first: *"the back of the gun has to be locked to
the right controller as the anchor … left controller moves the front end, so it doesn't really matter
how far the controllers are apart."* That is what was built — rear hand keeps the position and the
twist of the wrist, off hand sets where the barrel points, distance ignored.

⚠️ **One thing in the plan above changed on contact with the code.** It said to keep the translation
and take the forward axis from `tha::decide()`. The shipped version builds the whole weapon **pose**
instead, in OpenVR's own tracking space, before any of the engine's scaling — because the world
transform is scaled non-uniformly (pixelstretch, and a flipped Z), so its axes are not a clean set of
directions to rotate. `engine/two_handed_pose.h` does that, and the shot deliberately stays on the
untouched one-handed matrix so the hand line is not applied twice.
`[inferred-static 2026-09-20, read from GetHandTransformEx and MapAttackDir]`

**What to look at in the headset, and what each outcome points at:**
[`engine/TWO-HANDED-DRAW.md`](../../engine/TWO-HANDED-DRAW.md). If it is worse than before,
`vr_two_handed_draw 0` in the console puts it straight back.

The second thing to decide is still open: the VR fit (`GRIP`, `VR_NUDGE_*` in `kit/gz_shotgun.py`)
was tuned against the controller's own tilt, and the two-handed pose no longer applies that tilt on
top. If the gun sits in the wrong place — as opposed to pointing the wrong way — that is where it
gets fixed `[hypothesis]`.
