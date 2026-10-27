#!/usr/bin/env python3
"""Draws the FilmStar app icon: an engraving-style cinema camera on the violet tile.

Spec: 512-unit full-bleed tile (rx=112), exactly three colours (ink, paper, FilmStar violet), the
figure filling the tile, line work in an engraving style (hatching, knurling, stipple). Original
artwork drawn as code; no third-party material.

    python3 make_icon.py out.svg
"""
import math
import sys

INK, PAPER, VIOLET = "#0b0b0c", "#efe9dc", "#8b5cf6"


def f(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def line(x1, y1, x2, y2, w, color=INK, cap="round", dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{f(x1)} {f(y1)}L{f(x2)} {f(y2)}" stroke="{color}" stroke-width="{f(w)}" stroke-linecap="{cap}"{d} fill="none"/>'


def polar(r, deg, cx, cy):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def ticks(cx, cy, r1, r2, n, w, color=INK, start=0.0):
    out = []
    for i in range(n):
        x1, y1 = polar(r1, start + 360.0 * i / n, cx, cy)
        x2, y2 = polar(r2, start + 360.0 * i / n, cx, cy)
        out.append(line(x1, y1, x2, y2, w, color, "butt"))
    return "".join(out)


def star(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        x, y = polar(r_out if i % 2 == 0 else r_in, rot + i * 36, cx, cy)
        pts.append(f"{f(x)} {f(y)}")
    return "M" + "L".join(pts) + "Z"


def reel(cx, cy, r):
    """A film magazine seen side-on: ringed rim, six cut-outs, hub, engraved shadow."""
    g = []
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PAPER}" stroke="{INK}" stroke-width="9"/>')
    # engraved shadow on the lower-right of the rim
    sh = []
    for k in range(24):
        d = 10 + k * 3.4
        x1, y1 = polar(r - 16, d, cx, cy)
        x2, y2 = polar(r - 3, d, cx, cy)
        sh.append(line(x1, y1, x2, y2, 3.0, INK, "butt"))
    g.append("".join(sh))
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 16}" fill="none" stroke="{INK}" stroke-width="4"/>')
    # six cut-outs
    for i in range(6):
        x, y = polar(r * 0.55, 30 + i * 60, cx, cy)
        g.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r * 0.21)}" fill="{INK}"/>')
        x2, y2 = polar(r * 0.55 + r * 0.07, 30 + i * 60 - 28, cx, cy)
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{f(r * 0.24)}" fill="{INK}"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{f(r * 0.12)}" fill="{PAPER}"/>')
    return "".join(g)


def build():
    g = []
    defs = (
        '<defs>'
        '<clipPath id="t"><rect width="512" height="512" rx="112"/></clipPath>'
        '<clipPath id="b"><rect x="56" y="206" width="352" height="190" rx="26"/></clipPath>'
        '</defs>'
    )
    g.append(f'<rect width="512" height="512" fill="{VIOLET}"/>')

    # --- engraved field: sunburst behind the camera -------------------------------------------
    g.append(ticks(256, 250, 250, 430, 72, 2.4, INK, 2.5))

    # --- tripod legs (behind everything), running off the bottom edge -------------------------
    for pts in ("178 388 150 388 96 520 134 520", "334 388 306 388 380 520 418 520"):
        g.append(f'<path d="M{pts}Z" fill="{PAPER}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    for k in range(9):                                                  # leg hatching
        t = 0.1 + k * 0.1
        for (ax, ay, bx, by) in ((150, 388, 96, 520), (306, 388, 380, 520)):
            x, y = ax + (bx - ax) * t, ay + (by - ay) * t
            g.append(line(x + 2, y, x + 26 - 2 * k * 0.5, y + 4, 2.4, INK, "butt"))
    # tripod head
    g.append(f'<rect x="150" y="394" width="212" height="44" rx="12" fill="{PAPER}" stroke="{INK}" stroke-width="8"/>')
    for k in range(18):
        g.append(line(164 + k * 11, 402, 160 + k * 11, 430, 3.0, INK, "butt"))

    # --- film run: strip from each reel into the body ------------------------------------------
    for x in (126, 338):
        g.append(f'<rect x="{x}" y="176" width="46" height="44" fill="{INK}"/>')
        g.append(line(x + 23, 178, x + 23, 218, 28, PAPER, "butt", "7 6"))

    # --- magazines (the two reels) --------------------------------------------------------------
    g.append(reel(150, 118, 84))
    g.append(reel(362, 118, 84))

    # --- body ---------------------------------------------------------------------------------
    g.append(f'<rect x="56" y="206" width="352" height="190" rx="26" fill="{PAPER}" stroke="{INK}" stroke-width="9"/>')
    body = []
    for row in range(13):                                                # leatherette stipple, left grip
        y = 232 + row * 13
        for col in range(5):
            x = 78 + col * 14 + (7 if row % 2 else 0)
            body.append(f'<circle cx="{f(x)}" cy="{y}" r="2.4" fill="{INK}"/>')
    for k in range(-6, 46):                                              # shading along the bottom edge
        x = 40 + k * 9.0
        body.append(line(x, 396, x + 30, 358, 2.2 + 1.0 * ((k % 4) == 0), INK, "butt"))
    for k in range(6):
        body.append(line(56, 384 + k * 3, 408, 384 + k * 3, 1.6 + k * 0.5, INK, "butt"))
    g.append(f'<g clip-path="url(#b)">{"".join(body)}</g>')
    # star badge
    g.append(f'<circle cx="226" cy="296" r="56" fill="{INK}"/>')
    g.append(f'<circle cx="226" cy="296" r="48" fill="none" stroke="{PAPER}" stroke-width="3"/>')
    g.append(f'<path d="{star(226, 296, 38, 16)}" fill="{PAPER}"/>')
    g.append(ticks(226, 296, 41, 46, 36, 1.8, PAPER, 5))
    # counter window and record light
    g.append(f'<rect x="316" y="228" width="62" height="28" rx="7" fill="{INK}"/>')
    g.append(f'<rect x="324" y="235" width="24" height="9" rx="3" fill="{VIOLET}"/>')
    g.append(f'<circle cx="364" cy="272" r="10" fill="{INK}"/><circle cx="361" cy="269" r="3.4" fill="{PAPER}"/>')
    g.append(f'<rect x="56" y="206" width="352" height="190" rx="26" fill="none" stroke="{INK}" stroke-width="9"/>')

    # --- rear eyepiece (left) -------------------------------------------------------------------
    g.append(f'<rect x="22" y="262" width="44" height="76" rx="12" fill="{PAPER}" stroke="{INK}" stroke-width="8"/>')
    g.append(f'<rect x="12" y="276" width="20" height="48" rx="8" fill="{INK}"/>')
    for k in range(4):
        g.append(line(40, 274 + k * 16, 58, 274 + k * 16, 3.0, INK, "butt"))

    # --- lens barrel and matte box (right) ------------------------------------------------------
    g.append(f'<rect x="402" y="246" width="46" height="108" rx="8" fill="{PAPER}" stroke="{INK}" stroke-width="8"/>')
    for k in range(7):                                                   # knurled focus ring
        g.append(line(410 + k * 5.4, 252, 410 + k * 5.4, 348, 3.2, INK, "butt"))
    g.append(f'<path d="M444 226L506 190L506 410L444 374Z" fill="{PAPER}" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
    for k in range(8):                                                   # bellows folds
        x = 452 + k * 6.6
        g.append(line(x, 224 - k * 4.4, x, 376 + k * 4.4, 2.8, INK, "butt"))
    g.append(f'<ellipse cx="506" cy="300" rx="30" ry="98" fill="{INK}"/>')                  # front opening
    g.append(f'<ellipse cx="506" cy="300" rx="19" ry="84" fill="{VIOLET}"/>')
    g.append(f'<ellipse cx="506" cy="300" rx="9" ry="62" fill="{INK}"/>')
    g.append(f'<ellipse cx="503" cy="268" rx="3" ry="14" fill="{PAPER}"/>')

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">' + defs +
        '<g clip-path="url(#t)">' + "".join(g) + '</g></svg>\n'
    )


if __name__ == "__main__":
    open(sys.argv[1], "w", encoding="utf-8").write(build())
