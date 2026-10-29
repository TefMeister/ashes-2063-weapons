# Running presidentkoopa's VR add-ons in Ashes: what our engine is missing (2026-10-29)

Tefa, 2026-10-29: *"please use all of it in Ashes, that will boost our mod quality by a gazillion %."*

presidentkoopa's add-ons ([RSQ_UBQSeries](https://github.com/presidentkoopa/RSQ_UBQSeries): distance grab, shield-saw,
lightsaber, holster rig, slow motion, laser sight, grappling hook, HP bars, arcade score, minibosses, Gun Bonsai for VR,
one accessibility menu) are pure ZScript, written for stock **QuestZDoom 17.3**. Ashes runs on **our patched GZDoomVR
4.13.2.2** on PC. His readme says the arcade parts read what monsters do rather than their names, so they should run on
Ashes's monsters too `[reported]`.

## The gap, measured from his code and both engines' sources `[inferred-static 2026-10-29]`

Read: every `.zs` in his repo (commit of 2026-10-28), QuestZDoom's engine (`DrBeef/gzdoom`, branch `questzdoom`) and
ours (`E:/Ashes2063VR-dev/src/gzdoomvr` on the dev PC, which builds).

| What his add-ons use | QuestZDoom | Ours | Used by |
| --- | --- | --- | --- |
| A real weapon in the OFF hand: `+OFFHANDWEAPON` / `bOffhandWeapon`, `player.OffhandWeapon`, `LAF_ISOFFHAND`, `ALF_ISOFFHAND`, `CHAN_OFFWEAPON` | yes (about 130 C++ lines over 20 files, plus the weapon scripts) | **no** | ShieldSaw, Saber, TacticalRig, GunBonsaiVR, LaserSight, Grapple, DistanceGrab, Score, HP bars |
| `OffhandDir(actor, angle, pitch)` as a function | yes | a FIELD of the same name (no mod of ours reads it) | Grapple, ShieldSaw (+ BD22Q's own scripts) |
| `player.PlayInVR` | yes | **no** | GunBonsaiVR, ShieldSaw, Saber |
| `WF_TWOHANDSTABILIZED` | yes | **no** | Score, ShieldSaw |
| `AttackPos/Dir/Angle/Pitch/Roll`, `OverrideAttackPosDir`, `OffhandPos/Angle/Pitch/Roll` | yes | yes | all |
| `vr_control_scheme`, `vr_height_adjust`, `vr_crouch_use_button`, `vr_secondary_button_mappings` | yes | no | read through `CVar.FindCVar`, so missing ones only fall back to defaults; nothing breaks |
| Rumble | his own (`A_Quake` based) | works anywhere | DistanceGrab, SlowMo, LaserSight |

So one engine job unlocks all of it: **teach our GZDoomVR QuestZDoom's script-side VR API.** Nothing of his has to be
edited, which keeps his add-ons updatable as he improves them.

## The plan

1. **Small pieces first** (script side of the engine, `wadsrc/`, plus a few C++ lines): `OffhandDir()` as a function
   (our field renamed, no mod uses it), `player.PlayInVR`, `WF_TWOHANDSTABILIZED`, `CHAN_OFFWEAPON`, the four settings.
   Then SlowMo, TopHPBars, Score, Accessibility, Miniboss should load: they need little or none of the off-hand weapon.
2. **The off-hand weapon**, ported from QuestZDoom's engine: the weapon flag, `player.OffhandWeapon`, its own psprite
   layer drawn at the off hand, its attacks fired from the off hand, its sounds. Then ShieldSaw, Saber, TacticalRig,
   LaserSight, Grapple, DistanceGrab, GunBonsaiVR.
3. **Ashes's own off hand**: the lantern lives there today. Decide with Tefa how the lantern, the shield-saw and the
   saber share the left hand (a holster on the rig is the obvious answer).
4. Each add-on loaded and checked flat on the dev PC, then worn at home.

QuestZDoom is GPL-3.0, as GZDoomVR is, so porting its engine code into ours is allowed with credit (DrBeef / Team
Beef, emawind84). Engine changes stay in our patch file (`gzdoomvr-gvr4.13.2.2-offhand-stopmotion.patch`).

His add-ons themselves carry no licence file, so they are not copied into any of our repos: they are loaded from his
own pk3s, as he ships them.

## Done so far

- **Step 1, 2026-10-29 (dev PC):** `gzdoomvr-quest-compat-step1.patch`, on top of the dev PC's engine tree (commit
  `85c33e8`, branch `quest-compat` there). `OffhandDir(actor, angle, pitch)` is now a function returning angle and pitch,
  exactly as QuestZDoom's (`MapOffhandDir`, our `MapAttackDir`'s maths on the off hand); our old field of that name is
  now `OffhandForward`. `player.PlayInVR` is set while the headset view is on. The off-hand weapon-state flags
  (`WF_OFFHAND*`) and `WF_TWOHANDSTABILIZED` exist with QuestZDoom's values, nothing sets them yet.
  The engine and its script pack build `[compile-verified 2026-10-29]`; the scripts have not been loaded by a running
  engine yet. ⚠️ The home PC's engine has the 2026-10-25 darkness change that this tree lacks: apply this patch on top
  of the main patch there.
- **Step 2a, 2026-10-29 (dev PC):** `gzdoomvr-quest-compat-step2a.patch` (apply after step 1). The data side of the
  off-hand weapon, copied from emawind84/gzdoom (questzdoom, "4.15pre"): `player.OffhandWeapon`,
  `PremorphWeaponOffhand`, `ohattackdown` (saved with the game and kept by the garbage collector), `WeaponState` widened
  to 32 bits (step 1's off-hand flags go past 16: without this they were silently cut off), the weapon flags
  `+WEAPON.OFFHANDWEAPON` / `NOHANDSWITCH` / `TWOHANDED` / `NO_AUTO_REVERSE`, the buttons `BT_OFFHANDATTACK` /
  `ALTATTACK` / `RELOAD`, and `CHAN_OFFWEAPON`. Nothing uses them yet. Builds `[compile-verified 2026-10-29]`.
- **Next, step 2b:** `p_pspr.cpp` from emawind: the `PSP_OFFHANDWEAPON` layer (1000000), `GetPSprite`/`P_SetPsprite`
  with a caller, the off-hand rows of the weapon-button table, `P_CheckWeaponButtons(hand)`, raising and lowering the
  off-hand weapon. Then the scripts (`weapons.zs`, `stateprovider.zs`, `attacks.zs`, `player.zs`), the attack flags
  (`LAF_/ALF_/RGF_/FPF_/TRF_ISOFFHAND` in `p_map.cpp` / `p_mobj.cpp`), drawing it at the off hand (`hw_weapon.cpp`), and
  the left trigger as `BT_OFFHANDATTACK` in `gl_openvr.cpp`. The two engines differ in version (4.13 vs 4.15pre), so
  each hunk is carried by hand, not merged.
