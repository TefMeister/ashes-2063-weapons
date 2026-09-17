# Ashes 2063 EP1 weapons: first rough models and animations (2026-09-17, home PC)

Our own models, built from scratch in Blender 5.2. Nothing is taken from the game files. The look is
the same as the lantern (`lantern/`, moved into this repo 2026-09-17): low-poly, flat-shaded, blocky
procedural pixel textures, EEVEE at 320×240, 35 fps. Repo: github.com/TefMeister/ashes-2063-weapons (created 2026-09-17).

## Layout: one Blender file per job (Tefa's request)
| Folder | File | What |
| --- | --- | --- |
| `handgun/` | `Ashes_2063_EP1_handgun_model.blend` | the gun on its own |
| `handgun/` | `Ashes_2063_EP1_handgun_shoot1.blend` | one shot, 16 frames |
| `handgun/` | `Ashes_2063_EP1_handgun_reload.blend` | magazine swap, 44 frames |
| `jackhammer/` | `Ashes_2063_EP1_jackhammer_model.blend` | the machine on its own |
| `jackhammer/` | `Ashes_2063_EP1_jackhammer_shoot1.blend` | hammering loop, 12 frames |
| `crowbar/` | `Ashes_2063_EP1_crowbar_model.blend` | the bar on its own |
| `crowbar/` | `Ashes_2063_EP1_crowbar_shoot1.blend` | one swing, 24 frames |
| `handgun/` | `Ashes_2063_EP1_handgun_shoot1_static.blend` | shot with the gun held still |
| `handgun/` | `Ashes_2063_EP1_handgun_reload_static.blend` | magazine out and in, gun held still |
| `revolver/` | `Ashes_2063_EP1_revolver_model.blend` | the .45 revolver on its own |
| `revolver/` | `Ashes_2063_EP1_revolver_shoot1.blend` | one shot, 14 frames, game timing |
| `revolver/` | `Ashes_2063_EP1_revolver_reload.blend` | cases out, speedloader in, 68 frames, game timing |
| `revolver/` | `Ashes_2063_EP1_revolver_shoot1_static.blend` | shot with the gun held still |
| `revolver/` | `Ashes_2063_EP1_revolver_reload_static.blend` | cylinder out, cases out, rounds in, gun held still |
| `jackhammer/` | `Ashes_2063_EP1_jackhammer_shoot1_static.blend` | bit and smoke only, machine held still |

**Rule (Tefa, 2026-09-17, all weapons, all games):** every animation comes in two files. The normal
one is the game's own movement. The `_static` one keeps the weapon itself fixed in its rest pose and
moves only its parts (flash, slide, casing, magazine, bit), so hands can be added later. The static
files use the same frame numbers as the normal ones and open looking through `SideCam`, which shows
the whole weapon (`ViewCam`, the player's view, is still there). The crowbar has no static file: it
has no moving parts, so it would be a still bar.

The animation files **link** their model file (Library Override), so fixing a model updates every
animation of it. Future alternate fires go in `..._shoot2.blend` and so on.

Everything is rebuilt from the scripts in `kit/` (run inside Blender with `exec(open(path).read())`):
`pixel_kit.py` (materials, mesh helpers), `anim_kit.py` (linking, first-person camera, constant keys),
`build_<weapon>.py`, `anim_<weapon>_<action>.py`, `handgun_settings.py`.
**Background mode (no window, never takes focus, safe beside /pd and /lm):**
`blender.exe -b --factory-startup --python kit/run_background.py -- anim_handgun_reload.py static`
(add `render:1,12,22` for test pictures). Skip test renders during a live VR test: they load the GPU. ⚠️ Running a build script
overwrites its `.blend`, so hand edits made in Blender are lost unless copied into the script.

## Stop-motion
Every key is CONSTANT: the pose jumps, nothing slides in between. Poses are held 1 to 4 frames.

## What is guessed `[hypothesis]` (all by eye from Tefa's screenshots, n=1 per view)
- **Handgun** (`Handgun/shoot 1`, `Handgun/reload`): chunky steel pistol with worn red paint, rear
  serrations, round ring hammer, rubber grip. The left side, underside, muzzle face and magazine are
  invented. Shot: flash + kick up + slide back + brass casing flies right. Reload: gun turns on its
  side and tips up, magazine drops out, new one rises from below and slaps in (small jolt), gun
  comes back. There is no slide pull, because the screenshots do not show one.
- **Jackhammer** (`jackhammer/`): red ribbed body, white hood with vents, black band with two blocky
  yellow "R" glyphs, black handle loop with a brown wrapped grip, black fuel tank with a silver cap on
  the left. The bit, the underside and the far side are invented. Firing: body jolts, the bit
  punches down, blocky grey exhaust puffs.
- **Crowbar** (`crowbar/`): hex bar, worn red paint, dark steel chisel end and claw. There were no
  crowbar attack screenshots, so "shoot 1" is a guessed swing: wind up right, strike across,
  follow through low left.
- First-person placement and lens are set by eye, not measured against the game.

## Next
- Tefa's feedback on shapes, colours and the animation poses.
- Check real game animation timing (the 35 fps = one tic assumption comes from the lantern and is
  unchecked).

## Changes 2026-09-17 (from Tefa's `CHANGES and questions.txt`)
- Handgun casing now leaves fast and far: at the port on the shot frame, 0.3 m out the next frame,
  0.8 m the frame after, then gone. It travels in world space, so turning the gun does not bend its path.
  (Rule for every weapon.)
- Reload: the old magazine falls 0.6 m before vanishing. The new one starts at the player's left hip
  (world -0.28, 0.10, -0.50 from the eye), swings to the bottom of the grip over frames 21–26, then pushes in.

## What the game actually is (read from `C:/NonSteam/Ashes 2063 VR`, 2026-09-17) `[inferred-static]`
- Installed by Mr. N!ce's PCVR hub. The engine is **GZDoomVR 4.13.2.2** (OpenVR), with `WeaponsForVR.pk3`
  (3D MD3 models for the *original Doom* weapons only) and `laser-sight.pk3` (the red dot). The mod is
  `Ashes2063Enriched2_23.pk3` on Freedoom 2.
- Ashes weapons are **DECORATE** sprite weapons (`Actors/Weapons/*.txt`): Glock ("9mm Autoloader", the
  magazine pistol this model is), Revolver, Crowbar (replaces Fist), JACKHAMMER (replaces Chainsaw),
  Shotgun (pumpaction), SawedOff, Ingram, FAL, Musket, pipebomb, NapalmGun. The lantern is a hotkey (+zoom).
- **Casings are already real world objects** (`pistolCasing` etc. in `Actors/Effects/Effects.txt`, thrown
  with Speed 6 by a spawner). Faster in-game casings = raise those speeds; the casing inside our Blender
  animation would then be dropped when models go in-game.
- The engine tells mods where the **weapon hand** is and where it points (`AttackPos`, `AttackAngle`,
  `AttackPitch`, `AttackRoll`, `OverrideAttackPosDir` in `gzdoom.pk3` `actor.zs`). **Nothing about the off
  hand** reaches mods (it is only used for "movement follows off hand").
- Verdicts from that `[inferred-static]`, none tried in game:
  - Left-hand lantern following the controller: not possible for a mod as-is; needs a change inside
    GZDoomVR itself (open source). Hip lantern on a button: easy.
  - Real crowbar swings: plausible, since the weapon hand position is readable each tic, so hand speed can be worked out.
  - Manual reload / racking by button press and release: plausible (weapon states + ZScript button checks).
  - Sprites to 3D via MODELDEF: supported by the engine, which is exactly what `WeaponsForVR.pk3` does. Big job.

## Revolver (2026-09-17)
**Timing is the game's own, one Blender frame per tic** (new rule, Tefa 2026-09-17: every weapon, every game).
Source: `Actors/Weapons/Revolver.txt` in `Ashes2063Enriched2_23.pk3` `[inferred-static]`.
- Shoot (`FireReal`): REVF A 2, B 1, D 1, E 2, F 2, G 2, H 1, then REVG A 1+1 → frames 2–13, rest at 1 and 13–14.
- Reload (`Work1` + `ReloadDone`): REVR A B 3 each; C C C D E F 2; G G H I J L L L L 2; M N O P 2;
  P P P Q R S 2; T U V W X 1; REVL C B A 2 → 67 tics, frames 1–67. The game spawns one casing per
  round loaded (`pistolCasingspawner`) during the zero-tic `ReloadLoop`.
- Poses are by eye from `revolver/shoot 1` (17 shots) and `revolver/reload` (55 shots) `[hypothesis]`;
  which sprite letter each screenshot shows is matched by order, not checked.

Model `[hypothesis]`: stainless six-shot .45 with full underlug and vented rib, red front sight insert, black
rubber finger-groove grip. Parts: `RV_Crane` (swings out left) > `RV_Cylinder` (turns 60° per shot) >
`RV_Ejector`, `RV_Casings` (spent), `RV_Rounds` (loaded); `RV_Hammer`, `RV_Trigger`, `RV_MuzzleFlash`,
`RV_FlashLight`, `RV_Speedloader` (+ `RV_SpeedloaderBody`). Numbers in `kit/revolver_settings.py`.
- Shoot: hammer already down on the shot tic (the game has no cocking frame), cylinder turns 60°, big flash,
  kick up and right, settles over F–H.
- Reload: cylinder swings out; gun tips muzzle-up; ejector pushes the cases out and they drop 0.8 m in the
  world in 3 frames, then vanish; gun tips down so the cylinder's back faces you; speedloader comes from the
  left hip (same spot as the handgun magazine), seats the rounds on tic R and disappears; flick closes it.
