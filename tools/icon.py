#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""BentoBook's icon: a bento box of PDF tools, drawn once and written as
Android adaptive-icon layers and as SVG.

    python3 tools/icon.py [--preview DIR]

Writes res/drawable/ic_launcher_{background,foreground,monochrome}.xml and
docs/icon.svg (the icon cut to a rounded square, for the README and the
About page). --preview also renders PNGs under the launcher masks (circle,
rounded square) at a few sizes, for a look before building.

Adaptive icon geometry: 108 x 108 dp layers; launchers show the middle
72 dp, and anything that matters stays in the 66 dp circle in the middle.
"""
import argparse
import math
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Colours: BentoPDF's indigo in Material 3 tonal steps, and three bright
# "foods" for the compartments.
BG_TOP, BG_BOTTOM = "#ECE9FF", "#CFC8FF"   # primary container, light
SIDE = "#3730A3"                           # indigo 800: the box's front wall
BOX = "#4F46E5"                            # indigo 600: its top
WELL = "#272277"                           # the compartments, recessed
PAGE, FOLD, LINE, BAND = "#FFFFFF", "#CBC6FF", "#B9B3F4", "#FF5A5F"
COOKIE, PILL = "#FFB938", "#2ED3A0"


def rrect(x, y, w, h, r):
    """A rounded rectangle as path data."""
    return (f"M{x + r:g},{y:g} H{x + w - r:g} A{r:g},{r:g} 0 0 1 {x + w:g},{y + r:g} V{y + h - r:g} "
            f"A{r:g},{r:g} 0 0 1 {x + w - r:g},{y + h:g} H{x + r:g} A{r:g},{r:g} 0 0 1 {x:g},{y + h - r:g} "
            f"V{y + r:g} A{r:g},{r:g} 0 0 1 {x + r:g},{y:g} Z")


def circle(cx, cy, r):
    return f"M{cx - r},{cy} A{r},{r} 0 1 0 {cx + r},{cy} A{r},{r} 0 1 0 {cx - r},{cy} Z"


def cookie(cx, cy, r, bumps, depth):
    """Material's scalloped "cookie" shape: a circle with rounded bumps."""
    pts = []
    n = bumps * 24
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        rr = r + depth * math.cos(bumps * t)
        pts.append((cx + rr * math.cos(t - math.pi / 2), cy + rr * math.sin(t - math.pi / 2)))
    return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"


# The box: 50 x 42 dp on a 4 dp front wall, centred; that is about two
# thirds of the 72 dp a launcher shows, inside the 66 dp safe circle.
W, H, DEPTH, R = 50, 42, 4, 13
X, Y = (108 - W) / 2, (108 - H - DEPTH) / 2
WALL, GAP, CR = 4.5, 4, 6
INNER_W, INNER_H = W - 2 * WALL, H - 2 * WALL
COL = (INNER_W - GAP) / 2
LEFT = (X + WALL, Y + WALL, COL, INNER_H, CR)                        # the tall one: a PDF page
TOP_RIGHT = (X + WALL + COL + GAP, Y + WALL, COL, (INNER_H - GAP) / 2, CR)
BOTTOM_RIGHT = (X + WALL + COL + GAP, Y + WALL + (INNER_H + GAP) / 2, COL, (INNER_H - GAP) / 2, CR)


def page_paths():
    x, y, w, h, _ = LEFT
    px, py, pw, ph, f = x + 3.5, y + 4, w - 7, h - 8, 4  # the page and its folded corner
    body = (f"M{px:g},{py + 2:g} A2,2 0 0 1 {px + 2:g},{py:g} H{px + pw - f:g} L{px + pw:g},{py + f:g} "
            f"V{py + ph - 2:g} A2,2 0 0 1 {px + pw - 2:g},{py + ph:g} H{px + 2:g} A2,2 0 0 1 {px:g},{py + ph - 2:g} Z")
    fold = f"M{px + pw - f:g},{py:g} V{py + f - 1:g} A1,1 0 0 0 {px + pw - f + 1:g},{py + f:g} H{px + pw:g} Z"
    lines = rrect(px + 2, py + 6.5, pw - 4, 1.9, 0.95) + " " + rrect(px + 2, py + 10.2, pw - 6, 1.9, 0.95)
    band = rrect(px + 2, py + ph - 6.4, pw - 4, 3.8, 1.4)
    return body, fold, lines, band


def layers():
    """(path, fill, alpha[, fill type]) lists for the foreground and the monochrome layer."""
    body, fold, lines, band = page_paths()
    tx, ty, tw, th, _ = TOP_RIGHT
    bx, by, bw, bh, _ = BOTTOM_RIGHT
    cookie_path = cookie(tx + tw / 2, ty + th / 2, 4.4, 8, 0.95)
    # A capsule lying at an angle, drawn directly so no transform is needed.
    cx, cy, length, rad, ang = bx + bw / 2, by + bh / 2, 12.5, 3, math.radians(-30)
    dx, dy = math.cos(ang) * (length / 2 - rad), math.sin(ang) * (length / 2 - rad)
    nx, ny = -math.sin(ang) * rad, math.cos(ang) * rad
    pill = (f"M{cx - dx + nx:.2f},{cy - dy + ny:.2f} L{cx + dx + nx:.2f},{cy + dy + ny:.2f} "
            f"A{rad},{rad} 0 0 0 {cx + dx - nx:.2f},{cy + dy - ny:.2f} L{cx - dx - nx:.2f},{cy - dy - ny:.2f} "
            f"A{rad},{rad} 0 0 0 {cx - dx + nx:.2f},{cy - dy + ny:.2f} Z")
    wells = [rrect(*LEFT), rrect(*TOP_RIGHT), rrect(*BOTTOM_RIGHT)]
    fg = [
        (rrect(X, Y + DEPTH, W, H, R), SIDE, 1),              # the front wall, below the top
        (rrect(X, Y, W, H, R), BOX, 1),
        *[(w, WELL, 1) for w in wells],
        (body, PAGE, 1), (fold, FOLD, 1), (lines, LINE, 1), (band, BAND, 1),
        (cookie_path, COOKIE, 1),
        (pill, PILL, 1),
    ]
    # Themed icons: one colour. The box with its compartments cut out (even-odd)
    # and the three things in them.
    mono = [
        (rrect(X, Y, W, H + DEPTH, R) + " " + " ".join(wells), "#000000", 1, "evenOdd"),
        (body, "#000000", 1), (cookie_path, "#000000", 1), (pill, "#000000", 1),
    ]
    return fg, mono


def vector(paths, background=None):
    out = ['<?xml version="1.0" encoding="utf-8"?>',
           "<!-- Written by tools/icon.py: edit that, not this. -->",
           '<vector xmlns:android="http://schemas.android.com/apk/res/android"'
           + (' xmlns:aapt="http://schemas.android.com/aapt"' if background else ""),
           '    android:width="108dp" android:height="108dp"',
           '    android:viewportWidth="108" android:viewportHeight="108">']
    if background:
        out += ['  <path android:pathData="M0,0 H108 V108 H0 Z">',
                '    <aapt:attr name="android:fillColor">',
                '      <gradient android:type="linear" android:startX="0" android:startY="0"'
                ' android:endX="108" android:endY="108">',
                f'        <item android:offset="0" android:color="{background[0]}" />',
                f'        <item android:offset="1" android:color="{background[1]}" />',
                "      </gradient>", "    </aapt:attr>", "  </path>"]
    for p in paths:
        d, fill, alpha = p[:3]
        attrs = f'android:fillColor="{fill}"'
        if alpha != 1:
            attrs += f' android:fillAlpha="{alpha}"'
        if len(p) > 3:
            attrs += f' android:fillType="{p[3]}"'
        out.append(f'  <path {attrs}\n      android:pathData="{d}" />')
    out.append("</vector>")
    return "\n".join(out) + "\n"


def svg(paths, size=108, shape="squircle"):
    """The icon as launchers show it: the middle 72 dp, cut to a shape."""
    clip = {"squircle": rrect(18, 18, 72, 72, 22), "circle": circle(54, 54, 36),
            "square": "M18,18 H90 V90 H18 Z"}[shape]
    body = "\n".join(
        f'  <path d="{p[0]}" fill="{p[1]}"' + (f' fill-opacity="{p[2]}"' if p[2] != 1 else "")
        + (' fill-rule="evenodd"' if len(p) > 3 else "") + "/>" for p in paths)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="18 18 72 72" width="{size}" height="{size}">
  <title>BentoBook</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="108" y2="108" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{BG_TOP}"/><stop offset="1" stop-color="{BG_BOTTOM}"/>
    </linearGradient>
    <clipPath id="shape"><path d="{clip}"/></clipPath>
  </defs>
  <g clip-path="url(#shape)">
  <path d="M0,0 H108 V108 H0 Z" fill="url(#bg)"/>
{body}
  </g>
</svg>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--preview", help="also render PNG previews into this directory")
    args = ap.parse_args()
    fg, mono = layers()
    drawable = os.path.join(ROOT, "res", "drawable")
    os.makedirs(drawable, exist_ok=True)
    with open(os.path.join(drawable, "ic_launcher_background.xml"), "w") as f:
        f.write(vector([], background=(BG_TOP, BG_BOTTOM)))
    with open(os.path.join(drawable, "ic_launcher_foreground.xml"), "w") as f:
        f.write(vector(fg))
    with open(os.path.join(drawable, "ic_launcher_monochrome.xml"), "w") as f:
        f.write(vector(mono))
    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
    with open(os.path.join(ROOT, "docs", "icon.svg"), "w") as f:
        f.write(svg(fg, 128))
    if args.preview:
        os.makedirs(args.preview, exist_ok=True)
        for shape in ("squircle", "circle"):
            src = os.path.join(args.preview, f"icon-{shape}.svg")
            with open(src, "w") as f:
                f.write(svg(fg, 512, shape))
            for px in (512, 96, 48):
                subprocess.run(["rsvg-convert", "-w", str(px), "-h", str(px), "-o",
                                os.path.join(args.preview, f"icon-{shape}-{px}.png"), src], check=True)
        mono_svg = svg(mono, 512, "circle").replace('fill="url(#bg)"', 'fill="#E8E6F0"')
        with open(os.path.join(args.preview, "icon-mono.svg"), "w") as f:
            f.write(mono_svg.replace('fill="#000000"', 'fill="#3B3551"'))
        subprocess.run(["rsvg-convert", "-w", "512", "-h", "512", "-o", os.path.join(args.preview, "icon-mono-512.png"),
                        os.path.join(args.preview, "icon-mono.svg")], check=True)
        print(args.preview)


if __name__ == "__main__":
    main()
