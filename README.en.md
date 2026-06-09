# Blix PowerPoint / PDF Compatibility Fix

[繁體中文 README](README.md)

This repository provides PowerPoint-compatible TrueType builds of
**Blix (卜力士)**, a renamed derivative of IBM Plex Sans TC.

These builds fix an issue where the fonts displayed correctly in PowerPoint,
but Traditional Chinese characters became square boxes after PDF export. They
also improve font embedding, PDF subsetting, and Windows font-cache
compatibility.

## Downloads

The eight repaired Blix weights are available in [`fonts/Blix`](fonts/Blix):

- Blix Thin
- Blix ExtraLight
- Blix Light
- Blix Regular
- Blix Text
- Blix Medium
- Blix SemiBold
- Blix Bold

## Fixes

- Populated the previously empty Windows BMP Unicode mapping tables:
  - `cmap` platform `3`, encoding `1`, format `4`
  - `cmap` platform `0`, encoding `3`, format `4`
- Preserved the complete format-12 Unicode mappings, including non-BMP
  characters.
- Confirmed `OS/2.fsType = 0`, allowing installation and embedding.
- Normalized the nonstandard `Blix-Text` weight metadata from `450` to `400`.
- Updated font revisions and unique IDs to reduce stale Windows font-cache
  reuse.
- Recalculated TrueType checksums and validated every font table.

## Validation

The repaired builds passed:

- Windows `T2Embed.dll` full-font embedding
- Windows `T2Embed.dll` subset embedding
- PowerPoint font embedding
- PowerPoint PDF export
- PDF embedded-font inspection
- Traditional Chinese PDF text extraction

Run the included validator:

```powershell
python -m pip install fonttools
python tools/validate_fonts.py fonts/Blix
```

## Installation

1. Remove older Blix installations through Windows Settings or Control Panel.
2. Restart Windows to clear stale Office and Windows font caches.
3. Install every font in [`fonts/Blix`](fonts/Blix).
4. Enable **Embed fonts in the file** when saving a PowerPoint presentation.

## IBM Plex Sans TC

The included repair tool can also be applied to IBM Plex Sans TC. Because
`Plex` is a Reserved Font Name under the SIL OFL, this repository does not
distribute modified builds that retain the original name.

Download IBM Plex Sans TC from the
[official IBM Plex repository](https://github.com/IBM/plex).

## License Agreements

The applicable official agreement is the
**SIL Open Font License 1.1 (SIL OFL 1.1)**. There is no official font license
named “SLC” for IBM Plex or Blix; if “SLC” was intended to mean “SIL,” the
corresponding files are:

- [Blix SIL OFL 1.1 agreement](LICENSES/Blix-SIL-OFL-1.1.txt)
- [Blix modification notice](LICENSES/Blix-MODIFICATION-NOTICE.md)
- [IBM Plex Sans TC SIL OFL 1.1 agreement](LICENSES/IBM-Plex-Sans-TC-SIL-OFL-1.1.txt)
- [IBM official original agreement](OFL.txt)

IBM's original agreement reserves the font name **Plex**. This derivative uses
the renamed family **Blix / 卜力士** and declares no additional Reserved Font
Names.

