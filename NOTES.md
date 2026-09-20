# Ashes 2063 EP1 weapons: first rough models and animations (2026-09-17, home PC)

Our own models, built from scratch in Blender 5.2. Nothing is taken from the game files. The look is
the same as the lantern (`lantern/`, moved into this repo 2026-09-17): low-poly, flat-shaded, blocky
procedural pixel textures, EEVEE at 320×240, 35 fps. Repo: github.com/TefMeister/ashes-2063-weapons (created 2026-09-17).

## Layout: one Blender file per job (Tefa's request)
| Folder | File | What |
| --- | --- | --- |
| `handgun/` | `Ashes_2063_EP1_handgun_model.blend` | the gun on its own |
| `handgun/` | `Ashes_2063_EP1_handgun_shoot1.blend` | one shot, 7 frames, game timing |
| `handgun/` | `Ashes_2063_EP1_handgun_reload.blend` | magazine swap, 47 frames, game timing |
| `jackhammer/` | `Ashes_2063_EP1_jackhammer_model.blend` | the machine on its own |
| `jackhammer/` | `Ashes_2063_EP1_jackhammer_shoot1.blend` | hammering loop, 5 frames, game timing |
| `crowbar/` | `Ashes_2063_EP1_crowbar_model.blend` | the bar on its own |
| `crowbar/` | `Ashes_2063_EP1_crowbar_shoot1.blend` | one swing, 30 frames, game timing |
| `handgun/` | `Ashes_2063_EP1_handgun_shoot1_static.blend` | shot with the gun held still |
| `handgun/` | `Ashes_2063_EP1_handgun_reload_static.blend` | magazine out and in, gun held still |
| `revolver/` | `Ashes_2063_EP1_revolver_model.blend` | the .45 revolver on its own |
| `revolver/` | `Ashes_2063_EP1_revolver_shoot1.blend` | one shot, 14 frames, game timing |
| `revolver/` | `Ashes_2063_EP1_revolver_reload.blend` | cases out, speedloader in, 68 frames, game timing |
| `revolver/` | `Ashes_2063_EP1_revolver_shoot1_static.blend` | shot with the gun held still |
| `revolver/` | `Ashes_2063_EP1_revolver_reload_static.blend` | cylinder out, cases out, rounds in, gun held still |
| `jackhammer/` | `Ashes_2063_EP1_jackhammer_shoot1_static.blend` | bit and smoke only, machine held still |
| `shotgun/` | `Ashes_2063_EP1_shotgun_model.blend` | the pump-action shotgun on its own |
| `shotgun/` | `Ashes_2063_EP1_shotgun_shoot1.blend` | one shot and the pump stroke, 30 frames, game timing |
| `shotgun/` | `Ashes_2063_EP1_shotgun_reload.blend` | fired dry: action cycled, six shells in, 164 frames, game timing |
| `shotgun/` | `Ashes_2063_EP1_shotgun_reload_partial.blend` | shells still in it: three more go in, 76 frames, game timing |

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

## Shotgun (2026-09-18, home PC) `[hypothesis]`

Built by eye from Tefa's screenshots in `Ashes 2063/shotgun/` (three sets: `shoot 1`,
`reload when not fully out of ammo`, `reload when fully out of ammo`, plus `shotgun model.png`).
Every shot is a heavy zoom on the first-person view, so **the length and proportions are guessed**;
only the parts that appear on screen are drawn from evidence.

**What the screenshots actually show** (n=1 per view, by eye):
- A long dark barrel with a magazine tube under it, a chunky pale barrel band part-way along, and a
  blocky pale front sight on a ramp at the muzzle.
- A **deeply ribbed warm brown wooden pump**, the only warm colour on the gun.
- A dark green-grey receiver with a large rectangular **port showing a red shell with a brass head**,
  a big round pin head, a stamped row of marks, and a swept trigger guard below.
- A **near-black stock** with a strong sheen and a dark pad.

**Deliberate choices, both Tefa-directed (2026-09-18):**
- **Darker than the revolver and the lantern.** Those read "light grey and even white". Every ramp
  here is narrow and low, and the shared weathering colours (scratch, rust, grime) are overridden
  darker at the top of `build_shotgun.py` — the toolkit's bright scratch colour reads as white cracks
  on a dark gun.
- **The port is on the gun's LEFT.** That is the side the game's own sprite shows it on, because the
  player sees the left flank. Real 12-gauges eject to the right. `PORT_X` in `build_shotgun.py` flips
  it if we ever want the real side.

**Invented, with no evidence at all:** the right-hand side, the underside, the butt pad, the sling
stud, the receiver's internals, and the whole length of the gun.

**Moving parts:** `SG_Pump` (racks back along -Y, `PUMP_BACK`), `SG_Trigger`, `SG_PortShell`, and
hidden `SG_MuzzleFlash`, `SG_Casing`, `SG_LoadShell`. Numbers live in `kit/shotgun_settings.py`.

### Animations (2026-09-18) — timing is the game's own `[inferred-static 2026-09-18]`

Read straight out of `Actors/Weapons/Shotgun.txt` in `Ashes2063Enriched2_23.pk3`, actor `pumpaction`
(the wooden-pump one in Tefa's screenshots; `pumpaction2`, the "Classic shotgun", is a separate upgrade
and is NOT modelled). One frame = one tic.

| File | Game states | Tics |
| --- | --- | --- |
| `shoot1` | `FireReal` (GRIF A 1, B 1, C 1, GRIP C 4, B 2) then `Pump` (GRIP A-G 1 each, H 3, I-M 2 each, GRIZ A 1) | **30** |
| `reload` | `Reloadpump` in full: cycle the action (26), first shell and the action closing on it (47), then `Reloadloop` 15 × 5, `ReloadDone` 15 | **164** |
| `reload_partial` | `ReloadStart` (16), `Reloadloop` 15 × 3, `ReloadDone` 15 | **76** |

The 164 matches Tefa's `reload when fully out of ammo` folder (162 screenshots) almost exactly, which is
the best confirmation we have that one frame really is one tic.

The spent shell leaves on tic 17 of the shot, right where the game throws its `grizzlySpawner`, and it
travels in **world** space — turning the gun cannot bend its path (the rule set for the handgun on
2026-09-17).

⚠️ **The first-person pose (`REST_LOC` / `REST_ROT`) is by eye and is the weakest part** `[hypothesis]`.
It was pushed around until the framing resembled Tefa's screenshots, but nothing is measured against the
game, and in VR the controller decides where the gun is anyway. The revolver's took seven wears to settle.
The `_static` files open through `SideCam`, which is where the motion is actually readable.

## Shotgun in the game (2026-09-19, home PC) `[verified-live 2026-09-19, n=3 launches]`

Exported the same way as the revolver (`kit/gz_shotgun.py` + `kit/gz_export.py`), flat and VR builds,
and checked unattended with `tools/shotgun_test.py`. It replaces the sprite, fires, throws the shell
right, works the pump and plays the dry reload. Details, evidence and the VR checklist:
[`shotgun/gzdoom/TEST.md`](shotgun/gzdoom/TEST.md).

**Three things learned that apply to every weapon after this one:**
- **`Model <name>` in MODELDEF names the ACTOR CLASS, not the file.** It matched the file for the
  revolver only because Ashes calls that actor `revolver`. The shotgun's is `pumpaction`, and getting
  it wrong shows the flat sprite with **no error at all**. `ACTOR_CLASS` now exists for this.
- **The Blender first-person camera must match the game's field of view.** The kit's 32 mm is about
  61°; GZDoom plays at about 90°. On a gun as long as this one the butt sits outside the Blender
  frame while the game still draws it, filling half the screen. `VIEW_LENS_SG = 18` fixes it, and
  every long gun from here should do the same.
- **Export only the frames a sprite letter names.** `ANIMS` now takes an explicit frame list, and the
  exporter fails loudly if a sprite points at a frame that was left out. The shotgun ships 42 frames
  instead of 194, which is a 1.2 MB model instead of tens of megabytes.

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

## Re-timed from the game (2026-09-17)
The handgun, jackhammer and crowbar were first timed by eye. They now use the game's own tics too
(sources in `Ashes2063Enriched2_23.pk3` → `Actors/Weapons/`) `[inferred-static]`; poses are unchanged apart from
being moved onto the new frames.
- **Handgun shoot 1** (`Glock.txt`, `FireReal`): GLKF A 1, GLKF B 1, GLOK B 2, GLOK C 1, GLOK A 1 → 7 frames incl. the ready frame.
- **Handgun reload** (`Glock.txt`, `Work2` + `ReloadDone`, the reload with a round still chambered): 46 tics → 47 frames.
  The game hides the gun for 1 tic and later 3 tics (`TNT1`); the 3D gun holds its pose there. The empty-gun
  reload (`Work1`, slide locked back) is not made yet.
- **Jackhammer shoot 1** (`Hammer.txt`, `FIREGAS`): E F G H E, 1 tic each, hit on F → 5-frame loop.
  Not made yet: the wind-down when you let go (HIHEABCDCB, 2 tics each) and the overcharge alt-fire.
- **Crowbar shoot 1** (`Crowbar.txt`, `Fire` + `Downswing`, one click): 29 tics → 30 frames; hit on tic 13.
  Where the game hides the bar the 3D bar is swung out of view. Not made yet: the held-button return
  swing (`Upswing`) and the heavy alt-fire strike.

## Fire rates, worked out from the game files (2026-09-17) `[inferred-static]`
No recording is needed: each weapon's state list says how many tics (1/35 s) pass between shots.
"Held" = fire button held down; the game re-fires by itself at the end of the cycle.

| Weapon | Tics per shot (held) | Shots per second | Per minute | Notes |
| --- | --- | --- | --- | --- |
| 9mm handgun | 6 | 5.8 | 350 | |
| .45 revolver | 12 | 2.9 | 175 | quick re-clicking can fire after 8 tics (NOAUTOFIRE + fire allowed on sprite G) |
| Pump shotgun | 30 (9 shot + 21 pump) | 1.2 | 70 | second shotgun actor `pumpaction2` pumps faster: 24 tics, 87/min |
| Sawed-off | 10 between the two barrels | | | then reload; alt-fire shoots both barrels in the same tic |
| Ingram (plain) | 3 shots every 8 tics | 13.1 | 790 | bursts of 3-2-3 tic gaps; aimed alt-fire: 2 tics, 1050/min |
| Ingram (suppressed) | 3 every 8 | 13.1 | 790 | aimed alt-fire 2 tics |
| Ingram (third version) | 3 every 6 | 17.5 | 1050 | aimed alt-fire 2 tics |
| FAL | 7 | 5.0 | 300 | scoped: 8 tics, 262/min |
| Musket | single shot | | | 15 tics of recoil animation, then reload |
| Napalm gun | 22 | 1.6 | 95 | flamethrower alt-fire: 8 flame puffs per 14-tic ammo cycle |
| Jackhammer | 5 | 7 | 420 | |
| Crowbar | 15-16 per hit (held, alternating swings) | 2.3 | 135 | one click = 29-tic swing |
| Pipe bomb | thrown | | | cook time up to about 21 × 5 tics |

Caveat: counted by hand from the DECORATE states (a state's action runs when it is entered, `A_ReFire`
jumps at once while fire is held). Worth one check in game with a stopwatch on the handgun if exact numbers matter.

## Getting a model into the game (2026-09-17) `[compile-verified]`-level only: built and read back, not run
GZDoomVR shows 3D weapons through MODELDEF (the bundled `WeaponsForVR.pk3` does this for Doom's guns: MD3 files,
+X forward, origin at the top rear, about 50 units long). Our pipeline, all in `kit/`:
- `gz_bake.py`: one shared UV atlas for every part, base colours baked to a 512×512 PNG (runs at the end of `build_revolver.py`).
- `gz_md3.py`: small MD3 writer. Hidden parts are collapsed to a point per frame; every triangle is written twice
  (both windings) so the face-winding convention cannot hide the gun.
- `gz_export.py -- gz_<weapon>.py`: reads every frame of the animation files, writes the MD3, the MODELDEF and a test `.pk3`.
- The MD3 was read back and drawn from its own data (frames 0, 1, 20, 77): gun, flash and reload poses are correct.
Test plan and what each outcome means: `revolver/gzdoom/TEST.md`.

## First in-game test: the revolver works in flat mode (2026-09-17, `/lm`) `[verified-live 2026-09-17, n=4 launches]`
The 3D revolver shows up in place of the sprite, fires (flash, kick) and plays the whole reload in the game.
Two fixes came out of it, both explained by the engine source (hh79/gzdoomvr tag gvr4.13.2.2, read by the session's reader):
- Flat mode puts the MD3 origin at the player's eye, so the flat build is exported in Blender camera space.
- MD3 +Y is the viewer's RIGHT; our first export mirrored the gun. Cross-checked against `Fist.md3` / `FistLeft.md3`.
Also from the source `[inferred-static]`: VR hangs the model off the controller in centimetres (hand at MD3 30, 0, -5);
`openvr_weaponScale` does not touch models; HUD models are not back-face culled; `Skin` overrides `SurfaceSkin`;
unmapped weapon frames fall back to the flat sprite. A VR build exists and is untested. Details: `revolver/gzdoom/TEST.md`.
Test harness: `tools/gzdrive.py` (window capture, scancode input, focus fix) and `tools/revolver_test.py`.

## First headset wear of the revolver (2026-09-17) `[reported 2026-09-17, n=1 wear]`
Shows up in the hand and *"feels awesome already and works really well"*, but sat 8-10 cm too high. So the engine's hand
point (MD3 30, 0, -5) is not mid-palm on Quest 3 controllers through Virtual Desktop; the VR build now puts the grip centre
9 cm lower (MD3 Z -14), close to where the bundled VR pistol has its grip (about -12). The lowered build is not worn yet.

## ✅ The revolver works in VR (2026-09-17) `[reported 2026-09-17, n=1 wearer]`
After seven headset rounds Tefa: *"it's pointing straight now. mission accomplished isn't it!! it works"*. Final VR setup:
grip about 7 cm below the engine's hand point, nudged 5 cm back toward the player overall (right/left cancelled out), reload
whole-gun movement cut to 40% (the player tilts the controller anyway), and `openvr_weaponRotate=-50` (was -40) in the test
config. Lesson: `+openvr_weaponRotate` on the command line does not apply; set it in the ini. The desktop shortcut
"Ashes 2063 VR - 3D revolver test" runs the test build with its own config copy.

## Our own GZDoomVR build: left hand for mods + stop-motion weapon hand (2026-09-17)
See `engine/README.md` (patch, build recipe). Test mod: `lantern/gzdoom/Ashes2063_lefthand_lantern_test.pk3`, built by
`kit/gz_lantern.py`: our Blender lantern as a world model, moved to the off hand every tic by a small ZScript event handler,
with a flickering dynamic light. Desktop shortcut on the home PC: "Ashes 2063 VR - Tefa engine test". Headset test pending.

## ✅ The left hand works: lantern in the off hand, lighting the world (2026-09-17) `[reported 2026-09-17, n=1 wear]`
First headset wear of our GZDoomVR build. The lantern follows the left controller and its dynamic light moves with it.
Fixes after that wear (not worn yet): light radius halved (55/62), light colour blue-white, and the lamp no longer bakes grey:
its glow materials are plain Emission nodes, which the first bake ignored. The glow now flickers in the game's own three
brightness steps and measured 66-tic order (`lantern/NOTES.md`), as three skins on sprite frames LHLN A/B/C.
Stop-motion hand at 12 updates a second felt bad; now a frames-to-skip setting starting at 1. See `engine/README.md`.

## Lantern, second wear (2026-09-17) `[reported 2026-09-17, n=1]` and what changed (not worn yet)
Tefa, with two headset screenshots: glows blue now, but the glass is a solid blue tube (no inner tube, no sparks), the keypad
is mirrored, the lid screen should not flicker, and the lantern rubber-bands instead of being fixed to the hand. Stop-motion dropped.
- **Three actors instead of one** (`kit/gz_lantern.py`): body (opaque), glass (`RenderStyle Add`, alpha 0.35, so the inner tube
  shows), sparks (additive; one model frame per distinct lightning picture, 12 of them, played with the Blender timeline:
  610 tics, rare 1-2 tic strikes).
- **Mirror:** world models in this engine want MD3 +Y = LEFT; held-weapon (HUD) models want +Y = RIGHT `[verified-live 2026-09-17, n=1 each]`.
- **Flicker mask** is now only materials named `...Glow`; the lid screen and LEDs stay steady.
- **Rubber-banding:** fixed in the engine with `FollowOffhand` (see `engine/README.md`).

## Lantern, third wear (2026-09-17): locked to the hand, but flat textures `[reported 2026-09-17, n=1]`
Tefa's screenshots: see-through glass and keypad now right, but the body, lid and core were flat colours. Two causes, both in
`kit/gz_lantern.py`: (1) Blender's `smart_project` / `pack_islands` silently did nothing in background mode, and the bake went to
the lamp's original UV layer, where every face covers the whole 16x16 pixel texture; (2) glow materials were reduced to one flat colour.
Now: our own UV layout written in Python (each face flat at true size, shelf-packed, about 890 texels per metre in a 1024 atlas)
on a new layer that is both active and the render layer; glow materials are baked as they are (cloudy glass, white-hot core).
Checked by looking at the atlas: weathering, rust specks and the glass pattern are there. Not worn yet.
⚠️ The Blender file itself was never changed (export only reads it). Grey in Blender = the viewport is in Solid mode: press Z.

## Everything is unlit from now on (2026-09-17, Tefa's rule)
*"can we from now, not have the light source or anything shining on whatever is being made, so i know exactly what it will look like?"*
- `kit/pixel_kit.py`: every material is now a plain Emission shader at strength 1 (node `GameColor`); `metal`, `rough` and `emit`
  are ignored. `studio()` and `fp_view()` no longer add lights. `gz_bake.py` bakes the materials as they are.
- All weapon files rebuilt; new pictures `progress/2026-09-17-*-unlit-v1.png`. The muzzle-flash point lights still exist as objects
  (the animations key them) but light nothing.
- Lantern (hand-built file): converted by `kit/unlit_lantern.py`: non-glow materials show their base colour flat, lights and the
  studio floor removed. The lit version is kept as `lantern/Ashes_2063_EP1_lantern_v07_lit_backup.blend`.
- Consequence: highlights, shadows and chrome shine no longer exist anywhere; if we want them, they get painted into the texture.

## Gloved hands on the shotgun (2026-09-20)

Tefa's brief, with a Duke-style screenshot as the reference: *"add hands to the gun ... black
gloves, the line where the wrist should start, make that black leather as well and fingers showing
so like half-gloves"*, and *"make a new blender file, one with all the animation"*.

**Files**
- `kit/shotgun_hands.py` — the hands. Fingerless leather gloves: glove over the back of the hand,
  the palm and the first knuckle; middle and tip segments bare; a raised leather **cuff** at the
  wrist, with a dark sleeve past it so the cuff reads as a *line* rather than black-on-black.
- `kit/anim_shotgun_hands_all.py` — builds **one** file holding the gun, the hands and **every**
  animation on one timeline, with markers: `SHOOT` 1–30, `RELOAD_FULL` 43–206,
  `RELOAD_PARTIAL` 219–294.
- `shotgun/Ashes_2063_EP1_shotgun_hands_all.blend` and its `_static` twin.

**⚠️ The left hand is parented to `SG_Pump`, not to `SG_Root`.** A support hand parented to the gun
slides through the wood every time the action is racked. Checked both ways in
`shotgun/progress/hands-2026-09-20/` (`pump-forward.png` vs `pump-racked-back.png`).

**Why the driver re-runs the existing animation scripts instead of re-typing them.** The timing in
`anim_shotgun_shoot1.py` and `anim_shotgun_reload.py` was read tic-for-tic from the mod's own
`Actors/Weapons/Shotgun.txt`, and the 164-tic dry reload matches Tefa's 162-screenshot recording.
That is the expensive part and it is already right, so the driver runs those files with four of
their helpers replaced and keys everything into one scene at an offset. Neither file is edited, so
a timing fix there is a fix here.

**⚠️ Three traps this hit, all recorded because they will recur:**
1. **The sub-scripts re-import the kit at their top**, which re-defines `key()`, `finish()` and
   `link_model()` and throws away the replacements. The first run therefore **saved over all three
   real per-animation `.blend` files** (restored from git). The driver now strips those
   `exec(open(...))` lines, and makes `save_as_mainfile` raise while a sub-script is running.
2. **Fingers cannot be chained by stepping and rotating each segment in turn** — the drift
   compounds and every fingertip ends up standing off the wood like a row of bricks. They are
   placed on an arc around the grip's cross-section instead.
3. **Tan skin on the warm-brown pump is invisible**, which is exactly where the support hand sits.
   The skin tone is pulled pinker and flatter to separate it from both the wood and the steel.

**Everything about the hands' size, pose and colour is by eye** `[hypothesis]` — the reference is a
screenshot of a different game. Tefa judges it.
