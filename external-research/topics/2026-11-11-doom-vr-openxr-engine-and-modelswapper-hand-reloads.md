# Two new public Doom-engine VR projects (Nov 2026): an OpenXR-native PC VR engine on UZDoom 5.0.1, and ModelSwapper's hand reloads for 3D guns

**Status:** 🆕 new · **Priority:** medium. Neither replaces our engine (`gzdoomvr-tefa`, with our off-hand and body-rig
patches); both bear on two open board rows: "ASHES RUNS ON THE PRETEND HEADSET" (the OpenComposite + OpenVR 1.16.8
rebuild, no simulator pictures) and the side-saddle shells "to be made usable by hand".

## What is public

Read online on 2026-11-11 (README files, release lists, commit lists through the GitHub viewer and API). Nothing was
downloaded. All `[reported 2026-11-11]`.

### GameOrDie007, *Doom VR* (created 2026-11-01; v1.2.3 on 2026-11-10; GPL-3.0-or-later program)

- **UZDoom 5.0.1** (the continuation of GZDoom) with a VR mode added, and its own **OpenXR** layer (`pcvr-xr/`, also
  GPL-3.0). Needs "a PC VR headset with an OpenXR runtime": Virtual Desktop, Steam Link, Quest Link. Standalone builds
  for Quest 3 / Quest 2 / Steam Frame from the same source.
- 3D guns "held in our own hands, with a trigger finger, recoil and a punch you throw yourself"; two hands on the
  shotgun (v1.2.2); a weapon wheel; "bullets where you aim" (v1.2.3); your own WADs and pk3s load from a "My WADs"
  folder. Tested on Quest 3 over Virtual Desktop at 90 frames a second.
- Source and build instructions are in the repo (`source/`, `pcvr-xr/`, a CMake switch `DOOMVR_PCVRXR`).
- Ashes 2063 is not named anywhere in its README; whether Ashes runs on UZDoom 5.0.1 is not known `[hypothesis]`.

### presidentkoopa, *ModelSwapper* 1.5 (`RS_ModelSwapper`, created 2026-08-12, no licence file) and the RSQ suite

- "Puts VR weapon models on the guns of any Doom weapon mod, and lets you reload them with your hands": the mod keeps
  its weapons, ammo and reload rules; ModelSwapper changes what is held, from 145 models in 19 VR weapon sets.
- **Hand reloads built from per-model "cards":** magazine (pull the empty, take one from a pouch, seat it, rack after
  empty), **pump (push shells into the port one by one, work the pump after a shot)**, break-open and revolver (open,
  load the rounds, flick shut). Seen working on QuestZDoom 17.3 "on the rig", not yet confirmed in a headset.
- PC VR build targets an engine the author calls **UZDXREMA** (also the target of `RS_Radiance`, "the lighting package
  for UZDXREMA", and `RSQ_UBQSeries`, updated today). No public UZDXREMA repository was found by name.
- `RSQ_QuestEngineSurvey` (2026-10-30 to 11-05): a teardown of emawind84's QuestZDoom, incl. a note on VR melee on stock
  QuestZDoom 17.3. `RS_Avatar` (2026-11-10): full-body player IK with body holsters.

### Engines and the game, checked and quiet

- GZDoom: last release g4.14.2 (2025-05-03). hh79/gzdoomvr: last release gvr4.13.2.2 (2025-01-24), last push
  2025-10-18. QuestZDoom (Team Beef): 1.6.2 "VR HUB Release" on 2026-09-30.
- Ashes 2063: no 2026 update found. ModDB refused the automated fetch (HTTP 403), so this is NOT a negative (rule 7);
  a web search shows a pk3-only Episode 1 build "v2.3" on ModDB, undated, and a GOG store listing of Ashes 2063.

## Why it matters here

1. **The pretend-headset row.** Our engine speaks OpenVR, so the OpenXR simulator needs OpenComposite, which refused
   the newer OpenVR interface and forced a second build against OpenVR 1.16.8 headers; screenshots through it still
   go unanswered. An engine that speaks OpenXR natively, from the same GZDoom family, shows the shape of the other
   route: OpenXR in the engine itself, no translation layer `[hypothesis]` that the simulator's pictures then work.
   Moving Ashes to it would mean carrying our patches across; this is a design note, not a recommendation.
2. **Hand loading.** ModelSwapper's pump card (shells pushed into the port one by one, pump worked after a shot) is the
   same interaction as the side-saddle shells Tefa decided to make usable by hand; worth reading as a design before
   writing ours (read only: no licence file, so nothing is reused).
3. **Arcade feel stays:** both keep the mod's own weapon logic and change only what is held, the same line Ashes is on.

## Next step it unlocks (modding side)

- When the pretend-headset row is next taken: note whether Doom VR's OpenXR layer starts in the OpenXR simulator and
  answers its screenshot requests (a five-minute check with Freedoom, no Ashes needed), to price the OpenXR route.
- Before building hand-loaded shells: read ModelSwapper's pump card report online (`card_pump.report.md`).

## Sources

- GameOrDie007, Doom VR: <https://github.com/GameOrDie007/Doom-VR> (README, releases v1.2-v1.2.3)
- UZDoom: <https://github.com/UZDoom/UZDoom>
- presidentkoopa: ModelSwapper <https://github.com/presidentkoopa/RS_ModelSwapper>; RSQ_UBQSeries
  <https://github.com/presidentkoopa/RSQ_UBQSeries>; RSQ_QuestEngineSurvey
  <https://github.com/presidentkoopa/RSQ_QuestEngineSurvey>; RS_Avatar <https://github.com/presidentkoopa/RS_Avatar>
- Team Beef, QuestZDoom: <https://github.com/Team-Beef-Studios/QuestZDoom>; hh79, gzdoomvr:
  <https://github.com/hh79/gzdoomvr>; ZDoom, GZDoom: <https://github.com/ZDoom/gzdoom>
- ModDB, Ashes Episode 1 pk3-only build (fetch refused, seen in search only):
  <https://www.moddb.com/downloads/ashes-episode-1ashes-2063pk3-only-v22>
