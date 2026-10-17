# Vendored build dependencies

Everything the build and the tests need, so the project builds offline.

| Path | What | Licence |
| --- | --- | --- |
| `xdt99/xas99.py`, `xdt99/xcommon.py` | The xas99 TMS9900 cross-assembler from xdt99 by Ralph Benzinger, at the commit in `xdt99/COMMIT` (https://github.com/endlos99/xdt99) | GPL v3, see `xdt99/COPYING` |
| `sim9900.py` | The TI-99/4A simulator the tests run on, from the ti99-4a-dev skill (originally from The Lantern Coast) | MIT, (c) 2026 Rebecca Sutter |
| `render.py` | The simulator's screenshot renderer, with Graphics II added for this game | MIT, (c) 2026 Rebecca Sutter |
| `../booklet/fonts/` | Lora and Poppins (the guide's text and headings) and DejaVu Sans Mono (commands), with their licence files | Lora, Poppins: SIL Open Font License 1.1; DejaVu: Bitstream Vera licence |
| `../wheels/` (full distribution only) | Pillow, reportlab, pypdf and charset-normalizer wheels, pinned in `../requirements.txt`. Pillow is built per platform: Linux x86-64 and ARM64, macOS Apple silicon and Intel, Windows x64, each for CPython 3.12 and 3.13 | Pillow: MIT-CMU; reportlab: BSD; pypdf: BSD; charset-normalizer: MIT |
