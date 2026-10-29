# A body and arms for the player in Ashes 2063 VR (started 2026-10-29)

Tefa, 2026-10-29, with a picture: *"based on this picture, start work on actually having a body and arms in Ashes
2063"*. The picture is fan art of the Ashes 2063 wanderer by **NotMuchNormal** (ArtStation), sent as a reference for the CLOTHING AND LOOK
only (Tefa, 2026-10-29); it is kept
in the MEGA folder (`ashes-2063-weapons/body/reference/`), not on GitHub, because it is their art.

## What the picture shows (the look to build, in our cube style)

- A dark brown **leather jacket**, worn and creased, hood up, ribbed knitted cuffs and waistband.
- **Black fingerless gloves**: the approved Ashes gloves (2026-09-23) already are these.
- Dark **jeans**, boots below the frame.
- An olive-grey **backpack** with buckled straps and pouches, a wrapped blade handle over the right shoulder.
- A gas mask with orange goggles under the hood: never seen from inside, so not built for first person (a mirror
  could show it later).

## What you would see in the headset

Looking down: the jacket's chest and front, the backpack's shoulder straps, the legs and boots.
Looking at your hands: jacket sleeves running from the gloves up to the shoulders, bending at the elbow where your
real elbow roughly is.

## How it is built

- **Parts, each its own piece** (the 2026-10-23 rule): torso (jacket + straps), hips, upper arm L/R, forearm L/R (sleeve
  + cuff), thigh L/R, shin L/R with boot, the gloves we have. No radio
  (Tefa, 2026-10-29: "the radio is not needed on the body rig"). Cube style, made with the forge like the guns.
- **The arms follow the controllers** with two-bone IK: the shoulder is placed from the head (lower and to the side,
  turning with the body), the hand is the controller, the elbow is solved between them, bending down and out. Arm lengths
  scale with the player's height.
- **The body turns with the head**, lagging a little behind it (so a glance sideways does not swing the chest), and
  sinks with crouching. The legs stand, step when you walk, and bend when you crouch.
- **Drawn every rendered frame, not every game tic.** A part moved only 35 times a second rubber-bands in the headset
  (seen with the lantern, 2026-09-17), so the body is placed by the engine at draw time, the way `FollowOffhand` already
  places the off hand. This needs a small engine addition (a "body rig": head + both hands in, part poses out).
- **Fits the rest:** presidentkoopa's holster rig puts guns on the hips and shoulders; with a real body, those holsters
  sit on our jacket. His rig also has a mirror that shows your body, which would show the gas mask and backpack.

## Steps

1. The look: a first set of cube parts from the picture, judged together in Blender.
2. The engine body rig: IK maths written and tested numerically first (as the two-handed aim was), then drawn.
3. Arms only in the headset first (the part that matters most), then torso, then legs.
