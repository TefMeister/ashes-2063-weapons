# Revolver in GZDoomVR: first in-game test (not yet run)

`Ashes2063_revolver3d_test.pk3` is built by `kit/gz_export.py -- gz_revolver.py` and holds:
- `models/ashes2063/revolver/revolver.md3`: 82 frames (shoot 1 frames 1-14 = model frames 0-13,
  reload frames 1-68 = model frames 14-81), 4568 triangles, drawn two-sided.
- `revolver.png`: the 512×512 baked texture atlas.
- `modeldef.revolver`: maps the game's revolver sprite frames (REVG, REVF, REVR, REVL A-C) to model frames.

## Flat test (do first), from `C:\NonSteam\Ashes 2063 VR`
Uses a copy of the VR config so the VR settings are never overwritten.
```
copy gzdoomvr\ashes-vr.ini gzdoomvr\ashes-flat-test.ini
gzdoomvr\gzdoomvr.exe -iwad Resources\freedoom-0.12.1\freedoom2.wad -file Resources\AshesSAMenu.pk3 Resources\lightmodepatch.pk3 Resources\Ashes2063Enriched2_23.pk3 Resources\Ashes2063EnrichedFDPatch.pk3 "C:\Users\TD3KX\ashes-2063-weapons\revolver\gzdoom\Ashes2063_revolver3d_test.pk3" -config gzdoomvr\ashes-flat-test.ini +vr_mode 0 +fullscreen 0 +vid_defwidth 1280 +vid_defheight 720
```
In a level, open the console (`~`): `give revolver`, `give fortyfiveammo`, then `use revolver`.

## What each result means
| You see | Means |
| --- | --- |
| Our silver 3D revolver instead of the flat picture | the model loads; move on to size/position |
| The old flat revolver picture | the model file was not picked up (check the console for MODELDEF errors) |
| Nothing at all where the gun should be | model loads but is off-screen or tiny: change `UNITS_PER_M` / `ORIGIN`, or add `Offset` in the modeldef |
| Gun visible but facing the wrong way | fix with `AngleOffset` / `PitchOffset` in the modeldef |
| Fire: jumps and flashes; reload: cylinder swings out, cases drop, rounds go in | animations work |

Then the same in VR with the normal launcher plus the extra `-file`. Unchecked guesses `[hypothesis]`: size
(250 units per metre), pivot (top rear of the gun, copied from the VR pistol model), and facing (+X forward).
Known limit: one game sprite letter shows one pose, so poses inside a long-held letter (e.g. the
speedloader coming up during REVR P) are skipped.
