#!/usr/bin/env python3
"""Play The Obsidian Clock in the skill's simulator.  Each test types
commands as a player would and checks the text window.  --png renders
screenshots.  Uses the simulator bundled in vendor/."""
import os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "vendor"))   # the bundled simulator and renderer
if os.environ.get("SIM"):                           # SIM=/path/to/another simulator overrides it
    sys.path.insert(0, os.environ["SIM"])
import sim9900 as S
S.KEY_AT = 10**12
CART = open(os.path.join(ROOT, "build", "obsidian8.bin"), "rb").read()
PNG = "--png" in sys.argv

class Chord(frozenset):
    """several keys down at once: the simulator compares its held key with =="""
    def __eq__(self, pos): return pos in self
    __hash__ = frozenset.__hash__
FCTN = (0, 4)

class Game:
    def __init__(self, f18a=True):
        self.m = S.Machine(CART, f18a=f18a); self.cpu = S.CPU(self.m)
        self.cpu.pc = self.m.rw(self.m.rw(0x6006) + 2); self.log = []
    def run(self, n):
        for _ in range(n): self.cpu.step()
    def text(self):
        return [l.rstrip() for l in S.screen(self.m).split("\n")[16:]]
    def key(self, ch, hold=6000, gap=6000):
        self.m.held = S.key_pos(ch) if ch != "\r" else (0, 2); self.run(hold)
        self.m.held = None; self.run(gap)
    def fctn(self, ch, together=True, hold=6000, gap=6000):
        """FCTN + key: pressed together (as emulators send it) or FCTN first"""
        if not together:
            self.m.held = Chord({FCTN}); self.run(3000)
        self.m.held = Chord({FCTN, S.key_pos(ch)}); self.run(hold)
        self.m.held = None; self.run(gap)
    def typed(self):
        return [l for l in self.text() if l.startswith("> ")][-1]
    def until(self, pred, limit=40_000_000, step=20000):
        n = 0
        while n < limit:
            if pred(): return True
            self.run(step); n += step
        return False
    def prompt(self): return any(l.startswith("> ") and l.endswith("_") for l in self.text())
    def more(self): return any("--MORE--" in l for l in self.text())
    def cmd(self, s):
        for ch in s: self.key(ch)
        self.key("\r")
        out = []
        while True:
            ok = self.until(lambda: self.prompt() or self.more() or self.m.rw(0xF010))
            out.append(self.text())
            if self.more(): self.key(" "); continue
            break
        return out
    def joined(self, out): return " ".join(" ".join(l.strip() for l in scr) for scr in out)
    def png(self, name):
        if PNG:
            import render; render.render(self.m, os.path.join(ROOT, "build", name + ".png"))

def start(f18a=True):
    g = Game(f18a)
    assert g.until(lambda: any("PRESS ENTER" in l for l in g.text()), 6_000_000), "no title"
    g.png("title")
    g.until(lambda: len(g.m.chip_log) > 8 and list(g.m.chip_log[-4:]) == [0x9F, 0xBF, 0xDF, 0xFF])
    g.run(20000)
    g.key("\r")
    out = []
    while True:
        g.until(lambda: g.prompt() or g.more()); out.append(g.text())
        if g.more(): g.key(" "); continue
        break
    return g, out

results = []
def check(name, ok, detail=""):
    results.append(ok); print(f"{name:<12}", "ok " if ok else "FAILED", detail)

WHICH = [a for a in sys.argv[1:] if not a.startswith("-")] or ["walk", "other", "f18a", "keys", "ford", "nomem", "alock"]
if "walk" in WHICH:
    g, out = start()
    t = g.joined(out)
    check("start", "GRASS STRIP" in t and "SUPPLY CRATE" in t, t[-120:])
    g.png("airstrip")
    WALK = ["OPEN CRATE", "TAKE MACHETE", "TAKE LANTERN", "GET MATCHES", "LIGHT LANTERN", "N",
            "CUT VINES", "N", "N", "READ STELA", "E", "SEARCH TENT", "TAKE CROWBAR", "TAKE ROPE",
            "W", "S", "TIE ROPE", "N", "N", "PRY SLAB", "D", "D", "PRESS SERPENT", "PRESS SUN",
            "PRESS JAGUAR", "E", "FREE SILAS", "TAKE CLOCK", "W", "U", "U", "S", "S", "S", "S"]
    expect = {"OPEN CRATE": "INSIDE", "TAKE MACHETE": "TAKEN", "LIGHT LANTERN": "FLARES",
              "CUT VINES": "HACK", "READ STELA": "SERPENT WAKES", "SEARCH TENT": "CROWBAR",
              "TIE ROPE": "CEIBA", "PRY SLAB": "LEVER", "D": "", "PRESS JAGUAR": "EAST",
              "FREE SILAS": "OWE YOU", "TAKE CLOCK": "RAIN"}
    shots = {"N": None}
    for i, c in enumerate(WALK):
        o = g.joined(g.cmd(c))
        want = expect.get(c, "")
        check(c[:12], want in o, o[-90:])
        if c in ("N", "D", "E") and PNG: g.png(f"step{i:02d}")
        if g.m.rw(0xF010): break
    check("won", g.m.rw(0xF010) == 1 and g.m.rw(0xF004) == 100, f"over={g.m.rw(0xF010)} score={g.m.rw(0xF004)}")
    g.png("end")


if "f18a" in WHICH:
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import art as A
    # an F18A: found, unlocked, and each scene's palette loaded
    g, _ = start()
    check("f18a found", g.m.unlocked and g.m.rw(0xF01E) != 0, f"unlocked={g.m.unlocked}")
    pal = [g.m.palette.get(i) for i in range(16)]
    check("airstrip pal", pal == A.palette("airstrip"), " ".join(f"{v:03X}" for v in pal if v is not None))
    check("vdp regs", list(g.m.vregs[:8]) == [2, 0xC0, 6, 0xFF, 3, 0x36, 7, 1], " ".join(f"{v:02X}" for v in g.m.vregs[:8]))
    g.png("f18a_airstrip")
    g.cmd("N")
    pal = [g.m.palette.get(i) for i in range(16)]
    check("trail pal", pal == A.palette("trail"))
    g.png("f18a_trail")
    # quitting puts the standard palette back and locks it again
    g.cmd("QUIT"); g.until(lambda: any("PLAY AGAIN" in l for l in g.text())); g.run(50000)
    # the simulator's reset selects bank 0 itself; a real console doesn't, so
    # note the bank the game left selected when it reset
    _wb = g.m.wb
    def wb(a, v, _wb=_wb, m=g.m):
        _wb(a, v)
        if 0x6000 <= a < 0x8000 and not getattr(m, "console_resets", 0):
            m.bank_seen = m.bank           # up to the reset only: the loader runs again after it
    g.m.bank_seen = g.m.bank; g.m.wb = wb
    g.key("N")
    g.until(lambda: g.m.at_reset is not None if hasattr(g.m, "at_reset") else False, 2_000_000)
    ar = getattr(g.m, "at_reset", None)
    ok = ar is not None and [ar[1].get(i) for i in range(16)] == A.STDPAL and not g.m.unlocked
    check("f18a restored", ok, f"unlocked={g.m.unlocked}")
    check("bank 0 reset", getattr(g.m, "bank_seen", None) == 0 and getattr(g.m, "console_resets", 0) == 1,
          f"bank left selected={getattr(g.m, 'bank_seen', None)}")
    # already unlocked (left so by another program): found without a second unlock
    g = Game(); g.m.unlocked = True
    g.until(lambda: any("PRESS ENTER" in l for l in g.text()), 6_000_000)
    check("pre-unlocked", g.m.unlocked and g.m.rw(0xF01E) != 0 and g.m.rw(0xF050) == 0,
          f"unlocked={g.m.unlocked} weunlk={g.m.rw(0xF050)}")
    # a plain 9918A: nothing changes, and the probe's stray writes are undone
    g, out = start(f18a=False)
    check("9918a", g.m.rw(0xF01E) == 0 and not g.m.palette and list(g.m.vregs[:8]) == [2, 0xC0, 6, 0xFF, 3, 0x36, 7, 1]
          and "GRASS STRIP" in g.joined(out), " ".join(f"{v:02X}" for v in g.m.vregs[:8]))
    g.png("9918a_airstrip")
if "ford" in WHICH:
    # the clock taken with the rope still in hand: the ford must stop you, not
    # kill you, and the rope tied at the stela must get you home
    g, _ = start()
    for c in ["OPEN CRATE", "TAKE MACHETE", "TAKE LANTERN", "GET MATCHES", "LIGHT LANTERN", "N",
              "CUT VINES", "N", "N", "E", "SEARCH TENT", "TAKE CROWBAR", "TAKE ROPE", "W", "N",
              "PRY SLAB", "D", "D", "PRESS SERPENT", "PRESS SUN", "PRESS JAGUAR", "E",
              "TAKE CLOCK", "W", "U", "U", "S"]:
        g.cmd(c)
    o = g.joined(g.cmd("S"))
    check("ford blocks", "TORRENT" in o and g.m.rw(0xF010) == 0 and g.m.rw(0xF000) == 4, o[-90:])
    o = g.joined(g.cmd("TIE ROPE"))
    check("tie at stela", "STELA" in o and "SNAGS" in o, o[-90:])
    o = g.joined(g.cmd("S"))
    check("haul across", "HAUL" in o and g.m.rw(0xF000) == 3, o[-90:])
    o = g.joined(g.cmd("N"))
    check("back again", "HAUL" in o and g.m.rw(0xF000) == 4, o[-60:])
    for c in ["S", "S"]: g.cmd(c)
    o = g.joined(g.cmd("S"))
    check("ford win", g.m.rw(0xF010) == 1, f"over={g.m.rw(0xF010)} score={g.m.rw(0xF004)}")
if "nomem" in WHICH:
    # a console with no 32K: the 32K ranges hold nothing, and the bus floats
    # to the last value written (the worst case for a RAM check)
    class NoExp(S.Machine):
        bus = 0
        def _exp(self, a): a &= 0xFFFF; return 0x2000 <= a < 0x4000 or a >= 0xA000
        def rb(self, a): return self.bus >> 8 if self._exp(a) else S.Machine.rb(self, a)
        def rw(self, a): return self.bus if self._exp(a) else S.Machine.rw(self, a)
        def wb(self, a, v):
            if self._exp(a): self.bus = (v & 0xFF) << 8; return
            S.Machine.wb(self, a, v)
        def ww(self, a, v):
            if self._exp(a): self.bus = v & 0xFFFF; return
            S.Machine.ww(self, a, v)
    for f18a in (False, True):
        g = Game(f18a); g.m = NoExp(CART, f18a=f18a); g.cpu = S.CPU(g.m)
        g.cpu.pc = g.m.rw(g.m.rw(0x6006) + 2)
        shown = g.until(lambda: any("32K MEMORY EXPANSION" in l for l in S.screen(g.m).split("\n")), 2_000_000)
        text = [l.strip() for l in S.screen(g.m).split("\n") if l.strip()]
        check(f"no 32k msg{'/f18a' if f18a else ''}", shown, " | ".join(text))
        if not f18a: g.png("nomem")
        g.key(" "); g.run(100000)
        check(f"no 32k exit{'/f18a' if f18a else ''}", getattr(g.m, "console_resets", 0) == 1 and g.m.bank == 0)
    # and with the 32K there, the check passes and the game starts as before
    g = Game(False)
    check("32k present", g.until(lambda: any("PRESS ENTER" in l for l in g.text()), 3_000_000))
if "alock" in WHICH:
    # ALPHA LOCK down, with CRU output 21 left low (its state is up to the
    # console): the lock pulls keyboard row 4, FCTN's row, in every column
    class Locked(S.Machine):
        p5 = 0
        def cru_write(self, bit, v):
            if bit == 21: self.p5 = v
            S.Machine.cru_write(self, bit, v)
        def cru_read(self, bit):
            if bit == 3 + 4 and self.keycol < 6 and not self.p5: return 0
            return S.Machine.cru_read(self, bit)
    for chip in (False, True):
        g = Game(chip); g.m = Locked(CART, f18a=chip); g.cpu = S.CPU(g.m)
        g.cpu.pc = g.m.rw(g.m.rw(0x6006) + 2)
        assert g.until(lambda: any("PRESS ENTER" in l for l in g.text()), 6_000_000)
        g.until(lambda: len(g.m.chip_log) > 8 and list(g.m.chip_log[-4:]) == [0x9F, 0xBF, 0xDF, 0xFF])
        g.run(20000); g.key("\r")
        while True:
            g.until(lambda: g.prompt() or g.more())
            if g.more(): g.key(" "); continue
            break
        o = g.joined(g.cmd("OPEN CRATE"))
        check(f"alock typing{'/f18a' if chip else ''}", "INSIDE" in o, o[-70:])
        g.cmd("QUIT"); g.until(lambda: any("PLAY AGAIN" in l for l in g.text())); g.run(50000)
        g.key("Y")
        seen = g.until(lambda: any("STARTING A NEW GAME" in l for l in g.text()), 400000)
        back = g.until(lambda: any("PRESS ENTER" in l for l in g.text()), 6_000_000)
        check(f"alock Y{'/f18a' if chip else ''}", seen and back)
if "keys" in WHICH:
    g, _ = start()
    for ch in "INVX": g.key(ch)
    g.fctn("S")
    check("backspace", g.typed() == "> INV_", g.typed())
    g.key("\r"); g.until(g.prompt)
    check("bksp result", "CARRYING" in g.joined([g.text()]))
    for ch in "LOOKX": g.key(ch)
    g.fctn("S", together=False)
    check("fctn first", g.typed() == "> LOOK_", g.typed())
    g.fctn("1")
    check("fctn-1 del", g.typed() == "> LOO_", g.typed())
    g.fctn("3")
    check("fctn-3 erase", g.typed() == "> _", g.typed())
    for ch in "XYZ": g.key(ch)
    g.fctn("X")
    check("down clears", g.typed() == "> _", g.typed())
    g.fctn("E")
    check("up recalls", g.typed() == "> INV_", g.typed())
    g.fctn("X"); g.fctn("D"); g.fctn("D")
    check("right types", g.typed() == "> IN_", g.typed())
    g.fctn("Q")
    check("fctn-q none", g.typed() == "> IN_", g.typed())
    for _ in range(6): g.fctn("S")
    check("bksp floor", g.typed() == "> _", g.typed())
    o = g.joined(g.cmd("I"))
    check("still works", "CARRYING" in o)
if "other" in WHICH:
    g2, _ = start()
    for c in ["OPEN CRATE", "TAKE MACHETE", "N", "CUT VINES", "N", "N", "E", "SEARCH TENT", "TAKE CROWBAR", "W", "N", "PRY SLAB"]:
        g2.cmd(c)
    o = g2.joined(g2.cmd("D"))
    check("dark death", "FALL" in o and g2.m.rw(0xF010) == 2, o[-80:])
    # the parser
    g3, _ = start()
    check("unknown", "DON'T UNDERSTAND" in g3.joined(g3.cmd("XYZZY")))
    check("two words", "DON'T KNOW THAT WORD" in g3.joined(g3.cmd("TAKE BANANA")))
    check("not here", "DON'T SEE" in g3.joined(g3.cmd("TAKE CLOCK")))
    check("noway", "CAN'T GO" in g3.joined(g3.cmd("WEST")))
    check("go north", "VINES" in g3.joined(g3.cmd("GO NORTH")))
    check("inventory", "JOURNAL" in g3.joined(g3.cmd("I")))
    scr = g3.text()
    check("cleared", not any("VINES" in l for l in scr) and any(l.startswith("> I") for l in scr),
          " | ".join(l for l in scr if l.strip()))
    check("look at", "CLOCK WAS HIDDEN" in g3.joined(g3.cmd("LOOK AT THE JOURNAL")))

print(f"{sum(results)}/{len(results)} passed")
sys.exit(0 if all(results) else 1)
