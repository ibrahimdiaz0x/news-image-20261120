#!/usr/bin/env python3
"""Draw entry.png: a one-page front page summing up Friday 20 November 2026.

Original flat artwork rendered with PIL + DejaVu fonts. Generated locally;
the sandbox entrypoint (main.py) only copies the finished entry.png.

All six stories were verified as reported on 20 November 2026:
 1. GTA VI first-day sales $2.36bn / 24.58m units (Reuters, BusinessToday)
 2. Anthropic shares close up 17% after record IPO (NEXA, OneTurn)
 3. Kyiv hit by four ballistic missiles (Daily Baku, 04:07 Nov 20)
 4. Houthis claim strikes on four Saudi targets (Daily Baku, 03:47 Nov 20)
 5. Migrant boat sinks off Senegal, dozens missing (GT Daily, Nov 20)
 6. Lula to sign decree for Brazil's five-day workweek (News-Public.World, Nov 20)
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (244, 238, 226)
INK = (24, 24, 24)
NAVY = (20, 32, 58)
GOLD = (228, 196, 112)
RED = (186, 32, 40)
CARD = (255, 255, 255)
BORDER = (214, 208, 194)
SUBINK = (62, 62, 62)
FOOTINK = (105, 105, 105)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


F_KICK = font("DejaVuSans-Bold.ttf", 19)
F_DATE = font("DejaVuSerif-Bold.ttf", 52)
F_SUBKICK = font("DejaVuSans.ttf", 18)
F_TAG = font("DejaVuSans-Bold.ttf", 14)
F_HEAD = font("DejaVuSerif-Bold.ttf", 27)
F_SUB = font("DejaVuSans.ttf", 18)
F_FOOT = font("DejaVuSans.ttf", 16)


def centered(d, cx, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def sun_rays(d, cx, cy, r, fill, width=3):
    for k in range(12):
        a = math.radians(k * 30)
        x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a)
        x2, y2 = cx + (r + 10) * math.cos(a), cy + (r + 10) * math.sin(a)
        d.line([(x1, y1), (x2, y2)], fill=fill, width=width)


# ---------------- icon scenes (each in a 280x140 box) ----------------

def icon_game(d, x, y):
    # Neon dusk skyline + game controller
    d.rectangle([x, y, x + 280, y + 140], fill=(38, 22, 64))
    # sun disc
    d.ellipse([x + 196, y + 12, x + 252, y + 68], fill=(255, 120, 60))
    # skyline
    for bx, bw, bh in ((12, 30, 58), (48, 24, 82), (78, 34, 48),
                       (118, 28, 96), (152, 32, 66), (190, 26, 78),
                       (222, 30, 54)):
        d.rectangle([x + bx, y + 140 - bh, x + bx + bw, y + 140],
                    fill=(16, 10, 28))
        for wy in range(y + 140 - bh + 8, y + 136, 13):
            for wx in range(x + bx + 5, x + bx + bw - 4, 9):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
    # controller, floating over the skyline
    cx, cy = x + 96, y + 52
    d.rounded_rectangle([cx - 52, cy - 22, cx + 52, cy + 22], radius=18,
                        fill=(240, 240, 245), outline=(30, 30, 40), width=3)
    d.ellipse([cx - 34, cy - 4, cx - 20, cy + 10], fill=(30, 30, 40))
    d.ellipse([cx + 20, cy - 10, cx + 34, cy + 4], fill=(30, 30, 40))
    for dx, dy, c in ((-8, -12, (186, 32, 40)), (2, -12, (40, 120, 60)),
                      (-8, -2, (40, 90, 180)), (2, -2, (220, 180, 0))):
        d.ellipse([cx + dx - 4, cy + dy - 4, cx + dx + 4, cy + dy + 4], fill=c)
    d.line([(cx - 44, cy + 6), (cx - 44, cy + 16)], fill=(30, 30, 40), width=3)
    d.line([(cx - 49, cy + 11), (cx - 39, cy + 11)], fill=(30, 30, 40), width=3)


def icon_chart(d, x, y):
    # Stock chart: rising line over bars, dollar coin
    d.rectangle([x, y, x + 280, y + 140], fill=(232, 240, 232))
    # grid
    for gy in (y + 30, y + 62, y + 94):
        d.line([(x + 12, gy), (x + 268, gy)], fill=(200, 212, 200), width=2)
    # bars
    for i, bh in enumerate((26, 40, 34, 56, 48, 72, 66, 92)):
        bx = x + 22 + i * 26
        d.rectangle([bx, y + 118 - bh, bx + 16, y + 118],
                    fill=(90, 140, 100))
    # rising line with arrowhead
    pts = [(x + 20, y + 100), (x + 70, y + 88), (x + 120, y + 92),
           (x + 170, y + 66), (x + 220, y + 52), (x + 258, y + 26)]
    d.line(pts, fill=(20, 90, 50), width=5, joint="curve")
    d.polygon([(x + 258, y + 26), (x + 244, y + 24), (x + 256, y + 40)],
              fill=(20, 90, 50))
    # dollar coin
    d.ellipse([x + 214, y + 88, x + 262, y + 136], fill=(228, 196, 112),
              outline=(160, 120, 40), width=3)
    d.text((x + 232, y + 96), "$", font=font("DejaVuSans-Bold.ttf", 30),
           fill=(90, 60, 10))


def icon_kyiv(d, x, y):
    # Kyiv at night: golden church domes, missile streaks, blast flash
    d.rectangle([x, y, x + 280, y + 140], fill=(28, 36, 64))
    # stars
    for sx, sy in ((30, 18), (70, 34), (120, 14), (180, 26), (240, 16),
                   (262, 44), (150, 40), (96, 20)):
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3],
                  fill=(230, 230, 255))
    # skyline with golden domes
    d.rectangle([x, y + 96, x + 280, y + 140], fill=(14, 18, 34))
    for bx, bw, bh in ((16, 34, 52), (58, 28, 70), (150, 30, 58),
                       (196, 34, 76), (238, 26, 48)):
        d.rectangle([x + bx, y + 96 - bh + 30, x + bx + bw, y + 96],
                    fill=(40, 48, 76))
    # two golden onion domes
    for dx, dw in ((100, 34), (160, 28)):
        d.ellipse([x + dx, y + 44, x + dx + dw, y + 44 + dw],
                  fill=(232, 190, 60))
        d.rectangle([x + dx + dw // 2 - 2, y + 38, x + dx + dw // 2 + 2,
                     y + 46], fill=(232, 190, 60))
        d.rectangle([x + dx - 4, y + 44 + dw, x + dx + dw + 4, y + 96],
                    fill=(60, 70, 100))
    # missile streaks from the top right
    d.line([(x + 276, y + 6), (x + 216, y + 46)], fill=(255, 200, 120),
           width=4)
    d.line([(x + 262, y + 30), (x + 222, y + 60)], fill=(255, 160, 80),
           width=3)
    # blast flash
    fx, fy = x + 208, y + 56
    sun_rays(d, fx, fy, 12, (255, 140, 0), 4)
    d.ellipse([fx - 12, fy - 12, fx + 12, fy + 12], fill=(255, 196, 0))
    d.ellipse([fx - 6, fy - 6, fx + 6, fy + 6], fill=(255, 90, 0))


def icon_drone(d, x, y):
    # Desert dusk, quadcopter drone above a target compound
    d.rectangle([x, y, x + 280, y + 140], fill=(246, 214, 170))
    d.rectangle([x, y + 104, x + 280, y + 140], fill=(190, 150, 100))
    # low compound buildings
    for bx, bw, bh in ((20, 44, 30), (76, 36, 44), (196, 44, 34),
                       (248, 26, 24)):
        d.rectangle([x + bx, y + 104 - bh, x + bx + bw, y + 104],
                    fill=(150, 112, 74))
    # target building with red flash
    d.rectangle([x + 128, y + 62, x + 172, y + 104], fill=(120, 88, 60))
    tx, ty = x + 150, y + 56
    sun_rays(d, tx, ty, 10, (255, 120, 0), 4)
    d.ellipse([tx - 10, ty - 10, tx + 10, ty + 10], fill=(255, 180, 0))
    # quadcopter drone
    cx, cy = x + 150, y + 26
    d.ellipse([cx - 10, cy - 5, cx + 10, cy + 5], fill=(50, 50, 60))
    for px in (cx - 26, cx + 26):
        d.line([(cx - 8, cy), (px, cy - 2)], fill=(50, 50, 60), width=3)
        d.line([(px - 12, cy - 6), (px + 12, cy - 6)], fill=(90, 90, 100),
               width=3)
        d.line([(px, cy - 2), (px, cy + 8)], fill=(50, 50, 60), width=3)
    # dashed descent line from drone to target
    for i in range(4):
        yy = cy + 12 + i * 8
        d.line([(cx, yy), (cx, yy + 4)], fill=(120, 90, 60), width=2)


def icon_boat(d, x, y):
    # Open sea, small boat in trouble, lifebuoy
    d.rectangle([x, y, x + 280, y + 140], fill=(214, 232, 244))
    d.rectangle([x, y + 78, x + 280, y + 140], fill=(36, 92, 140))
    for wx in range(x + 8, x + 272, 34):
        d.arc([wx, y + 88, wx + 26, y + 102], 200, 340,
              fill=(255, 255, 255), width=3)
        d.arc([wx + 12, y + 116, wx + 38, y + 130], 200, 340,
              fill=(180, 210, 235), width=3)
    # tilted boat hull
    d.polygon([(x + 88, y + 62), (x + 192, y + 48), (x + 176, y + 76),
               (x + 104, y + 84)], fill=(140, 60, 40))
    d.line([(x + 140, y + 56), (x + 140, y + 22)], fill=(70, 50, 40),
           width=4)
    d.polygon([(x + 140, y + 22), (x + 140, y + 48), (x + 168, y + 48)],
              fill=(240, 240, 240))
    # person waving in the water
    d.ellipse([x + 216, y + 96, x + 226, y + 106], fill=(60, 40, 30))
    d.line([(x + 221, y + 96), (x + 214, y + 84)], fill=(60, 40, 30),
           width=4)
    # lifebuoy
    d.ellipse([x + 36, y + 96, x + 72, y + 132], fill=(255, 255, 255),
              outline=(220, 60, 40), width=6)
    d.ellipse([x + 48, y + 108, x + 60, y + 120], fill=(36, 92, 140))


def icon_calendar(d, x, y):
    # Desk calendar: green field, yellow diamond, five working days marked
    d.rectangle([x, y, x + 280, y + 140], fill=(0, 140, 70))
    d.polygon([(x + 140, y + 12), (x + 262, y + 70), (x + 140, y + 128),
               (x + 18, y + 70)], fill=(255, 210, 0))
    # calendar page
    d.rounded_rectangle([x + 74, y + 26, x + 206, y + 116], radius=8,
                        fill=(255, 255, 255), outline=(30, 60, 120), width=3)
    d.rectangle([x + 74, y + 26, x + 206, y + 50], fill=(30, 60, 120))
    d.text((x + 86, y + 29), "NOVEMBER", font=font("DejaVuSans-Bold.ttf", 13),
           fill=(255, 255, 255))
    # weekday row: M T W T F marked, S S crossed out
    for i, (lbl, on) in enumerate((("M", 1), ("T", 1), ("W", 1), ("T", 1),
                                   ("F", 1), ("S", 0), ("S", 0))):
        cx = x + 88 + i * 17
        if on:
            d.ellipse([cx - 7, y + 60, cx + 7, y + 74], fill=(0, 140, 70))
            d.text((cx - 4, y + 61), lbl,
                   font=font("DejaVuSans-Bold.ttf", 11), fill=(255, 255, 255))
        else:
            d.text((cx - 4, y + 61), lbl,
                   font=font("DejaVuSans-Bold.ttf", 11), fill=(180, 180, 180))
            d.line([(cx - 7, y + 60), (cx + 7, y + 74)], fill=(186, 32, 40),
                   width=2)
    # big "5" for the five-day week
    d.text((x + 122, y + 76), "5", font=font("DejaVuSerif-Bold.ttf", 34),
           fill=(20, 32, 58))


PANELS = [
    ("CULTURE  •  GAMES", (120, 40, 160), "GTA VI BANKS $2.36BN IN A DAY",
     "24.58 million copies sold by Thursday evening — the biggest launch in history.",
     icon_game),
    ("ECONOMY  •  TECH", (20, 100, 60), "ANTHROPIC'S $1.8TN DEBUT",
     "Shares close up 17% after the largest IPO on record, raising $81.3 billion.",
     icon_chart),
    ("UKRAINE  •  WAR", (150, 40, 40), "KYIV HIT BY FOUR MISSILES",
     "Four ballistic missiles hit the capital overnight; one lands near the Dutch embassy.",
     icon_kyiv),
    ("MIDDLE EAST  •  WAR", (186, 32, 40), "HOUTHIS CLAIM SAUDI STRIKES",
     "The rebels claim drone and missile hits on four Saudi targets.",
     icon_drone),
    ("AFRICA  •  MIGRATION", (20, 90, 130), "BOAT SINKS OFF SENEGAL",
     "A migrant boat goes down off the Senegalese coast; dozens are missing.",
     icon_boat),
    ("AMERICAS  •  WORK", (30, 110, 80), "BRAZIL MOVES TO A FIVE-DAY WEEK",
     "Lula is set to sign a decree starting Brazil's transition to a five-day workweek.",
     icon_calendar),
]

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# masthead
d.rectangle([0, 0, W, 166], fill=NAVY)
centered(d, W // 2, 22, "THE WORLD IN ONE PAGE", F_KICK, GOLD)
centered(d, W // 2, 52, "FRIDAY 20 NOVEMBER 2026", F_DATE, (255, 255, 255))
d.rectangle([W // 2 - 110, 126, W // 2 + 110, 130], fill=RED)
centered(d, W // 2, 138, "SIX STORIES THAT DEFINED THE DAY", F_SUBKICK,
         (201, 210, 224))

# grid
MARGIN, GAP = 26, 18
PW = (W - 2 * MARGIN - 2 * GAP) // 3
PH = 378
TOPS = (186, 584)
for i, (tag, color, head, sub, icon) in enumerate(PANELS):
    col, row = i % 3, i // 3
    px = MARGIN + col * (PW + GAP)
    py = TOPS[row]
    d.rectangle([px, py, px + PW, py + PH], fill=CARD, outline=BORDER, width=2)
    d.rectangle([px, py, px + PW, py + 8], fill=color)
    icon(d, px + 16, py + 20)
    ty = py + 172
    d.text((px + 16, ty), tag, font=F_TAG, fill=color)
    hy = ty + 26
    for line in wrap(d, head, F_HEAD, PW - 32):
        d.text((px + 16, hy), line, font=F_HEAD, fill=INK)
        hy += 33
    sy = hy + 6
    for line in wrap(d, sub, F_SUB, PW - 32):
        d.text((px + 16, sy), line, font=F_SUB, fill=SUBINK)
        sy += 23

# footer
d.line([(MARGIN, 980), (W - MARGIN, 980)], fill=BORDER, width=2)
centered(d, W // 2, 988,
         "Every story above happened, or was first reported, on Friday 20 November 2026.",
         F_FOOT, FOOTINK)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
