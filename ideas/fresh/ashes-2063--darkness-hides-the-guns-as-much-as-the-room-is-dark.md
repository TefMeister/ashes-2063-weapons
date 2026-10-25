# Darkness hides the guns, as much as the room is dark

Order: 1
From: the ideas repo, `games/ashes-2063.md` (<https://github.com/TefMeister/mod-ideas/blob/main/games/ashes-2063.md>), copied 2026-10-25

`[raw]` · `[looks doable]` — *checked against our engine's code, not yet seen in the game*

> "just as light lights them up, darkness must really also hide the gun models depending how dark it is"

Lamps and fire already light the 3D guns. The other half: in a dark corner the gun should sink into the dark with
the room, and in pitch black be nearly gone, instead of staying lit as if a lamp were on it.

Verbatim record: [`inbox/2026-10-25h-guns-hide-in-darkness.md`](../inbox/2026-10-25h-guns-hide-in-darkness.md)
Shared with Doom 1 & 2 (Brutal Doom guns): both games run on the same engine, so one change covers both.

**What it'd take:** the engine brightens whatever you hold on purpose (an old Doom habit, so the weapon always
shows): in a half-dark room the gun is drawn at about one and a half times the room's light. A setting in our
engine that turns that brightening down, so the gun gets the room's own light; lamps, fire and muzzle flashes still
light it on top. Being built 2026-10-25.

⚠️ **Checked in the engine's code only.** How dark is right is for the headset to say.

---
