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
3. **Stop-motion weapon hand (dropped by Tefa 2026-09-17, left in the code, off).** `vr_weapon_stopmotion` (on/off) and `vr_weapon_stopmotion_skip` (rendered frames the
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
- **Two-handed long guns: the missing engine change is now WRITTEN and its maths is checked** (2026-09-18, `/pd`).
  Mods could already read both hands every tic and draw a rifle along the line between them; only the SHOT still followed the rear
  controller's own tilt. `two_handed_aim.h` computes the aim from the hand-to-hand line, with two guards so it refuses — and changes
  nothing — when the off hand is not actually on the gun. `two_handed_aim_test.cpp` compiles that same header: **36/36 checks**, proved
  able to fail on **ten** mutants of it, all ten caught `[verified-numerically 2026-09-18]`. Run it with `run_aim_test.bat`.
  ⚠️ **NOT built and NOT worn** — the dev PC has no engine source and no headset. The four edits to make on the home PC, the mod-side
  ZScript, and what each headset outcome would mean are in [`TWO-HANDED-AIM.md`](TWO-HANDED-AIM.md). Both threshold numbers are
  guesses until someone measures a comfortable rifle hold `[hypothesis]`.
If this is ever released, GPL-3.0 means the patched source must be published with it (a public fork).
