#!/usr/bin/env python3
"""Build local TTF/WOFF2 iconfonts from the 16 function SVGs."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pathops
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
SVG_DIR = ROOT / "assets" / "function"
FONT_DIR = ROOT / "font"
FONT_DIR.mkdir(parents=True, exist_ok=True)

# 24 px grid -> 1000 upem, baseline at y=800, descender -200.
SCALE = 1000.0 / 24.0
BASE = 800.0
STROKE = 2.0 * SCALE
FAMILY = "MemberSpace Icons 1841"
PS_NAME = "MemberSpaceIcons1841-Regular"
START_CP = 0xE001

SLUGS = [
    "hall", "event-signup", "benefits", "service", "map", "meeting", "podcast",
    "package", "booking", "log", "publish", "connect", "ticket", "checkin",
    "message", "privacy",
]


def read_paths(svg_file: Path) -> list[str]:
    text = svg_file.read_text(encoding="utf-8")
    return re.findall(r'<path[^>]*\sd="([^"]+)"', text)


def stroke_to_contours(d: str) -> pathops.Path:
    path = pathops.Path()
    parse_path(d, path.getPen())
    # Scale the 24 px grid to font units before stroking, otherwise the
    # stroke width would be multiplied by the scale as well.
    path = path.transform(SCALE, 0, 0, -SCALE, 0, BASE)
    # pathops.Path.stroke mutates in place and returns None.
    path.stroke(
        STROKE,
        cap=pathops.LineCap.ROUND_CAP,
        join=pathops.LineJoin.ROUND_JOIN,
        miter_limit=4.0,
    )
    path.convertConicsToQuads(0.1)
    return path


def make_glyph(svg_file: Path):
    pen = TTGlyphPen(None)
    for d in read_paths(svg_file):
        path = stroke_to_contours(d)
        path.draw(pen)
    return pen.glyph()


def main() -> None:
    glyph_order = [".notdef"]
    glyphs = {".notdef": TTGlyphPen(None).glyph()}
    cmap = {}
    names = {}
    glyph_names = []
    for index, slug in enumerate(SLUGS):
        name = "icon-app-" + slug
        glyph_name = "uniE%03X" % (START_CP + index - 0xE000)
        glyph_order.append(glyph_name)
        glyphs[glyph_name] = make_glyph(SVG_DIR / (name + ".svg"))
        cmap[START_CP + index] = glyph_name
        names[name] = {"codepoint": START_CP + index,
                       "glyph": glyph_name}
        glyph_names.append(name)

    fb = FontBuilder(1000, isTTF=True)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics({g: (1000, 0) for g in glyph_order})
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupOS2(
        sTypoAscender=800, sTypoDescender=-200, sTypoLineGap=0,
        usWinAscent=800, usWinDescent=200, sxHeight=500, sCapHeight=700,
        achVendID="MSIC",
    )
    fb.setupNameTable({
        "familyName": FAMILY,
        "styleName": "Regular",
        "uniqueFontIdentifier": PS_NAME,
        "fullName": FAMILY + " Regular",
        "psName": PS_NAME,
        "version": "Version 1.000",
        "copyright": "Synthetic icon set for a fictional membership platform. No third-party icon assets.",
    })
    fb.setupPost()
    ttf_path = FONT_DIR / "memberspace-icons-1841.ttf"
    fb.save(ttf_path)

    woff2_path = FONT_DIR / "memberspace-icons-1841.woff2"
    font = TTFont(ttf_path)
    font.flavor = "woff2"
    font.save(woff2_path)

    check = TTFont(ttf_path)
    cmap_table = check.getBestCmap()
    missing = [cp for cp in cmap if cp not in cmap_table]
    if missing:
        raise SystemExit("missing cmap: " + repr(missing))
    if len(cmap_table) != len(SLUGS):
        raise SystemExit(f"expected {len(SLUGS)} cmap entries, got {len(cmap_table)}")

    (FONT_DIR / "glyphs.json").write_text(
        json.dumps({"family": FAMILY, "font": "memberspace-icons-1841",
                    "version": "1.0.0", "icons": names},
                   ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print(f"built {ttf_path.name} ({ttf_path.stat().st_size} B) and "
          f"{woff2_path.name} ({woff2_path.stat().st_size} B); cmap {len(cmap_table)}")


if __name__ == "__main__":
    main()
