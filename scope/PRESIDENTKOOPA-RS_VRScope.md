# President_Koopa's isolated VR scope (RS_VRScope, sent to Tefa 2026-11-02)

Tefa, 2026-11-02: *"this is what President_Koopa sent me to give you."* The zip is kept in MEGA
`Game Files/ashes-2063-weapons/from-presidentkoopa/RS_VRScope_2026-11-02.zip`. It is his code, lifted by him out of
[RS_Brutal22WeaponsQ](https://github.com/presidentkoopa/RS_Brutal22WeaponsQ) 2.0 (no licence file), so it is loaded as
he ships it and not copied into this repo.

## What it is

A real telescopic sight: a camera parked at the lens, pointed down the bore, its picture drawn at 3x onto the scope's
own glass on the held model (`TexMan.SetCameraToTexture` + `A_ChangeModel(... CMDL_USESURFACESKIN)`), mono on purpose,
off and free with alt fire. The same method our FAL scope (`build_scope_test.py`) was built on, as a clean component.

## What a gun needs to use it (his README, checked against our exporter)

1. **The glass as its own MD3 surface, UV-mapped 0..1.** Our `gz_forge_export.py` already does this for a part named in
   the job's `glass_part` (the FAL's `glass`, surface 0). The Junker Musket's big scope is the next candidate.
2. **A MODELDEF block with `SurfaceSkin` lines and no whole-model `Skin`.** ⚠️ Our exporter writes BOTH a `Skin 0` and
   `SurfaceSkin` lines; his note says a whole-model `Skin` beats the swap and the scope never shows. Check whether our
   FAL scope works because of a difference, or drop the `Skin` line for scoped guns.
3. **Six numbers per gun** (lens centre, bore axis, the glass's up, glass radius, surface index, magnification),
   measured off the mesh at the ready frame. ⚠️ The detailed guns are 1.5x bigger (2026-11-02), so any table measured
   on the old size is wrong for them.

Needs only stock natives (QuestZDoom 17.3 / GZDoom 4.14): `AttackPos`, `AttackDir`, `OverrideAttackPosDir`, `PlayInVR`.
Ours has all but `PlayInVR` until the quest-compat step-1 patch is on the home engine (`engine/QUEST-COMPAT.md`).

## His other projects worth a look later (2026-11-02, read from GitHub, not tried)

- RS_Brutal22WeaponsQ: `RECOIL_DESIGN.md`, `ACCURACY_NOTES.md`, a Two-Hand Aim test (the off hand on a measured support
  point steers the shots), a voxel pack.
- RS_Aliens_VR-WeaponsQ: a flamethrower and smartgun model set with its own gldefs and shaders, VR melee from the pose
  history with hitstop and per-arm rumble.
- RSQ_UBQSeries: the add-ons already being ported (`engine/QUEST-COMPAT.md`); new on 2026-11-02: a cigarette ritual on
  the tactical rig, grapple pull mode, distance-grab fixes.
