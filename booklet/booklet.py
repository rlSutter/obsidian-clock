#!/usr/bin/env python3
"""The Obsidian Clock - player guide, 5.5 x 8.5 in, eight pages.
Writes guide-pages.pdf (reading order, one page per sheet), and two imposed
print files, two-up on letter landscape, for duplex printing, folding and
stapling as a booklet: guide-print.pdf for printers that flip on the long
edge (the usual default) and guide-print-short-edge.pdf for short-edge flip."""
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Table, TableStyle, Spacer, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import os
G = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + os.sep   # bundled, with their licences
pdfmetrics.registerFont(TTFont("Lora", G + "Lora-Variable.ttf"))
pdfmetrics.registerFont(TTFont("Lora-I", G + "Lora-Italic-Variable.ttf"))
pdfmetrics.registerFont(TTFont("Pop", G + "Poppins-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Pop-M", G + "Poppins-Medium.ttf"))
pdfmetrics.registerFont(TTFont("Pop-B", G + "Poppins-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", G + "DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("Mono-B", G + "DejaVuSansMono-Bold.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Lora", normal="Lora", bold="Pop-M", italic="Lora-I", boldItalic="Pop-M")

W, H = 5.5 * inch, 8.5 * inch
INK = HexColor("#2a2420")
RUST = HexColor("#8c3b1f")
GOLD = HexColor("#c9a24a")
NIGHT = HexColor("#14142a")
PAPER = HexColor("#f4ede0")
RULE = HexColor("#c8b89a")

body = ParagraphStyle("body", fontName="Lora", fontSize=9.6, leading=13.4, textColor=INK, spaceAfter=6)
lead = ParagraphStyle("lead", parent=body, fontName="Lora-I", fontSize=10.4, leading=14.6)
h1 = ParagraphStyle("h1", fontName="Pop-B", fontSize=15, leading=18, textColor=RUST, spaceAfter=7)
h2 = ParagraphStyle("h2", fontName="Pop-M", fontSize=10.5, leading=13, textColor=RUST, spaceBefore=6, spaceAfter=3)
cmd = ParagraphStyle("cmd", fontName="Mono", fontSize=8.8, leading=12.5, textColor=INK, leftIndent=12, spaceAfter=6)
cap = ParagraphStyle("cap", fontName="Lora-I", fontSize=8.2, leading=11, textColor=HexColor("#6b5d50"), alignment=TA_CENTER, spaceAfter=8)
cell = ParagraphStyle("cell", fontName="Lora", fontSize=8.6, leading=11, textColor=INK)
cellh = ParagraphStyle("cellh", fontName="Pop-M", fontSize=8.2, leading=10, textColor=white)
cellm = ParagraphStyle("cellm", fontName="Mono-B", fontSize=8.2, leading=11, textColor=INK)

def C(t): return f'<font name="Mono">{t}</font>'

def table(rows, widths, head=True):
    data = [[Paragraph(x, cellh if (head and r == 0) else (cellm if c == 0 else cell)) for c, x in enumerate(row)]
            for r, row in enumerate(rows)]
    t = Table(data, colWidths=widths)
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
          ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
          ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE)]
    if head: st += [("BACKGROUND", (0, 0), (-1, 0), RUST)]
    t.setStyle(TableStyle(st))
    return t

def picture(c, path, x, y, w):
    h = w / 2
    c.setFillColor(NIGHT); c.rect(x - 3, y - 3, w + 6, h + 6, stroke=0, fill=1)
    c.drawImage(path, x, y, w, h)
    return h

# ------------------------------------------------------------------ pages
M_OUT, M_IN, M_TOP, M_BOT = 0.5 * inch, 0.62 * inch, 0.55 * inch, 0.62 * inch

def frame_for(page):
    left = M_IN if page % 2 else M_OUT      # odd pages sit right of the fold
    right = M_OUT if page % 2 else M_IN
    return left, M_BOT, W - left - right, H - M_TOP - M_BOT

def folio(c, page):
    c.setFont("Pop", 7.5); c.setFillColor(HexColor("#8a7a68"))
    c.setStrokeColor(RULE); c.setLineWidth(0.5)
    left, _, fw, _ = frame_for(page)
    c.line(left, M_BOT - 14, left + fw, M_BOT - 14)
    label = "THE OBSIDIAN CLOCK  \u00b7  PLAYER'S GUIDE"
    if page % 2:
        c.drawRightString(left + fw, M_BOT - 26, f"{label}    {page}")
    else:
        c.drawString(left, M_BOT - 26, f"{page}    {label}")

def flow(c, page, items, top_pad=0):
    left, bot, fw, fh = frame_for(page)
    f = Frame(left, bot, fw, fh - top_pad, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
    rest = list(items)
    f.addFromList(rest, c)
    if rest: raise SystemExit(f"page {page}: {len(rest)} item(s) did not fit")
    return f._y                      # where the text ended

def paper(c):
    c.setFillColor(PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)

def p_cover(c):
    c.setFillColor(NIGHT); c.rect(0, 0, W, H, stroke=0, fill=1)
    inset = 0.32 * inch
    c.setStrokeColor(GOLD); c.setLineWidth(1.2); c.rect(inset, inset, W - 2 * inset, H - 2 * inset, stroke=1, fill=0)
    c.setLineWidth(0.4); c.rect(inset + 4, inset + 4, W - 2 * inset - 8, H - 2 * inset - 8, stroke=1, fill=0)
    c.setFillColor(GOLD); c.setFont("Pop-M", 8.5)
    c.drawCentredString(W / 2, H - 0.85 * inch, "AN ILLUSTRATED ADVENTURE FOR THE TI-99/4A")
    pw = W - 1.1 * inch
    picture(c, "title.png", (W - pw) / 2, H - 0.95 * inch - pw / 2 - 0.22 * inch, pw)
    y = H - 0.95 * inch - pw / 2 - 0.22 * inch - 0.62 * inch
    c.setFont("Pop-B", 30); c.setFillColor(GOLD)
    c.drawCentredString(W / 2, y, "THE OBSIDIAN"); c.drawCentredString(W / 2, y - 34, "CLOCK")
    c.setStrokeColor(GOLD); c.setLineWidth(0.8)
    c.line(W / 2 - 0.9 * inch, y - 52, W / 2 + 0.9 * inch, y - 52)
    c.setFont("Lora-I", 12.5); c.setFillColor(PAPER)
    c.drawCentredString(W / 2, y - 74, "Sierra del Humo, 1934")
    c.setFont("Pop-M", 11); c.setFillColor(GOLD)
    c.drawCentredString(W / 2, 1.05 * inch, "PLAYER'S GUIDE")
    c.setFont("Pop", 7.5); c.setFillColor(HexColor("#a9a3c4"))
    c.drawCentredString(W / 2, 0.82 * inch, "Version 1.0  \u00b7  Requires the 32K memory expansion  \u00b7  F18A enhanced")

def p2(c):
    paper(c)
    flow(c, 2, [
        Paragraph("The Story", h1),
        Paragraph("The rains are a day away. When they break, the river will rise and the valley will drown, "
                  "and whatever lies in its ruins will be lost for another thousand years.", lead),
        Paragraph("You are <b>Dr. Ada Vance</b>, archaeologist. Your pilot, Teo, has just set his patched biplane "
                  "down on a grass strip hacked from the cloud forests of the Sierra del Humo. Somewhere beneath the "
                  "great pyramid beyond lies the <b>Obsidian Clock</b>: a disc of black volcanic glass carved with the "
                  "days of a lost year, the calendar stone of a forgotten people.", body),
        Paragraph("You are not the first to come looking. <b>Silas Grieve</b>, a dealer in stolen relics, made camp "
                  "in the ruins days ago, and nobody has seen him since.", body),
        Paragraph("Find the clock. Then get back to the plane before the water does.", body),
        Spacer(1, 8),
    ])
    left, _, fw, _ = frame_for(2)
    h = picture(c, "chamber.png", left + 3, 2.05 * inch, fw - 6)
    c.setFont("Lora-I", 8.2); c.setFillColor(HexColor("#6b5d50"))
    c.drawCentredString(left + fw / 2, 2.05 * inch - 16, "The clock chamber, as it appears with the F18A's tuned colors.")
    folio(c, 2)

def p3(c):
    paper(c)
    left, _, fw, _ = frame_for(3)
    flow(c, 3, [
        Paragraph("Getting Started", h1),
        Paragraph("What you need", h2),
        Paragraph("A TI-99/4A with the <b>32K memory expansion</b>, and the cartridge file <b>obsidian8.bin</b> on a "
                  "FinalGROM 99 or in an emulator such as js99er or Classic99. No disk drive, speech or SAMS is needed. "
                  "An F18A is optional: if you have one, the game uses it automatically.", body),
        Paragraph("Starting the game", h2),
        Paragraph("Choose <b>THE OBSIDIAN CLOCK</b> from the TI menu. The title picture appears and a short tune plays. "
                  "When it ends, press <b>ENTER</b>. Read the introduction, pressing any key at "
                  f"{C('--MORE--')}, and you will find yourself at the airstrip.", body),
        Paragraph("The game cannot save your progress, so set aside time to play in one sitting.", body),
        Paragraph("The screen", h2),
        Paragraph("The top of the screen shows a picture of where you are. The eight lines below it are the story. "
                  "When the game is ready for you, it shows a prompt and a cursor:", body),
        Paragraph("&gt; _", cmd),
        Paragraph("Each command you give clears the text and starts fresh: your command at the top, the answer "
                  f"beneath it. If an answer runs long, the game pauses at {C('--MORE--')}; press any key to read on.", body),
        Paragraph("Keys pressed while a picture is drawing or a tune is playing are not seen. If nothing happens, "
                  "wait a moment and press again.", body),
    ])
    folio(c, 3)

def p4(c):
    paper(c)
    flow(c, 4, [
        Paragraph("Giving Commands", h1),
        Paragraph("Type a command of one or two words and press <b>ENTER</b>: a verb, and usually the thing you "
                  "want to act on.", body),
        Paragraph("&gt; TAKE LAMP<br/>&gt; OPEN CRATE<br/>&gt; EXAMINE TREE", cmd),
        Paragraph("Moving", h2),
        Paragraph(f"Type a direction: {C('NORTH')}, {C('SOUTH')}, {C('EAST')}, {C('WEST')}, {C('UP')} or "
                  f"{C('DOWN')}, or just its first letter. {C('GO NORTH')} works too. Each description tells you "
                  "which ways lead somewhere.", body),
        Paragraph("Longer sentences", h2),
        Paragraph("The game reads the first two words that matter and skips small ones such as THE, A, AT, TO, WITH "
                  f"and IN. So {C('LOOK AT THE STELA')} means {C('EXAMINE STELA')}, and "
                  f"{C('CUT VINES WITH MACHETE')} means {C('CUT VINES')}. You never need to say what you are using: "
                  "if you are carrying the right thing, it works.", body),
        Paragraph("Only the first six letters of a word count, so LANTERN and LANTERNS are the same word.", body),
        Paragraph("Editing what you type", h2),
        table([["Key", "What it does"],
               ["FCTN-S \u2190", "Erase the last letter (FCTN-1 also works)"],
               ["FCTN-E \u2191", "Bring back your last command"],
               ["FCTN-D \u2192", "Re-type your last command one letter at a time"],
               ["FCTN-X \u2193", "Clear the line (FCTN-3 also works)"]],
              [1.05 * inch, None]),
        Spacer(1, 6),
        Paragraph("In an emulator, your PC's Backspace and arrow keys do the same. Capital letters only; "
                  "ALPHA LOCK makes no difference.", body),
    ])
    folio(c, 4)

def p5(c):
    paper(c)
    left, _, fw, _ = frame_for(5)
    flow(c, 5, [
        Paragraph("Words the Game Knows", h1),
        Paragraph("Words on the same row mean the same thing.", body),
        table([["Verb", "Also", "What it does"],
               ["LOOK", "L", "Describe where you are"],
               ["EXAMINE", "X, INSPECT, SEARCH", "Look closely at something"],
               ["READ", "", "Read writing"],
               ["INVENTORY", "I, INV", "List what you carry"],
               ["TAKE", "GET, GRAB", "Pick something up"],
               ["DROP", "LEAVE", "Put something down"],
               ["OPEN", "", "Open things"],
               ["CUT", "CHOP, HACK, SLASH", "Cut, with a blade"],
               ["LIGHT", "IGNITE", "Light things"],
               ["TIE", "KNOT", "Tie things"],
               ["PRY", "LEVER, FORCE, MOVE, LIFT", "Shift heavy things"],
               ["PRESS", "PUSH, TOUCH", "Press things"],
               ["TALK", "ASK, SPEAK", "Talk to someone"],
               ["FREE", "RESCUE", "Free someone stuck"],
               ["BOARD", "ENTER, FLY", "Climb aboard"],
               ["WAIT", "Z", "Let a moment pass"],
               ["SCORE", "", "Show your score"],
               ["HELP", "HINT", "How to give commands"],
               ["QUIT", "", "End the game"]],
              [0.95 * inch, 1.42 * inch, None]),
        Spacer(1, 7),
        Paragraph("Directions: NORTH (N), SOUTH (S), EAST (E), WEST (W), UP (U, CLIMB), DOWN (D, DESCEND).", body),
    ])
    folio(c, 5)

def p6(c):
    paper(c)
    flow(c, 6, [
        Paragraph("Time, Danger and Glory", h1),
        Paragraph("Every command the game understands takes one turn. The weather keeps its own time: dawdle long "
                  "enough and the rains will come on their own, and some deeds may bring them sooner. Once the rain "
                  "starts, the game warns you as the water rises, and you have only a handful of turns to reach safety.", body),
        Paragraph("There are a few ways for the adventure to end badly. When it ends, win or lose, you see your score "
                  "and the question <b>PLAY AGAIN? (Y/N)</b>. Press <b>Y</b> to begin again, or <b>N</b> to return to "
                  "the TI title screen.", body),
        Paragraph("The perfect score is <b>100 points</b>. Points come from solving problems and from a few acts of "
                  f"decency along the way, not only from reaching the end. Type {C('SCORE')} at any time.", body),
        Paragraph("F18A enhanced color", h2),
        Paragraph("If your console has an F18A, the game finds it when it starts, and every scene gets its own tuned "
                  "colors: layered greens and bark-brown trunks in the jungle, murky water at the ford, warm "
                  "limestone in the ruins, amber lantern light on the stairs. The story text stays white on black. "
                  "When you quit, the standard colors are put back for the next program.", body),
        Spacer(1, 4),
    ])
    left, _, fw, _ = frame_for(6)
    picture(c, "trail.png", left + 3, 1.0 * inch, fw - 6)
    c.setFont("Lora-I", 8.2); c.setFillColor(HexColor("#6b5d50"))
    c.drawCentredString(left + fw / 2, 1.0 * inch - 16, "The jungle trail, with the F18A's palette.")
    folio(c, 6)

def p7(c):
    paper(c)
    flow(c, 7, [
        Paragraph("Advice for Adventurers", h1),
        Paragraph("None of these will spoil a puzzle.", lead),
        Paragraph("<b>Examine everything.</b> Descriptions mention more than what you can carry. Containers, carvings "
                  "and people often have more to say when you look closely or search them.", body),
        Paragraph("<b>Read what is written.</b> Your field journal is a good place to start.", body),
        Paragraph("<b>Talk to people.</b> Not everyone you meet is an enemy, and some know this country better than you.", body),
        Paragraph("<b>Think about the way back.</b> Reaching the clock is only half the adventure. What is easy to "
                  "cross on the way in may not be on the way out.", body),
        Paragraph("<b>Be prepared before you go somewhere dark.</b>", body),
        Paragraph("<b>Make a map.</b> Note each place and which way leads where. There are nine of them.", body),
        Paragraph("<b>Kindness counts.</b> Not every point comes from treasure.", body),
        Paragraph("If something goes wrong", h2),
        table([["Problem", "Try"],
               ["Not on the menu", "Name the file obsidian8.bin and load it as a cartridge."],
               ["A message asks for 32K", "Add the 32K memory expansion (in an emulator, turn it on) and restart."],
               ["A key is ignored", "Wait for the picture or tune to finish, then press again."],
               ["No F18A colors", "In js99er, enable the F18A in its settings and restart."]],
              [1.25 * inch, None]),
    ])
    folio(c, 7)

def p8(c):
    c.setFillColor(NIGHT); c.rect(0, 0, W, H, stroke=0, fill=1)
    inset = 0.32 * inch
    c.setStrokeColor(GOLD); c.setLineWidth(1.2); c.rect(inset, inset, W - 2 * inset, H - 2 * inset, stroke=1, fill=0)
    c.setLineWidth(0.4); c.rect(inset + 4, inset + 4, W - 2 * inset - 8, H - 2 * inset - 8, stroke=1, fill=0)
    pw = W - 1.3 * inch
    picture(c, "hall.png", (W - pw) / 2, H - 1.0 * inch - pw / 2, pw)
    c.setFont("Lora-I", 10.5); c.setFillColor(PAPER)
    y = H - 1.0 * inch - pw / 2 - 0.45 * inch
    for line in ["Find the clock.", "Then get back to the plane", "before the water does."]:
        c.drawCentredString(W / 2, y, line); y -= 15
    c.setFont("Pop-B", 13); c.setFillColor(GOLD)
    c.drawCentredString(W / 2, 2.55 * inch, "THE OBSIDIAN CLOCK")
    c.setFont("Pop", 7.8); c.setFillColor(HexColor("#c9c3e0"))
    for i, line in enumerate(["An original illustrated adventure for the TI-99/4A.",
                              "Story, text, art, engine and tools by Rebecca Sutter,",
                              "built with Claude, 2026.",
                              "",
                              "TI-99/4A with 32K memory expansion  \u00b7  FinalGROM 99 or emulator",
                              "Enhanced for the F18A  \u00b7  Version 1.0"]):
        c.drawCentredString(W / 2, 2.25 * inch - i * 12, line)

PAGES = [p_cover, p2, p3, p4, p5, p6, p7, p8]

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    c = canvas.Canvas("guide-pages.pdf", pagesize=(W, H))
    c.setTitle("The Obsidian Clock - Player's Guide"); c.setAuthor("Rebecca Sutter")
    for p in PAGES:
        p(c); c.showPage()
    c.save()
    # impose: saddle stitch, eight pages on two letter sheets printed both sides
    from pypdf import PdfReader, PdfWriter, PageObject, Transformation
    r = PdfReader("guide-pages.pdf"); n = len(r.pages); assert n % 4 == 0
    order = []
    for s in range(n // 4):
        order += [(n - 2 * s, 1 + 2 * s), (2 + 2 * s, n - 1 - 2 * s)]   # front, back
    def impose(path, flip_long):
        """flip_long: the printer turns the sheet over its long edge (the usual
        duplex default), which shows a landscape sheet's back upside down, so
        each back side is rotated 180 degrees to come out upright in the booklet"""
        w = PdfWriter()
        for k, (a, b) in enumerate(order):
            back = k % 2 == 1
            sheet = PageObject.create_blank_page(width=2 * W, height=H)
            for page, x in ((a, 0), (b, W)):
                t = Transformation().translate(x, 0)
                if back and flip_long:
                    t = t.rotate(180).translate(2 * W, H)
                sheet.merge_transformed_page(r.pages[page - 1], t)
            w.add_page(sheet)
        w.add_metadata({"/Title": "The Obsidian Clock - Player's Guide (print, flip on "
                        + ("long" if flip_long else "short") + " edge)", "/Author": "Rebecca Sutter"})
        with open(path, "wb") as f: w.write(f)
    impose("guide-print.pdf", flip_long=True)
    impose("guide-print-short-edge.pdf", flip_long=False)
    print(n, "pages; imposed sheets:", order)
