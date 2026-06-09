#!/usr/bin/env python3
"""Repair Windows BMP cmap subtables for PowerPoint/PDF compatibility."""

from __future__ import annotations

import argparse
from pathlib import Path

from fontTools.ttLib import TTFont


def repair_font(path: Path, output: Path) -> tuple[int, int]:
    font = TTFont(path, lazy=False, recalcBBoxes=True, recalcTimestamp=False)
    best_cmap = font.getBestCmap()
    if not best_cmap:
        raise ValueError(f"{path}: no usable Unicode cmap")

    bmp_cmap = {codepoint: glyph for codepoint, glyph in best_cmap.items() if codepoint <= 0xFFFF}
    repaired = 0

    for table in font["cmap"].tables:
        if table.format == 4 and (table.platformID, table.platEncID) in {(0, 3), (3, 1)}:
            table.cmap = dict(bmp_cmap)
            table.language = 0
            repaired += 1

    if repaired != 2:
        raise ValueError(f"{path}: expected two Unicode format-4 cmap tables, found {repaired}")

    font.save(output, reorderTables=True)
    font.close()
    return len(best_cmap), len(bmp_cmap)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("fonts", nargs="+", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for path in args.fonts:
        output = args.output_dir / path.name
        total, bmp = repair_font(path, output)
        print(f"{path.name}: repaired {bmp} BMP mappings ({total} total Unicode mappings)")


if __name__ == "__main__":
    main()

