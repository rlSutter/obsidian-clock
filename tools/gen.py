#!/usr/bin/env python3
"""Compile tools/game.py and tools/art.py into
  gen/tables.a99  - the engine's tables (copied into RAM with the program)
  gen/data.bin    - the data banks: compressed pictures and packed strings
Data banks start at bank DATA0 (after the loader and the program banks).
Never edit gen/ by hand: the build overwrites it."""
import os, sys, textwrap
sys.path.insert(0, os.path.dirname(__file__))
import game as G
import art as A

ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA0 = 3                       # bank 0 loader, banks 1-2 the program, data from bank 3
WRAP = 31

# ----------------------------------------------------------------- pictures
def nearest(c, choices):
    r, g, b = A.PAL[c]
    return min(choices, key=lambda k: (A.PAL[k][0] - r) ** 2 + (A.PAL[k][1] - g) ** 2 + (A.PAL[k][2] - b) ** 2)

def convert(im):
    """256x128 palette image -> 4096 pattern bytes + 4096 colour bytes, in VRAM
    order for the top two thirds of a Graphics II screen."""
    px = im.load(); pat = bytearray(4096); col = bytearray(4096); clash = 0
    for y in range(128):
        third, row, line = y // 64, (y % 64) // 8, y % 8
        for cx in range(32):
            run = [max(1, px[cx * 8 + i, y]) for i in range(8)]
            counts = {}
            for c in run: counts[c] = counts.get(c, 0) + 1
            top = sorted(counts, key=lambda c: -counts[c])
            if len(top) > 2: clash += 1
            fg = top[0]; bg = top[1] if len(top) > 1 else top[0]
            bits = 0
            for i, c in enumerate(run):
                cc = c if c in (fg, bg) else nearest(c, [fg, bg])
                if cc == fg and fg != bg: bits |= 0x80 >> i
            off = third * 2048 + (row * 32 + cx) * 8 + line
            pat[off] = bits; col[off] = (fg << 4) | bg
    return bytes(pat + col), clash

def lz(data):
    """literal run: 0nnnnnnn + n+1 bytes; match: 1lllllll + offset hi, lo (length l+3)"""
    out = bytearray(); lit = bytearray(); i = 0; n = len(data); heads = {}
    def flush():
        nonlocal lit
        while lit:
            chunk = lit[:128]; out.append(len(chunk) - 1); out.extend(chunk); lit = lit[128:]
    while i < n:
        best_len, best_off = 0, 0
        if i + 3 <= n:
            key = data[i:i + 3]
            for j in reversed(heads.get(key, [])[-48:]):
                if i - j > 8191: break
                l = 3
                while i + l < n and l < 130 and data[j + l] == data[i + l]: l += 1
                if l > best_len: best_len, best_off = l, i - j
                if l == 130: break
        if best_len >= 3:
            flush(); out.append(0x80 | (best_len - 3)); out += bytes([best_off >> 8, best_off & 255])
            step = best_len
        else:
            lit.append(data[i]); step = 1
        for k in range(i, min(i + step, n - 2)):
            heads.setdefault(data[k:k + 3], []).append(k)
        i += step
    flush()
    return bytes(out)

def unlz(src, size=8192):        # the engine's decoder, in Python, to check the encoder
    out = bytearray(); i = 0
    while len(out) < size:
        t = src[i]; i += 1
        if t < 0x80:
            out += src[i:i + t + 1]; i += t + 1
        else:
            l = (t & 0x7F) + 3; off = src[i] << 8 | src[i + 1]; i += 2
            for _ in range(l): out.append(out[-off])
    return bytes(out)

# ----------------------------------------------------------------- strings
strings = []          # (text bytes)
def sid(text, nl=True):
    if text == "":
        b = b"\r"
    else:
        lines = textwrap.wrap(text, WRAP) if len(text) > WRAP else [text]
        b = "\r".join(lines).encode("ascii") + (b"\r" if nl else b"")
    for ch in b:
        assert ch == 13 or 32 <= ch < 96, f"character {chr(ch)!r} not in the console font: {text}"
    strings.append(b)
    return len(strings) - 1

def main():
    out = []; e = out.append
    sid("")                                         # id 0: an empty line (and "no text")
    # vocabulary
    vocab = {}
    def word(w, i):
        k = w[:6]
        if k in vocab and vocab[k] != i: sys.exit(f"vocabulary clash: {w} ({k})")
        vocab[k] = i
    dirn = {d: n + 1 for n, d in enumerate("NSEWUD")}
    for d, ws in G.DIRS.items():
        for w in ws: word(w, dirn[d])
    verbid = {}
    for n, (v, ws) in enumerate(G.VERBS.items()):
        verbid[v] = 10 + n
        for w in ws: word(w, verbid[v])
    # nouns: words that share an object share an id
    groups = []
    for o in G.OBJECTS.values():
        s = set(o["nouns"]); merged = [g for g in groups if g & s]
        for g in merged: groups.remove(g); s |= g
        groups.append(s)
    nounid = {}
    for n, g in enumerate(sorted(groups, key=lambda g: sorted(g))):
        for w in sorted(g): nounid[w] = 64 + n; word(w, 64 + n)
    for w in G.NOISE: word(w, 0xFE)
    rooms = list(G.ROOMS); roomno = {k: i + 1 for i, k in enumerate(rooms)}
    objs = list(G.OBJECTS); objno = {k: i + 1 for i, k in enumerate(objs)}
    pics = [n for n, f in A.SCENES]; picno = {n: i for i, n in enumerate(pics)}
    flags, ctrs = {}, {"turns": 0}
    def flag(n): return flags.setdefault(n, len(flags))
    def ctr(n): return ctrs.setdefault(n, len(ctrs))

    # tables
    e("* generated by tools/gen.py - do not edit")
    for k, t in G.MSG.items():
        e(f"M{k.upper()[:5]:<6} EQU  {sid(t, nl=k not in ('scor1', 'more', 'again'))}")
    tl = [sid(t) for t in G.TITLE_TEXT]
    e("TITLES DATA " + ",".join(map(str, tl)) + ",-1")
    for v, i in verbid.items(): e(f"V{v.upper()[:5]:<6}EQU  {i}")
    e(f"NROOMS EQU  {len(rooms)}\nNOBJS  EQU  {len(objs)}\nSTARTR EQU  {roomno[G.START]}")
    e("* rooms: desc, picture, exits N S E W U D, pad")
    e("ROOMS")
    for k in rooms:
        name, desc, pic, ex = G.ROOMS[k]
        exits = [roomno[ex[d]] if d in ex else 0 for d in "NSEWUD"]
        e(f"       DATA {sid(desc)}\n       BYTE {picno[pic]}," + ",".join(map(str, exits)) + ",0")
    e("* objects: location, flags (1 take, 2 listed), noun, pad, room line, inventory line, description")
    e("OBJS")
    for k in objs:
        o = G.OBJECTS[k]
        loc = 255 if o["loc"] == "carried" else roomno[o["loc"]] if o["loc"] else 0
        fl = (1 if o.get("take") else 0) | (2 if o.get("list") else 0)
        rs = sid(o["room"]) if "room" in o else 0
        iv = sid("  " + o["inv"]) if "inv" in o else 0
        ds = sid(o["desc"]) if "desc" in o else 0
        e(f"       BYTE {loc},{fl},{nounid[o['nouns'][0]]},0\n       DATA {rs},{iv},{ds}")
    e("* vocabulary: six letters, id, 0")
    e("VOCAB")
    for k, i in vocab.items():
        e(f"       TEXT '{k:<6}'\n       BYTE {i},0")
    e("       DATA 0")

    COND = {"here": 1, "carry": 2, "room": 3, "flag": 4, "nflag": 5, "at": 6, "ncarry": 7, "ge": 8, "eq": 9}
    ACT = {"msg": 1, "set": 2, "clr": 3, "move": 4, "goto": 5, "score": 6, "win": 7, "die": 8,
           "exit": 9, "ctr": 10, "inc": 11, "look": 12, "get": 13}
    def enc(rule, auto):
        verb, noun, conds, acts = rule
        b = []
        if auto: b += [1, 0]
        else:
            b.append(dirn[verb] if verb in dirn else verbid[verb])
            b.append(0 if noun is None else 0xFF if noun == G.NONE else nounid[G.OBJECTS[noun]["nouns"][0]])
        b.append(0)                                  # the length, filled in below
        for c in conds:
            op = c[0]; b.append(COND[op])
            if op in ("here", "carry", "ncarry"): b.append(objno[c[1]])
            elif op == "room": b.append(roomno[c[1]])
            elif op in ("flag", "nflag"): b.append(flag(c[1]))
            elif op == "at": b += [objno[c[1]], roomno[c[2]] if c[2] else 0]
            elif op in ("ge", "eq"): b += [ctr(c[1]), c[2]]
        b.append(0)
        for a in acts:
            op = a[0]; b.append(ACT[op])
            if op == "msg": s = sid(a[1]); b += [s >> 8, s & 255]
            elif op in ("set", "clr"): b.append(flag(a[1]))
            elif op == "move": b += [objno[a[1]], roomno[a[2]] if a[2] else 0]
            elif op == "goto": b.append(roomno[a[1]])
            elif op == "score": b.append(a[1])
            elif op == "exit": b += [roomno[a[1]], dirn[a[2]], roomno[a[3]]]
            elif op == "ctr": b += [ctr(a[1]), a[2]]
            elif op == "inc": b.append(ctr(a[1]))
            elif op == "get": b.append(objno[a[1]])
        b.append(0)
        assert len(b) < 256; b[2] = len(b)
        return b
    for name, lst, auto in (("CRULES", G.RULES, False), ("ARULES", G.AUTO, True)):
        e(name)
        for rl in lst:
            bs = enc(rl, auto)
            for i in range(0, len(bs), 16): e("       BYTE " + ",".join(map(str, bs[i:i + 16])))
        e("       BYTE 0\n       EVEN")
    assert len(flags) <= 64 and len(ctrs) <= 16

    # data banks: pictures, then strings; nothing crosses a bank
    banks = [bytearray()]
    def place(blob):
        if len(banks[-1]) + len(blob) > 8192: banks.append(bytearray())
        addr = 0x6000 + len(banks[-1]); bank = DATA0 + len(banks) - 1
        banks[-1] += blob
        return 0x6000 + 2 * bank, addr
    e("PICTAB")
    total = 0
    for n, f in A.SCENES:
        raw, clash = convert(f()); z = lz(raw)
        assert unlz(z) == raw, n
        sel, addr = place(z); total += len(z)
        e(f"       DATA >{sel:04X},>{addr:04X}       {n}: {len(z)} bytes, {clash} colour clashes")
    e("* F18A palettes: 16 colours (>0RGB) for each picture, then the standard set")
    e("PALTAB")
    for n, f in A.SCENES:
        p = A.palette(n)
        e("       DATA " + ",".join(f">{v:03X}" for v in p[:8]) + f"     {n}")
        e("       DATA " + ",".join(f">{v:03X}" for v in p[8:]))
    e("STDPAL DATA " + ",".join(f">{v:03X}" for v in A.STDPAL[:8]))
    e("       DATA " + ",".join(f">{v:03X}" for v in A.STDPAL[8:]))
    e("STRTAB")
    for s in strings:
        sel, addr = place(s + b"\0")
        e(f"       DATA >{sel:04X},>{addr:04X}")
    os.makedirs(os.path.join(ROOT, "gen"), exist_ok=True)
    open(os.path.join(ROOT, "gen", "tables.a99"), "w").write("\n".join(out) + "\n")
    blob = b"".join(bytes(b) + b"\xff" * (8192 - len(b)) for b in banks)
    open(os.path.join(ROOT, "gen", "data.bin"), "wb").write(blob)
    print(f"gen: {len(rooms)} rooms, {len(objs)} objects, {len(vocab)} words, {len(strings)} strings, "
          f"{len(G.RULES)}+{len(G.AUTO)} rules, pictures {total} bytes, {len(banks)} data banks")

if __name__ == "__main__":
    main()
