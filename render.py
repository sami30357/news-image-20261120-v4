#!/usr/bin/env python3
"""news-image-20261120 V4 — "The Friday Edition, cream broadsheet".
One page, 35 verified stories from Friday 20 November 2026, drawn fresh with PIL.
1024x1024 RGB PNG. Run: python3 render.py  ->  writes entry.png next to this file.
All facts are the verified V3 story set (see BUILD-NOTES.md); no new stories were
added. Layout follows the classic broadsheet the day's best pages use — cream paper,
black serif masthead, six-number stat strip, proportional region bar, three tall
hero panels, a seven-moment timeline, ten drawn mid stories, a records strip, a
world map with numbered pins, two-column briefs and a two-part date check — with
two things none of the leaders has: the RECORDS OF THE DAY strip and a status
legend (CONFIRMED / OFFICIAL / REPORTED) on every story.
"""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER   = (247, 243, 232)   # cream broadsheet
PAPER2  = (242, 236, 220)   # slightly deeper cream for bands
INK     = (24, 24, 22)      # near-black text
RED     = (178, 34, 28)     # headline-chip red
RED_DK  = (140, 24, 20)
BLUE    = (28, 58, 110)     # navy accents
TAN     = (214, 196, 158)   # map land
TAN_DK  = (186, 164, 124)
GREY    = (110, 108, 100)
LINE    = (60, 58, 52)
WHITE   = (255, 255, 255)
BLACK   = (16, 16, 16)
GOLD    = (198, 158, 44)
GREEN   = (46, 110, 62)
TEAL    = (24, 110, 108)
NAVY_BG = (18, 32, 64)      # dark panels (night scenes, charts)
SKY     = (168, 205, 228)
SEA     = (96, 140, 176)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

def serif(size, bold=False):
    name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    return ImageFont.truetype(FONT_DIR + name, size)

def sans(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(FONT_DIR + name, size)

# ---------------------------------------------------------------- text helpers
def tw(draw, text, font):
    """Width of text in px."""
    return draw.textlength(text, font=font)

def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if tw(draw, trial, font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def fit_lines(draw, text, font, max_w, max_lines):
    """Wrap to at most max_lines; ellipsize the last line if it overflows."""
    lines = wrap(draw, text, font, max_w)
    if len(lines) <= max_lines:
        return lines
    out = lines[:max_lines]
    last = out[-1]
    while last and tw(draw, last + "…", font) > max_w:
        last = last[:-1]
    out[-1] = last + "…"
    return out

def one_line(draw, text, font, max_w):
    """Truncate a single line with an ellipsis."""
    if tw(draw, text, font) <= max_w:
        return text
    s = text
    while s and tw(draw, s + "…", font) > max_w:
        s = s[:-1]
    return s + "…"

def center(draw, cx, y, text, font, fill):
    draw.text((cx - tw(draw, text, font) / 2, y), text, font=font, fill=fill)

def chip(draw, x, y, text, font, fg=WHITE, bg=RED, pad_x=7, h=20):
    """A solid label chip; returns its width."""
    w = int(tw(draw, text, font)) + pad_x * 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    draw.text((x + pad_x, y + (h - font.size) // 2 - 1), text, font=font, fill=fg)
    return w

def status_tag(draw, x, y, text, font):
    """Small grey status tag with a thin outline; returns width."""
    w = int(tw(draw, text, font)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=2, outline=GREY, width=1)
    draw.text((x + 5, y + 1), text, font=font, fill=GREY)
    return w

def rule(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)

# ---------------------------------------------------------------- story data
# Every fact below was verified for V3 (see BUILD-NOTES.md). No new stories.
# Regions: EUROPE 7 · ASIA 11 · MIDDLE EAST 3 · AFRICA 3 · AMERICAS 5 · OCEANIA 1
#          · GLOBAL 5 = 35 stories.

STATS = [
    ("3", "bridges hit\nin Kyiv"),
    ("300,000+", "evacuated\nbefore Akvan"),
    ("−6.2%", "Taiex, Friday's\nclose"),
    ("100,000", "youth visas a year\nin the UK–EU deal"),
    ("2.3%", "Japan consumer\ninflation, Oct"),
    ("118", "runs by Glenn Phillips\nagainst India"),
]

REGIONS = [
    ("EUROPE", 7, (28, 58, 110)),
    ("ASIA", 11, (178, 34, 28)),
    ("MIDDLE EAST", 3, (24, 110, 108)),
    ("AFRICA", 3, (46, 110, 62)),
    ("AMERICAS", 5, (104, 62, 140)),
    ("OCEANIA", 1, (198, 158, 44)),
    ("GLOBAL", 5, (110, 108, 100)),
]

HEROES = [
    dict(
        n=1, place="KYIV, UKRAINE · WAR", region="EUROPE",
        title="Russian missiles hit three Kyiv bridges",
        deck="An overnight barrage of 80+ missiles and 400 drones killed 8 and cut power and water in the capital.",
        source="Reuters · Kyiv Post", status="Officials say",
        chip="KYIV", sub="3 bridges hit",
    ),
    dict(
        n=2, place="ODISHA, INDIA · CYCLONE", region="ASIA",
        title="Cyclone Akvan comes ashore in eastern India",
        deck="The storm crossed the coast near Gopalpur; 300,000+ moved to shelters. No deaths reported.",
        source="IMD · NDTV", status="Officials say",
        chip="CYCLONE AKVAN", sub="Landfall · 8 am",
    ),
    dict(
        n=3, place="TAIPEI · SEOUL · TOKYO · MARKETS", region="ASIA",
        title="AI sell-off sinks Asia's stock markets",
        deck="Taiex fell 6.2% in its worst week since 1991 as chipmakers led the slide.",
        source="Al Jazeera · Reuters", status="Reported",
        chip="AI SELL-OFF", sub="Asia, Friday's close",
    ),
]

MIDS = [
    dict(n=4, place="BRUSSELS · DIPLOMACY", title="UK and EU seal a “reset” deal",
         deck="Food trade, youth visas, carbon link.", source="Reuters", status="Agreed",
         chip="UK–EU DEAL"),
    dict(n=5, place="EASTERN POLAND · WAR", title="Russian missile lands in Poland",
         deck="Kh-101 down; NATO jets scrambled.", source="Ukrainska Pravda", status="Officials say",
         chip="KH-101 IN POLAND"),
    dict(n=6, place="ANTALYA · CLIMATE", title="COP31 reaches its last day with no deal",
         deck="Draft leaves out fossil fuels.", source="AFP", status="Ongoing",
         chip="COP31: NO DEAL"),
    dict(n=7, place="CENTRAL IRAQ · SECURITY", title="Iraqi army enters a militia stronghold",
         deck="Troops deploy to Jurf al-Sakhar.", source="AFP", status="Witnessed",
         chip="IRAQ: ARMY IN"),
    dict(n=8, place="SAN SALVADOR · POLITICS", title="Bukele files to run for a third term",
         deck="The vote is on 28 February 2027.", source="Reuters", status="Filed",
         chip="BUKELE: 3RD TERM"),
    dict(n=9, place="ROME · LABOUR", title="General strike over Italy's budget",
         deck="Workers and students march.", source="Reuters", status="Reported",
         chip="SCIOPERO"),
    dict(n=10, place="TOKYO · ECONOMY", title="Japan's inflation picks up to 2.3%",
         deck="A December rate rise stays in view.", source="Japan Times", status="Official data",
         chip="JAPAN: +2.3%"),
    dict(n=11, place="WELLINGTON · CRICKET", title="Phillips hits 118 against India",
         deck="Hundreds in all three formats.", source="Cricinfo", status="Scorecard",
         chip="PHILLIPS: 118"),
    dict(n=12, place="CALIFORNIA · TECH", title="California subpoenas Nvidia",
         deck="China chips probe; investors misled.", source="Reuters", status="Reported",
         chip="NVIDIA: SUBPOENA"),
    dict(n=13, place="SEOUL · EDUCATION", title="Suneung: 111 caught cheating",
         deck="Glasses, cameras; ban proposed.", source="Yonhap", status="Officials say",
         chip="SUNEUNG: 111 CAUGHT"),
]

BRIEFS = [
    (14, "Kenya oil rig — first crude due Dec 1", "Business Daily"),
    (15, "China holds loan rates for an 18th straight month", "Xinhua"),
    (16, "Senegal boat capsizes; 4 dead, dozens missing", "Al Jazeera"),
    (17, "Malawi fuel crisis brings night-long petrol queues", "Al Jazeera"),
    (18, "F1 Russell fastest in wet Las Vegas FP2", "formula1.com"),
    (19, "Cancer pill: tumours shrank in 60.7% of patients", "Reuters"),
    (20, "Rohingya: Myanmar calls ICJ ruling “unfair”", "Reuters"),
    (21, "GTA VI: $2.36bn by end of launch day, est.", "Reuters"),
    (22, "Seoul ruling party moves to impeach top judge", "Yonhap"),
    (23, "Brent $92.60 as Hormuz fears rise", "Reuters"),
    (24, "Houthi missiles at Riyadh intercepted", "Reuters"),
    (25, "Iran says two tankers hit mines in Hormuz (claim)", "Reuters"),
    (26, "Erasca: 44% of pancreatic patients respond", "Reuters"),
    (27, "Antonelli confirmed F1's youngest champion", "FIA"),
    (28, "Court overturns ex-PM Han's conviction", "Yonhap"),
    (29, "Lviv: a strike on a railway station kills two", "BBC"),
    (30, "Rzeszow airport shut; rail halted", "Ukrainska Pravda"),
    (31, "Youth protests spread to five countries", "Reuters"),
    (32, "SoftBank shares fall more than 14% in a day", "Al Jazeera"),
    (33, "TSMC falls 5.2% in the sell-off", "Reuters"),
    (34, "EU calls the COP31 draft “not acceptable”", "Carbon Brief"),
    (35, "Gopalpur landfall 07:30–08:30; 209mm rain", "PTI"),
]

MOMENTS = [
    ("01:20", "KYIV", "Missiles hit 3 bridges"),
    ("07:30", "GOPALPUR", "Landfall begins"),
    ("08:30", "TOKYO", "CPI 2.3% released"),
    ("11:20", "ODISHA", "Landfall done, no deaths"),
    ("AFTERNOON", "ANTALYA", "COP31 runs past close"),
    ("EVENING", "BRUSSELS", "UK–EU deal sealed"),
    ("NIGHT", "NEW YORK", "Nvidia probe reported"),
]

RECORDS = [
    ("WORST WEEK SINCE 1991", "Taiex −17.5% on the week"),
    ("YOUNGEST CHAMPION", "Antonelli: F1's youngest champion"),
    ("ONLY THE 2ND EVER", "Phillips: 100s in all 3 formats vs India"),
    ("8 YEARS IN FLIGHT", "BepiColombo reaches Mercury on Saturday"),
]

DATE_LEFT = ("LEFT OUT — first reported Thursday 19 November: Anthropic's $83 IPO pricing "
             "& Nasdaq debut · Wall Street −2%, Dow under 50,000 · the ICJ ruling itself "
             "(reactions are Friday's news) · the Riyadh tower attack · COP31's second draft · "
             "the $190.4m Van Gogh sale · Voyager 1's one light-day confirmation · the Senate's "
             "40–51 Iran war-powers vote.")
DATE_NOTYET = ("NOT YET — BepiColombo's Mercury orbit capture (Saturday) · COP31's final text · "
               "the ATP Finals final (Sunday) · Estonia's border closure (1 December).")

# ---------------------------------------------------------------- hero panels
def hero_kyiv(d, x, y, w, h):
    """Night skyline, a bridge, fires and missile trails over Kyiv."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY_BG)
    # stars
    for sx, sy, r in [(12, 12, 1), (40, 26, 1), (70, 10, 2), (120, 20, 1),
                      (180, 8, 1), (230, 24, 2), (280, 12, 1), (310, 30, 1),
                      (95, 34, 1), (200, 38, 1), (150, 14, 1)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r], fill=WHITE)
    # missile trails
    for (x0, y0, x1, y1) in [(30, 18, 120, 62), (200, 12, 270, 58), (150, 22, 210, 66)]:
        d.line([(x + x0, y + y0), (x + x1, y + y1)], fill=(230, 220, 180), width=2)
        d.ellipse([x + x1 - 3, y + y1 - 3, x + x1 + 3, y + y1 + 3], fill=(255, 200, 90))
    # skyline
    base = y + h - 26
    for bx, bw, bh in [(0, 34, 34), (38, 26, 52), (68, 40, 30), (112, 30, 58),
                       (146, 36, 40), (186, 28, 62), (218, 34, 36), (256, 30, 48),
                       (290, 40, 30)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=BLACK)
        for wy in range(base - bh + 6, base - 6, 10):
            for wx in range(bx + 5, bx + bw - 4, 9):
                d.rectangle([x + wx, wy, x + wx + 3, wy + 4], fill=(255, 214, 120))
    # bridge arc + deck
    d.arc([x + 20, base - 34, x + w - 20, base + 46], 200, 340, fill=(200, 200, 200), width=3)
    d.line([(x + 8, base), (x + w - 8, base)], fill=(220, 220, 220), width=3)
    for px in range(30, w - 20, 34):
        d.line([(x + px, base - 12), (x + px, base)], fill=(200, 200, 200), width=2)
    # fires on the deck
    for fx in (70, 175, 255):
        d.ellipse([x + fx - 7, base - 14, x + fx + 7, base - 2], fill=(255, 140, 40))
        d.ellipse([x + fx - 4, base - 10, x + fx + 4, base - 3], fill=(255, 210, 80))
    # water below
    d.rectangle([x, base + 2, x + w, y + h], fill=(14, 26, 52))
    for wx in range(14, w - 10, 26):
        d.line([(x + wx, base + 12), (x + wx + 12, base + 12)], fill=(70, 110, 160), width=2)

def hero_akvan(d, x, y, w, h):
    """A cyclone spiral over the Bay of Bengal coast."""
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    # land (India's east coast) on the left
    d.polygon([(x, y), (x + 96, y), (x + 78, y + 46), (x + 92, y + 92),
               (x + 66, y + h), (x, y + h)], fill=TAN)
    d.line([(x + 96, y), (x + 78, y + 46), (x + 92, y + 92), (x + 66, y + h)],
           fill=TAN_DK, width=2)
    d.text((x + 10, y + 12), "ODISHA", font=sans(11, True), fill=(90, 70, 40))
    d.text((x + 10, y + 27), "GOPALPUR", font=sans(10), fill=(90, 70, 40))
    # spiral
    cx, cy = x + w - 118, y + 78
    for k in range(4):
        r = 14 + k * 13
        d.arc([cx - r, cy - r, cx + r, cy + r], 20 + k * 55, 300 + k * 55,
              fill=WHITE, width=5)
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=WHITE)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    # rain bands
    for rx in range(150, w - 8, 22):
        d.line([(x + rx, y + 14), (x + rx - 8, y + 44)], fill=(210, 225, 240), width=2)
        d.line([(x + rx + 4, y + 96), (x + rx - 4, y + 126)], fill=(210, 225, 240), width=2)
    # landfall arrow
    d.line([(cx - 62, cy + 6), (cx - 26, cy + 6)], fill=WHITE, width=3)
    d.polygon([(cx - 26, cy - 2), (cx - 14, cy + 6), (cx - 26, cy + 14)], fill=WHITE)

def hero_ai(d, x, y, w, h):
    """A falling market chart with the four index rows."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY_BG)
    # gridlines
    for gy in range(22, h - 34, 22):
        d.line([(x + 10, y + gy), (x + w - 10, y + gy)], fill=(52, 74, 116), width=1)
    # falling line, kept in the top half so it never meets the index rows
    pts = []
    for i in range(9):
        px = x + 14 + i * (w - 28) / 8
        py = y + 14 + i * i * 0.6 + (i % 2) * 3
        pts.append((px, py))
    d.line(pts, fill=(255, 90, 70), width=3)
    for px, py in pts:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 180, 160))
    # index rows
    rows = [("TAIEX", "−6.2%"), ("NIKKEI", "−5.1%"), ("KOSPI", "−5.2%"), ("HANG SENG", "−1.9%")]
    ry = y + h - 62
    for name, val in rows:
        d.text((x + 12, ry), name, font=sans(12, True), fill=WHITE)
        vw = tw(d, val, sans(12, True))
        d.text((x + w - 12 - vw, ry), val, font=sans(12, True), fill=(255, 110, 90))
        ry += 16

# ---------------------------------------------------------------- mid panels
def mid_flags(d, x, y, w, h):
    """Union Jack beside the EU flag, gold star between."""
    d.rectangle([x, y, x + w, y + h], fill=PAPER2)
    # Union Jack (simplified)
    fx, fy, fw, fh = x + 6, y + 14, 76, 56
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(0, 36, 125))
    d.line([(fx, fy), (fx + fw, fy + fh)], fill=WHITE, width=7)
    d.line([(fx + fw, fy), (fx, fy + fh)], fill=WHITE, width=7)
    d.line([(fx, fy), (fx + fw, fy + fh)], fill=(200, 16, 46), width=3)
    d.line([(fx + fw, fy), (fx, fy + fh)], fill=(200, 16, 46), width=3)
    d.line([(fx + fw / 2, fy), (fx + fw / 2, fy + fh)], fill=WHITE, width=12)
    d.line([(fx, fy + fh / 2), (fx + fw, fy + fh / 2)], fill=WHITE, width=12)
    d.line([(fx + fw / 2, fy), (fx + fw / 2, fy + fh)], fill=(200, 16, 46), width=6)
    d.line([(fx, fy + fh / 2), (fx + fw, fy + fh / 2)], fill=(200, 16, 46), width=6)
    # EU flag
    ex, ey, ew, eh = x + w - 82, y + 14, 76, 56
    d.rectangle([ex, ey, ex + ew, ey + eh], fill=(0, 51, 153))
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx = ex + ew / 2 + 22 * math.cos(a)
        sy = ey + eh / 2 + 17 * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
    # gold handshake star
    cx, cy = x + w / 2, y + 42
    for k in range(8):
        a = math.radians(k * 45)
        d.line([(cx, cy), (cx + 12 * math.cos(a), cy + 12 * math.sin(a))],
               fill=GOLD, width=2)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=GOLD)

def mid_missile(d, x, y, w, h):
    """A cruise missile over a field, with a blast."""
    d.rectangle([x, y, x + w, y + h], fill=(58, 72, 48))
    d.polygon([(x + 30, y + 34), (x + 118, y + 26), (x + 138, y + 38),
               (x + 118, y + 50), (x + 30, y + 44)], fill=(210, 210, 205))
    d.polygon([(x + 138, y + 38), (x + 158, y + 32), (x + 158, y + 44)], fill=(160, 160, 155))
    d.rectangle([x + 52, y + 22, x + 66, y + 30], fill=(160, 160, 155))
    d.rectangle([x + 52, y + 46, x + 66, y + 54], fill=(160, 160, 155))
    d.ellipse([x + 22, y + 36, x + 34, y + 46], fill=(255, 160, 60))
    d.line([(x + 8, y + 41), (x + 24, y + 41)], fill=(255, 200, 120), width=3)
    # blast bottom right
    d.ellipse([x + w - 52, y + h - 30, x + w - 12, y + h - 2], fill=(255, 140, 40))
    d.ellipse([x + w - 42, y + h - 22, x + w - 22, y + h - 6], fill=(255, 210, 80))
    d.line([(x + 10, y + h - 8), (x + w - 10, y + h - 8)], fill=(40, 50, 34), width=3)

def mid_globe(d, x, y, w, h):
    """A globe with a rising thermometer."""
    d.rectangle([x, y, x + w, y + h], fill=(186, 214, 232))
    cx, cy, r = x + 62, y + 46, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 120, 180))
    d.polygon([(cx - 18, cy - 26), (cx + 2, cy - 30), (cx + 10, cy - 12),
               (cx - 6, cy - 2), (cx - 22, cy - 10)], fill=(120, 180, 120))
    d.polygon([(cx + 4, cy + 8), (cx + 22, cy + 4), (cx + 26, cy + 20),
               (cx + 8, cy + 28), (cx - 2, cy + 16)], fill=(120, 180, 120))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=2)
    # thermometer
    tx = x + w - 34
    d.rounded_rectangle([tx, y + 10, tx + 10, y + 62], radius=5, fill=WHITE, outline=RED)
    d.rectangle([tx + 2, y + 34, tx + 8, y + 60], fill=RED)
    d.ellipse([tx - 4, y + 58, tx + 14, y + 76], fill=RED)
    d.text((tx - 4, y + 78), "°C", font=sans(9, True), fill=INK)

def mid_tanks(d, x, y, w, h):
    """Two tanks crossing a desert with palm trees."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 200, 150))
    d.ellipse([x + w - 40, y + 8, x + w - 10, y + 38], fill=(255, 230, 150))
    # palms
    for px in (18, 158):
        d.line([(x + px, y + h - 18), (x + px, y + 26)], fill=(120, 80, 40), width=4)
        for a in (-50, -20, 10, 40):
            ang = math.radians(a - 90)
            d.line([(x + px, y + 26), (x + px + 16 * math.cos(ang), y + 26 + 12 * math.sin(ang))],
                   fill=(70, 130, 70), width=3)
    # tanks
    for tx, ty, s in [(34, 52, 1.0), (96, 58, 0.85)]:
        tw_, th_ = int(58 * s), int(16 * s)
        d.rounded_rectangle([x + tx, y + ty, x + tx + tw_, y + ty + th_], radius=4,
                            fill=(90, 96, 70))
        d.rectangle([x + tx + 10, y + ty - 8, x + tx + 34, y + ty], fill=(70, 76, 54))
        d.line([(x + tx + 34, y + ty - 4), (x + tx + 54, y + ty - 6)], fill=(70, 76, 54), width=3)
        for wx in range(tx + 4, tx + tw_ - 4, 9):
            d.ellipse([x + wx, y + ty + th_, x + wx + 6, y + ty + th_ + 6], fill=(50, 54, 40))
    d.line([(x + 6, y + h - 10), (x + w - 6, y + h - 10)], fill=(170, 140, 95), width=2)

def mid_ballot(d, x, y, w, h):
    """A ballot box with a checked paper."""
    d.rectangle([x, y, x + w, y + h], fill=PAPER2)
    # paper
    d.polygon([(x + 96, y + 8), (x + 138, y + 14), (x + 132, y + 48), (x + 90, y + 42)],
              fill=WHITE, outline=INK)
    d.line([(x + 100, y + 24), (x + 112, y + 36), (x + 128, y + 16)], fill=RED, width=3)
    # box
    d.rectangle([x + 22, y + 44, x + 118, y + h - 8], fill=(28, 58, 110))
    d.rectangle([x + 22, y + 44, x + 118, y + 56], fill=(20, 44, 84))
    d.rectangle([x + 56, y + 47, x + 84, y + 53], fill=BLACK)
    d.text((x + 38, y + 62), "VOTE", font=sans(13, True), fill=WHITE)
    d.text((x + 128, y + 58), "FEB 2027", font=sans(11, True), fill=INK)

def mid_crowd(d, x, y, w, h):
    """A street crowd under a red SCIOPERO banner."""
    d.rectangle([x, y, x + w, y + h], fill=(210, 196, 170))
    d.rectangle([x + 8, y + 8, x + w - 8, y + 28], fill=RED)
    center(d, x + w / 2, y + 11, "SCIOPERO", sans(13, True), WHITE)
    # crowd heads
    cols = [(24, 52, (60, 50, 44)), (58, 60, (120, 90, 70)), (92, 50, (60, 50, 44)),
            (126, 58, (40, 40, 40)), (156, 52, (120, 90, 70))]
    for hx, hy, skin in cols:
        d.ellipse([x + hx - 9, y + hy - 9, x + hx + 9, y + hy + 9], fill=skin)
        d.rectangle([x + hx - 12, y + hy + 8, x + hx + 12, y + h - 4], fill=(70, 90, 120))
    # placards
    d.rectangle([x + 40, y + 30, x + 76, y + 46], fill=WHITE, outline=INK)
    d.text((x + 46, y + 33), "NO", font=sans(10, True), fill=RED)
    d.rectangle([x + 108, y + 28, x + 150, y + 44], fill=WHITE, outline=INK)
    d.text((x + 114, y + 31), "26 bn", font=sans(10, True), fill=INK)

def mid_cpi(d, x, y, w, h):
    """Rising bars with a yen symbol."""
    d.rectangle([x, y, x + w, y + h], fill=PAPER2)
    base = y + h - 14
    bars = [(26, 16), (66, 24), (106, 34)]
    for bx, bh in bars:
        d.rectangle([x + bx, base - bh, x + bx + 28, base], fill=BLUE)
    d.line([(x + 14, base), (x + w - 14, base)], fill=INK, width=2)
    d.text((x + 18, y + 8), "CPI", font=sans(11, True), fill=GREY)
    plus = "+2.3%"
    d.text((x + w - 14 - tw(d, plus, sans(12, True)), y + 7), plus,
           font=sans(12, True), fill=RED)

def mid_cricket(d, x, y, w, h):
    """A cricket pitch with bat, ball and a big 118."""
    d.rectangle([x, y, x + w, y + h], fill=(90, 150, 80))
    d.rectangle([x + 58, y + 8, x + w - 58, y + h - 8], fill=(214, 186, 140))
    d.line([(x + 58, y + h / 2), (x + w - 58, y + h / 2)], fill=WHITE, width=2)
    # stumps
    for sx in (70, 76, 82):
        d.line([(x + sx, y + 14), (x + sx, y + 26)], fill=(240, 210, 130), width=2)
    # bat
    d.line([(x + 118, y + 30), (x + 138, y + 58)], fill=(190, 150, 100), width=7)
    d.rectangle([x + 132, y + 52, x + 146, y + 66], fill=(190, 150, 100))
    # ball
    d.ellipse([x + w - 30, y + 16, x + w - 18, y + 28], fill=RED)
    d.text((x + 14, y + h - 34), "118", font=serif(30, True), fill=WHITE)

def mid_chip(d, x, y, w, h):
    """A green chip under a magnifier."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY_BG)
    # chip
    cx, cy = x + 62, y + 44
    d.rectangle([cx - 30, cy - 24, cx + 30, cy + 24], fill=(118, 185, 0))
    d.rectangle([cx - 18, cy - 14, cx + 18, cy + 14], fill=(88, 145, 0))
    d.text((cx - 16, cy - 8), "AI", font=sans(13, True), fill=WHITE)
    for px in range(cx - 30, cx + 31, 12):
        d.line([(px, cy - 30), (px, cy - 24)], fill=(200, 220, 150), width=2)
        d.line([(px, cy + 24), (px, cy + 30)], fill=(200, 220, 150), width=2)
    # magnifier
    mx, my, mr = x + w - 42, y + 26, 20
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=WHITE, width=3)
    d.line([(mx + 14, my + 14), (mx + 30, my + 30)], fill=WHITE, width=4)
    d.text((mx - 7, my - 8), "?", font=sans(15, True), fill=WHITE)

def mid_glasses(d, x, y, w, h):
    """Smart glasses over a crossed-out earpiece."""
    d.rectangle([x, y, x + w, y + h], fill=PAPER2)
    # glasses
    d.ellipse([x + 28, y + 22, x + 68, y + 54], outline=INK, width=3)
    d.ellipse([x + 84, y + 22, x + 124, y + 54], outline=INK, width=3)
    d.line([(x + 68, y + 36), (x + 84, y + 36)], fill=INK, width=3)
    d.line([(x + 28, y + 34), (x + 12, y + 28)], fill=INK, width=3)
    d.line([(x + 124, y + 34), (x + 140, y + 28)], fill=INK, width=3)
    d.ellipse([x + 40, y + 30, x + 56, y + 46], fill=(140, 200, 230))
    d.ellipse([x + 96, y + 30, x + 112, y + 46], fill=(140, 200, 230))
    # crossed earpiece
    d.ellipse([x + 138, y + 58, x + 162, y + 78], outline=RED, width=2)
    d.line([(x + 138, y + 58), (x + 162, y + 78)], fill=RED, width=2)
    d.line([(x + 162, y + 58), (x + 138, y + 78)], fill=RED, width=2)
    d.text((x + 12, y + h - 18), "111 CAUGHT", font=sans(11, True), fill=RED)

MID_DRAW = {4: mid_flags, 5: mid_missile, 6: mid_globe, 7: mid_tanks,
            8: mid_ballot, 9: mid_crowd, 10: mid_cpi, 11: mid_cricket,
            12: mid_chip, 13: mid_glasses}

# ---------------------------------------------------------------- world map
CONTINENTS = [
    # North America
    [(-168, 66), (-156, 71), (-140, 70), (-128, 71), (-115, 73), (-100, 73),
     (-90, 74), (-82, 66), (-76, 62), (-68, 58), (-60, 52), (-55, 47),
     (-60, 44), (-66, 44), (-70, 41), (-74, 39), (-76, 35), (-80, 32),
     (-81, 26), (-84, 30), (-89, 29), (-91, 19), (-87, 13), (-83, 9),
     (-79, 9), (-86, 12), (-92, 15), (-97, 16), (-102, 18), (-106, 22),
     (-112, 28), (-117, 33), (-122, 37), (-124, 42), (-124, 48), (-130, 54),
     (-140, 60), (-152, 58), (-162, 55)],
    # Greenland
    [(-58, 64), (-45, 60), (-40, 64), (-32, 68), (-25, 70), (-20, 74),
     (-30, 76), (-45, 76), (-55, 72)],
    # South America
    [(-79, 9), (-77, 4), (-75, -2), (-80, -5), (-81, -6), (-77, -12),
     (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50),
     (-70, -54), (-66, -55), (-68, -50), (-65, -45), (-62, -40), (-58, -34),
     (-52, -32), (-48, -27), (-41, -23), (-35, -18), (-35, -9), (-40, -5),
     (-44, -3), (-50, 0), (-55, 5), (-60, 8), (-68, 11), (-75, 11)],
    # Africa
    [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-5, 35), (0, 36), (10, 37),
     (11, 34), (20, 32), (30, 31), (32, 31), (34, 28), (36, 27), (38, 22),
     (40, 18), (43, 12), (48, 11), (51, 11), (48, 5), (44, 0), (40, -5),
     (38, -12), (35, -18), (32, -26), (28, -33), (20, -35), (17, -32),
     (15, -27), (13, -20), (12, -15), (13, -10), (9, -2), (9, 4), (4, 6),
     (-8, 5), (-13, 8), (-17, 12)],
    # Europe
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-2, 48), (-4, 50), (-1, 51),
     (2, 51), (4, 53), (8, 57), (10, 59), (5, 60), (5, 62), (10, 64),
     (13, 66), (18, 69), (25, 71), (30, 70), (32, 68), (28, 66), (24, 64),
     (21, 60), (23, 58), (24, 56), (21, 54), (18, 54), (15, 54), (12, 54),
     (8, 55), (8, 57), (4, 53), (0, 50), (-2, 49), (-5, 48), (-2, 46),
     (0, 44), (3, 43), (7, 44), (10, 44), (13, 45), (16, 44), (19, 42),
     (21, 40), (23, 38), (26, 38), (28, 36), (23, 36), (20, 39), (18, 40),
     (15, 40), (12, 44), (8, 44), (4, 43), (0, 43), (-2, 37), (-6, 36)],
    # Asia
    [(30, 36), (36, 36), (40, 38), (44, 39), (48, 40), (52, 42), (55, 45),
     (58, 46), (62, 46), (66, 45), (70, 44), (75, 45), (80, 48), (85, 50),
     (90, 52), (95, 55), (100, 58), (105, 60), (110, 62), (115, 65),
     (120, 68), (125, 70), (130, 71), (135, 72), (140, 72), (145, 72),
     (150, 70), (155, 68), (160, 66), (165, 66), (170, 66), (175, 65),
     (178, 65), (178, 62), (170, 60), (162, 58), (158, 52), (156, 50),
     (150, 45), (142, 42), (140, 38), (135, 34), (130, 32), (127, 30),
     (122, 28), (120, 24), (116, 22), (112, 20), (108, 18), (106, 10),
     (104, 8), (102, 8), (100, 6), (98, 10), (96, 14), (94, 17), (92, 21),
     (90, 22), (88, 22), (86, 20), (84, 18), (82, 16), (80, 14), (78, 10),
     (76, 9), (74, 12), (72, 20), (70, 22), (68, 23), (66, 25), (64, 25),
     (62, 25), (60, 25), (58, 26), (56, 26), (54, 26), (52, 28), (50, 29),
     (48, 30), (46, 30), (44, 29), (42, 28), (40, 30), (38, 31), (36, 33),
     (34, 36)],
    # Australia
    [(114, -22), (114, -30), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -11), (137, -12),
     (132, -11), (126, -14), (122, -17), (118, -20)],
]

PINS = [
    (1, 50.45, 30.52), (2, 19.3, 84.9), (3, 25.0, 121.6), (4, 50.85, 4.35),
    (5, 50.4, 22.2), (6, 36.9, 30.7), (7, 33.3, 44.4), (8, 13.7, -89.2),
    (9, 41.9, 12.5), (10, 35.7, 139.7), (11, -41.3, 174.8),
    (12, 37.3, -121.9), (13, 37.6, 127.0),
]

def draw_map(d, x0, y0, w, h):
    """Cream map, tan continents, 13 numbered red pins."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(238, 232, 214))
    def proj(lon, lat):
        px = x0 + (lon + 180) / 360 * w
        py = y0 + (85 - lat) / 140 * h
        return (px, py)
    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=TAN, outline=TAN_DK)
    # Indonesia dots
    for lon, lat in [(105, -5), (113, -8), (120, -9), (130, -3), (138, -4)]:
        px, py = proj(lon, lat)
        d.ellipse([px - 3, py - 2, px + 3, py + 2], fill=TAN, outline=TAN_DK)
    # pins
    for n, lat, lon in PINS:
        px, py = proj(lon, lat)
        r = 6
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=WHITE, width=1)
        t = str(n)
        tw_ = tw(d, t, sans(8, True))
        d.text((px - tw_ / 2, py - 5), t, font=sans(8, True), fill=WHITE)

# ---------------------------------------------------------------- layout
MX = 28                 # side margin
CW = W - 2 * MX         # content width (968)
RX = W - MX             # right edge

def section_label(d, x, y, text, font=None):
    d.text((x, y), text, font=font or serif(13, True), fill=INK)

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 10

    # kicker line
    d.text((MX, y), "THE WORLD IN ONE DAY", font=sans(11, True), fill=RED)
    rt = "35 STORIES · 7 REGIONS · FRIDAY 20 NOVEMBER 2026"
    d.text((RX - tw(d, rt, sans(11, True)), y), rt, font=sans(11, True), fill=INK)
    y += 18

    # masthead
    mast = "Friday 20 November 2026"
    mf = serif(54, True)
    center(d, W // 2, y, mast, mf, INK)
    y += 62

    # sub-dek
    sub = ("Russian missiles hit Kyiv's bridges · Cyclone Akvan strikes India · "
           "An AI sell-off sinks Asia's markets · UK and EU seal a deal")
    center(d, W // 2, y, sub, serif(15), RED)
    y += 24
    rule(d, MX, RX, y, 2)
    y += 8

    # stat strip: six numbers, red left rules
    col_w = CW / 6
    for i, (val, lab) in enumerate(STATS):
        cx = MX + i * col_w
        d.line([(cx + 2, y + 2), (cx + 2, y + 44)], fill=RED, width=3)
        d.text((cx + 10, y), val, font=serif(22, True), fill=RED)
        for j, line in enumerate(lab.split("\n")):
            d.text((cx + 10, y + 26 + j * 11), line, font=sans(9), fill=INK)
    y += 50

    # region ribbon: proportional segments, smallest segment kept readable
    total = sum(c for _, c, _ in REGIONS)
    widths = [max(46, int(CW * c / total)) for _, c, _ in REGIONS]
    over = sum(widths) - CW
    if over > 0:
        big = widths.index(max(widths))
        widths[big] -= over
    bx = MX
    for (name, count, color), seg in zip(REGIONS, widths):
        d.rectangle([bx, y, bx + seg, y + 20], fill=color)
        lab = f"{name} {count}"
        lf = sans(8, True)
        lw = tw(d, lab, lf)
        if lw <= seg - 4:
            d.text((bx + (seg - lw) / 2, y + 5), lab, font=lf, fill=WHITE)
        else:
            d.text((bx + 2, y + 5), lab, font=lf, fill=WHITE)
        bx += seg
    y += 26

    # heroes: three tall panels
    hcol = (CW - 2 * 12) / 3
    hero_draw = [hero_kyiv, hero_akvan, hero_ai]
    hy = y
    for i, hero in enumerate(HEROES):
        hx = MX + i * (hcol + 12)
        hero_draw[i](d, int(hx), hy, int(hcol), 130)
        ty = hy + 134
        d.text((hx, ty), hero["place"], font=sans(9, True), fill=RED)
        ty += 13
        for line in fit_lines(d, hero["title"], serif(17, True), hcol, 2):
            d.text((hx, ty), line, font=serif(17, True), fill=INK)
            ty += 20
        for line in fit_lines(d, hero["deck"], sans(11), hcol, 2):
            d.text((hx, ty), line, font=sans(11), fill=INK)
            ty += 13
        src = hero["source"]
        d.text((hx, ty + 2), src, font=sans(9), fill=GREY)
        tag_w = int(tw(d, hero["status"], sans(8))) + 10
        status_tag(d, hx + hcol - tag_w, ty, hero["status"], sans(8))
    y = hy + 134 + 13 + 40 + 26 + 14

    # timeline band
    d.rectangle([MX, y, RX, y + 38], fill=PAPER2)
    d.text((MX + 8, y + 3), "THE DAY IN SEVEN MOMENTS", font=sans(10, True), fill=RED)
    mom_w = CW / 7
    for i, (t, city, ev) in enumerate(MOMENTS):
        mx = MX + i * mom_w
        d.text((mx + 8, y + 17), t, font=sans(10, True), fill=RED)
        d.text((mx + 8 + tw(d, t + " ", sans(10, True)), y + 17), city,
               font=sans(10, True), fill=INK)
        d.text((mx + 8, y + 29), ev, font=sans(9), fill=INK)
    y += 44

    # mids label
    section_label(d, MX, y, "THE DAY'S TEN")
    note = "Each panel is drawn for that story"
    d.text((RX - tw(d, note, sans(10)), y + 3), note, font=sans(10), fill=GREY)
    y += 20

    # mid rows: 5 across, 2 rows
    mcol = (CW - 4 * 10) / 5
    for row in range(2):
        ry = y + row * 140
        for col in range(5):
            mid = MIDS[row * 5 + col]
            mx = MX + col * (mcol + 10)
            MID_DRAW[mid["n"]](d, int(mx), ry, int(mcol), 72)
            ty = ry + 76
            d.text((mx, ty), mid["place"], font=sans(9, True), fill=RED)
            ty += 11
            for line in fit_lines(d, mid["title"], serif(15, True), mcol, 2):
                d.text((mx, ty), line, font=serif(15, True), fill=INK)
                ty += 16
            deck = one_line(d, mid["deck"], sans(10), mcol)
            d.text((mx, ty), deck, font=sans(10), fill=INK)
            ty += 12
            d.text((mx, ty), mid["source"], font=sans(8), fill=GREY)
            tag_w = int(tw(d, mid["status"], sans(8))) + 10
            status_tag(d, mx + mcol - tag_w, ty - 1, mid["status"], sans(8))
    y += 280

    # records strip
    section_label(d, MX, y, "RECORDS OF THE DAY")
    y += 16
    d.rectangle([MX, y, RX, y + 28], fill=PAPER2)
    rec_w = CW / 4
    for i, (t, fact) in enumerate(RECORDS):
        rx = MX + i * rec_w
        d.text((rx + 8, y + 3), t, font=sans(9, True), fill=RED)
        d.text((rx + 8, y + 15), one_line(d, fact, sans(10), rec_w - 14),
               font=sans(10), fill=INK)
    y += 34

    # map + briefs
    section_label(d, MX, y, "WHERE IT HAPPENED")
    section_label(d, 486, y, "MORE OF THE DAY, IN BRIEF")
    y += 16
    map_y = y
    draw_map(d, MX, map_y, 442, 106)
    d.text((MX, map_y + 110), "Pins 1–13 mark the drawn stories.",
           font=sans(9), fill=GREY)
    bx0, bw = 486, 248
    for i, (n, text, src) in enumerate(BRIEFS):
        col = i // 11
        j = i % 11
        bx = bx0 + col * (bw + 14)
        by = map_y + j * 9.5
        line = f"{n}  {text} · {src}"
        d.text((bx, by), one_line(d, line, sans(9), bw), font=sans(9), fill=INK)
    y = map_y + 120

    # date check
    d.rectangle([MX, y, RX, y + 32], outline=GREY, width=1)
    for j, line in enumerate(fit_lines(d, DATE_LEFT, sans(9), CW - 16, 2)):
        d.text((MX + 8, y + 2 + j * 11), line, font=sans(9), fill=INK)
    d.text((MX + 8, y + 2 + 21), DATE_NOTYET, font=sans(9), fill=INK)
    y += 38

    # footer
    foot = ("Every story here happened, or was first reported, on Friday 20 November 2026. "
            "Claims are attributed, not stated as fact.")
    d.text((MX, y), foot, font=sans(9), fill=GREY)
    y += 11
    foot2 = ("CONFIRMED 2+ outlets · OFFICIAL on the record · REPORTED one outlet    "
             "Sources named beside each story · Original drawings")
    d.text((MX, y), foot2, font=sans(9), fill=GREY)
    y += 11
    print("final y:", y, "of", H)
    return img

def main():
    img = build()
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)

if __name__ == "__main__":
    main()
