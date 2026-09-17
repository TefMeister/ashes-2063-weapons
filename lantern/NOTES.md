# Ashes 2063 EP1 lantern: rough sketch v01 (2026-09-15, home PC)

`Ashes_2063_EP1_lantern.blend` is our own model, built from scratch in Blender and not taken from the
game's files. No repo holds it yet; Ashes 2063 has no project repo.

## What is in it
- A cylindrical lamp with 12 sides on purpose, for a low-poly look. It has a top cap and dome, chrome
  rims, 8 cage bars, see-through glowing glass, a bright inner core, a bottom cap and foot, and a bail
  handle arching over the top on two pivots. It also has the orange and blue connector and the cable
  loop seen in the game sprite.
- Textures are tiny (16×16) with nearest-pixel filtering, so they look pixelated.
- A point light inside the lamp lights the floor. The fill light is there only so the metal shows up.

## The flicker was measured from the game, not invented
Source: 66 screenshots Tefa took on 2026-09-13 (15:11:20 to 15:15:37), stepping the game's recording one
frame at a time. The glow is **three fixed brightness steps**, not a smooth fade. Each frame was sorted by
counting bright core pixels and taking the average colour of the halo:

| Step | Core pixels | Halo red channel | Used in Blender (core / glass / light) |
| --- | --- | --- | --- |
| B bright | ~7,100 to 7,400 | 187 | 20 / 6.0 / 40 |
| M mid | ~6,600 to 6,900 | 186, smaller halo | 15 / 4.6 / 30 |
| D dim | ~6,100 to 6,500 | 180 to 182, bluer | 10.5 / 3.2 / 21 |

The order across the 66 frames, one letter per frame:

```
MDBMDBDBMDBDBBBDBDBBDBMDBDBMDBBMDBMBMDDMDMDDMDMDDMDBDDMDBMDMDBMDMD
```

Keys use CONSTANT interpolation (no blending, stop-motion). The scene runs at 35 fps on the
assumption that one recorded frame is one GZDoom tic. That is unchecked. ⚠️ There is a time gap
between 15:13:29 and 15:13:48 and another up to 15:14:27, so a few game frames may be missing there.
The brightness levels in Blender are scaled by eye; only the order and the three steps are measured.

## Next
- Take the real proportions from the sprite: cage height against width, and the rim thickness.
- Paint proper pixel textures, like the scratched grey metal in the game.
- Check the game's real animation speed.
- Later: weapons in the same stop-motion style.

## v02 tweaks (2026-09-16, from Tefa's drawn-over screenshots)
- The orange ball is the **handle grip**: a row of 6 orange balls with dark joints, riding the top of
  the grey handle, with a small blue ball at each end. The old single orange knob, blue knob and cable
  loop are removed (the cable loop was scribbled out; read as "remove" `[hypothesis]`).
- The glass is **one solid round cylinder**: the 8 cage bars are gone, and the glass, rims, caps, dome
  and foot are rebuilt as 24-sided smooth rounds.
- Flicker: the glow now holds each step for an uneven 2 to 11 frames (fixed random seed 2063), still in
  the measured B/M/D order, so one loop is 305 frames (about 8.7 s). The light cast outward barely
  changes (32 / 30 / 28), to avoid eye strain. The hold lengths are chosen by eye, not measured.
- ⚠️ Correction: v01 notes said the keys were CONSTANT, but they were saved as smooth (BEZIER). v02
  sets them to CONSTANT for real, and loops them.
- Backup of v01: `Ashes_2063_EP1_lantern_v01_backup.blend`.

## v03 refinements (2026-09-16, read from game shot "Screenshot 2026-09-13 151427.png", hand ignored)
Everything below is judged by eye from one low-resolution frame `[inferred-static]`, n=1.
- The handle is a **thin dark wire** (new material L_Wire), not a thick chrome bar. It comes down to
  the **rim edge** at each side rather than to pivots on the lid. The grip balls were re-seated on it,
  and the orange was pushed hotter and redder.
- The rims were only slightly wider than the glass in the shot: rim radius 0.100 → 0.092 and caps
  0.095 → 0.088. The rims got a small bevel and a paler, less mirror-like finish, so they read as the
  bright grey band seen in the game.
- The glass has a frosted pale-blue edge and a clearer, brighter middle (Layer Weight facing → mix).
  The bright core is wider (diameter 0.060 → 0.074), matching the white centre at about 45% of the
  glass width.
- Not changed, because the frame does not show them: glass height, the lid shape (hidden under the
  hand), the bottom. The vertical light streaks at the glass edges are left to the frosted-edge effect,
  not modelled as strips (strips would bring back the "sections" Tefa ruled out).
- The viewport was left looking through LanternCam. Backup of v02: `Ashes_2063_EP1_lantern_v02_backup.blend`.

## v04 rebuild from Tefa's side-view drawing (2026-09-16, "lantern 2.png")
Proportions measured off the drawing (1 px ≈ 0.000643 m, glass width 0.164 as the reference).
- Glass: one plain cylinder, 0.164 wide × 0.177 tall (a little taller than wide).
- Top: **one flat grey block** (radius 0.090, 0.032 tall), slightly wider than the glass. The chrome
  rim, the dark cap and the dome are gone.
- Bottom: a grey base that **flares outwards** (radius 0.082 at the glass → 0.095 at the floor, 0.0225 tall).
- Handle: a thin dark wire from a small knob on each side of the top block, out a little, **straight up,
  then straight across** with rounded corners, about 0.09 above the block.
- Grip: **one straight orange bar** across the top (0.174 long), replacing the row of balls. Small blue
  end caps were kept from the game shot; the drawing does not show them `[hypothesis]`.
- Open question: the blue zigzags drawn inside the glass (asked Tefa what they mean).
- Backup of v03: `Ashes_2063_EP1_lantern_v03_backup.blend`.

## v05 "fusion battery, year 2063" pass (2026-09-16)
Tefa: grip silver; look a little like a 2063 fusion battery part (direction not settled yet); the blue
zigzags in their drawing are real electric sparks; glass noticeably thick and weathered. They also
shared the in-world pickup sprite: grey top with a blue band, glass section, blue band, and a grey
lower section with a small front detail. The new lower section is based on that `[inferred-static]`, n=1.
- Grip bar is silver (L_Silver); blue end caps kept.
- New glowing blue band (L_BandGlow) under the top block, and a grey collar with a blue band under the glass.
- New **fusion cell** under the glass: grey body 0.12 tall, two dark grooves, 13 dark cooling ribs, and a
  front port facing the camera side with a glowing indicator and a blue readout slot. Foot and floor
  moved down (floor z = -0.245).
- Glass: real wall thickness (open tube + Solidify 0.012 inward). Weathering is procedural and snapped to
  3 mm blocks for a pixel look: dark grime noise, heavier near top and bottom, plus light Voronoi-edge
  scratches. The middle was kept fairly clear so the sparks show through.
- Sparks: 14 jagged glowing blue zigzag lines between the core and the glass wall. Each pops on for 1–3
  frames at uneven moments, sometimes 2–3 at once (seed 2063), stop-motion keys, loops with the 305-frame
  cycle. The outgoing lamp light is not tied to the sparks, to avoid eye strain.
- LanternCam moved closer, framing the whole lantern. Backup of v04: `Ashes_2063_EP1_lantern_v04_backup.blend`.

## v06 lightning discharges + detailed lid (2026-09-16)
Tefa: drop the zigzag sparks; use lightning-shaped discharges, much rarer, hitting the inside of the
glass at uneven intervals, with only the faint flicker in between. The lid is the exposed end of a part
that slots into a round socket: a numpad, green and red lights, more shape. The whole thing is a
**makeshift lantern built from a glowing fusion-battery machine part**. They love the blocky glass and
light, and want it as the look for all future weapon work on older games (Doom, Heretic, Duke Nukem).
- Sparks removed. 16 branching **lightning bolts** (core → inner glass wall, 1–2 forks each) with a small
  glow flash where each hits the glass. Discharges come about 3 times per 17 s at uneven gaps: 1–3 quick
  strikes, 1–2 frames each, stop-motion. The loop was lengthened to 610 frames; the glow keeps its own
  305-frame cycle. The lamp light is not tied to them.
- Lid: raised insert flange; dark face; 36-tooth knurled grip band; 3×4 numpad on a raised panel (a few
  keys sit worn or pushed in); green, green and red status lights (red blinks unevenly); a small glowing
  readout; a power terminal boss; 3 bolts plus one empty bolt hole.
- Makeshift touches: a silver hose clamp round the lid with its screw housing (the handle wire hooks
  onto it), and black electrical tape wrapped round the silver grip.
- Backup of v05: `Ashes_2063_EP1_lantern_v05_backup.blend`.

## v07 keypad labels, lid texture, second wear layer (2026-09-17)
Tefa: keypad keys labelled 1–9 from the top left, then C, 0, E along the bottom row; keypad metallic grey;
the little screen gets a green striped backlight (their reference picture: dark green with brighter green
horizontal lines); the lid gets the same blocky pixel texture as the glass; one more layer of wear on
the whole lantern.
- Key labels are flat glowing pale-green letters on each key (LidKeyLabel00–32), read upright from
  the LanternCam side.
- Keys (L_KeyMetal) and keypad panel (L_KeyPanelMetal) are grey metal. The screen (L_Screen) is a green
  glow with 7 horizontal stripes.
- Lid top block, face and flange use L_LidBlocks: blue-grey blocks at three sizes (9, 4.5 and 2.2 mm)
  snapped together, like the picture.
- Wear layer: shared node group G_Wear, added to every solid material (not the floor or glow-only
  parts). On 2.5 mm blocks it adds dark grime patches, rust-brown spots and pale scratch lines, and it
  roughens grimy areas. The glass gets dark dirt smudges laid over the glow with the same pattern.
- Backup of v06: `Ashes_2063_EP1_lantern_v06_backup.blend`.

## Fourth wear: turn, size, and WHY the light did not follow the hand (2026-09-17)
Tefa, with a drawing: turn the lantern a sixth of a turn counter-clockwise (*"if the lid was a 6 slice pizza,
then move it one slice's worth"*), make it about twice the size, and — *"the light barely moves"* when the
lantern is waved while standing still, but *"moves accurately when the player is moving"*.
- Turn and size are MODELDEF, not the model: `AngleOffset 60` and `Scale 2.0` on every block
  (`MODEL_SCALE` / `YAW_OFFSET` in `kit/gz_lantern.py`). Our own flicker light drops 10 units instead of 5,
  to stay inside the glass of the bigger lamp. ⚠️ The turn direction is read from the drawing and from the
  engine source (`models.cpp`: `AngleOffset` rotates exactly like actor yaw, so + is counter-clockwise seen
  from above) `[inferred-static]`. If it comes out turned the wrong way, use `-60`.
- **The light was never ours.** Ashes lights the room with its own invisible actor, `LanternGlow`, which every
  weapon's lantern-on state spawns **at the player** roughly once a tic (`A_SpawnItemEx("lanternglow",0,0,8,0)`
  in `Actors/Weapons/*.txt`); its GLDEFS light `Lantern1` is **size 130, offset 0 36 0** — a 3.8 m blue glow at
  the player's chest. Ours is 55/62 at the hand. So the room light really was body-mounted, and waving the hand
  only moved the small one `[inferred-static]` — read out of the game's own pk3, not yet worn.
- Fix: the event handler now catches every `LanternGlow` as it spawns (`WorldThingSpawned`, by class name, so
  the mod still compiles without Ashes) and puts it on the lantern every tic, 36 units below the hand so its
  light lands inside the lamp. When the game's lantern is off, nothing spawns and nothing changes.
- Flat compile check passed (no script errors, reaches `player 1 of 1`). Not worn yet.

## Fifth wear: 30 back, a quarter smaller, and the "spotlight" is the game's lighting, not a light (2026-09-17)
Tefa: *"it needs turning back 30 degrees"*, *"make the lantern 25% smaller"*, and *"the light seems to be following
the lantern more, but still it's like there is a spotlight that follows me around"*.
- `YAW_OFFSET` 60 → 30, `MODEL_SCALE` 2.0 → 1.5, `LIGHT_DROP` 10 → 8.
- **The follow-me spotlight is not a light source at all, so no light of ours could ever beat it.** Ashes forces
  light mode 3 ("dark") with its own `lightmodepatch.pk3`. In every Doom light mode except the plainest, the engine
  derives a fog density from each sector's light level and fades surfaces to black **by distance from the eye**
  (`hw_lighting.cpp` `GetFogDensity`, `distfogtable[lightmode != LinearStandard]`, and `R_DoomLightingEquation` in
  `main.fp`, which takes `z = distance(pixel, camera)`). Whatever you stand next to is therefore the brightest thing
  in the room, wherever you point the lantern `[inferred-static]`.
- Fix: our MAPINFO now adds `gamedefaults { nolightfade }` (`LEVEL3_NOLIGHTFADE`), which switches that distance fade
  off and leaves light mode 3's dark look alone — so a surface is only bright if something really lights it.
  Switch: `KILL_LIGHT_FADE` in `kit/gz_lantern.py`. ⚠️ Not worn yet; it changes how the WHOLE game reads, and the
  likely cost is that far-away dark areas no longer fade into black.
- Loads clean on a flat screen into MAP01, no script or MAPINFO errors.
