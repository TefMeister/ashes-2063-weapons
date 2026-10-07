# Light probes — does the held cube gun catch the game's real lights? (2026-10-08)

Small test files that paint, onto the cube shotgun, what the engine's lighting actually receives, plus a
test light that floats ahead of and above the player. Built after the 2026-10-06 belief that "the held weapon
gets no normal and no position" — which turned out to be a misread (see below).

| file | what it makes |
| --- | --- |
| `build_light_probe.py <out dir>` | `lightprobe_A.pk3` (red = normal arrived, green = light list arrived, blue = light reaches the face), `lightprobe_B.pk3` (the normal as colour), `lightprobe_C.pk3` (the test light only, the gun keeps its paint) |
| `build_spec_probe.py <out dir> <shotgun pk3>` | `lightprobe_E.pk3`: the test light + a metal **shine map** made from the skin (grey = shiny, coloured = not) + a flat bump map, because the engine only switches to its shiny shader when BOTH are given (`hw_material.cpp`) |
| `light_probe_run.py <probe pk3> <shot.bmp> <log> [console cmd...]` | one unattended flat run: launch, OBS-record the game window, screenshot, run the console commands, screenshot again, quit |
| `md3_normals.py <pk3> <md3 path>` | counts the normals inside an exported md3 (zero / distinct) |
| `Play Ashes 2063 VR (light probe - *).bat` | the two headset shortcuts (copies of the ones in the game folder): probe A as "colours", probe E as "real shine" |

## What the flat runs proved (home PC, 2026-10-08, pictures in `_renders/live/light-probe-2026-10-08/`)
- The gun's normals arrive (every face its own axis colour), the light list arrives, and light reaches each face that
  faces the light: probe A is white on lit faces and yellow on faces turned away `[verified-live 2026-10-08, n=1]`.
- With its own paint the gun is plainly brighter and warmer next to the test light (gun mean 77/54/37 against 34/27/26
  without it) `[measured 2026-10-08]`.
- The shine map adds a faint sheen on the grey metal (`glossiness 3`, `specularlevel 1.5`; mean +0.7). Subtle: tune up
  if it cannot be seen in the headset. `glossiness` is raised to the 4th power by the engine, so 24 gave a pin-point nobody could see.
- The md3 exporter's normals are right (`kit/gz_md3.py` packs lat/lng the way `models_md3.cpp` unpacks them).

## Why the 2026-10-06 test said "black"
A readout written into `Material.Bright` is **multiplied** by the paint (`main.fp`: Bright is added to the LIGHT colour,
and the paint is then multiplied by that light), so a black paint always came out black whatever the normal was.
Probes A and B write the readout into `Material.Base` and set `Bright` to full white instead.

## Not yet proven
VR mode. The VR engine draws the gun in world space from the controller pose (`hw_models.cpp`, `PrepareRenderHUDModel`)
with the same lighting inputs, so it should behave the same `[inferred-static]`. The two desktop shortcuts are the check.
