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

## VR test: NOT RUN (needs the headset)
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
