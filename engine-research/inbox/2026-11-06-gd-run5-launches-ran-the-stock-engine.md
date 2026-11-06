# Gold Digger, 2026-11-06 (dev PC): the Run 5 test launches ran the stock engine with none of our files

Source: the Ashes shelves in the Gold Digger folder, read on the dev PC (they arrived from the home PC through the
synced folder: the two-PC hand-over works, Run 5 D7).

1. **Today's three launches (Run 5, D1-D5) loaded the stock GZDoomVR and no test pk3 of ours** `[measured 2026-11-06,
   n=3]`. Item `PC1-2026-11-06_09-58-53-787001` (run5.log): `GZDoomVR version gvr4.13.2.2`, engine files from
   `gzdoomvr/`, then the Ashes Enriched files only. The last flat check on 2026-11-02 (item
   `PC1-2026-11-06_08-40-24-e89014`, flatcheck.log, log dated 2026-11-02) ran our engine `gvr4.13.2.2-6-gf3815e7-m` from
   `gzdoomvr-tefa/` with eight test pk3s (cube revolver, pistol, shotgun, lantern with glove and left hand, forge guns of
   10-19 and 11-02, fire lights, VR fixes).
   What it means: a run started with the KNOWN.md command line (`-skill 3 +map MAP01 ...`) tests the game and the tools,
   not the mod. Fine for Run 5 (it tested the tools); wrong for any test of our guns.
   Proposed board row: `[PD] the Ashes launch route names the engine (ours or stock) and the -file list, and the run
   card says which one ran (the collector reads it from the log's version line). MODEL: SONNET.`
2. **The home PC's NVIDIA driver changed between 2026-11-02 and 2026-11-06: 617.42 -> 621.14** `[measured 2026-11-06]`
   (GL_VERSION lines of the two logs). Worth knowing when a VR result differs from before 11-06.
3. Flat at 1280x720 on the home PC, stock build: the game's own resolution line reads 1264 x 681 (the window's inside),
   script parsing 365 ms, peak memory about 420 MB, CPU about one core flat out while in front `[measured 2026-11-06, n=3]`.
