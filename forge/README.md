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

**Still to do:** hands on each gun, upgrade variants (the episode 2 and Hard Reset "builds"), animations, and the
game export (the exporter cannot read forge models yet). The earlier hand-shaped guns in this repo are untouched.
