# Revolver in GZDoomVR: in-game tests

Two builds from `kit/gz_export.py -- gz_revolver.py [flat|vr]`:
- `Ashes2063_revolver3d_test.pk3`: **flat screen** (model space = the Blender first-person camera, eye at the origin).
- `Ashes2063_revolver3d_VR_test.pk3`: **VR** (real size, 100 units per metre, grip centre at the controller).

Each holds one MD3 (82 frames: shoot 1 = 0-13, reload = 14-81), the baked `revolver.png`, and a
`modeldef.revolver` mapping the game's revolver sprite frames (REVG, REVF, REVR, REVL A-C) to model frames.

## Flat test: PASSED 2026-09-17 `[verified-live 2026-09-17, n=1 launch per build, 4 launches]`
Run unattended: `python tools/revolver_test.py <tag>` (launches windowed into MAP01, binds R to reload,
captures idle / one shot / one reload, quits). Evidence: `evidence-2026-09-17/`.
- The 3D revolver replaces the sprite as soon as the level starts (the player spawns holding it).
- Fire: muzzle flash, kick, settle. Reload: cylinder swings out LEFT, cases drop, rounds seat, flick closed, back to rest.
- Fixed during the test: (1) first build put the gun's origin at the eye, so the view was inside the gun
  (`first-launch-origin-at-eye.png`); now exported in camera space. (2) the model was mirrored, so the cylinder swung
  right (`before-mirror-fix-reload.png`); MD3 +Y is the viewer's RIGHT in this engine.
- Not judged yet (needs Tefa's eye): whether the resting pose and size look good. The game's FOV (90) is wider than
  the Blender camera (32 mm lens), so the gun looks smaller and more stretched at the edges than in the Blender renders.
- Frames with no model mapped (lantern-lit REVL J-T, melee REVG B-D, knife KNIF) fall back to the flat sprite `[inferred-static]`.

## VR test: WORKS, first wear 2026-09-17 `[reported 2026-09-17, n=1 wear]`
Tefa: *"it shows up, but is about 10 cm too high in relation to my hand and motion controller. maybe 8 cm ... but it
feels awesome already and works really well"*. Rebuilt with the grip 9 cm lower (`VR_GRIP_DROP` in `kit/gz_revolver.py`);
worn the same day: *"3 cm down, 2 cm to the right and 3 cm back my way"* (move it that way) → applied as `VR_NUDGE_*`. Third wear: *"not sure if back my way worked at all ... when turning the weapon sideways ... the handle being away from the motion controller"*, *"the weapon tilt when reloading has to be about 60% less"*, *"still 2cm lower"* → 5 cm further back (a big step, to make the direction obvious), 2 cm lower, and the reload's whole-gun movement cut to 40% (`GUN_MOTION_SCALE`, VR build only). Fourth wear: *"up please now 3cm and back 2cm"* → applied. Fifth wear (with a headset screenshot): *"needs 2cm to the
left again"*, and with the controller held relaxed the barrel points about 10° up (measured by eye from the screenshot).
→ 2 cm left in the build; the angle is fixed with the engine's `openvr_weaponRotate` (-40 → -50) rather than in the model,
because bullets follow that setting too, so the barrel and the shots stay lined up. The test launcher now uses its own
settings copy, `gzdoomvrshes-vr-3dtest.ini`, so the normal game's settings are untouched. Sixth wear: *"it's still pointing up"*. Cause: `+openvr_weaponRotate -50` on the command line did NOT apply (the ini was saved back with -40 on exit) `[verified-live 2026-09-17]`. Now set to -50 inside `ashes-vr-3dtest.ini` itself. Seventh wear: *"it's pointing straight now ... it works"* ✅

**Result: the VR revolver works, sits right in the hand and points straight** `[reported 2026-09-17, n=1 wearer, 7 wears]`.
Locked-in numbers: `kit/gz_revolver.py` VR block (grip drop, nudges, 40% reload movement) + `openvr_weaponRotate=-50`.
⚠️ The -50 angle lives only in the test settings copy. Anything released must carry it (tell players, or tip the model 10° instead and accept that the shots then leave 10° off the barrel).

On the home PC there is a desktop shortcut for it, **"Ashes 2063 VR - 3D revolver test"**, which runs
`Play Ashes 2063 VR (3D revolver test).bat` in the game folder. The original "Ashes 2063 VR" shortcut does NOT load our file.
From `C:\NonSteam\Ashes 2063 VR`, with Virtual Desktop / SteamVR running, the normal VR launcher line plus our file:
```
gzdoomvr\gzdoomvr.exe -iwad Resources\freedoom-0.12.1\freedoom2.wad -file Resources\AshesSAMenu.pk3 Resources\lightmodepatch.pk3 Resources\Ashes2063Enriched2_23.pk3 Resources\Ashes2063EnrichedFDPatch.pk3 "C:\Users\TD3KX\ashes-2063-weapons\revolver\gzdoom\Ashes2063_revolver3d_VR_test.pk3" -config gzdoomvr\ashes-vr.ini +set language enu +vr_mode 10
```
| You see | Means / fix |
| --- | --- |
| Revolver in your right hand, sensible size | works; judge comfort and look |
| Gun too high/low/forward in the hand | MODELDEF `Offset x y z` in cm (x right, y back toward you, z up), no rebuild |
| Gun huge or tiny | `UNITS_PER_M` in `kit/gz_revolver.py` (100 = real size) |
| Gun sits right but points 40° off your aim | leave the model; bullets follow `openvr_weaponRotate` too |
| Flat sprite instead of the model | the pk3 was not loaded (check the `-file` path) |
Grip placement uses the controller origin at MD3 (30, 0, -5) `[inferred-static]`; whether that is mid-palm on Quest
controllers through Virtual Desktop is `[hypothesis]`. The VR pistol puts its grip about 7 cm lower.
