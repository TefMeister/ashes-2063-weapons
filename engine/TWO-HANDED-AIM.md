# Two-handed long guns — the engine change, ready to apply

**2026-09-18, `/pd` on the dev PC. Nothing here has been built or worn — there is no GZDoomVR
source and no headset on this machine.** The maths is verified; the wiring is not.

---

## What was actually missing

Less than the board row implied. Our existing patch already gives mods **both hands, every tic**
(`OffhandValid`, `OffhandPos`, `OffhandDir`, `OffhandAngle/Pitch/Roll`, plus the weapon hand's
`AttackPos` / `AttackAngle` / `AttackPitch`), and `FollowOffhand` already lets a mod draw an actor
locked to the off hand on every rendered frame — that is how the lantern works today.

So a mod can already **draw** a rifle along the line between the hands. What it cannot do is make
the **shot** follow that line: aiming still comes from the weapon controller's own rotation. The
gun would look two-handed and shoot one-handed, and the mismatch gets worse the further the front
hand is from the trigger hand — exactly the long guns this is for.

**One thing is genuinely missing, and it is small:** when a mod asks for it, aim from the rear hand
*through* the front hand.

## The maths is done and checked

`two_handed_aim.h` — a pure function, no GZDoom and no OpenVR types. `two_handed_aim_test.cpp`
compiles **that same header** and runs it against ground truth written in plain geometry (due
north, thirty degrees up) rather than re-deriving it with the formula under test.

- **36/36 checks pass** `[verified-numerically 2026-09-18]`.
- The suite was proved able to fail by mutating the shipped header **ten** ways — pitch sign
  flipped, `atan2` arguments swapped, the aim line reversed, each guard removed, the separation
  threshold halved, the forward vector left unnormalised, a zero-length forward accepted, an
  absolute position leaked into the yaw, and the agreement guard's sign inverted. **All ten were
  caught**, and the header was restored and re-run at 36/36.
- ⚠️ The unnormalised-forward mutant **escaped the first version of the test**, and the fix is
  written into the test as a comment: a forward pointing the *same* way hides the bug, because the
  oversized dot product clamps to 1 and reads as perfect agreement. A *short* forward at a real
  angle is what bites. The original check is kept beside the new one.

Run it: `engine\run_aim_test.bat` (needs VS Build Tools; C++17, because the two named limits are
`inline constexpr` so the engine and the test share one definition of them).

## The two guards, which are the whole design

A line between two tracked points is a terrible aim vector exactly when the player is **not**
holding a rifle with both hands — and that is most of the time. Hands at the sides, off hand on a
ladder, off hand holding the lantern. Without guards the gun swings wildly and can fire backwards,
which in a headset reads as "the mod is broken".

1. **Minimum separation** — two nearly coincident points give pure tracking noise.
2. **Agreement with the gun** — the rear hand still says where the gun points. If the hand-to-hand
   line disagrees by more than the limit, the front hand is not on the fore-end. This one is
   unit-free, so it works whatever the map scale turns out to be, and it carries most of the weight.

**Refusing means "leave the aim exactly as it is today"**, so the worst case is the behaviour we
already have, never a wrong shot.

⚠️ **Both default numbers are guesses** (`kMinSeparation` 8 map units, `kMaxDisagreeDeg` 55°). They
are named in one place so replacing them is a single edit. The first headset session should replace
them with measurements from a comfortable rifle hold.

## The four edits, on the home PC

⚠️ **These are written as instructions, not as a unified diff, on purpose.** There is no GZDoomVR
source on this machine, so a diff's context lines could not be checked and would probably fail to
apply. Each anchor below is a line the existing patch already adds or touches, so they are easy to
find.

**1. Put the header where the engine can see it.** Copy `two_handed_aim.h` next to
`src/rendering/gl/stereo3d/gl_openvr.cpp`, and `#include "two_handed_aim.h"` at the top of that file.

**2. A new field the mod can set** — in `src/playsim/actor.h`, beside the `FollowOffhand` line the
existing patch adds:

```cpp
bool TwoHandedAim;    // set by a mod: aim shots from the weapon hand THROUGH the off hand
```

**3. Expose it to ZScript** — two places, both beside the `FollowOffhand` entries the existing
patch adds:

```cpp
DEFINE_FIELD(AActor, TwoHandedAim)          // in src/scripting/vmthunks_actors.cpp
```
```
native bool TwoHandedAim;                   // in wadsrc/static/zscript/actors/actor.zs
```

Note it is **writable** from ZScript, like `FollowOffhand`, not `readonly` like `AttackAngle`.

**4. The override itself** — in `gl_openvr.cpp`, **immediately after the "Off hand, for mods" block**
the existing patch adds (it must come after, so `OffhandPos` is this frame's):

```cpp
// Two-handed long guns (2026-09-18): when a mod asks, the shot follows the line between the
// hands instead of the rear controller's own tilt. Guarded; see engine/two_handed_aim.h.
if (player->mo->TwoHandedAim && player->mo->OffhandValid)
{
    tha::Hands hh;
    hh.rear_x  = player->mo->AttackPos.X;  hh.rear_y  = player->mo->AttackPos.Y;  hh.rear_z  = player->mo->AttackPos.Z;
    hh.front_x = player->mo->OffhandPos.X; hh.front_y = player->mo->OffhandPos.Y; hh.front_z = player->mo->OffhandPos.Z;
    const DVector3 fwd = player->mo->AttackAngle.ToVector(player->mo->AttackPitch);
    hh.fwd_x = fwd.X; hh.fwd_y = fwd.Y; hh.fwd_z = fwd.Z;

    const tha::Aim aim = tha::decide(hh, tha::Limits{ tha::kMinSeparation, tha::kMaxDisagreeDeg });
    if (aim.use)
    {
        player->mo->AttackAngle = DAngle::fromDeg(aim.yaw_deg);
        player->mo->AttackPitch = DAngle::fromDeg(aim.pitch_deg);
    }
}
```

⚠️ **The one line to check by eye when you have the source open:** how the weapon hand's forward
direction is obtained. `AttackAngle.ToVector(AttackPitch)` is the natural way to say it, but if
that helper is not available in this GZDoom version, build the vector from `weaponangles` a few
lines above instead — it is the same direction either way. Everything else uses fields the existing
patch already defines.

## The mod side

Nothing exotic — the lantern already does the hard part. Per tic, with the rifle selected:

```
let pmo = players[consoleplayer].mo;
if (pmo && pmo.OffhandValid)
{
    pmo.TwoHandedAim = true;              // ask the engine to aim down the hand line
    rifle.FollowOffhand = false;          // the rifle rides the WEAPON hand, not the off hand
    rifle.SetOrigin(pmo.AttackPos, true);
    rifle.angle = pmo.AttackAngle;        // and after the engine change, this IS the two-hand line
    rifle.pitch = pmo.AttackPitch;
}
else pmo.TwoHandedAim = false;            // one-handed, or the off hand is busy: back to normal
```

Set `TwoHandedAim` **false** whenever a one-handed weapon is out, or the shots for the handgun will
start following an idle left hand.

## What to test in the headset, and what each answer means

Hold the rifle with both hands and fire at something small.

- **Shots land where the barrel points** → done. Then tune the two numbers.
- **Shots land where they did before** → the override never fired. The guards are the likely
  reason: put the log line back in (`aim.sep` and `aim.disagree_deg` are returned for exactly
  this) and see which one refused. If `disagree_deg` sits around 20–40°, the limit is simply too
  tight for how you hold it.
- **Shots are consistently high or low by the same amount** → the pitch sign or the hand order. The
  maths is pinned by the test, so suspect step 4's forward vector first.
- **The gun swings wildly when the off hand moves away** → the guards are not firing at all; check
  step 2 actually compiled in as writable.

## Left to decide

- Both threshold numbers, in the headset.
- Whether the **rifle model** should ride the weapon hand (as above) or be drawn along the
  hand-to-hand line, which would look better when the hold is slightly off but means the barrel and
  the shot can disagree. Worth trying both — it is a one-line change in the mod, no engine rebuild.
- Which Ashes weapons count as long guns (`NOTES.md` lists Shotgun, SawedOff, Ingram, FAL, Musket,
  NapalmGun).
