#!/usr/bin/env python3
"""Rename the public IBM Plex Sans TC-derived builds to INK Sans TC."""

from __future__ import annotations

import argparse
from pathlib import Path

from fontTools.ttLib import TTFont


ENGLISH_FAMILY = "INK Sans TC"
TRADITIONAL_FAMILY = "墨黑體"
SIMPLIFIED_FAMILY = "墨黑体"
POSTSCRIPT_FAMILY = "INKSansTC"
VERSION = "1.003"
UNIQUE_SUFFIX = "2026-INKFIX"

TRADITIONAL_LANGUAGES = {(3, 1, 0x404), (3, 1, 0xC04)}
SIMPLIFIED_LANGUAGES = {(3, 1, 0x804)}


def localized_family(platform_id: int, encoding_id: int, language_id: int) -> str:
    language = (platform_id, encoding_id, language_id)
    if language in TRADITIONAL_LANGUAGES:
        return TRADITIONAL_FAMILY
    if language in SIMPLIFIED_LANGUAGES:
        return SIMPLIFIED_FAMILY
    return ENGLISH_FAMILY


def legacy_family(family: str, style: str) -> str:
    return family if style in {"Regular", "Bold"} else f"{family} {style}"


def full_name(family: str, style: str) -> str:
    return family if style == "Regular" else f"{family} {style}"


def rename_font(path: Path) -> Path:
    font = TTFont(path, lazy=False, recalcBBoxes=False, recalcTimestamp=False)
    name_table = font["name"]
    styles = {record.toUnicode() for record in name_table.names if record.nameID == 17}
    if len(styles) != 1:
        raise ValueError(f"{path}: expected one typographic style, found {sorted(styles)}")
    style = styles.pop()

    for record in list(name_table.names):
        family = localized_family(record.platformID, record.platEncID, record.langID)
        replacements = {
            1: legacy_family(family, style),
            3: f"{POSTSCRIPT_FAMILY};{style};{VERSION};{UNIQUE_SUFFIX}",
            4: full_name(family, style),
            5: f"Version {VERSION}",
            6: POSTSCRIPT_FAMILY if style == "Regular" else f"{POSTSCRIPT_FAMILY}-{style}",
            16: family,
        }
        replacement = replacements.get(record.nameID)
        if replacement is not None:
            name_table.setName(
                replacement,
                record.nameID,
                record.platformID,
                record.platEncID,
                record.langID,
            )

    font["head"].fontRevision = float(VERSION)
    output = path.with_name(f"{POSTSCRIPT_FAMILY}-{style}.ttf")
    font.save(output, reorderTables=True)
    font.close()
    if output != path:
        path.unlink()
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("font_dir", type=Path)
    args = parser.parse_args()

    for path in sorted(args.font_dir.glob("*.ttf")):
        output = rename_font(path)
        print(f"{path.name} -> {output.name}")


if __name__ == "__main__":
    main()
