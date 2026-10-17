#!/usr/bin/env python3
"""Generate the game's tables and data, assemble the loader and the engine,
and pack build/obsidian8.bin (FinalGROM 99 "8" scheme):
  bank 0      header + loader
  banks 1-2   the engine and its tables, copied to RAM at >A000-DFFF
  banks 3...  data: compressed pictures, strings
Uses the bundled assembler in vendor/xdt99; XAS99=/path/to/xas99.py overrides it."""
import os, subprocess, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
XAS = os.environ.get("XAS99", os.path.join(ROOT, "vendor", "xdt99", "xas99.py"))
B = os.path.join(ROOT, "build"); os.makedirs(B, exist_ok=True)
VERSION = open(os.path.join(ROOT, "VERSION")).read().strip()
r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "gen.py")], capture_output=True, text=True)
print(r.stdout.strip()); 
if r.returncode: sys.exit(r.stderr)
def asm(src, out):
    cmd = ([sys.executable, XAS] if XAS.endswith(".py") else [XAS]) + ["-R", "-b", src, "-o", out, "-L", out[:-4] + ".lst"]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(src))
    if r.returncode or not os.path.exists(out): sys.exit(f"{src}:\n{r.stdout}{r.stderr}")
    if r.stdout.strip() or r.stderr.strip(): print(r.stdout, r.stderr)
    return open(out, "rb").read()
loader = asm(os.path.join(ROOT, "src", "bank0.a99"), os.path.join(B, "bank0.bin"))
engine = asm(os.path.join(ROOT, "src", "engine.a99"), os.path.join(B, "engine.bin"))
assert len(loader) <= 8192
if len(engine) > 16384: sys.exit(f"engine: {len(engine)} bytes, more than two banks")
print(f"loader {len(loader)} bytes, engine+tables {len(engine)} of 16384 bytes (RAM >A000-{0xA000+len(engine)-1:04X})")
data = open(os.path.join(ROOT, "gen", "data.bin"), "rb").read()
pad = lambda b, n: b + b"\xff" * (n - len(b))
image = pad(loader, 8192) + pad(engine, 16384) + data
n = 1
while n < len(image) // 8192: n *= 2
image = pad(image, n * 8192)
cart = os.path.join(B, "obsidian8.bin"); open(cart, "wb").write(image)
print(f"-> {cart} ({len(image)//1024}K, {n} banks), version {VERSION}")
