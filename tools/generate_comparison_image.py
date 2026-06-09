#!/usr/bin/env python3
"""Generate the README typeface comparison image from the published fonts."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "ibm-plex-blix-ink-comparison.png"
INK_FONT = ROOT / "fonts" / "INK-Sans-TC" / "INKSansTC-Regular.ttf"
BLIX_FONT = ROOT / "fonts" / "Blix" / "Blix-Regular.ttf"

WIDTH = 1800
HEIGHT = 1120
MARGIN = 72
CARD_LEFT = 64
CARD_RIGHT = WIDTH - 64
TEXT_LEFT = 590
SAMPLE = (
    "IBM Plex Sans TC 承襲 Franklin Gothic 特徵，字體採用大中宮、接近正方形的結構，\n"
    "繁體中文版更採用臺灣傳統印刷體寫法，散發冷靜理性的工程美學與清晰度。\n"
    "字形比較：臺灣 墨黑體 簡報輸出 PDF，標點「，。！？（）」。"
)


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size=size)


def rounded_card(draw: ImageDraw.ImageDraw, top: int, bottom: int, accent: str) -> None:
    draw.rounded_rectangle(
        (CARD_LEFT, top, CARD_RIGHT, bottom),
        radius=28,
        fill="#ffffff",
        outline="#d8dee8",
        width=2,
    )
    draw.rounded_rectangle(
        (CARD_LEFT, top, CARD_LEFT + 14, bottom),
        radius=7,
        fill=accent,
    )


def main() -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), "#f4f6f9")
    draw = ImageDraw.Draw(image)
    title_font = font(INK_FONT, 56)
    subtitle_font = font(INK_FONT, 25)
    label_font = font(INK_FONT, 34)
    sample_ink = font(INK_FONT, 28)
    sample_blix = font(BLIX_FONT, 28)

    draw.text((MARGIN, 48), "IBM Plex Sans TC 衍生字型比較", font=title_font, fill="#141820")
    draw.text(
        (MARGIN, 121),
        "相同文字、相同字級。INK Sans TC 僅修正命名與 PowerPoint / PDF 相容性，不重新設計字形。",
        font=subtitle_font,
        fill="#4b5565",
    )

    rows = [
        (
            190,
            460,
            "#4263eb",
            "IBM Plex Sans TC",
            sample_ink,
        ),
        (
            485,
            755,
            "#e8590c",
            "Blix（卜力士）",
            sample_blix,
        ),
        (
            780,
            1050,
            "#087f5b",
            "INK Sans TC（墨黑體）",
            sample_ink,
        ),
    ]

    for top, bottom, accent, label, sample_font in rows:
        rounded_card(draw, top, bottom, accent)
        draw.text((104, top + 96), label, font=label_font, fill="#171a21")
        draw.multiline_text(
            (TEXT_LEFT, top + 36),
            SAMPLE,
            font=sample_font,
            fill="#111318",
            spacing=11,
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, optimize=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
