# Darkness test: does the dark of the room hide the held gun? (2026-10-25)

`darkness_run.py <out dir>`: one unattended FLAT run of Ashes 2063 with the cube shotgun. A tiny pk3 (`pk3/`, built by
the script) holds the light of the sector the player stands in at 64, 96, 128 and 160 (`tefa_testlight`), and the gun
is pictured with `vr_gun_darkness` (engine/README.md item 6) at 0, 1 and 2. No recording.

## Result, home PC 2026-10-25 `[verified-live 2026-10-25, n=1, flat]`
Mean brightness of the gun area (0-255), same room light, only the setting changed:

| room light | 0 (old) | 1 (room's light) | 2 (darker) |
| --- | --- | --- | --- |
| 64 | 18.0 | 15.2 | 9.9 |
| 96 | 24.8 | 18.9 | 12.0 |
| 128 | 27.2 | 22.6 | 15.2 |
| 160 | 29.5 | 26.1 | 19.4 |

The gun darkens step by step, and at 2 in a dim spot it is close to black. Pictures: `D:\Claude shared screenshots\ashes-2063-weapons\darkness-2026-10-25\` (home PC).

⚠️ Test limit: at the MAP01 start the player stands on a small floor sector of its own, so changing its light darkened
the gun but not the room seen in the pictures. In a real dark room the gun and the room darken together. How dark
looks right is for the headset to say.
