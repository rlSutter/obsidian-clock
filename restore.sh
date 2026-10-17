#!/bin/sh
# Build The Obsidian Clock from this folder alone, offline, and prove the
# result matches the released cartridge byte for byte.
#   sh restore.sh          set up, build, verify, run the quick test suite
#   sh restore.sh --all    ... and every test suite (slow: several minutes each)
# Needs only Python 3.12 or 3.13.  Everything else is bundled: the assembler
# and simulator in vendor/, the fonts in booklet/fonts/, and (in the full
# distribution) the Python packages in wheels/.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$HERE"
PY=python3
if ! $PY -c "import PIL, reportlab, pypdf" 2>/dev/null; then
  echo "setup: installing the bundled Python packages into .venv (offline)"
  $PY -m venv .venv
  PY=$HERE/.venv/bin/python
  if [ -d wheels ]; then
    $PY -m pip install -q --no-index --find-links wheels -r requirements.txt
  else
    $PY -m pip install -q -r requirements.txt      # no bundled wheels: from PyPI
  fi
fi
$PY build.py
if (cd build && $PY -c "import hashlib,sys; h=hashlib.sha256(open('obsidian8.bin','rb').read()).hexdigest(); sys.exit(h != open('../checkpoint/SHA256').read().split()[0])"); then
  echo "restore: rebuild matches the released cartridge $(cat VERSION) byte for byte"
else
  echo "restore: WARNING - rebuild differs from checkpoint/obsidian8.bin"
fi
(cd booklet && $PY booklet.py >/dev/null && echo "restore: player's guide rebuilt in booklet/")
if [ "$1" = "--all" ]; then
  for s in walk other keys ford f18a nomem alock; do $PY test.py $s; done
else
  $PY test.py other
fi
