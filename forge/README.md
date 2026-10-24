# Ashes weapons, forge cube set (first pass, 2026-10-19)

Every weapon from all three Ashes episodes, built in mixed cube sizes with `blender-cubekit`'s forge
(`docs/FORGE.md` there). Each one is drawn from the game's own pickup and in-hand pictures, kept as close to them
as the cubes allow. Tefa asked for the whole set on 2026-10-19, to be refined together afterwards.

The `.blend` files are in the MEGA transfer folder, `Game Files/ashes-2063-weapons/3D blender/forge-2026-10-19/`
(not on GitHub). One preview sheet per weapon is in `renders/`.

| File | Weapon | Episode |
| --- | --- | --- |
| `revolver.py` | .45 revolver | 1, Dead Man Walking, 2 |
| `handgun.py` | 9mm Autoloader | 1, Dead Man Walking, 2 |
| `crowbar.py` | Crow-bar | all |
| `pump_shotgun.py` | Pump-action shotgun | 1, Dead Man Walking, 2 |
| `sawed_off.py` | Sawed-off shotgun | 1, Dead Man Walking, 2 |
| `machine_pistol.py` | Machine Pistol (Ingram) | 1, Dead Man Walking, 2 |
| `master_blaster.py` | Master Blaster flamethrower | all |
| `junker_musket.py` | Junker Musket | 1, Dead Man Walking, 2 |
| `pipe_bomb.py` | Pipebomb | all |
| `jackhammer.py` | JackHammer | 1, Dead Man Walking, 2 |
| `battle_rifle.py` | Battle Rifle (FAL) | 1, Dead Man Walking |
| `military_rifle.py` | Military Rifle (AR-15) | 2 |
| `killer_pig.py` | Killer P.I.G. | 2 |
| `lazer_gun.py` | Lazer Gun | 2 |
| `police_pistol.py` | Police pistol (S&W 5906) | Hard Reset |
| `lever_shotgun.py` | Lever-action shotgun | Hard Reset |
| `hunter_shotgun.py` | Hunter shotgun | Hard Reset |
| `modular_rifle.py` | Modular rifle | Hard Reset |
| `crossbow.py` | Crossbow | Hard Reset |
| `thumper.py` | Thumper grenade launcher | Hard Reset |
| `bowling_ball.py` | Bowling ball | Hard Reset |

Weapon names and lists were read from each episode's `Actors/Weapons/` files `[measured 2026-10-19]`.
Dead Man Walking ships inside the Episode 1 pack and uses the same weapons.

**Rebuild** one or all (Blender 5.2, no window):

```
python ../../blender-cubekit/forge_make.py "<blend folder>" renders pump_shotgun.py revolver.py
```

**In the game (2026-10-24):** `brutal-doom-3d-guns/tools/gz_forge_export.py` (one exporter for both games) exports a
forge gun with its hands as a still model held in the right hand; `brutal-doom-3d-guns/tools/forge_jobs.py` names the
class each one stands in for. Episode 1's crowbar, sawed-off, Ingram (all three builds), Master Blaster, Junker Musket,
pipe bomb, JackHammer, FAL, and the pump shotgun's upgraded build (`pumpaction2`) are in
`Ashes2063_forge_guns_VR_test.pk3` (MEGA `3D blender/forge-2026-10-19/gzdoom/`), loaded by
"Play Ashes 2063 VR (all 3D guns test)". The revolver, 9mm and pump shotgun Tefa shaped stay as they are.

**Still to do:** upgrade variants, animations, the Afterglow and Hard Reset weapons in their own episodes. The earlier
hand-shaped guns in this repo are untouched.
