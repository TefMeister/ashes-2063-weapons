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
| `MapAttackDir()` | ⚠️ **RETRACTED — see the 2026-09-20 wear at the foot of this page.** It briefly used `GetWeaponTransformRaw()`; it now uses the two-handed matrix, so the bullet leaves the barrel you can see. The per-tic `AttackPos` block still uses the raw one, which is only the bullet's starting point and is the same either way. |
| `vr_two_handed_draw` (new setting, ON) | Options → VR Options, "Two-handed: turn the gun too". Switches the whole thing off for comparison without a rebuild. |

### ⚠️ ~~Why the shot deliberately uses the RAW transform~~ — **DISPROVED 2026-09-20, by a wear**

> ~~`MapAttackDir()` maps `AttackAngle` / `AttackPitch` through the weapon matrix. The aim block has
> **already** turned those onto the hand-to-hand line. Handing it the re-aimed matrix as well would
> apply the same turn a second time, and the shot would swing about twice as far as the gun.~~
> ~~`[inferred-static 2026-09-20]`~~

`[disproved 2026-09-20]` — **nothing on a bullet's path reads `AttackAngle` or `AttackPitch`**, so
there was no double application to avoid. The full reading of the call sites, and what it cost, is at
the foot of this page. Left here struck through rather than deleted, because the wrong reasoning is
the useful part.

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

---

## Worn 2026-09-20 — ✅ IT WORKS. And the shot did not follow it.

Tefa, in the headset, on the build above:

> "it does actually work!!! very cool, but the bullets still go to where i aim with right
> controller, not where the muzzle is pointed."

**So the drawing is right and stays.** `[verified-live 2026-09-20, n=1 wear]` The off hand swings the
front of a long gun and you can see it.

### ⚠️ The shot was wrong because of a wrong call made in this very document

The section above says the shot deliberately keeps the raw one-handed transform, "because
`AttackAngle`/`AttackPitch` are already turned onto the hand line and feeding the re-aimed matrix in
as well would apply the same turn twice". **That reasoning was wrong, and this is where it broke.**

A shot's direction does not come from `AttackAngle`/`AttackPitch` at all. It comes from the weapon
matrix, inside `MapAttackDir`:

- the `yaw`/`pitch` handed to `MapAttackDir` are the **actor's** angles plus whatever spread the
  weapon adds — `p_map.cpp` and `p_mobj.cpp` pass `source->Angles.Yaw` and friends, never
  `AttackAngle` `[inferred-static 2026-09-20, read from all five call sites]`;
- `MapAttackDir` then subtracts the actor's own angles, so what is left is **only the spread**;
- with no spread that leaves the identity, and the answer is exactly the matrix's forward axis.

So pointing it at the raw matrix did not prevent a double application — there was never going to be
one. It simply aimed the gun one way and sent the bullets another, which is precisely what the wear
found.

**Fixed:** `MapAttackDir` now takes the same two-handed matrix the gun is drawn with, so the bullet
leaves the barrel you can see by construction. `AttackAngle`/`AttackPitch` are derived from that same
matrix as well — nothing on the bullet's path reads them, but the laser-sight mod does, and a laser
that disagrees with the barrel is worse than no laser. One source, so they cannot drift apart.

⭐ **Worth keeping, because it is the second time the same shape of mistake has cost a wear:** the
first was shipping a correctness fix with no visible half; this was reasoning about which value feeds
which, from the names of the values, instead of reading the call sites. Both were caught by a wear
rather than by a check — and both were readable statically in about ten minutes.

`vr_two_handed_draw 0` still puts everything back, gun and shot together.
