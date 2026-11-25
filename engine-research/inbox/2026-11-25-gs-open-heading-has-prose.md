# /gs 2026-11-25: the board's OPEN heading has words inside its date brackets

status/ashes-2063-weapons.md line 80: `OPEN (2026-11-20, the Keeper's tidy: ...`

`gate-scan.sh --check` accepts exactly `OPEN (YYYY-MM-DD):` and rejects the whole block otherwise, so `/gates` counts
none of this project's open rows (the board's own comment above the block warns about this). Fix (modding lane, one
line): move the words out of the brackets, e.g. `OPEN (2026-11-20):` with the note on the next line or in an HTML
comment. Found by the weekly tidiness check (check 7).
