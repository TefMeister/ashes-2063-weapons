# Our GZDoomVR changes (engine patch)

A small patch on top of **GZDoomVR** by hh79 (https://github.com/hh79/gzdoomvr, tag `gvr4.13.2.2`, GPL-3.0),
the VR engine Ashes 2063 runs on here. Patch file: `gzdoomvr-gvr4.13.2.2-offhand-stopmotion.patch`.

## What it adds
1. **The off hand, for mods.** New read-only ZScript fields on the player actor: `OffhandValid`, `OffhandPos`,
   `OffhandDir`, `OffhandAngle`, `OffhandPitch`, `OffhandRoll` (same conventions as the existing `AttackPos` etc. for
   the weapon hand). Before this, mods could not see the off hand at all.
2. **Stop-motion weapon hand.** `vr_weapon_stopmotion` (on/off) and `vr_weapon_stopmotion_rate` (updates per second,
   2 to 35). The weapon follows the controller only that many times a second; the world and the view stay smooth.
   Shots use the same frozen pose, so bullets still leave the barrel you see. Menu: Options → VR Options.

## Building (Windows, as done on 2026-09-17) `[verified-live 2026-09-17, n=1]`
VS 2022 Build Tools + CMake. The upstream `auto-setup-windows.cmd` failed here (vcpkg could not build yasm for ZMusic), so:
- clone `ValveSoftware/openvr` (headers only are enough) and pass `-DOPENVR_SDK_PATH=<that folder>`;
- build ZMusic **without** vcpkg (`cmake -A x64 -S zmusic -B zmusic/build`, then `--config Release`);
- configure the engine with the vcpkg toolchain and `-DZMUSIC_INCLUDE_DIR` / `-DZMUSIC_LIBRARIES`, build `RelWithDebInfo`.
The result goes in its own folder (`gzdoomvr-tefa/`) beside the original engine; nothing of the original is overwritten.

## Status
Builds with no errors; starts, loads Ashes plus our test files, and both settings exist `[verified-live 2026-09-17, flat, n=1]`.
**Not yet tried in the headset**: the lantern following the left hand, and how the stop-motion hand feels.
If this is ever released, GPL-3.0 means the patched source must be published with it (a public fork).
