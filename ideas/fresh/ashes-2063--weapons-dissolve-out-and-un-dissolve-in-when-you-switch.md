# Weapons dissolve out and un-dissolve in when you switch

Order: 1
From: mod-ideas `games/ashes-2063.md` (<https://github.com/TefMeister/mod-ideas/blob/main/games/ashes-2063.md>), copied 2026-09-23

`[considered]` · `[looks doable]` — *the cheap version is ruled out; see the honest part below*

> "when changing weapons the previous weapon dissolves quickly and the new weapon 'un-dissolves'
> into players hand"

> "a dissolve into nothing and then the chosen weapon materialize into existance (reverse of
> dissolving)" — 2026-09-14, answering the question below

Replaces the standard lower-and-raise weapon switch: instead of the old gun sliding down off the
bottom of the screen and the new one sliding up, the old one **breaks up and vanishes on the spot**
and the new one **assembles into your hand** from nothing.

Verbatim record: [`inbox/2026-09-11-ashes-weapon-switch-dissolve.md`](../inbox/2026-09-11-ashes-weapon-switch-dissolve.md)

**Why it's filed here and not under Weapons:** it changes nothing about what switching *does* —
same guns, same speed, same rules — only what you see while it happens. Cross-referenced from
**Weapons & combat** below so it's findable from the obvious place.

**✅ Answered 2026-09-14: the real dissolve, and the cheap fade is out.** Your words: *"a dissolve
into nothing and then the chosen weapon materialize into existance (reverse of dissolving)."* That
settles two things at once — it is the **effect itself** you want, not merely the gun to stop
sliding; and the two halves are **one animation played forwards and backwards**, not two separately
designed effects. The second point is worth as much as the first: it halves the design work and it
means the two ends will match by construction.

**What it'd take:** the gun has to *erode* — eaten away in patches or specks — rather than fade
evenly, which means the effect must vary across the image instead of applying to all of it at once.
Two plausible routes:

- **Hand-made frames** of the weapon progressively eaten away. Certain to work, but it is art work
  per weapon, and every new gun costs again.
- **A shader** doing it properly. One piece of work covering all weapons, forwards and backwards —
  but it needs GZDoom to apply a shader to the **held-weapon sprite layer** specifically.

⚠️ **Not checked against the real engine.** The above is from knowing how GZDoom is built, not from
having tried it. **The one thing worth confirming before anything else: can a shader reach the
held-weapon layer?** That single answer decides which of the two routes this becomes — one-off work
or per-gun work — and it is a quick thing to find out.

⭐ **And the answer makes this worth more than one game.** Ashes and Doom 1 & 2 share GZDoom, so a
dissolve built here is a short step from the Brutal Doom weapons on the Doom page — which, since
2026-09-14, are 3D models. A shader route would carry across; hand-drawn erosion frames would not.
That is a second reason to answer the shader question first.

---
