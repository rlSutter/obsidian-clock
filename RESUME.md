# RESUME: The Obsidian Clock checkpoint

Checkpoint taken 2026-10-17 at **version 1.0**. Read this first when picking
the project up in a new session.

## Restore in a new session

1. Upload `obsidian-clock-1.0.zip` (2 MB; everything but the Python wheels) and
   unzip it. `obsidian-clock-1.0-full.zip` (65 MB) is the distribution with the
   wheels too, for building offline anywhere.
2. Run `sh obsidian/restore.sh`. It needs nothing from the network or the skill:
   the assembler (xdt99's xas99, commit in `vendor/xdt99/COMMIT`) and the
   simulator are in `vendor/`, the booklet fonts in `booklet/fonts/`. If Pillow,
   reportlab or pypdf are missing it installs them into `.venv`, from `wheels/`
   when present, otherwise from PyPI. It rebuilds, checks the cartridge against
   `checkpoint/obsidian8.bin`, rebuilds the player's guide, and runs the quick
   `other` suite (`--all` runs every suite).

## Where things stand

| Version | Change |
| --- | --- |
| 1.0 | Release: Rebecca confirmed every manual checklist on real use (F18A console and a stock 9918A console); same binary as 0.8 |
| 0.8 | Y/N answer echoed with STARTING A NEW GAME... / GOODBYE.; keyboard scans deselect ALPHA LOCK (CRU bit 21), which otherwise reads as FCTN; image now 128K |
| 0.7 | Loader checks for the 32K expansion and says so on screen instead of freezing (a stock console hung at its last screen) |
| 0.6 | Bank 0 selected before the console reset on N, so the cartridge stays on the TI menu |
| 0.5 | Flooded ford stops you instead of killing you; rope can be tied at the stela on the way out |
| 0.4 | Text window clears on each command; the command shows at the top |
| 0.3 | Backspace fixed (FCTN is keyboard row 4, not 3); arrow-key line editing and recall |
| 0.2 | F18A detection; per-scene tuned palettes; standard palette restored and F18A relocked on exit |
| 0.1 | Original game: engine, nine rooms, ten pictures, two-word parser |

Automated: 79/79 checks pass in seven suites (`walk` 37, `keys` 11, `other` 9,
`f18a` 8, `ford` 5, `nomem` 5, `alock` 4).  Note: the simulator's console reset selects bank 0 by
itself (a real console doesn't), which hid the 0.5 menu bug; the `bank 0 reset`
check records the bank the game leaves selected up to the reset.

Confirmed by Rebecca on real use: loading and title; every parser and keyboard
check (including the 0.3 arrow keys and 0.4 window clearing); the F18A's look;
six wrong-order/missing-tool checks; the dark-stairway death and the score +
PLAY AGAIN on death; and the full happy path (100/100).

Also confirmed since: every wrong-order check, every death (including the 0.5
ford warning and the flood timer), and F18A normal colours after QUIT/N and
the palette returning after a win and Y.

Status at 1.0: every manual checklist in the testing guide is confirmed,
including the 0.8 Y/N prompt on the 9918A console (likely cause of the hang:
ALPHA LOCK) and the no-32K message (the cause of the stock console's original
blue-screen freeze).  Open: the real-hardware observation table, recorded as
notes rather than pass/fail.

## Documents

- Player's guide booklet: `booklet/guide-print.pdf` (print, long-edge flip; short-edge variant alongside) and `guide-pages.pdf`; source `booklet/booklet.py`

- User manual (Claude Doc): https://claude.ai/code/artifact/08ce989f-424b-4296-954d-38beb7db881d
- Testing guide (Claude Doc, with the tick list): https://claude.ai/code/artifact/b0d926bf-2b4e-42ef-85e7-5a92f5839642

## Working conventions

- Game content is `tools/game.py`; art and F18A palettes are `tools/art.py`;
  never edit `gen/`. The engine is `src/engine.a99`, the loader `src/bank0.a99`.
- Every change: bump `VERSION`, rebuild, run all five suites, update the
  manual's credits line and the testing guide's counts, re-zip.
- Tests are slow (minutes per suite). Run suites in parallel in the
  background, each with its own log; never share a log file.
- The simulator holds one key at a time; `test.py`'s `Chord` helper holds
  several (needed for FCTN combinations). Its screenshots use a stand-in font.
- Keyboard column 0: `=` row 0, space 1, Enter 2, FCTN 4, SHIFT 5, CTRL 6
  (the skill's keyboard reference is ambiguous here and should be corrected).
- Rebecca's copyright line: original work only; no conversion of copyrighted
  games' art, text, music or levels.
