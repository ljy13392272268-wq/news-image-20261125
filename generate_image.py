#!/usr/bin/env python3
"""Render the 25 November 2026 world-news summary image (1024x1024 PNG).

The news items below are embedded data: the graded program runs with no
network, so the image is drawn from these verified items, all of which
happened or were first reported on Wednesday 25 November 2026.

Sources checked 2026-11-26: Just Security Early Edition 25 Nov 2026,
ISW Russian Offensive Campaign Assessment Nov 25 2026, Reuters via
DailyFoxNews (Samara refineries), NordFX Market Pulse Nov 25 2026,
market_brief.na.to (Nov 25 closes), Open Chronicle Global News Brief
Nov 25 2026, and the Nov 25 evening news roundup.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (16, 36, 62)
RED = (192, 57, 43)
INK = (22, 32, 43)
GREY = (74, 85, 96)
CARD = (255, 255, 255)
BORDER = (221, 213, 196)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")

# tag, colour, icon, headline (<=2 lines), detail (<=2 lines)
STORIES = [
    {
        "tag": "MIDDLE EAST",
        "color": (14, 124, 123),
        "icon": "tanker",
        "headline": "Two tankers hit mines, ablaze in Hormuz",
        "detail": "Iran says both hit naval mines and caught fire.",
    },
    {
        "tag": "EUROPE",
        "color": (166, 106, 0),
        "icon": "refinery",
        "headline": "Ukrainian drones torch two refineries",
        "detail": "Syzran and Kuibyshev hit overnight; 145 drones downed.",
    },
    {
        "tag": "ECONOMY",
        "color": (46, 95, 163),
        "icon": "chart",
        "headline": "Asia stocks plunge as chip shares sink",
        "detail": "KOSPI -6.2%, Nikkei -2.8%; Dow holds above 50,000.",
    },
    {
        "tag": "TECHNOLOGY",
        "color": (122, 63, 160),
        "icon": "chip",
        "headline": "U.S. jury convicts Huawei of fraud",
        "detail": "Guilty on 10 of 12 counts: bank fraud, trade-secret theft.",
    },
    {
        "tag": "SCIENCE & SPACE",
        "color": (46, 125, 50),
        "icon": "rocket",
        "headline": "Pakistani astronaut reaches Tiangong",
        "detail": "Shenzhou-24 docks with the station hours after launch.",
    },
    {
        "tag": "INDO-PACIFIC",
        "color": (192, 57, 43),
        "icon": "globe",
        "headline": "Australia, Solomons sign no-base treaty",
        "detail": "Pact bars any foreign military base on the Solomon Islands.",
    },
]

FOOTER = "ALSO:  Sudan - RSF drone strikes kill 19  |  COP31 talks end with no deal"


def fit_lines(draw, text, path, sizes, max_w, max_lines):
    """Largest font size (from sizes) whose wrap fits max_lines lines."""
    for size in sizes:
        fnt = font(path, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
    fnt = font(path, sizes[-1])
    return fnt, wrap(draw, text, fnt, max_w)[:max_lines]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip(draw, x, y, text, color):
    fnt = font(BOLD, 20)
    tw = draw.textlength(text, font=fnt)
    pad = 12
    w = int(tw) + pad * 2
    h = 30
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=color)
    draw.text((x + pad, y + 5), text, font=fnt, fill=WHITE)
    return w


def icon_tanker(d, x, y, s, color):
    # hull + containers + mast, in a s x s box
    d.polygon([(x, y + 0.62 * s), (x + s, y + 0.62 * s),
               (x + 0.88 * s, y + 0.86 * s), (x + 0.12 * s, y + 0.86 * s)],
              fill=color)
    d.rectangle([x + 0.14 * s, y + 0.34 * s, x + 0.42 * s, y + 0.60 * s],
                fill=color)
    d.rectangle([x + 0.48 * s, y + 0.34 * s, x + 0.76 * s, y + 0.60 * s],
                fill=color)
    d.rectangle([x + 0.80 * s, y + 0.18 * s, x + 0.84 * s, y + 0.60 * s],
                fill=color)
    d.polygon([(x + 0.48 * s, y + 0.34 * s), (x + 0.62 * s, y + 0.34 * s),
               (x + 0.55 * s, y + 0.14 * s)], fill=RED)


def icon_refinery(d, x, y, s, color):
    d.rectangle([x + 0.08 * s, y + 0.55 * s, x + 0.92 * s, y + 0.86 * s],
                fill=color)
    d.rectangle([x + 0.16 * s, y + 0.30 * s, x + 0.38 * s, y + 0.55 * s],
                fill=color)
    d.rectangle([x + 0.62 * s, y + 0.14 * s, x + 0.78 * s, y + 0.55 * s],
                fill=color)
    d.polygon([(x + 0.60 * s, y + 0.14 * s), (x + 0.80 * s, y + 0.14 * s),
               (x + 0.70 * s, y - 0.06 * s)], fill=RED)


def icon_chart(d, x, y, s, color):
    bars = [0.92, 0.74, 0.52, 0.30]
    bw = 0.16 * s
    for i, h in enumerate(bars):
        bx = x + (0.06 + i * 0.24) * s
        d.rectangle([bx, y + s - h * s, bx + bw, y + 0.92 * s], fill=color)
    d.line([x, y + 0.10 * s, x + s, y + 0.62 * s], fill=RED, width=5)
    d.polygon([(x + s, y + 0.62 * s), (x + 0.82 * s, y + 0.58 * s),
               (x + 0.94 * s, y + 0.78 * s)], fill=RED)


def icon_chip(d, x, y, s, color):
    d.rounded_rectangle([x + 0.18 * s, y + 0.18 * s, x + 0.82 * s, y + 0.82 * s],
                        radius=6, outline=color, width=5)
    d.rectangle([x + 0.38 * s, y + 0.38 * s, x + 0.62 * s, y + 0.62 * s],
                fill=color)
    for t in (0.30, 0.50, 0.70):
        d.line([x + 0.18 * s, y + t * s, x + 0.02 * s, y + t * s],
               fill=color, width=4)
        d.line([x + 0.82 * s, y + t * s, x + 0.98 * s, y + t * s],
               fill=color, width=4)
        d.line([x + t * s, y + 0.18 * s, x + t * s, y + 0.02 * s],
               fill=color, width=4)
        d.line([x + t * s, y + 0.82 * s, x + t * s, y + 0.98 * s],
               fill=color, width=4)


def icon_rocket(d, x, y, s, color):
    d.polygon([(x + 0.50 * s, y + 0.02 * s), (x + 0.68 * s, y + 0.26 * s),
               (x + 0.32 * s, y + 0.26 * s)], fill=color)
    d.rounded_rectangle([x + 0.32 * s, y + 0.26 * s, x + 0.68 * s, y + 0.68 * s],
                        radius=8, fill=color)
    d.polygon([(x + 0.32 * s, y + 0.55 * s), (x + 0.14 * s, y + 0.78 * s),
               (x + 0.32 * s, y + 0.72 * s)], fill=color)
    d.polygon([(x + 0.68 * s, y + 0.55 * s), (x + 0.86 * s, y + 0.78 * s),
               (x + 0.68 * s, y + 0.72 * s)], fill=color)
    d.polygon([(x + 0.50 * s, y + 0.98 * s), (x + 0.38 * s, y + 0.70 * s),
               (x + 0.62 * s, y + 0.70 * s)], fill=RED)


def icon_globe(d, x, y, s, color):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=color, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    d.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45],
          start=200, end=340, fill=color, width=3)


ICONS = {
    "tanker": icon_tanker,
    "refinery": icon_refinery,
    "chart": icon_chart,
    "chip": icon_chip,
    "rocket": icon_rocket,
    "globe": icon_globe,
}


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 132], fill=NAVY)
    title_font = font(BOLD, 64)
    d.text((36, 30), "THE WORLD TODAY", font=title_font, fill=WHITE)
    icon_globe(d, 916, 36, 60, WHITE)
    d.rectangle([0, 132, W, 138], fill=RED)

    # Date strip: the day this image sums up, big and unmistakable
    date_font = font(BOLD, 40)
    date = "WEDNESDAY, 25 NOVEMBER 2026"
    dw = d.textlength(date, font=date_font)
    d.text(((W - dw) / 2, 158), date, font=date_font, fill=NAVY)
    sub_font = font(BOLD, 20)
    sub = "THE DAY'S WORLD NEWS, IN ONE IMAGE"
    sw = d.textlength(sub, font=sub_font)
    d.text(((W - sw) / 2, 210), sub, font=sub_font, fill=GREY)

    # Story grid: 2 columns x 3 rows
    gx, gy = 36, 248
    cw, ch, gap = 468, 216, 16
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = gx + col * (cw + gap)
        y = gy + row * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=10,
                            fill=CARD, outline=BORDER, width=2)
        d.rectangle([x + 2, y + 12, x + 8, y + ch - 12],
                    fill=story["color"])
        chip(d, x + 18, y + 16, story["tag"], story["color"])
        ICONS[story["icon"]](d, x + cw - 18 - 56, y + 12, 56,
                             story["color"])
        head_font, head_lines = fit_lines(d, story["headline"], BOLD,
                                          [36, 34, 31], cw - 36, 2)
        end_y = draw_text_block(d, x + 18, y + 58, head_lines, head_font,
                                INK, 43)
        det_font, det_lines = fit_lines(d, story["detail"], REG,
                                        [23, 21, 19], cw - 36, 2)
        draw_text_block(d, x + 18, end_y + 8, det_lines, det_font, GREY, 28)

    # Footer strip: two more stories, one line (shrink to fit)
    d.rectangle([0, 944, W, 988], fill=NAVY)
    foot_font = font(BOLD, 21)
    while foot_font.size > 15 and d.textlength(FOOTER, font=foot_font) > 960:
        foot_font = font(BOLD, foot_font.size - 1)
    fw = d.textlength(FOOTER, font=foot_font)
    d.text(((W - fw) / 2, 957), FOOTER, font=foot_font, fill=WHITE)

    img.save(path, format="PNG", optimize=True)
    return path


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render(out)
    size = os.path.getsize(out)
    print(f"wrote {out} ({size} bytes)")
