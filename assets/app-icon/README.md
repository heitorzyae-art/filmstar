# FilmStar app icon

A **cinema camera with a star on its body**: an engraving-style drawing, seen from the side, filling the
tile (full-bleed field, two film magazines on top, a matte box running off the right edge and tripod
legs running off the bottom). The line work is hatching, knurling and stipple; the star badge on the
body is the "Star" in FilmStar.

## Palette

Exactly three colours:

| Colour | Hex | Used for |
|---|---|---|
| Ink | `#0b0b0c` | line work and contours |
| Paper | `#efe9dc` | the figure |
| FilmStar violet (app colour) | `#8b5cf6` | the full-bleed field |

## Geometry

A 512-unit tile (`viewBox="0 0 512 512"`), rounded square with `rx=112`, no border. The macOS
renders (`filmstar.icns`, `filmstar-macos-512.png`, `filmstar-1024.png`) pad it onto Apple's
824/1024 icon grid; the Windows, Linux and web renders crop 22 units off each side so the figure
reads at 16-48 px.

## Provenance

Original artwork drawn as code by an AI assistant (Claude) for the FilmStar fork, in the style of
the icon it replaces. `make_icon.py` in this directory writes `filmstar.svg`; nothing is traced
from, or copied out of, another work. This replaces FilmCraft's earlier owl icon. License: see
`LICENSE.txt`.

## Files

| File | What |
|---|---|
| `make_icon.py` | draws the canonical artwork |
| `filmstar.svg`, `filmstar-small.svg` | the drawing (the small one is also the hicolor scalable icon) |
| `filmstar-1024.png` | 1024 px render on the macOS grid |
| `filmstar-macos-512.png` | runtime Dock icon on macOS (embedded by `apps/filmstar/src/main.rs`) |
| `filmstar.icns` | macOS bundle icon (`CFBundleIconFile`) |
| `filmstar.ico` | Windows icon, 16-256 px (embedded in `filmstar.exe` by `apps/filmstar/build.rs`) |
| `hicolor/<size>/apps/ai.storyteller.filmstar.png`, `hicolor/scalable/...svg` | Linux icon theme, used by `packaging/linux/ai.storyteller.filmstar.desktop` |

The web app's `apps/filmstar-web/web/favicon.png` (128 px) comes from the same drawing.
