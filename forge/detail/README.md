# Ashes weapons, DETAILED forge set (started 2026-11-02)

Tefa, 2026-11-02: *"really and i mean really dig into weapon images online to have a knowledge of little things like
screws, cavities, scratches, how the stocks look, where the hammers sit ... then please use blender and cubekit to modify
the existing weapons in ashes to have a LOT of small details to them, make them very complex and use different qube
sizes ... guns need to be about 1.5 times as big ... reduce the light reflection ... 2.5x ... the main theme for these
weapons is to mix both the games sprite looks and real life examples, then add a layer of post apocalyptic filters on
top with scratches, cloth, duct tape, rust, chipped parts, makeshift parts, like having a used soda bottle for a
canister on the flamethower."*

## How a detailed gun is made

1. **References first.** `../../tools/ref_photos.py` pulls free-licence photos from Wikimedia Commons (credits written
   to `SOURCES.tsv` beside them), `../../tools/ref_sheet.py` puts several on one sheet. The game's own in-hand and pickup
   pictures are copied from the game file beside them. All pictures stay in the MEGA folder
   `3D blender/refs-2026-11-02/<gun>/`, never in git. What was learned goes into `refs/<gun>.md`, in our own words.
2. **The design file** here (`<gun>.py`) builds the gun in three cube sizes with the forge, gun only (no gloves: the
   body rig's hands dock on). Every piece has its own part name; the main hand grip is the part called `grip`.
3. **The wasteland layer** (`_wasteland.py`): tape, cloth, wire, rust and pits, soot, chipped paint, tally marks,
   makeshift plates, hose clamps, the soda bottle. Then `cavity()` paints depth into grooves and corners (cube guns have
   no real shading, so without it a groove seen straight on is invisible), and `simplify()` keeps the face count sane.
4. **Build:** `python ../../../blender-cubekit/forge_make.py "<MEGA>/3D blender/forge-2026-11-02" "<...>/renders" <gun>.py`
5. **Into the game:** `python ../../tools/pack_detail_guns.py` exports every detailed gun whose .blend exists (1.5x,
   faint shine) into `forge-2026-11-02/gzdoom/Ashes2063_detailed_guns_VR_test.pk3`; the launcher
   "Play Ashes 2063 VR (detailed guns test)" loads it last so it wins over the older models.

## Insides and load

Only the outside skin of a cube model is turned into faces; cubes inside a solid part are never drawn. So a solid part
costs nothing inside, and a hollow shell would actually draw a second skin on its inside. Parts are left solid on
purpose. The load to watch is the skin: aim for 80 000 to 170 000 faces a gun (the heaviest first-pass gun already in
the game, the Master Blaster, is 120 000).

## Status

| Gun | Design | Faces | In the test pk3 |
| --- | --- | --- | --- |
| Revolver | `revolver.py` | 78 000 | yes (2026-11-02) |
| Master Blaster | `master_blaster.py` | 164 000 | yes (2026-11-02) |
| the other nine of Episode 1 | to do after Tefa's look at these two | | |
