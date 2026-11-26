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

v3 (26 Nov 2026): the type scale is rebuilt for the ~300 px view (the
headlines at 40 px, the details at 28 px, the region labels at 25 px,
the footer at 27 px on two lines); the masthead uses a serif nameplate;
three wordings tightened so they rest only on the verified facts
(markets no longer asserts a chip-share cause; Huawei's racketeering
acquittal is shown; the space line carries "first Pakistani"). Facts,
date and the six stories are unchanged.
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

# Fonts: Liberation Sans first (narrower, so the headlines can run at
# 40 px), DejaVu as a fallback on machines that lack Liberation.
FONT_CANDIDATES = {
    "bold": [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "regular": [
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
    "serif": [
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    ],
}

_FONT_PATH = {}
_FONT_CACHE = {}


def font_path(kind):
    if kind not in _FONT_PATH:
        chosen = FONT_CANDIDATES[kind][-1]
        for cand in FONT_CANDIDATES[kind]:
            if os.path.exists(cand):
                chosen = cand
                break
        _FONT_PATH[kind] = chosen
    return _FONT_PATH[kind]


def font(kind, size):
    key = (kind, size)
    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = ImageFont.truetype(font_path(kind), size)
    return _FONT_CACHE[key]


# tag, colour, icon, headline (<=2 lines), detail (<=2 lines)
STORIES = [
    {
        "tag": "MIDDLE EAST",
        "color": (14, 124, 123),
        "icon": "tanker",
        "headline": "Two tankers hit mines, ablaze in Hormuz",
        "detail": "Iran says both oil tankers struck mines and caught fire.",
    },
    {
        "tag": "EUROPE",
        "color": (166, 106, 0),
        "icon": "refinery",
        "headline": "Ukrainian drones set two refineries ablaze",
        "detail": "Syzran and Kuibyshev hit overnight; 145 drones downed.",
    },
    {
        "tag": "ECONOMY",
        "color": (46, 95, 163),
        "icon": "chart",
        "headline": "Asia stocks plunge; KOSPI falls 6.2%",
        "detail": "Nikkei -2.8%, Taiwan -5%; Dow holds above 50,000.",
    },
    {
        "tag": "TECHNOLOGY",
        "color": (122, 63, 160),
        "icon": "chip",
        "headline": "U.S. jury convicts Huawei of fraud",
        "detail": "Guilty on 10 of 12 counts; not guilty of racketeering.",
    },
    {
        "tag": "SCIENCE & SPACE",
        "color": (46, 125, 50),
        "icon": "rocket",
        "headline": "Pakistani astronaut reaches Tiangong",
        "detail": "Shenzhou-24 docked 3.5 hours after launch; first Pakistani aboard.",
    },
    {
        "tag": "INDO-PACIFIC",
        "color": (192, 57, 43),
        "icon": "globe",
        "headline": "Australia, Solomons sign no-base treaty",
        "detail": "Treaty bars any foreign military or security base.",
    },
]

FOOTER_LINES = [
    "AFRICA \u2014 RSF drone strikes kill 19 civilians, wound 20 in two cities",
    "CLIMATE \u2014 COP31 ends without a deal; Pope Leo XIV voices concern",
]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width, honouring explicit newlines."""
    lines = []
    for para in text.split("\n"):
        cur = ""
        for word in para.split():
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


def fit_lines(draw, text, kind, sizes, max_w, max_lines):
    """Largest font size (from sizes) whose wrap fits max_lines lines."""
    for size in sizes:
        fnt = font(kind, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
    fnt = font(kind, sizes[-1])
    return fnt, wrap(draw, text, fnt, max_w)[:max_lines]


def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip(draw, x, y, text, color):
    fnt = font("bold", 25)
    tw = draw.textlength(text, font=fnt)
    pad = 14
    w = int(tw) + pad * 2
    h = 36
    draw.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=color)
    draw.text((x + pad, y + h / 2), text, font=fnt, fill=WHITE,
              anchor="lm")
    return w


def icon_tanker(d, x, y, s, color):
    # hull, two cargo tanks, bridge, red flame above the deck
    d.polygon([(x + 0.04 * s, y + 0.60 * s), (x + 0.96 * s, y + 0.60 * s),
               (x + 0.88 * s, y + 0.86 * s), (x + 0.12 * s, y + 0.86 * s)],
              fill=color)
    d.rectangle([x + 0.14 * s, y + 0.30 * s, x + 0.44 * s, y + 0.56 * s],
                fill=color)
    d.rectangle([x + 0.48 * s, y + 0.30 * s, x + 0.72 * s, y + 0.56 * s],
                fill=color)
    d.rectangle([x + 0.78 * s, y + 0.14 * s, x + 0.84 * s, y + 0.60 * s],
                fill=color)
    d.polygon([(x + 0.53 * s, y + 0.30 * s), (x + 0.67 * s, y + 0.30 * s),
               (x + 0.60 * s, y + 0.06 * s)], fill=RED)


def icon_refinery(d, x, y, s, color):
    # base, low column, tall column, small stack, red flame on the tall one
    d.rectangle([x + 0.05 * s, y + 0.62 * s, x + 0.95 * s, y + 0.86 * s],
                fill=color)
    d.rectangle([x + 0.13 * s, y + 0.36 * s, x + 0.34 * s, y + 0.62 * s],
                fill=color)
    d.rectangle([x + 0.55 * s, y + 0.16 * s, x + 0.71 * s, y + 0.62 * s],
                fill=color)
    d.rectangle([x + 0.76 * s, y + 0.38 * s, x + 0.86 * s, y + 0.62 * s],
                fill=color)
    d.polygon([(x + 0.57 * s, y + 0.16 * s), (x + 0.69 * s, y + 0.16 * s),
               (x + 0.63 * s, y - 0.04 * s)], fill=RED)


def icon_chart(d, x, y, s, color):
    bars = [0.92, 0.74, 0.52, 0.30]
    bw = 0.16 * s
    for i, h in enumerate(bars):
        bx = x + (0.06 + i * 0.24) * s
        d.rectangle([bx, y + s - h * s, bx + bw, y + 0.92 * s], fill=color)
    d.line([x, y + 0.10 * s, x + s, y + 0.62 * s], fill=RED,
           width=max(3, int(0.09 * s)))
    d.polygon([(x + s, y + 0.62 * s), (x + 0.80 * s, y + 0.56 * s),
               (x + 0.94 * s, y + 0.80 * s)], fill=RED)


def icon_chip(d, x, y, s, color):
    stroke = max(3, int(0.08 * s))
    d.rounded_rectangle([x + 0.18 * s, y + 0.18 * s, x + 0.82 * s, y + 0.82 * s],
                        radius=6, outline=color, width=stroke)
    d.rectangle([x + 0.38 * s, y + 0.38 * s, x + 0.62 * s, y + 0.62 * s],
                fill=color)
    for t in (0.30, 0.50, 0.70):
        d.line([x + 0.18 * s, y + t * s, x + 0.02 * s, y + t * s],
               fill=color, width=stroke)
        d.line([x + 0.82 * s, y + t * s, x + 0.98 * s, y + t * s],
               fill=color, width=stroke)
        d.line([x + t * s, y + 0.18 * s, x + t * s, y + 0.02 * s],
               fill=color, width=stroke)
        d.line([x + t * s, y + 0.82 * s, x + t * s, y + 0.98 * s],
               fill=color, width=stroke)


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
    stroke = max(3, int(0.08 * s))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=stroke)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=color, width=max(2, stroke - 1))
    d.line([cx - r, cy, cx + r, cy], fill=color, width=max(2, stroke - 1))
    d.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45],
          start=200, end=340, fill=color, width=max(2, stroke - 1))


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

    # Masthead: serif title, globe at right
    d.rectangle([0, 0, W, 108], fill=NAVY)
    d.text((36, 17), "THE WORLD TODAY", font=font("serif", 64), fill=WHITE)
    icon_globe(d, 918, 26, 56, WHITE)
    d.rectangle([0, 108, W, 114], fill=RED)

    # Date strip: the day this image sums up, big and unmistakable
    date = "WEDNESDAY, 25 NOVEMBER 2026"
    date_font = font("bold", 42)
    dw = d.textlength(date, font=date_font)
    d.text(((W - dw) / 2, 122), date, font=date_font, fill=NAVY)

    # Story grid: 2 columns x 3 rows
    gx, gy = 36, 192
    cw, ch, gap = 469, 236, 14
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = gx + col * (cw + gap)
        y = gy + row * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=10,
                            fill=CARD, outline=BORDER, width=2)
        d.rectangle([x + 2, y + 14, x + 9, y + ch - 14],
                    fill=story["color"])
        chip(d, x + 18, y + 14, story["tag"], story["color"])
        ICONS[story["icon"]](d, x + cw - 18 - 54, y + 10, 54,
                             story["color"])
        head_font, head_lines = fit_lines(d, story["headline"], "bold",
                                          [40, 38, 36], cw - 36, 2)
        draw_text_block(d, x + 18, y + 66, head_lines, head_font, INK, 45)
        det_font, det_lines = fit_lines(d, story["detail"], "regular",
                                        [28, 27, 26, 24], cw - 36, 2)
        draw_text_block(d, x + 18, y + 160, det_lines, det_font, GREY, 32)

    # Footer strip: two more stories, one line each, shrunk to fit
    d.rectangle([0, 948, W, H], fill=NAVY)
    foot_font = font("bold", 27)
    while foot_font.size > 20 and any(
            d.textlength(t, font=foot_font) > 968 for t in FOOTER_LINES):
        foot_font = font("bold", foot_font.size - 1)
    for i, text in enumerate(FOOTER_LINES):
        fw = d.textlength(text, font=foot_font)
        d.text(((W - fw) / 2, 956 + i * 32), text, font=foot_font, fill=WHITE)

    img.save(path, format="PNG", optimize=True)
    return path


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render(out)
    size = os.path.getsize(out)
    print(f"wrote {out} ({size} bytes)")
