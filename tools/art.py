#!/usr/bin/env python3
"""Original scene art for The Obsidian Clock, drawn in TI-99/4A palette
indices at 256x128 (the top two thirds of a Graphics II screen).
Run directly to write art/*.png previews."""
import random, os
from PIL import Image, ImageDraw, ImageFont

W, H = 256, 128
# TMS9918A colours as RGB (index 0 unused: transparent = black here)
PAL = [(0, 0, 0), (0, 0, 0), (33, 200, 66), (94, 220, 120), (84, 85, 237), (125, 118, 252),
       (212, 82, 77), (66, 235, 245), (252, 85, 84), (255, 121, 120), (212, 193, 84),
       (230, 206, 128), (33, 176, 59), (201, 91, 186), (204, 204, 204), (255, 255, 255)]
BLK, MGRN, LGRN, DBLU, LBLU, DRED, CYAN, MRED, LRED, DYEL, LYEL, DGRN, MAG, GRY, WHT = range(1, 16)

def new(bg=BLK):
    im = Image.new("P", (W, H), bg)
    flat = []
    for c in PAL: flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    return im, ImageDraw.Draw(im)

def bands(d, y0, y1, c1, c2, pattern=(0, 1)):
    """dithered sky: alternate rows of two colours in a run"""
    for y in range(y0, y1):
        d.line([(0, y), (W - 1, y)], fill=c1 if (y // 2) % 2 == 0 else c2)

def gradient(d, y0, y1, cols):
    """stacked bands, with a two-row dither where one colour meets the next"""
    n = len(cols); h = (y1 - y0) / n
    for y in range(y0, y1):
        i = int((y - y0) / h)
        c = cols[min(i, n - 1)]
        frac = (y - y0) / h - i
        if i + 1 < n and frac > 0.75 and y % 2 == 0: c = cols[i + 1]
        d.line([(0, y), (W - 1, y)], fill=c)

def hills(d, base, amp, col, seed, step=8):
    r = random.Random(seed); pts = [(0, H)]
    y = base
    for x in range(0, W + step, step):
        y = max(base - amp, min(base + amp, y + r.randint(-4, 4)))
        pts.append((x, y))
    pts.append((W, H)); d.polygon(pts, fill=col)

def leaves(d, box, cols, n, seed, size=(3, 7)):
    r = random.Random(seed); x0, y0, x1, y1 = box
    for _ in range(n):
        x = r.randint(x0, x1); y = r.randint(y0, y1); s = r.randint(*size)
        d.ellipse([x - s, y - s // 2, x + s, y + s // 2], fill=r.choice(cols))

def pyramid(d, cx, base, w, h, tiers, col, shade, top_w=None):
    top_w = top_w or w // 5
    for i in range(tiers):
        t0 = base - h * i // tiers; t1 = base - h * (i + 1) // tiers
        ww = w - (w - top_w) * i // tiers
        d.rectangle([cx - ww // 2, t1, cx + ww // 2, t0], fill=col)
        d.line([(cx - ww // 2, t1), (cx + ww // 2, t1)], fill=shade)
    # stairway
    d.polygon([(cx - 6, base), (cx + 6, base), (cx + 3, base - h), (cx - 3, base - h)], fill=shade)

def text_big(im, s, y, col, scale=2):
    f = ImageFont.load_default()
    tmp = Image.new("L", (W, 16), 0); td = ImageDraw.Draw(tmp)
    w = td.textlength(s, font=f); td.text(((W / scale - w) / 2, 0), s, fill=255, font=f)
    tmp = tmp.crop((0, 0, W // scale, 14)).resize((W, 14 * scale), Image.NEAREST)
    px = im.load(); tp = tmp.load()
    for yy in range(14 * scale):
        for xx in range(W):
            if tp[xx, yy] > 128 and 0 <= y + yy < H: px[xx, y + yy] = col

# ---------------------------------------------------------------- scenes
def title():
    im, d = new(DBLU)
    gradient(d, 0, 90, [BLK, DBLU, DBLU, MAG])
    r = random.Random(4)
    for _ in range(40):
        x, y = r.randint(0, 255), r.randint(0, 50); im.putpixel((x, y), WHT)
    # the clock: an obsidian disc in a grey rim, rising behind the pyramid
    d.ellipse([88, 14, 168, 94], fill=GRY); d.ellipse([93, 19, 163, 89], fill=BLK)
    for a in range(12):
        import math
        t = a * math.pi / 6; x = 128 + 30 * math.cos(t); y = 54 + 30 * math.sin(t)
        d.rectangle([x - 1, y - 1, x + 1, y + 1], fill=LYEL)
    d.line([(128, 54), (128, 32)], fill=LYEL); d.line([(128, 54), (144, 62)], fill=LYEL)
    pyramid(d, 128, 112, 150, 48, 6, DGRN, BLK)
    hills(d, 112, 4, BLK, 9)
    leaves(d, (0, 100, 255, 128), [DGRN, BLK], 60, 2)
    text_big(im, "THE OBSIDIAN CLOCK", 100, LYEL)
    return im

def airstrip():
    im, d = new()
    gradient(d, 0, 60, [LBLU, LBLU, CYAN])
    d.ellipse([20, 10, 70, 24], fill=WHT); d.ellipse([40, 6, 90, 22], fill=WHT)
    d.ellipse([170, 16, 230, 28], fill=WHT)
    hills(d, 52, 6, DBLU, 3)
    hills(d, 62, 5, DGRN, 5)
    d.rectangle([0, 70, 255, 127], fill=MGRN)
    d.polygon([(90, 70), (166, 70), (255, 127), (0, 127)], fill=LGRN)   # the grass strip
    leaves(d, (0, 60, 255, 74), [DGRN, MGRN], 70, 7)
    # the biplane
    d.rectangle([60, 78, 180, 90], fill=WHT)                       # fuselage
    d.polygon([(180, 78), (205, 70), (205, 92), (180, 90)], fill=WHT)
    d.polygon([(196, 62), (210, 62), (206, 80), (196, 80)], fill=MRED)  # tail fin
    d.rectangle([80, 66, 150, 70], fill=MRED)                      # upper wing
    d.rectangle([75, 92, 160, 96], fill=MRED)                      # lower wing
    for x in (90, 140): d.line([(x, 70), (x, 92)], fill=BLK)
    d.rectangle([52, 76, 60, 92], fill=GRY)                        # cowling
    d.line([(50, 70), (50, 98)], fill=BLK)                         # propeller
    d.ellipse([84, 98, 96, 110], fill=BLK); d.ellipse([140, 98, 152, 110], fill=BLK)
    d.rectangle([108, 74, 122, 78], fill=BLK)                      # cockpit
    # Teo, leaning on the wing
    d.rectangle([164, 84, 170, 106], fill=DYEL); d.ellipse([162, 77, 172, 86], fill=LRED)
    d.rectangle([160, 76, 174, 78], fill=DYEL)                     # hat
    # the crate
    d.rectangle([214, 96, 244, 118], fill=DYEL)
    d.line([(214, 96), (244, 118)], fill=DRED); d.line([(244, 96), (214, 118)], fill=DRED)
    d.rectangle([214, 96, 244, 118], outline=DRED)
    return im

def trail():
    im, d = new(DGRN)
    gradient(d, 0, 128, [BLK, DGRN, DGRN, DGRN])
    d.polygon([(110, 128), (146, 128), (134, 40), (122, 40)], fill=DYEL)  # path
    leaves(d, (0, 0, 255, 60), [MGRN, DGRN, LGRN], 220, 11, (4, 10))
    leaves(d, (0, 60, 100, 128), [MGRN, LGRN, DGRN], 90, 12, (4, 9))
    leaves(d, (156, 60, 255, 128), [MGRN, LGRN, DGRN], 90, 13, (4, 9))
    for x in (20, 60, 196, 236):
        d.rectangle([x, 20, x + 8, 128], fill=DRED)
    r = random.Random(5)
    for i in range(26):                                            # the vines across the path
        x = 100 + r.randint(0, 56); y0 = r.randint(0, 20)
        pts = [(x + int(6 * __import__('math').sin(y / 9 + i)), y) for y in range(y0, 92, 4)]
        d.line(pts, fill=LGRN if i % 3 else MGRN, width=2)
    return im

def river():
    im, d = new()
    gradient(d, 0, 40, [LBLU, LBLU, GRY])
    hills(d, 36, 4, DGRN, 21)
    leaves(d, (0, 24, 255, 50), [DGRN, MGRN], 140, 22, (4, 8))
    d.rectangle([0, 52, 255, 96], fill=DBLU)
    r = random.Random(23)
    for _ in range(60):
        x, y = r.randint(0, 250), r.randint(54, 94)
        d.line([(x, y), (x + r.randint(4, 12), y)], fill=CYAN if r.random() < .6 else LBLU)
    for x in range(30, 230, 22):                                   # stepping stones of the ford
        d.ellipse([x, 70 + (x % 3), x + 12, 76 + (x % 3)], fill=GRY)
    d.rectangle([0, 96, 255, 127], fill=DYEL)
    leaves(d, (0, 98, 255, 127), [MGRN, DGRN], 50, 24)
    # the ceiba, roots like walls
    d.rectangle([14, 0, 44, 110], fill=GRY)
    d.polygon([(0, 112), (14, 80), (14, 112)], fill=GRY); d.polygon([(44, 80), (66, 112), (44, 112)], fill=GRY)
    d.line([(26, 10), (26, 100)], fill=WHT)
    leaves(d, (0, 0, 90, 22), [DGRN, MGRN], 50, 25, (5, 10))
    return im

def plaza():
    im, d = new()
    gradient(d, 0, 70, [GRY, LBLU, LBLU])
    hills(d, 64, 5, DGRN, 31)
    pyramid(d, 150, 84, 160, 62, 7, GRY, WHT)
    leaves(d, (70, 40, 230, 84), [DGRN, MGRN], 40, 32, (2, 5))
    d.rectangle([0, 84, 255, 127], fill=GRY)
    for y in range(88, 128, 8):                                    # flagstones
        d.line([(0, y), (255, y)], fill=BLK)
        for x in range((y // 8) % 2 * 16, 256, 32): d.line([(x, y), (x, y + 8)], fill=BLK)
    leaves(d, (0, 84, 255, 127), [MGRN, DGRN], 40, 33, (2, 5))
    # the stela in the foreground
    d.rectangle([28, 40, 62, 120], fill=WHT); d.rectangle([32, 44, 58, 116], fill=GRY)
    for y in range(50, 112, 10):
        d.rectangle([36, y, 44, y + 6], fill=BLK); d.rectangle([47, y + 2, 54, y + 6], fill=BLK)
    return im

def camp():
    im, d = new()
    gradient(d, 0, 50, [GRY, GRY, LBLU])
    leaves(d, (0, 0, 255, 60), [DGRN, MGRN, BLK], 200, 41, (5, 11))
    d.rectangle([0, 60, 255, 127], fill=DYEL)
    leaves(d, (0, 60, 255, 75), [DGRN, MGRN], 60, 42)
    d.polygon([(70, 112), (130, 40), (190, 112)], fill=LYEL)       # the tent
    d.polygon([(118, 112), (130, 64), (142, 112)], fill=BLK)       # its flap, open
    d.line([(130, 40), (130, 30)], fill=DRED)
    d.line([(70, 112), (40, 118)], fill=WHT); d.line([(190, 112), (222, 118)], fill=WHT)
    # the dead fire and a broken crate
    d.ellipse([20, 104, 50, 116], fill=GRY)
    for i in range(4): d.line([(24 + 6 * i, 112), (40 - 4 * i, 102)], fill=DRED, width=2)
    d.rectangle([206, 92, 236, 112], fill=DRED); d.line([(206, 98), (236, 98)], fill=BLK)
    return im

def summit():
    im, d = new()
    gradient(d, 0, 90, [DBLU, LBLU, LBLU, WHT])
    for cx, cy in ((40, 24), (200, 14), (150, 40)):
        d.ellipse([cx - 30, cy - 6, cx + 30, cy + 6], fill=GRY)
    leaves(d, (0, 80, 255, 100), [DGRN, MGRN], 120, 51, (3, 7))
    d.rectangle([0, 96, 255, 127], fill=GRY)
    d.polygon([(0, 96), (40, 88), (216, 88), (255, 96)], fill=WHT)
    # the shrine on top, its doorway sealed by a slab
    d.rectangle([70, 30, 186, 96], fill=GRY)
    d.rectangle([66, 24, 190, 32], fill=WHT)
    for x in range(74, 186, 14): d.rectangle([x, 34, x + 8, 40], fill=BLK)
    d.rectangle([108, 52, 148, 96], fill=BLK)                      # the doorway
    d.rectangle([110, 54, 146, 96], fill=DYEL)                     # the slab
    d.line([(110, 70), (146, 70)], fill=DRED); d.line([(128, 54), (128, 70)], fill=DRED)
    return im

def stairs():
    im, d = new(BLK)
    # steps dropping away into the dark, lit from behind by the lantern
    n = 12
    for i in range(n):
        y = 127 - i * 8; w = 236 - i * 16
        tread = [LYEL, LYEL, LYEL, DYEL, DYEL, DYEL, DRED, DRED, DRED, BLK, BLK, BLK][i]
        riser = [DYEL, DYEL, DYEL, DRED, DRED, DRED, BLK, BLK, BLK, BLK, BLK, BLK][i]
        d.rectangle([128 - w // 2, y - 7, 128 + w // 2, y - 3], fill=tread)
        d.rectangle([128 - w // 2, y - 2, 128 + w // 2, y], fill=riser)
    for i in range(n):           # the walls narrow with the steps
        y = 127 - i * 8; w = 236 - i * 16
        c = DRED if i < 4 else BLK
        d.rectangle([0, y - 7, 128 - w // 2 - 1, y], fill=c)
        d.rectangle([128 + w // 2 + 1, y - 7, 255, y], fill=c)
    for x in (4, 240):
        d.rectangle([x, 100, x + 10, 110], fill=BLK)
    return im

def hall():
    im, d = new(GRY)
    for y in range(0, 128, 10):
        d.line([(0, y), (255, y)], fill=BLK)
        for x in range((y // 10) % 2 * 20, 256, 40): d.line([(x, y), (x, y + 10)], fill=BLK)
    d.rectangle([0, 104, 255, 127], fill=DRED)
    for cx, kind in ((52, "serpent"), (128, "sun"), (204, "jaguar")):
        d.rectangle([cx - 30, 22, cx + 30, 86], fill=WHT); d.rectangle([cx - 26, 26, cx + 26, 82], fill=GRY)
        if kind == "serpent":
            import math
            pts = [(cx - 20 + i, 54 + int(10 * math.sin(i / 5))) for i in range(0, 40, 2)]
            d.line(pts, fill=MGRN, width=4); d.ellipse([cx + 14, 44, cx + 24, 54], fill=MGRN)
            im.putpixel((cx + 20, 48), BLK)
        if kind == "sun":
            d.ellipse([cx - 12, 42, cx + 12, 66], fill=LYEL)
            for k in range(8):
                import math
                t = k * math.pi / 4
                d.line([(cx + 14 * math.cos(t), 54 + 14 * math.sin(t)), (cx + 22 * math.cos(t), 54 + 22 * math.sin(t))], fill=DYEL, width=2)
        if kind == "jaguar":
            d.ellipse([cx - 18, 36, cx + 18, 72], fill=DYEL)
            for (ex, ey) in ((-7, 48), (7, 48)): d.ellipse([cx + ex - 3, ey - 2, cx + ex + 3, ey + 2], fill=BLK)
            d.polygon([(cx - 18, 40), (cx - 12, 30), (cx - 6, 38)], fill=DYEL)
            d.polygon([(cx + 18, 40), (cx + 12, 30), (cx + 6, 38)], fill=DYEL)
            for (sx, sy) in ((-10, 60), (10, 60), (0, 64), (-12, 44), (12, 44)): d.ellipse([cx + sx - 2, sy - 2, cx + sx + 2, sy + 2], fill=BLK)
    # torches
    for x in (12, 244):
        d.rectangle([x - 2, 50, x + 2, 80], fill=DRED); d.ellipse([x - 5, 38, x + 5, 52], fill=LYEL)
    return im

def chamber():
    im, d = new(BLK)
    gradient(d, 0, 128, [BLK, DRED, BLK])
    d.rectangle([0, 100, 255, 127], fill=DRED)
    # the altar and the clock
    d.rectangle([92, 76, 164, 104], fill=GRY); d.rectangle([86, 72, 170, 78], fill=WHT)
    d.ellipse([100, 22, 156, 76], fill=GRY); d.ellipse([104, 26, 152, 72], fill=BLK)
    import math
    for a in range(12):
        t = a * math.pi / 6
        d.line([(128 + 18 * math.cos(t), 49 + 18 * math.sin(t)), (128 + 23 * math.cos(t), 49 + 23 * math.sin(t))], fill=WHT)
    d.line([(128, 49), (128, 34)], fill=LRED); d.line([(128, 49), (138, 55)], fill=LRED)
    # fallen stones from the collapsed shaft, and the man under them
    for (x, y, w) in ((196, 92, 30), (214, 80, 24), (180, 104, 40), (226, 100, 30)):
        d.rectangle([x, y, x + w, y + 14], fill=GRY); d.line([(x, y), (x + w, y)], fill=WHT)
    d.ellipse([168, 98, 180, 108], fill=LRED); d.rectangle([176, 102, 196, 110], fill=DYEL)
    for x in (20, 236):
        d.rectangle([x - 2, 50, x + 2, 84], fill=DYEL); d.ellipse([x - 5, 38, x + 5, 52], fill=LYEL)
    return im

SCENES = [("title", title), ("airstrip", airstrip), ("trail", trail), ("river", river),
          ("plaza", plaza), ("camp", camp), ("summit", summit), ("stairs", stairs),
          ("hall", hall), ("chamber", chamber)]

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "art")
    os.makedirs(out, exist_ok=True)
    sheet = Image.new("RGB", (W * 2, H * 5))
    for i, (n, f) in enumerate(SCENES):
        im = f(); im.save(os.path.join(out, n + ".png"))
        sheet.paste(im.convert("RGB"), ((i % 2) * W, (i // 2) * H))
    sheet.save(os.path.join(out, "_sheet.png"))

# ---------------------------------------------------------------- F18A palettes
# 12-bit RGB per palette index.  The F18A's power-on palette is the 9918A's;
# on an F18A each scene loads its own tuned set.  Indices 1 (black) and 15
# (white) never change: the text window is white on black in every scene.
STDPAL = [0x000, 0x000, 0x2C3, 0x5D6, 0x54F, 0x76F, 0xD54, 0x4EF, 0xF54, 0xF76,
          0xDC3, 0xED6, 0x2B2, 0xC5C, 0xCCC, 0xFFF]
TUNED = {MGRN: 0x3A3, LGRN: 0x7C5, DBLU: 0x235, LBLU: 0x7AE, DRED: 0x832, CYAN: 0x9DE,
         MRED: 0xC43, LRED: 0xE86, DYEL: 0xA83, LYEL: 0xEC7, DGRN: 0x152, MAG: 0xA57,
         GRY: 0x998}
SCENEPAL = {
    "title":    {DBLU: 0x113, MAG: 0xB46, DGRN: 0x052, LYEL: 0xFC4, GRY: 0xAAA},
    "airstrip": {LBLU: 0x8BF, CYAN: 0xBDF, DBLU: 0x557, MGRN: 0x4A3, LGRN: 0x8C5,
                 DGRN: 0x263, MRED: 0xC33, DYEL: 0xB93, DRED: 0x732, LRED: 0xD97},
    "trail":    {MGRN: 0x382, LGRN: 0x6B4, DGRN: 0x132, DRED: 0x531, DYEL: 0x862},
    "river":    {DBLU: 0x345, CYAN: 0x9BB, LBLU: 0x79C, GRY: 0x887, DYEL: 0xA85,
                 DGRN: 0x142, MGRN: 0x372},
    "plaza":    {GRY: 0xBA9, LBLU: 0x8AD, DGRN: 0x253, MGRN: 0x483},
    "camp":     {LYEL: 0xDC9, DYEL: 0x974, GRY: 0x999, DRED: 0x622, DGRN: 0x142, MGRN: 0x372},
    "summit":   {GRY: 0xAA9, LBLU: 0x6AE, DBLU: 0x34A, DYEL: 0xA95, DRED: 0x743},
    "stairs":   {LYEL: 0xFB5, DYEL: 0xC72, DRED: 0x621},
    "hall":     {GRY: 0x99A, DRED: 0xA43, MGRN: 0x3A6, DYEL: 0xB82, LYEL: 0xFD6},
    "chamber":  {DRED: 0x711, GRY: 0xA98, LRED: 0xE97, DYEL: 0xC93, LYEL: 0xFC5},
}
def palette(scene):
    p = list(STDPAL)
    for k, v in TUNED.items(): p[k] = v
    for k, v in SCENEPAL.get(scene, {}).items(): p[k] = v
    assert p[1] == 0x000 and p[15] == 0xFFF, "black and white are the text window's"
    return p

def preview(scene, im):
    """the scene as an F18A shows it"""
    p = palette(scene); flat = []
    for v in p: flat += [(v >> 8 & 15) * 17, (v >> 4 & 15) * 17, (v & 15) * 17]
    im = im.copy(); im.putpalette(flat + [0] * (768 - len(flat)))
    return im

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "art")
    sheet = Image.new("RGB", (W * 2, H * len(SCENES)))
    for i, (n, f) in enumerate(SCENES):
        im = f()
        sheet.paste(im.convert("RGB"), (0, i * H))
        sheet.paste(preview(n, im).convert("RGB"), (W, i * H))
    sheet.save(os.path.join(out, "_9918a_vs_f18a.png"))
