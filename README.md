# Blix PowerPoint / PDF Fix

PowerPoint-compatible TrueType builds of **Blix (卜力士)**, a renamed
derivative of IBM Plex Sans TC.

These builds fix an issue where slides displayed correctly in PowerPoint but
exported PDFs showed Traditional Chinese characters as square boxes.

## Downloads

The repaired fonts are in [`fonts/Blix`](fonts/Blix):

- Blix Thin
- Blix ExtraLight
- Blix Light
- Blix Regular
- Blix Text
- Blix Medium
- Blix SemiBold
- Blix Bold

## What was fixed

- Populated the empty Windows BMP Unicode mapping tables:
  - `cmap` platform `3`, encoding `1`, format `4`
  - `cmap` platform `0`, encoding `3`, format `4`
- Preserved the complete format-12 Unicode mappings, including non-BMP
  characters.
- Confirmed `OS/2.fsType = 0`, allowing installable embedding.
- Normalized `Blix-Text` weight metadata from `450` to `400` for PDF
  compatibility.
- Updated font revision and unique IDs to prevent Windows from reusing stale
  cached font data.
- Recalculated TrueType checksums and validated all font tables.

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

1. Remove older Blix installations from Windows Settings or Control Panel.
2. Restart Windows to clear stale Office and Windows font caches.
3. Install all files from `fonts/Blix`.
4. In PowerPoint, enable **Embed fonts in the file** when saving.

## Notes on IBM Plex Sans TC

The same repair tool can be applied locally to IBM Plex Sans TC. Modified
builds retaining the reserved `Plex` name are not distributed here. Download
the official IBM Plex source from <https://github.com/IBM/plex>.

## License

Blix is distributed under the SIL Open Font License 1.1 inherited from IBM
Plex. See [`OFL.txt`](OFL.txt).

IBM's original license reserves the font name **Plex**. This derivative uses
the renamed family **Blix / 卜力士**.

