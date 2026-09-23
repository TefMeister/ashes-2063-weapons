# Enemies come apart when you shoot them

Order: 8
From: mod-ideas `games/ashes-2063.md` (<https://github.com/TefMeister/mod-ideas/blob/main/games/ashes-2063.md>), copied 2026-09-23

`[raw]` · `[looks doable]` — *not tried; the honest limit is art, not code*

> "look at brutal doom and implement some of the dismembermet into the game."

Limbs and heads come off under fire, the way *Brutal Doom* does it, instead of enemies simply
falling over.

**What it'd take:** the behaviour is easy — GZDoom has done detachable gibs since forever and it is
a few lines of the game's own scripting language to say "this hit takes the arm off". The cost is
**pictures**: every enemy needs drawings of itself missing each piece, and of the pieces flying
away. Ashes does not ship those, and **Brutal Doom's own art cannot be copied over** — it belongs to
someone else, and this account never redistributes other people's assets. So the real question is
how much new artwork you want to sit through, and a cheaper first version could gib only on
overkill damage using generic chunks.

⚠️ Verdict unchecked against the real game.
