# Our GZDoomVR changes (engine patch)

A small patch on top of **GZDoomVR** by hh79 (https://github.com/hh79/gzdoomvr, tag `gvr4.13.2.2`, GPL-3.0),
the VR engine Ashes 2063 runs on here. Patch file: `gzdoomvr-gvr4.13.2.2-offhand-stopmotion.patch`.

## What it adds
1. **The off hand, for mods.** New read-only ZScript fields on the player actor: `OffhandValid`, `OffhandPos`,
   `OffhandDir`, `OffhandAngle`, `OffhandPitch`, `OffhandRoll` (same conventions as the existing `AttackPos` etc. for
   the weapon hand). Before this, mods could not see the off hand at all.
2. **`FollowOffhand`**, a bool any mod can set on any actor: the engine then draws that actor at the off hand's pose of the
   current rendered frame (position and yaw), exactly like the weapon, instead of at its once-per-tic position. Without it a
   hand-held actor rubber-bands: it lags when you walk and drifts back when you stop `[reported 2026-09-17, n=1]`.
3. **Two-handed long guns.** `TwoHandedAim`, a bool a mod sets on the **player**: while it is on and the off
   hand is tracked, the shot follows the line between the two hands instead of the rear controller's own tilt.
   Guarded twice — a least hand separation, and agreement with where the gun itself points — and refusing leaves
   aiming exactly as it was, so the worst case is today's behaviour. Both guard numbers are **settings, not
   constants**: `vr_two_handed_min_sep` and `vr_two_handed_max_disagree`, with sliders in Options → VR Options,
   plus `vr_two_handed_debug` which prints which guard refused. That is on purpose — both numbers are guesses
   until someone measures a comfortable rifle hold, and this way tuning them needs no rebuild.
   The maths is `two_handed_aim.h`, shipped unchanged from the copy the test compiles.
4. **Two-handed long guns, the visible half** (2026-09-20). The gun is now **drawn** along the same
   hand-to-hand line: the rear hand keeps its position and the twist of the wrist, and the off hand
   sets where the barrel points, however far apart the hands are. Before this, only the shot ever
   moved, so the change was invisible in the headset and read as "the left hand does nothing".
   Setting: `vr_two_handed_draw` (on), Options → VR Options. Anything missing falls back to the
   one-handed gun, so the worst case is the behaviour the engine had before. The maths is
   `two_handed_pose.h`; full write-up in [`TWO-HANDED-DRAW.md`](TWO-HANDED-DRAW.md).
5. **Stop-motion weapon hand (dropped by Tefa 2026-09-17, left in the code, off).** `vr_weapon_stopmotion` (on/off) and `vr_weapon_stopmotion_skip` (rendered frames the
   weapon stays frozen after each update, 1 to 12). The world and the view stay smooth.
   Shots use the same frozen pose, so bullets still leave the barrel you see. Menu: Options → VR Options.

## Building (Windows, as done on 2026-09-17) `[verified-live 2026-09-17, n=1]`
VS 2022 Build Tools + CMake. The upstream `auto-setup-windows.cmd` failed here (vcpkg could not build yasm for ZMusic), so:
- clone `ValveSoftware/openvr` (headers only are enough) and pass `-DOPENVR_SDK_PATH=<that folder>`;
- build ZMusic **without** vcpkg (`cmake -A x64 -S zmusic -B zmusic/build`, then `--config Release`);
- configure the engine with the vcpkg toolchain and `-DZMUSIC_INCLUDE_DIR` / `-DZMUSIC_LIBRARIES`, build `RelWithDebInfo`.
The result goes in its own folder (`gzdoomvr-tefa/`) beside the original engine; nothing of the original is overwritten.

## Status
- **Left hand: works in the headset** `[reported 2026-09-17, n=1 wear]`. Tefa: *"left hand is moving the lantern and it is also the
  light source, so it illuminates the world around it as i move it! this is awesome!"* Asked for: half the light radius, and the
  blue flicker (the lamp looked grey). Both changed, not worn yet.
- **Stop-motion hand: DROPPED.** 12 updates a second felt bad, and so did skipping a single frame: *"stop motion is not good in here, so we'll drop that going forward"* `[reported 2026-09-17, n=1]`. The setting is off; the code stays, harmlessly.
- **Two-handed long guns: BUILT AND IN THE GAME FOLDER, not yet worn** (2026-09-19, home PC `RTX`).
  The four edits described in `TWO-HANDED-AIM.md` were applied, plus three settings and menu sliders that the
  document did not ask for; the engine compiles clean and starts, ZScript loads with the new `TwoHandedAim`
  field, and all three settings read back their defaults in the running build `[verified-live 2026-09-19, n=1
  flat launch]`. Deployed to `gzdoomvr-tefa/`; the engine it replaced is kept beside it as
  `gzdoomvr.exe.pre-twohanded` / `gzdoom.pk3.pre-twohanded`.
  ⚠️ **One correction to that document:** it suggested `AttackAngle.ToVector(AttackPitch)` for the weapon
  hand's forward direction. That is not a real call here (`ToVector` takes a length), and the obvious
  substitute — the `TRotator` → `TVector3` conversion — has `Z = +sin(pitch)`, the **opposite sign** to the
  convention the engine actually shoots along. Using it would have made the gun shoot exactly as far high as
  it should have been low, which is the failure the test suite was built to catch. The shipped code writes the
  vector out longhand in `p_map.cpp`'s convention (`{ pc*cos(yaw), pc*sin(yaw), -sin(pitch) }`)
  `[inferred-static 2026-09-19, read from p_map.cpp and vectors.h]`.
  ⚠️ **Still unworn.** What to look for in the headset is in [`TWO-HANDED-AIM.md`](TWO-HANDED-AIM.md).
- **2026-09-20: the guard numbers stopped mattering.** Tefa asked for long guns to be two-handed always —
  *"no proximity at all… there is no way to fire a long rifle or shotgun with one hand"* — so the mod now
  switches `TwoHandedAim` on for every long gun by itself, and this setup runs with `vr_two_handed_min_sep 0`
  and `vr_two_handed_max_disagree 180`, which leaves the engine only its divide-by-zero guard. Nothing in the
  engine changed; both are settings. The mod side is in `ashes-2063-weapons/kit/gz_shotgun.py`, and
  `shotgun/gzdoom/TEST.md` describes what the wear should look like `[verified-live 2026-09-20, n=4 flat launches]`.
- **⭐ 2026-09-20, after the second wear: THE GUN IS NOW DRAWN ALONG THE HAND LINE.** Tefa wore the
  build and reported *"all weapons are still one handed and left hand does not affect aiming at all
  visually"* `[reported 2026-09-20, n=1 wear]`. That was correct and it was our own doing: every
  change so far moved the **shot**, and nothing had ever touched how the gun is **drawn**, so a
  working change was invisible by construction. Fixed in `GetWeaponTransform()`; the maths is
  `two_handed_pose.h` (103 checks, five deliberate breakages all caught
  `[verified-numerically 2026-09-20, n=103 checks]`), the shot path deliberately kept on the
  untouched raw transform, and the whole thing switchable with `vr_two_handed_draw`. Rebuilt clean,
  deployed to `gzdoomvr-tefa/` with the replaced build kept beside it as
  `gzdoomvr.exe.pre-twohanded-draw` / `gzdoom.pk3.pre-twohanded-draw`; both flat probes pass on it
  `[verified-live 2026-09-20, n=3 launches]`. ⚠️ **Not worn.** What to look for:
  [`TWO-HANDED-DRAW.md`](TWO-HANDED-DRAW.md).
If this is ever released, GPL-3.0 means the patched source must be published with it (a public fork).
