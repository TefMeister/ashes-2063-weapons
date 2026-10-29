# A live scope on the FAL (2026-10-29)

The FAL's eyepiece lens shows a 3x zoomed picture of where the gun points, while the FAL is in hand.

- The method (a camera picture drawn on the scope's glass, the glass skin swapped while the gun is held) is the one
  used by the scope in the BD22Q Brutal Doom VR pack another modder sent Tefa. Thanks to its author. The code here is
  our own, written for our engine's gun-hand fields; nothing of the pack is copied in.
- `zscript/ashes_scope.zs` (the script), `animdefs.ashesscope` (the picture, 256 x 256), `mapinfo.ashesscope`.
- The lens is the forge part `glass` in `forge/battle_rifle.py`; `brutal-doom-3d-guns/tools/gz_forge_export.py` makes
  it surface 0 with its own skin.
- `python scope/build_scope_test.py <export folder> <out pk3>`: the FAL, the scope and the shine in one test pk3.

Not yet run in the game `[hypothesis]`.
