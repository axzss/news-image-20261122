#!/usr/bin/env python3
"""Render THE WORLD - Sunday 22 November 2026 (news-image-20261122).

A newspaper front page summarising the day's world news, drawn with PIL so
every word is exactly as reported. All facts were checked against wire
reports of 22 November 2026 (multiple sources agreeing on each story).

Layout: 1024x1024, newsprint cream paper, serif masthead, a generated
dusk photograph of tankers in the Strait of Hormuz for the lead story,
three columns for the next stories, an ALSO TODAY strip and a markets line.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(ASSETS, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (20, 20, 20)
RED = (163, 22, 33)
GREY = (107, 100, 85)
BOX = (233, 226, 208)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_D = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, cx, y, text, fnt, fill, tracking=6):
    """Draw text centred on cx with letter tracking (for the dateline)."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36  # side margin

    # ---- masthead ----
    d.line([(mx, 10), (W - mx, 10)], fill=INK, width=3)
    d.text((W // 2, 24), "THE WORLD", font=font(SERIF_B, 96),
           fill=INK, anchor="ma")
    d.line([(mx, 128), (W - mx, 128)], fill=INK, width=2)
    tracked(d, W // 2, 138, "SUNDAY, 22 NOVEMBER 2026",
            font(SANS_B, 24), INK, tracking=7)
    d.line([(mx, 172), (W - mx, 172)], fill=INK, width=2)

    # ---- hero photograph (tankers, Strait of Hormuz at dusk) ----
    hero = Image.open(os.path.join(ASSETS, "hero.jpg")).convert("RGB")
    hw, hh = 952, 330
    scale = max(hw / hero.width, hh / hero.height)
    hero = hero.resize((int(hero.width * scale) + 1,
                        int(hero.height * scale) + 1), Image.LANCZOS)
    left = (hero.width - hw) // 2
    top = (hero.height - hh) // 2
    img.paste(hero.crop((left, top, left + hw, top + hh)), (mx, 184))
    d.rectangle([mx, 184, W - mx, 514], outline=INK, width=2)

    # ---- caption under the hero ----
    cap = ("Two tankers cross the Strait of Hormuz at dusk. Iran struck an "
           "industrial site in Bahrain late on Saturday, and two tankers "
           "were reported hit near the strait.")
    lines = wrap(d, cap, font(SERIF_I, 20), W - 2 * mx)
    y = 524
    for ln in lines:
        d.text((W // 2, y), ln, font=font(SERIF_I, 20), fill=GREY,
               anchor="ma")
        y += 26

    # ---- lead headline + dek ----
    d.text((W // 2, 584), "IRAN STRIKES BAHRAIN", font=font(SERIF_B, 48),
           fill=INK, anchor="ma")
    d.text((W // 2, 640), "AS GULF CRISIS DEEPENS", font=font(SERIF_B, 48),
           fill=INK, anchor="ma")
    dek = ("Tehran hits an industrial site in Bahrain; Bahrain says civilian "
           "property was struck, while Iran's Revolutionary Guards claim "
           "they targeted US bases.")
    lines = wrap(d, dek, font(SANS, 21), W - 2 * mx - 40)
    y = 700
    for ln in lines:
        d.text((W // 2, y), ln, font=font(SANS, 21), fill=INK, anchor="ma")
        y += 27
    d.line([(mx, 758), (W - mx, 758)], fill=INK, width=2)

    # ---- three columns ----
    cols = [
        ("CLIMATE", "COP31 talks run into overtime",
         "Antalya summit in overtime, deadlocked over fossil fuels."),
        ("JUSTICE", "Mexico captures \u2018El Chapo Isidro\u2019",
         "Eleven killed in the Sinaloa raid that caught the cartel boss."),
        ("MARKETS", "AI sell-off drags US stocks into correction",
         "The Dow and S&P 500 fall sharply as chip shares tumble."),
    ]
    col_w = (W - 2 * mx - 2 * 28) // 3
    for i, (kick, head, body) in enumerate(cols):
        x0 = mx + i * (col_w + 28)
        d.text((x0, 770), kick, font=font(SANS_B, 17), fill=RED)
        lines = wrap(d, head, font(SERIF_B, 24), col_w)
        y = 792
        for ln in lines:
            d.text((x0, y), ln, font=font(SERIF_B, 24), fill=INK)
            y += 27
        lines = wrap(d, body, font(SANS, 18), col_w)
        y += 4
        for ln in lines:
            d.text((x0, y), ln, font=font(SANS, 18), fill=INK)
            y += 22
        if i < 2:
            d.line([(x0 + col_w + 14, 770), (x0 + col_w + 14, 892)],
                   fill=GREY, width=1)

    # ---- also today ----
    d.rectangle([mx, 906, W - mx, 960], fill=BOX)
    also = ("ALSO TODAY  \u2014  Trump, Xi and Putin meet in Shenzhen  \u00b7  "
            "Russia hits Zelensky\u2019s home town, Kryvyi Rih  \u00b7  EU and "
            "Indonesia sign a trade deal  \u00b7  GTA VI sets a $3.8bn "
            "first-day sales record")
    lines = wrap(d, also, font(SANS, 18), W - 2 * mx - 24)
    y = 910
    for ln in lines:
        d.text((mx + 12, y), ln, font=font(SANS, 18), fill=INK)
        y += 23

    # ---- markets ticker + footer ----
    tick = ("MARKETS   S&P 500  6,910  \u25bc 3.70%     FTSE 100  10,346  "
            "\u25bc 1.02%     Brent crude  $89.95  \u25b2 0.57%")
    tick_size = 18
    while (d.textlength(tick, font=font(SANS_D, tick_size)) > W - 2 * mx
           and tick_size > 12):
        tick_size -= 1
    d.text((W // 2, 968), tick, font=font(SANS_D, tick_size), fill=INK,
           anchor="ma")
    d.text((W // 2, 996), "All stories as reported on Sunday 22 November 2026",
           font=font(SERIF_I, 16), fill=GREY, anchor="ma")

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
