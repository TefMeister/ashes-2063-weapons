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

## VR test: NOT WORN YET
Desktop-folder launcher: **`Play Ashes 2063 VR (shotgun + two-handed test).bat`** in `C:\NonSteam\Ashes 2063 VR`.
It loads our engine build plus the shotgun, the revolver and the lantern.

Two separate things are being tested at once, and they fail in different ways:

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
