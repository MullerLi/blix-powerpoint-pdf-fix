#!/usr/bin/env python3
"""Validate PowerPoint/PDF-relevant TrueType font properties."""

from __future__ import annotations

import argparse
from pathlib import Path

from fontTools.ttLib import TTFont


SAMPLE = "PowerPoint PDF 測試：中文國體，。！？（）— Aa09"


def validate_font(path: Path) -> list[str]:
    errors: list[str] = []
    font = TTFont(path, lazy=False, checkChecksums=2)
    best = font.getBestCmap() or {}
    bmp = {codepoint: glyph for codepoint, glyph in best.items() if codepoint <= 0xFFFF}

    try:
        unicode_bmp = next(
            table.cmap
            for table in font["cmap"].tables
            if (table.platformID, table.platEncID, table.format) == (0, 3, 4)
        )
        windows_bmp = next(
            table.cmap
            for table in font["cmap"].tables
            if (table.platformID, table.platEncID, table.format) == (3, 1, 4)
        )
    except StopIteration:
        errors.append("missing required format-4 cmap")
        return errors

    if unicode_bmp != bmp or windows_bmp != bmp:
        errors.append("format-4 cmap does not match the BMP portion of the best cmap")
    if font["OS/2"].fsType != 0:
        errors.append(f"embedding permission fsType is {font['OS/2'].fsType}, expected 0")
    if font["OS/2"].usWeightClass % 100 != 0:
        errors.append(f"nonstandard PDF weight class {font['OS/2'].usWeightClass}")

    missing = [char for char in SAMPLE if not char.isspace() and ord(char) not in windows_bmp]
    if missing:
        errors.append(f"sample characters missing: {''.join(missing)}")

    for tag in font.keys()[1:]:
        font.getTableData(tag)
    font.close()
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("font_dir", type=Path)
    args = parser.parse_args()

    failed = False
    for path in sorted(args.font_dir.glob("*.ttf")):
        errors = validate_font(path)
        if errors:
            failed = True
            print(f"FAIL {path.name}: {'; '.join(errors)}")
        else:
            print(f"PASS {path.name}")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

