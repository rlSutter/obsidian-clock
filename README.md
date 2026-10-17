# The Obsidian Clock

An original illustrated text adventure for the TI-99/4A, in TMS9900 assembly.

1934. The rains are a day away from the Sierra del Humo. Somewhere beneath
the great pyramid lies the Obsidian Clock, the calendar stone of a forgotten
people, and Silas Grieve, a dealer in stolen relics, got here first. Find the
clock, and get out before the valley floods.

## Requirements

- TI-99/4A with 32K memory expansion
- A cartridge loader that takes FinalGROM 99 "8" images (FinalGROM 99, or
  js99er / Classic99 / MAME as a cartridge)
- No F18A or SAMS needed; it runs on a stock 9918A
- With an F18A, each scene loads its own tuned 16-colour palette (detected at
  start; the standard palette is put back, and the F18A relocked if the game
  unlocked it, when you quit or restart)

Load `build/obsidian8.bin` and choose THE OBSIDIAN CLOCK from the menu.

## Playing

Type one or two words: `GO NORTH` or just `N`, `TAKE LAMP`, `LOOK AT STELA`,
`INVENTORY` (or `I`). Directions are N S E W U D. `LOOK`, `SCORE`, `WAIT`,
`HELP`, `QUIT`. Any key continues past `--MORE--`.

Editing (the TI's arrows are FCTN-E/S/D/X; emulators send FCTN-S for both
Backspace and Left): FCTN-S or FCTN-1 deletes a letter, FCTN-E recalls the
last command, FCTN-D re-types it a letter at a time, FCTN-X or FCTN-3 clears
the line.
Examine everything. The perfect score is 100.

## Building

    sh restore.sh          # set up, build, check against the release, quick test
    sh restore.sh --all    # ... and every test suite (several minutes each)

Needs only Python 3.12 or 3.13. The full distribution bundles everything else:
the xas99 assembler and the test simulator in `vendor/`, the booklet's fonts in
`booklet/fonts/`, and the Python packages as offline wheels in `wheels/`
(Linux x86-64 and ARM64, macOS Apple silicon and Intel, Windows x64). The script
installs those into a private `.venv` if they aren't already available; nothing
is downloaded. See `vendor/README.md` for versions and licences.

On Windows, run the steps by hand:

    py -m venv .venv
    .venv\Scripts\python -m pip install --no-index --find-links wheels -r requirements.txt
    .venv\Scripts\python build.py
    .venv\Scripts\python test.py other

## How it's built

| Bank | Contents |
| --- | --- |
| 0 | cartridge header and loader: copies banks 1-2 to RAM at >A000, starts the engine |
| 1-2 | the engine (`src/engine.a99`) and the game's tables, run from RAM |
| 3-7 | data: ten LZ-compressed pictures and the game's text |

The engine is generic. The game is data:

- `tools/game.py`: rooms, objects, vocabulary, messages, and the rules
  (conditions + actions) that make up the puzzles. Edit this to change or
  write a game.
- `tools/art.py`: the scenes, drawn in TI palette colours at 256x128, and
  each scene's F18A palette (`SCENEPAL`; black and white stay fixed for the
  text window). Running it writes `art/_9918a_vs_f18a.png` to compare.
- `tools/gen.py`: converts the art to Graphics II patterns and colours
  (two colours per 8-pixel run), compresses it, wraps and packs the text,
  and writes `gen/tables.a99` and `gen/data.bin`. Never edit `gen/`.

Screen: Graphics II. Rows 0-15 are the picture; rows 16-23 a scrolling text
window using the console font from GROM.

## Player's guide

`booklet/` holds the printed player's guide: `guide-pages.pdf` (eight 5.5 x 8.5 in
pages in reading order) and `guide-print.pdf` (imposed on letter for duplex printing with the
usual long-edge flip; `guide-print-short-edge.pdf` for short-edge flip). `python3 booklet/booklet.py` (run inside `booklet/`)
rebuilds both.

## Licence

Original work. Engine, tools, story, text and art (c) 2026 Rebecca Sutter.
