# Two-handed long guns, the half you can SEE (2026-09-20)

Companion to [`TWO-HANDED-AIM.md`](TWO-HANDED-AIM.md), which is about where the **shot** goes.
This one is about where the **gun** points, and it exists because the aim work, correct or not,
was invisible.

## Why this was needed

Tefa wore the two-handed build on 2026-09-20 and reported, unprompted:

> "Ashes problem is not shooting straight, but getting the left hand to move the front end of the
> barrel at all, right now all weapons are still one handed and left hand does not affect aiming at
> all visually."

⭐ **That is not a bug report about the aim code — it is the aim code working exactly as written.**
Everything built between 2026-09-18 and 2026-09-20 changed `AttackAngle` / `AttackPitch`, i.e. the
line the bullets leave along. Nothing ever changed `GetWeaponTransform()`, which is what decides
where the gun is **drawn**. The gun kept hanging off the weapon controller, the bullets quietly went
somewhere else, and from inside a headset that reads as "the left hand does nothing".

⚠️ **The lesson, worth more than the fix: in a headset the gun IS the feedback.** Shipping a
correctness change with no visible half costs a wear and teaches nobody anything. Visible first.

## The shape Tefa asked for

Confirmed in their own words, 2026-09-20:

> "the back of the gun has to be locked to the right controller as the anchor that moves with the
> right controller, and left controller moves the front end, so it doesn't really matter how far the
> controllers are apart, it's more the handle of the gun sits in the right hand and shoots to
> wherever the left controller is"

So:

- **Rear hand = the anchor.** It keeps the gun's position and the twist of the wrist (roll).
- **Off hand = the muzzle.** The barrel points at it.
- **Distance does not come into it.** Hands 10 cm apart and hands 80 cm apart give the same gun.
- **No button, no minimum separation, no agreement check.** Same deal as the aim side (2026-09-20).

⚠️ **The deliberate trade, unchanged:** with the off hand down at your side, the gun points at your
side. There is no one-handed long gun. Say so if it feels wrong in play.

## What changed in the engine

| Where | What |
| --- | --- |
| `two_handed_pose.h` (new) | The maths, on its own, in plain doubles. Given the rear hand's frame and both hand positions, it returns the frame the gun should be drawn in. |
| `GetPoseTransform()` (new) | The body of `GetHandTransformEx()`, split out so a pose we build ourselves goes through exactly the same chain as a real controller pose. Move-only. |
| `GetWeaponTransformRaw()` (new) | The old `GetWeaponTransform()`, unchanged. Still the fallback for everything. |
| `TwoHandedWeaponTransform()` (new) | Builds the two-handed pose. Returns false — and so falls back to the line above — if there is no player, the mod has not asked for two-handed on this weapon, either hand is untracked, or both hands are in the same place. |
| `GetWeaponTransform()` | Now: two-handed if it can, one-handed otherwise. |
| `MapAttackDir()` and the per-tic `AttackPos` block | Switched to `GetWeaponTransformRaw()`. **This matters** — see below. |
| `vr_two_handed_draw` (new setting, ON) | Options → VR Options, "Two-handed: turn the gun too". Switches the whole thing off for comparison without a rebuild. |

### ⚠️ Why the shot deliberately uses the RAW transform

`MapAttackDir()` maps `AttackAngle` / `AttackPitch` through the weapon matrix. The aim block has
**already** turned those onto the hand-to-hand line. Handing it the re-aimed matrix as well would
apply the same turn a second time, and the shot would swing about twice as far as the gun.
`[inferred-static 2026-09-20, read from MapAttackDir in gl_openvr.cpp]`

### `openvr_weaponRotate` is folded in, not applied on top

That setting (−50 in the Ashes test config) is the tilt that lines the barrel up with the
controller. The two-handed frame is built **from** the rear controller tilted by it, and then the
forward axis is replaced — so it is not applied again afterwards. Applying it on top would leave the
gun pointing 50° away from the off hand.

## What has been proved without a headset

- **`two_handed_pose.h`: 103 checks, 0 failures** (`run_pose_test.bat`), and five deliberate
  breakages — forward sign flipped, cross product order swapped, the up axis rebuilt the wrong way
  round, the hand-gap guard removed, the direction left un-normalised — **all five caught**
  `[verified-numerically 2026-09-20, n=103 checks]`.
- **The rebuilt engine runs and plays** (`tools/draw_test.py`): the new setting exists, is on by
  default, takes a value both ways, the shotgun still fires, and the long-gun handler still reports
  it is waiting only on a second tracked hand `[verified-live 2026-09-20, n=2 launches]`.
- **Nothing regressed**: `tools/grip_test.py` still passes on the same build
  `[verified-live 2026-09-20, n=1 launch]`.

⚠️ **Nothing here can see the gun turn.** That needs two tracked controllers. It is a headset job.

## What to look for in the headset

Launcher: **`Play Ashes 2063 VR (shotgun + two-handed test).bat`**. Take the shotgun, hold it with
both hands, and **move the left controller while keeping the right one still.**

| What you see | What it means |
| --- | --- |
| The front of the gun swings with the left hand | It works. Next question is whether the shots follow it — watch the red dot. |
| The gun still hangs off the right hand only | Switch on "Two-handed aim: print why" in VR Options and read the console. It names which of the four things is missing. |
| The gun points at the left hand but is rolled on its side | The twist is being taken from the wrong place. Say which way it is rolled and by roughly how much. |
| The gun points somewhere near the left hand but not at it | The barrel is not along the model's forward axis; it is a model offset, not this maths. |
| The gun jumps rather than sweeps as you move slowly | A rate fault, not a maths fault — say so and it gets looked at separately. |

If it is worse than before, **`vr_two_handed_draw 0`** in the console puts it back instantly.
