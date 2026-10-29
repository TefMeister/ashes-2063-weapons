# The body rig: a torso, arms and legs for the player, drawn every frame (2026-10-29, /pd, dev PC, Fable)

Tefa, 2026-10-29: *"please build a rough first version of the body, then we'll fix it at some point. main thing is
to get the mechanics and the plumbing and wiring right for ashes based on what we can do now, then worry about
the looks side of things"*, and later the same day: *"if you can already look into legs animating with player
speed that would be awesome"*. Both are in this build. **Nothing here has been run in the game or worn.**

## What was built

| Piece | Where | State |
| --- | --- | --- |
| The maths: head + two controllers in, ten part poses out | `engine/body_rig.h` (pure, no engine types) | 53 numeric checks pass `[verified-numerically 2026-10-29, n=53]` |
| Its test | `engine/body_rig_test.cpp`, `engine/run_body_rig_test.bat` (`--dump` prints the standing pose) | runs on either PC with the VS build tools |
| The engine side: `BodyPart` on any actor, the rig run once per rendered frame, parts drawn from it | `engine/gzdoomvr-body-rig.patch` (on top of quest-compat step 2a); dev PC tree `E:/Ashes2063VR-dev/src/gzdoomvr`, branch `quest-compat`, commit `629b030` | builds, RelWithDebInfo `[compile-verified 2026-10-29]` |
| A rough box body: ten parts in jacket / jeans / boot colours | `body/build_body_test.py` -> `body/gzdoom/Ashes2063_body_test.pk3` (6 KB, no Blender needed) | built; not loaded by any engine yet |
| Dev-PC test install | `E:/Ashes2063VR-dev/body-test/` (engine + DLLs + pk3), launcher `E:/Ashes2063VR-dev/Play Ashes 2063 VR - body test.bat` | deployed, hashes stamped (`deployed.sh`) |

## How it works, in one picture

```
   HMD pose ──► head centre (8 cm behind the lenses) ──► neck (12 cm below)
                                                          │
          hands' midpoint ──┐                              ├──► body yaw  (follows the head outside a 25° dead zone,
                            └─ 50 % ─────────────────────►│               half-pulled towards where the hands are)
                                                          │
             shoulders (±19 cm, 4 cm down) ◄──────────────┤──► TORSO (hangs 55 cm)  ──► HIPS (±10 cm hip joints)
                  │                                                                        │
   controller ──► wrist (6 cm behind, 2 cm below) ──► two-bone IK ──► elbow            ankle targets under each hip,
                  (pole: out, down, a little back)         │                            swung along the travel line
                                                UPPER ARM, FOREARM                     by the walk cycle (speed in)
                                                                                           │
                                                                       two-bone IK (knees forward) ──► THIGH, SHIN
```

- **Every joint comes from three tracked things** (head, left hand, right hand); everything else is an average
  adult's proportions for a 1.75 m player, scaled by `vr_body_height`. All of them are settings (`brg::Params`),
  not constants, because every one is a guess until someone stands in the headset `[hypothesis]`.
- **Each part is its own actor** carrying `BodyPart = 1..10`. The engine ignores the actor's position and angles and
  draws it at the rig's pose for THIS rendered frame, through the same chain a controller goes through
  (`GetPoseTransform`): the same door the lantern uses (`FollowOffhand`), so no rubber-banding.
- **Walking**: the player's game velocity (map units per tic -> m/s) drives a step cycle: 0.65 m per full cycle at
  full stride, feet alternate (never both off the floor), each swinging foot lifts 8 cm, the stride shortens with
  the speed and fades out over ~1/6 s when they stop, the feet settling back under the hips. The travel direction
  is taken RELATIVE TO THE FACING (velocity angle minus the player's angle) and rebuilt in headset space, so
  strafing steps sideways. Real-room steps (walking across the floor without the stick) do NOT move the legs yet.
- **Crouching**: the hips hang a fixed 55 cm under the neck, so a low head drops the hips and the two-bone legs bend
  at the knee (knee forward) with the feet staying on the floor. Standing tall, the hips are capped where the legs
  reach, a little lower mid-stride so a foot swung forward is still reachable.
- **Not tracked hand**: the sleeve hangs by the side rather than vanishing. **Out of reach**: the upper arm points at the
  hand and the forearm stops short (the glove is on the controller anyway).

## Settings (all `CVAR_ARCHIVE`, in the engine)

| Setting | Default | What it does |
| --- | --- | --- |
| `vr_body` | on | the rig runs and `BodyPart` actors are drawn from it |
| `vr_body_height` | 1.75 | the player's height in metres; every length scales with it |
| `vr_body_yaw_deadzone` | 25 | degrees of glance that do not turn the chest |
| `vr_body_yaw_rate` | 4 | per second: how fast the chest catches up |
| `vr_body_stride` | 0.65 | metres per full step cycle |
| `vr_body_step_height` | 0.08 | how high a swinging foot lifts |
| `vr_body_mirror` | off | flips every part left-for-right (see "what could be wrong") |
| `vr_body_debug` | off | prints yaw, neck, hips, elbows, speed and stride to the console every 120 frames |

## The model convention (what `body/build_body_test.py` writes, what `models.cpp` expects)

A part's md3: **+X along the part** (shoulder->elbow, elbow->wrist, hip->knee, knee->ankle; the body's FORWARD for
the torso and hips), **+Y the part's left, +Z the part's up**, origin at the part's upper joint (neck base for the
torso, hip centre for the hips), **centimetres with `Scale 0.01`** in MODELDEF. The part's "up" is the side its
up-hint points to: world up for an upper arm, the back of the hand (controller +Y) for a forearm, the body's forward
for a thigh and a shin (so a boot's toe sticks out along md3 +Z). In the engine the file's axes are turned into
the rig's frame by one fixed matrix (`kModelToPart` in `RenderModel`), then the usual MODELDEF scale and offsets.

## What is NOT established, and what each first sighting means

1. **Handedness.** Everything drawn at the off hand with `FollowOffhand` comes out mirrored (NOTES.md 2026-10-24),
   and where that swap happens is not found. The body parts go through the controller chain instead (the route
   the guns' hands take, which look right), so they SHOULD come out unmirrored `[inferred-static 2026-10-29]`. The
   box body is symmetric except for **a red patch on the OUTSIDE of the LEFT upper arm**. Red patch on the left
   arm, facing outward: fine. Red patch on the right arm, or on the inside of the left: set `vr_body_mirror 1`.
   (A mirror only ever flips each part about its own axis; which arm is where comes from the controllers.)
2. **The axis convention of the model files.** If the boxes point the wrong way (a thigh sticking out sideways, a
   torso lying flat) the fixed matrix `kModelToPart` has an axis crossed: that is a conversion bug, not a maths bug,
   and the numbers in the test still hold. The torso is the easiest to read: it must hang straight down from
   the neck with the straps on the chest.
3. **The proportions**: elbows too far out, shoulders too wide, the neck too low: turn `brg::Params` (a rebuild) or
   `vr_body_height`. Expected; this is the "fix it at some point" part.
4. **The travel direction of the steps.** Taken as velocity angle minus player angle; if walking forward makes the
   feet step sideways, that relation is wrong (rotate by the HMD-to-Doom yaw offset instead).
5. **Lighting and sector.** The actors sit at the player's position for the game (sector, light); drawing happens
   where the rig says. A part drawn through a wall into a dark sector will be lit by the player's sector.
6. **Flat screen**: the parts are hidden (`PlayInVR` false), so a flat run only proves the pack loads and the engine
   starts. The rig itself never runs without a headset: the simulator (OpenXR) cannot feed this OpenVR engine.

## How to try it (dev PC, flat first, then the headset)

```
E:\Ashes2063VR-dev\Play Ashes 2063 VR - body test.bat +vr_mode 0      (flat: must reach MAP01 with no script errors)
E:\Ashes2063VR-dev\Play Ashes 2063 VR - body test.bat                 (headset: SteamVR first)
```
Log: `E:\Ashes2063VR-dev\body-test\body-test.log` (the launcher turns `vr_body_debug` on: look for `body:` lines).
In the headset: look down (torso, hips, legs, boots); hold the hands out (sleeves from the gloves to the shoulders,
elbows bent down and out); walk with the stick (feet alternate); crouch (knees bend). Say what is wrong one thing
at a time; the fixes are mostly numbers.

## Later

- Real-room walking driving the legs (today only the stick does).
- A lean of the torso when crouching; a slight sway of the hips with the steps.
- Parts that scale with `vr_body_height` (the boxes are fixed centimetres).
- The look, together in Blender: jacket creases, hood, backpack with pouches and the blade handle, gloves already
  ours. presidentkoopa's holster rig (QUEST-COMPAT.md) will then have a body to hang the guns on.
- QuestZDoom's `player.PlayInVR` is what the pack checks; its off-hand weapon (step 2b) and this rig are
  independent, both on branch `quest-compat`.
