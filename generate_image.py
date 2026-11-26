#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news summary as a 1024x1024 PNG.

One-page newspaper layout: a navy masthead, a centred date line, six
story cards in a 2x3 grid, and a navy footer band with two more stories.

Every news wording below is fixed copy, verified against 25 November 2026
reporting. The generator takes no input and makes no network calls, so
re-running it produces byte-identical output.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

# --- page geometry -------------------------------------------------------
PAGE_W, PAGE_H = 1024, 1024
MASTHEAD_H = 132
RULE_H = 6
DATE_Y = 144
GRID_X, GRID_TOP = 36, 192
CARD_W, CARD_H = 469, 236
GAP = 14
FOOTER_Y, FOOTER_H = 952, 72
TEXT_W = CARD_W - 36  # text column inside a card

# --- palette -------------------------------------------------------------
PAPER = (247, 243, 234)
NAVY = (16, 36, 62)
RED = (192, 57, 43)
INK = (22, 32, 43)
GREY = (74, 85, 96)
CARD = (255, 255, 255)
BORDER = (221, 213, 196)
WHITE = (255, 255, 255)

# --- type ----------------------------------------------------------------
# Prefer the narrower Liberation faces (Arial metrics) so the 40 px
# headlines still fit two lines; DejaVu is the fallback on this machine.
_LIB = "/usr/share/fonts/truetype/liberation"
_DJV = "/usr/share/fonts/truetype/dejavu"
_FACES = {
    "sans-bold": [os.path.join(_LIB, "LiberationSans-Bold.ttf"),
                  os.path.join(_DJV, "DejaVuSans-Bold.ttf")],
    "sans": [os.path.join(_LIB, "LiberationSans-Regular.ttf"),
             os.path.join(_DJV, "DejaVuSans.ttf")],
    "serif-bold": [os.path.join(_LIB, "LiberationSerif-Bold.ttf"),
                   os.path.join(_DJV, "DejaVuSerif-Bold.ttf")],
}


def typeface(kind, size):
    """First available file for a face kind, at the requested size."""
    for path in _FACES[kind]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    raise FileNotFoundError("no font file found for %r" % kind)


# --- fixed copy (verified 25 November 2026) -------------------------------
DATE_LINE = "WEDNESDAY, 25 NOVEMBER 2026"

# detail may hold "\n" to force a line break (card 5: keep "3.5 hours"
# whole on the second line).
STORIES = [
    dict(tag="MIDDLE EAST", colour=(14, 124, 123), icon="tanker",
         headline="Two tankers hit mines, ablaze in Hormuz",
         detail="Iran says both oil tankers struck mines and caught fire."),
    dict(tag="EUROPE", colour=(166, 106, 0), icon="refinery",
         headline="Ukrainian drones set two refineries ablaze",
         detail="Syzran and Kuibyshev hit overnight; 145 drones downed."),
    dict(tag="ECONOMY", colour=(46, 95, 163), icon="chart",
         headline="Asia stocks plunge; KOSPI falls 6.2%",
         detail="Nikkei -2.8%, Taiwan -5%; Dow holds above 50,000."),
    dict(tag="TECHNOLOGY", colour=(122, 63, 160), icon="chip",
         headline="U.S. jury convicts Huawei of fraud",
         detail="Guilty on 10 of 12 counts; not guilty of racketeering."),
    dict(tag="SCIENCE & SPACE", colour=(46, 125, 50), icon="rocket",
         headline="Pakistani astronaut reaches Tiangong",
         detail="Shenzhou-24 docked in\n3.5 hours; first Pakistani aboard."),
    dict(tag="INDO-PACIFIC", colour=(192, 57, 43), icon="globe",
         headline="Australia, Solomons sign no-base treaty",
         detail="Treaty bars any foreign military or security base."),
]

FOOTER_LINES = [
    "AFRICA — RSF drone strikes kill 19 civilians, wound 20 in two cities",
    "CLIMATE — COP31 ends without a deal; Pope Leo XIV voices concern",
]


# --- text fitting --------------------------------------------------------
def wrap_words(draw, text, fnt, max_w):
    """Greedy word wrap; returns the lines for one unbroken paragraph."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_block(draw, text, kind, sizes, max_w, max_lines):
    """Pick the first size whose wrap fits max_lines lines.

    Returns (font, lines, size). A "\n" in the text forces a break and
    each part is wrapped on its own.
    """
    parts = text.split("\n")
    for size in sizes:
        fnt = typeface(kind, size)
        lines = []
        for part in parts:
            lines.extend(wrap_words(draw, part, fnt, max_w))
        if len(lines) <= max_lines:
            return fnt, lines, size
    fnt = typeface(kind, sizes[-1])
    lines = []
    for part in parts:
        lines.extend(wrap_words(draw, part, fnt, max_w))
    return fnt, lines[:max_lines], sizes[-1]


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    """Draw stacked lines; returns the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# --- card furniture ------------------------------------------------------
def draw_chip(draw, x, y, text, colour):
    """Coloured tag chip, 36 px tall, 27 px bold white label."""
    fnt = typeface("sans-bold", 27)
    width = int(draw.textlength(text, font=fnt)) + 24
    draw.rounded_rectangle([x, y, x + width, y + 36], radius=8, fill=colour)
    draw.text((x + 12, y + 18), text, font=fnt, fill=WHITE, anchor="lm")
    return width


def draw_tanker(d, x, y, s, colour):
    hull_top = y + 0.62 * s
    d.polygon([(x, hull_top), (x + s, hull_top),
               (x + 0.88 * s, y + 0.86 * s),
               (x + 0.12 * s, y + 0.86 * s)], fill=colour)
    d.rectangle([x + 0.14 * s, y + 0.34 * s, x + 0.42 * s, y + 0.60 * s],
                fill=colour)
    d.rectangle([x + 0.48 * s, y + 0.34 * s, x + 0.76 * s, y + 0.60 * s],
                fill=colour)
    d.rectangle([x + 0.80 * s, y + 0.18 * s, x + 0.84 * s, y + 0.60 * s],
                fill=colour)
    d.polygon([(x + 0.48 * s, y + 0.34 * s), (x + 0.62 * s, y + 0.34 * s),
               (x + 0.55 * s, y + 0.14 * s)], fill=RED)


def draw_refinery(d, x, y, s, colour):
    d.rectangle([x + 0.08 * s, y + 0.55 * s, x + 0.92 * s, y + 0.86 * s],
                fill=colour)
    d.rectangle([x + 0.16 * s, y + 0.30 * s, x + 0.38 * s, y + 0.55 * s],
                fill=colour)
    d.rectangle([x + 0.62 * s, y + 0.14 * s, x + 0.78 * s, y + 0.55 * s],
                fill=colour)
    d.polygon([(x + 0.60 * s, y + 0.14 * s), (x + 0.80 * s, y + 0.14 * s),
               (x + 0.70 * s, y - 0.06 * s)], fill=RED)


def draw_chart(d, x, y, s, colour):
    heights = [0.92, 0.74, 0.52, 0.30]
    bar_w = 0.16 * s
    for i, h in enumerate(heights):
        bx = x + (0.06 + i * 0.24) * s
        d.rectangle([bx, y + s - h * s, bx + bar_w, y + 0.92 * s],
                    fill=colour)
    d.line([x, y + 0.10 * s, x + s, y + 0.62 * s], fill=RED, width=5)
    d.polygon([(x + s, y + 0.62 * s), (x + 0.82 * s, y + 0.58 * s),
               (x + 0.94 * s, y + 0.78 * s)], fill=RED)


def draw_chip_icon(d, x, y, s, colour):
    d.rounded_rectangle([x + 0.18 * s, y + 0.18 * s,
                         x + 0.82 * s, y + 0.82 * s],
                        radius=6, outline=colour, width=5)
    d.rectangle([x + 0.38 * s, y + 0.38 * s, x + 0.62 * s, y + 0.62 * s],
                fill=colour)
    for t in (0.30, 0.50, 0.70):
        d.line([x + 0.18 * s, y + t * s, x + 0.02 * s, y + t * s],
               fill=colour, width=4)
        d.line([x + 0.82 * s, y + t * s, x + 0.98 * s, y + t * s],
               fill=colour, width=4)
        d.line([x + t * s, y + 0.18 * s, x + t * s, y + 0.02 * s],
               fill=colour, width=4)
        d.line([x + t * s, y + 0.82 * s, x + t * s, y + 0.98 * s],
               fill=colour, width=4)


def draw_rocket(d, x, y, s, colour):
    d.polygon([(x + 0.50 * s, y + 0.02 * s), (x + 0.68 * s, y + 0.26 * s),
               (x + 0.32 * s, y + 0.26 * s)], fill=colour)
    d.rounded_rectangle([x + 0.32 * s, y + 0.26 * s,
                         x + 0.68 * s, y + 0.68 * s],
                        radius=8, fill=colour)
    d.polygon([(x + 0.32 * s, y + 0.55 * s), (x + 0.14 * s, y + 0.78 * s),
               (x + 0.32 * s, y + 0.72 * s)], fill=colour)
    d.polygon([(x + 0.68 * s, y + 0.55 * s), (x + 0.86 * s, y + 0.78 * s),
               (x + 0.68 * s, y + 0.72 * s)], fill=colour)
    d.polygon([(x + 0.50 * s, y + 0.98 * s), (x + 0.38 * s, y + 0.70 * s),
               (x + 0.62 * s, y + 0.70 * s)], fill=RED)


def draw_globe(d, x, y, s, colour):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=5)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=colour, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=colour, width=3)
    d.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45],
          start=200, end=340, fill=colour, width=3)


ICON_DRAWERS = {
    "tanker": draw_tanker,
    "refinery": draw_refinery,
    "chart": draw_chart,
    "chip": draw_chip_icon,
    "rocket": draw_rocket,
    "globe": draw_globe,
}


# --- page ----------------------------------------------------------------
def render(path):
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(img)
    report = []

    # Masthead: serif nameplate, globe at right, red rule underneath.
    d.rectangle([0, 0, PAGE_W, MASTHEAD_H], fill=NAVY)
    name_font = typeface("serif-bold", 64)
    d.text((36, 34), "THE WORLD TODAY", font=name_font, fill=WHITE)
    draw_globe(d, 916, (MASTHEAD_H - 54) // 2, 54, WHITE)
    d.rectangle([0, MASTHEAD_H, PAGE_W, MASTHEAD_H + RULE_H], fill=RED)

    # Date line: the day this image sums up, big and unmistakable.
    date_font = typeface("sans-bold", 42)
    dw = d.textlength(DATE_LINE, font=date_font)
    d.text(((PAGE_W - dw) / 2, DATE_Y), DATE_LINE, font=date_font, fill=NAVY)
    report.append("date: 42px, width %dpx" % dw)

    # Story grid: 2 columns x 3 rows.
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = GRID_X + col * (CARD_W + GAP)
        y = GRID_TOP + row * (CARD_H + GAP)
        d.rounded_rectangle([x, y, x + CARD_W, y + CARD_H], radius=10,
                            fill=CARD, outline=BORDER, width=2)
        d.rectangle([x + 2, y + 12, x + 8, y + CARD_H - 12],
                    fill=story["colour"])
        draw_chip(d, x + 18, y + 14, story["tag"], story["colour"])
        # Icon sits in the top-right corner; the headline starts below it,
        # so the two can never overlap.
        ICON_DRAWERS[story["icon"]](d, x + CARD_W - 18 - 54, y + 12, 54,
                                    story["colour"])
        head_font, head_lines, head_size = fit_block(
            d, story["headline"], "sans-bold", [40], TEXT_W, 2)
        draw_lines(d, x + 18, y + 68, head_lines, head_font, INK, 48)
        det_font, det_lines, det_size = fit_block(
            d, story["detail"], "sans", [30, 29, 28, 26, 24], TEXT_W, 2)
        draw_lines(d, x + 18, y + 164, det_lines, det_font, GREY, 34)
        report.append(
            "card %d %s: headline %dpx %d lines, detail %dpx %d lines"
            % (i + 1, story["tag"], head_size, len(head_lines),
               det_size, len(det_lines)))
        if len(head_lines) != 2 or len(det_lines) != 2:
            raise SystemExit("card %d does not fit in two lines each"
                             % (i + 1))

    # Footer band: two extra stories, one line each, centred.
    d.rectangle([0, FOOTER_Y, PAGE_W, FOOTER_Y + FOOTER_H], fill=NAVY)
    foot_font = typeface("sans-bold", 27)
    fy = FOOTER_Y + (FOOTER_H - (27 + 32)) // 2
    for line in FOOTER_LINES:
        fw = d.textlength(line, font=foot_font)
        d.text(((PAGE_W - fw) / 2, fy), line, font=foot_font, fill=WHITE)
        report.append("footer: 27px, width %dpx" % fw)
        fy += 32

    img.save(path, format="PNG", optimize=True)
    return report


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    for line in render(out):
        print(line)
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))
