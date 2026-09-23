# A left hand that is always there, on the left controller

Order: 6
From: mod-ideas `games/ashes-2063.md` (<https://github.com/TefMeister/mod-ideas/blob/main/games/ashes-2063.md>), copied 2026-09-23

`[raw]` · `[looks doable]` — *not tried; the route is one that already works for the lantern*

> "we need to have left hand showing and movable with left motion controller, if possible, dock onto the weapon
> as well, but main thing is, before even attempting docking, to have a left hand just there, visible, it's weird
> to not have it in vr."

Today the pistol has a gloved right hand, and a left hand appears only to push a new magazine in. The rest of the
time your left hand is simply missing, which feels wrong in a headset.

**Your order, and it matters:**
1. **First, just a hand.** A gloved left hand, same look as the pistol's, that is always there and follows the left
   controller.
2. **Only then, docking:** the hand snapping onto the weapon when you bring it close.

**What it'd take:**
- **Step 1:** the hard part is already solved. In our own build of the VR program, the lantern already follows the
  left controller and is drawn as a 3D model [verified-live 2026-09-17]. A hand is the same trick with a different
  model: a cube-built left glove, like the right one. One thing to decide: what the hand does while the lantern is
  in it (probably the lantern simply replaces the empty hand).
- **Step 2, docking:** `[hard]`. The engine already knows where both hands are, and already tells when the off hand
  is really on a long gun's fore-end (that is what two-handed aiming uses). Docking means hiding the free hand and
  showing a hand baked onto the gun instead, whenever the two are close. Doable in principle; timing it so it does
  not flicker is the work.

⚠️ **Not checked:** nobody has put a hand model on the left controller yet. The lantern proves the route; it does
not prove how a hand looks or feels there. Related: [Floating hands you can see](#floating-hands-you-can-see) is
the same idea for both hands.
