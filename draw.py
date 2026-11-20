#!/usr/bin/env python3
"""Render the front page for 20 November 2026.

Draws a 1024x1024 newspaper front page with six stories, all verified
against news reports dated 20 November 2026. Pure PIL, no network.
Run it and it writes entry.png next to this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)
PAPER = (250, 244, 230)
CARD = (255, 253, 247)
INK = (24, 24, 24)
NAVY = (16, 28, 58)
GOLD = (214, 178, 94)
RULE = (196, 52, 44)
EDGE = (203, 192, 172)


def _font(name, size):
    """Load a DejaVu font, falling back to PIL's default bitmap font."""
    for path in (
        "/usr/share/fonts/truetype/dejavu/" + name,
        "/usr/share/fonts/dejavu/" + name,
    ):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


SERIF_BIG = _font("DejaVuSerif-Bold.ttf", 54)
SERIF_HEAD = _font("DejaVuSerif-Bold.ttf", 27)
SANS_DECK = _font("DejaVuSans.ttf", 15)
SANS_KICK = _font("DejaVuSans-Bold.ttf", 13)
SANS_TAG = _font("DejaVuSans-Bold.ttf", 21)
SANS_FOOT = _font("DejaVuSans.ttf", 14)


def wrap_text(draw, text, font, max_width):
    """Split text into lines that fit max_width pixels."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_gamepad(draw, x, y, w, h):
    """Night city skyline with a game controller above it."""
    draw.rectangle([x, y, x + w, y + h], fill=(38, 28, 66))
    draw.ellipse([x + w - 52, y + 14, x + w - 8, y + 58], fill=(232, 116, 44))
    for bx, bw, bh in ((8, 34, 74), (52, 26, 96), (88, 40, 62),
                        (138, 28, 88), (178, 34, 70), (222, 26, 98)):
        draw.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                       fill=(22, 18, 40))
        for wy in range(y + h - bh + 10, y + h - 6, 16):
            draw.rectangle([x + bx + 5, wy, x + bx + bw - 5, wy + 7],
                           fill=(240, 200, 80))
    draw.rounded_rectangle([x + 78, y + 26, x + 208, y + 66], radius=18,
                           fill=(245, 245, 245))
    for cx, cy, col in ((112, 46, (200, 40, 40)), (132, 40, (40, 140, 60)),
                        (152, 46, (40, 90, 200)), (132, 52, (220, 180, 40))):
        draw.ellipse([x + cx - 6, y + cy - 6, x + cx + 6, y + cy + 6],
                     fill=col)
    draw.ellipse([x + 176, y + 38, x + 188, y + 50], fill=(60, 60, 60))
    draw.ellipse([x + 176, y + 52, x + 188, y + 64], fill=(60, 60, 60))


def draw_chart(draw, x, y, w, h):
    """Rising bars with a trend arrow and a coin."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 236, 222))
    bars = (34, 52, 44, 66, 58, 82, 104)
    step = w // len(bars)
    for i, bh in enumerate(bars):
        bx = x + 12 + i * step
        draw.rectangle([bx, y + h - 14 - bh, bx + step - 10, y + h - 14],
                       fill=(62, 128, 84))
    pts = [(x + 16 + i * step, y + h - 20 - bh) for i, bh in enumerate(bars)]
    draw.line(pts, fill=(28, 84, 44), width=4)
    draw.polygon([(pts[-1][0], pts[-1][1] - 12), (pts[-1][0] + 14, pts[-1][1] + 2),
                  (pts[-1][0] - 2, pts[-1][1] + 6)], fill=(28, 84, 44))
    draw.ellipse([x + w - 58, y + h - 56, x + w - 10, y + h - 8],
                 fill=(216, 178, 80), outline=(150, 110, 30), width=2)
    draw.text((x + w - 42, y + h - 46), "$", font=SANS_TAG, fill=(90, 62, 10))


def draw_night_raid(draw, x, y, w, h):
    """Dark skyline under a burst, for the Kyiv strikes."""
    draw.rectangle([x, y, x + w, y + h], fill=(18, 26, 52))
    for sx, sy in ((30, 22), (90, 44), (150, 18), (210, 52), (260, 26)):
        draw.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4], fill=(255, 255, 255))
    for bx, bw, bh in ((10, 60, 66), (84, 44, 92), (142, 70, 58),
                        (226, 52, 80)):
        draw.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                       fill=(52, 62, 96))
    cx, cy = x + w - 62, y + 52
    for ang in range(0, 360, 30):
        import math
        ex = cx + 34 * math.cos(math.radians(ang))
        ey = cy + 34 * math.sin(math.radians(ang))
        draw.line([cx, cy, ex, ey], fill=(240, 180, 60), width=4)
    draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(245, 200, 80))


def draw_drone(draw, x, y, w, h):
    """A drone over desert blocks, for the Saudi strikes."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 214, 178))
    for bx, bw, bh in ((14, 56, 62), (86, 66, 84), (168, 60, 54),
                        (244, 48, 70)):
        draw.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                       fill=(176, 138, 96))
    cx, cy = x + w // 2, y + 44
    draw.rectangle([cx - 34, cy - 8, cx + 34, cy + 8], fill=(52, 52, 52))
    draw.line([cx - 58, cy - 6, cx - 30, cy - 6], fill=(52, 52, 52), width=3)
    draw.line([cx + 30, cy - 6, cx + 58, cy - 6], fill=(52, 52, 52), width=3)
    draw.ellipse([cx - 64, cy - 12, cx - 52, cy], fill=(90, 90, 90))
    draw.ellipse([cx + 52, cy - 12, cx + 64, cy], fill=(90, 90, 90))
    draw.ellipse([cx - 6, cy + 10, cx + 6, cy + 22], fill=(52, 52, 52))
    for ang in range(0, 360, 45):
        import math
        ex = cx + 26 * math.cos(math.radians(ang))
        ey = cy + 44 + 26 * math.sin(math.radians(ang))
        draw.line([cx, cy + 44, ex, ey], fill=(230, 120, 40), width=3)
    draw.ellipse([cx - 12, cy + 32, cx + 12, cy + 56], fill=(240, 160, 60))


def draw_sea(draw, x, y, w, h):
    """A small boat on rough waves, for the Senegal sinking."""
    draw.rectangle([x, y, x + w, y + h], fill=(196, 222, 236))
    draw.rectangle([x, y + h // 2, x + w, y + h], fill=(28, 84, 138))
    for wy in (8, 30, 52):
        for wx in range(0, w, 44):
            draw.arc([x + wx, y + h // 2 + wy, x + wx + 34,
                      y + h // 2 + wy + 18], 180, 360, fill=(255, 255, 255),
                     width=3)
    draw.polygon([(x + 96, y + h // 2 - 6), (x + 196, y + h // 2 - 6),
                  (x + 176, y + h // 2 + 26), (x + 116, y + h // 2 + 26)],
                 fill=(146, 74, 44))
    draw.line([x + 146, y + 22, x + 146, y + h // 2 - 6], fill=(80, 50, 30),
              width=4)
    draw.polygon([(x + 150, y + 26), (x + 196, y + h // 2 - 12),
                  (x + 150, y + h // 2 - 12)], fill=(250, 250, 250))
    draw.ellipse([x + 56, y + h // 2 + 34, x + 76, y + h // 2 + 54],
                 outline=(255, 255, 255), width=4)


def draw_calendar(draw, x, y, w, h):
    """A green field with a calendar showing a five-day week."""
    draw.rectangle([x, y, x + w, y + h], fill=(34, 130, 76))
    draw.polygon([(x + 20, y + h // 2), (x + w - 20, y + 26),
                  (x + w - 20, y + h - 26)], fill=(240, 210, 60))
    draw.rounded_rectangle([x + 30, y + 22, x + w - 30, y + h - 18], radius=8,
                           fill=(255, 255, 255))
    draw.rectangle([x + 30, y + 22, x + w - 30, y + 48], fill=(24, 60, 130))
    draw.text((x + w // 2, y + 26), "NOVEMBER", font=SANS_KICK,
              fill=(255, 255, 255), anchor="ma")
    for i, day in enumerate("MTWTFSS"):
        col = (34, 130, 76) if i < 5 else (196, 52, 44)
        draw.text((x + 44 + i * 28, y + 58), day, font=SANS_KICK, fill=col)
    draw.text((x + w // 2, y + 82), "5", font=_font("DejaVuSerif-Bold.ttf", 40),
              fill=(16, 28, 58), anchor="ma")


STORIES = [
    {
        "kicker": "GAMES  •  RECORDS",
        "tint": (110, 40, 150),
        "head": "GTA VI'S $2.36BN FIRST DAY",
        "deck": "Sensor Tower puts launch-day sales near 24.6 million copies — a record for any entertainment debut.",
        "art": draw_gamepad,
    },
    {
        "kicker": "MARKETS  •  TECH",
        "tint": (20, 100, 60),
        "head": "CLAUDE'S MAKER GOES PUBLIC",
        "deck": "Anthropic raises $81.3 billion in the biggest IPO ever; shares end day one up 17%.",
        "art": draw_chart,
    },
    {
        "kicker": "UKRAINE  •  WAR",
        "tint": (150, 40, 40),
        "head": "DRONE RAID SCARS KYIV",
        "deck": "Russian drones damage the Dutch and Austrian embassies; one person is killed, five hurt.",
        "art": draw_night_raid,
    },
    {
        "kicker": "MIDDLE EAST  •  WAR",
        "tint": (186, 32, 40),
        "head": "RIYADH TOWER HIT IN HOUTHI RAID",
        "deck": "A missile strike damages the PIF Tower as the rebels claim attacks on the airport and finance district.",
        "art": draw_drone,
    },
    {
        "kicker": "AFRICA  •  MIGRATION",
        "tint": (20, 90, 130),
        "head": "DOZENS LOST OFF SENEGAL",
        "deck": "A migrant boat bound for Europe capsizes near Yenne; around 100 people were aboard.",
        "art": draw_sea,
    },
    {
        "kicker": "AMERICAS  •  WORK",
        "tint": (30, 110, 80),
        "head": "BRAZIL'S WEEK GETS SHORTER",
        "deck": "Lula signs the decree ending the six-day week; hours fall to 42 in December, 40 by 2027.",
        "art": draw_calendar,
    },
]


def build():
    """Compose the front page and return the image."""
    img = Image.new("RGB", CANVAS, PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, 1024, 168], fill=NAVY)
    d.text((512, 26), "THE WORLD IN ONE PAGE", font=SANS_TAG, fill=GOLD,
           anchor="ma")
    d.text((512, 56), "FRIDAY 20 NOVEMBER 2026", font=SERIF_BIG,
           fill=(255, 255, 255), anchor="ma")
    d.rectangle([402, 128, 622, 132], fill=RULE)
    d.text((512, 140), "SIX STORIES THAT DEFINED THE DAY", font=SANS_KICK,
           fill=(201, 210, 224), anchor="ma")

    margin, gap = 26, 18
    cw = (1024 - 2 * margin - 2 * gap) // 3
    ch = 378
    tops = (186, 584)
    for i, story in enumerate(STORIES):
        col, row = i % 3, i // 3
        px = margin + col * (cw + gap)
        py = tops[row]
        d.rectangle([px, py, px + cw, py + ch], fill=CARD, outline=EDGE,
                    width=2)
        d.rectangle([px, py, px + cw, py + 8], fill=story["tint"])
        story["art"](d, px + 16, py + 20, cw - 32, 138)
        ty = py + 170
        d.text((px + 16, ty), story["kicker"], font=SANS_KICK,
               fill=story["tint"])
        hy = ty + 26
        for line in wrap_text(d, story["head"], SERIF_HEAD, cw - 32):
            d.text((px + 16, hy), line, font=SERIF_HEAD, fill=INK)
            hy += 32
        dy = hy + 6
        for line in wrap_text(d, story["deck"], SANS_DECK, cw - 32):
            d.text((px + 16, dy), line, font=SANS_DECK, fill=(64, 64, 64))
            dy += 20

    d.line([26, 984, 998, 984], fill=EDGE, width=1)
    d.text((512, 992),
           "Every story above happened, or was first reported, "
           "on Friday 20 November 2026.",
           font=SANS_FOOT, fill=(96, 96, 96), anchor="ma")
    return img


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    build().save(out)
    print("saved entry.png (1024, 1024)")
