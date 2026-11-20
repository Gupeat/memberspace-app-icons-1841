#!/usr/bin/env python3
"""Validate all #1841 icon assets and write artifacts/validation.json."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "validation.json"
SVG_NS = "{http://www.w3.org/2000/svg}"

FUNCTION = {
    "icon-app-hall": ("资源大厅", 0xE001),
    "icon-app-event-signup": ("活动报名", 0xE002),
    "icon-app-benefits": ("会员权益", 0xE003),
    "icon-app-service": ("智能客服", 0xE004),
    "icon-app-map": ("资源地图", 0xE005),
    "icon-app-meeting": ("洽谈室", 0xE006),
    "icon-app-podcast": ("创始人播客", 0xE007),
    "icon-app-package": ("服务包", 0xE008),
    "icon-app-booking": ("空间预订", 0xE009),
    "icon-app-log": ("航海日志", 0xE00A),
    "icon-app-publish": ("发布供需", 0xE00B),
    "icon-app-connect": ("我想对接", 0xE00C),
    "icon-app-ticket": ("电子票", 0xE00D),
    "icon-app-checkin": ("签到", 0xE00E),
    "icon-app-message": ("消息", 0xE00F),
    "icon-app-privacy": ("隐私设置", 0xE010),
}
TABBAR = {
    "icon-app-home": ("首页", "#57677C", "#1F5EFF"),
    "icon-app-opportunity": ("商机", "#57677C", "#1F5EFF"),
    "icon-app-event": ("活动", "#57677C", "#1F5EFF"),
    "icon-app-mine": ("我的", "#57677C", "#1F5EFF"),
    "icon-app-academy": ("学院", "#57677C", "#1F5EFF"),
}

failures: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)
    print("FAIL", msg)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_svg(path: Path) -> ET.Element:
    return ET.parse(path).getroot()


def check_function_svg(name: str, label: str, codepoint: int) -> dict:
    path = ROOT / "assets" / "function" / f"{name}.svg"
    if not path.exists():
        fail(f"missing function svg {path.relative_to(ROOT)}")
        return {}
    root = parse_svg(path)
    if root.tag != SVG_NS + "svg":
        fail(f"{name}: not svg root")
    if root.get("width") != "24" or root.get("height") != "24":
        fail(f"{name}: width/height must be 24")
    if root.get("viewBox") != "0 0 24 24":
        fail(f"{name}: viewBox must be 0 0 24 24")
    if (root.get("aria-label") or "") != label:
        fail(f"{name}: aria-label mismatch {root.get('aria-label')!r} != {label!r}")
    paths = root.findall(f".//{SVG_NS}path")
    if not paths:
        fail(f"{name}: no path")
    for i, el in enumerate(paths):
        if el.get("fill") != "none":
            fail(f"{name}: path {i} fill must be none")
        if (el.get("stroke") or "").upper() != "#1F5EFF":
            fail(f"{name}: path {i} stroke must be #1F5EFF")
        if el.get("stroke-width") != "2":
            fail(f"{name}: path {i} stroke-width must be 2")
        if el.get("stroke-linecap") != "round":
            fail(f"{name}: path {i} linecap must be round")
        if el.get("stroke-linejoin") != "round":
            fail(f"{name}: path {i} linejoin must be round")
    return {
        "path": f"assets/function/{name}.svg",
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "paths": len(paths),
        "codepoint": f"U+{codepoint:04X}",
    }


def check_tabbar_svg(name: str, label: str, color: str, state: str) -> dict:
    path = ROOT / "assets" / "tabbar" / f"{name}-{state}.svg"
    if not path.exists():
        fail(f"missing tabbar svg {path.relative_to(ROOT)}")
        return {}
    root = parse_svg(path)
    if root.get("viewBox") != "0 0 24 24":
        fail(f"{name}-{state}: viewBox must be 0 0 24 24")
    if (root.get("aria-label") or "") != label:
        fail(f"{name}-{state}: aria-label mismatch")
    paths = root.findall(f".//{SVG_NS}path")
    if not paths:
        fail(f"{name}-{state}: no path")
    for i, el in enumerate(paths):
        if state == "line":
            if el.get("fill") != "none":
                fail(f"{name}-line: path {i} fill must be none")
            if (el.get("stroke") or "").upper() != color:
                fail(f"{name}-line: path {i} stroke {el.get('stroke')} != {color}")
            if el.get("stroke-width") != "2":
                fail(f"{name}-line: path {i} stroke-width must be 2")
        else:
            if (el.get("fill") or "").upper() != color:
                fail(f"{name}-fill: path {i} fill must be {color}")
            if el.get("stroke"):
                fail(f"{name}-fill: path {i} must not have stroke")
    return {
        "path": f"assets/tabbar/{name}-{state}.svg",
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "paths": len(paths),
    }


def check_png(name: str, state: str) -> dict:
    path = ROOT / "artifacts" / "tabbar" / f"{name}-{state}.png"
    if not path.exists():
        fail(f"missing png {path.relative_to(ROOT)}")
        return {}
    with Image.open(path) as im:
        if im.size != (81, 81):
            fail(f"{name}-{state}.png: size {im.size} != (81,81)")
        rgba = im.convert("RGBA")
        if rgba.getpixel((0, 0))[3] != 0:
            fail(f"{name}-{state}.png: corner not transparent")
        bbox = rgba.getbbox()
        if not bbox:
            fail(f"{name}-{state}.png: empty image")
        alpha = rgba.getchannel("A")
        nontransparent = sum(alpha.histogram()[1:])
        if nontransparent < 100:
            fail(f"{name}-{state}.png: too few visible pixels")
    return {
        "path": f"artifacts/tabbar/{name}-{state}.png",
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "size": [81, 81],
        "nontransparent_pixels": nontransparent,
    }


def check_iconfont() -> dict:
    ttf = ROOT / "font" / "memberspace-icons-1841.ttf"
    woff2 = ROOT / "font" / "memberspace-icons-1841.woff2"
    css = ROOT / "font" / "iconfont.css"
    glyphs = ROOT / "font" / "glyphs.json"
    for p in (ttf, woff2, css, glyphs):
        if not p.exists():
            fail(f"missing font file {p.relative_to(ROOT)}")
            return {}
    expected = {name: cp for name, (_, cp) in FUNCTION.items()}
    for path in (ttf, woff2):
        font = TTFont(path)
        cmap = font.getBestCmap()
        missing = [hex(cp) for cp in expected.values() if cp not in cmap]
        if missing:
            fail(f"{path.name}: missing codepoints {missing}")
    data = json.loads(glyphs.read_text(encoding="utf-8"))
    icons = data.get("icons", {})
    if set(icons) != set(expected):
        fail("glyphs.json icon keys mismatch")
    for name, cp in expected.items():
        if int(icons.get(name, {}).get("codepoint", -1)) != cp:
            fail(f"glyphs.json codepoint mismatch for {name}")
    css_text = css.read_text(encoding="utf-8")
    if "http://" in css_text or "https://" in css_text:
        fail("iconfont.css references an external URL")
    if "@font-face" not in css_text:
        fail("iconfont.css missing @font-face")
    for name in expected:
        if f".{name}::before" not in css_text:
            fail(f"iconfont.css missing class {name}")
    return {
        "ttf": {"bytes": ttf.stat().st_size, "sha256": sha256(ttf)},
        "woff2": {"bytes": woff2.stat().st_size, "sha256": sha256(woff2)},
        "css": {"bytes": css.stat().st_size, "sha256": sha256(css)},
        "glyphs_json": {"bytes": glyphs.stat().st_size, "sha256": sha256(glyphs)},
        "glyph_count": len(expected),
    }


def check_demo() -> dict:
    path = ROOT / "demo" / "index.html"
    if not path.exists():
        fail("missing demo/index.html")
        return {}
    text = path.read_text(encoding="utf-8")
    if "../font/iconfont.css" not in text:
        fail("demo/index.html does not link ../font/iconfont.css")
    if re.search(r"https?://", text):
        fail("demo/index.html references an external URL")
    for name in FUNCTION:
        if name not in text:
            fail(f"demo/index.html missing {name}")
    return {"path": "demo/index.html", "bytes": path.stat().st_size, "sha256": sha256(path)}


def check_naming() -> dict:
    path = ROOT / "docs" / "NAMING.md"
    if not path.exists():
        fail("missing docs/NAMING.md")
        return {}
    text = path.read_text(encoding="utf-8")
    names = set(FUNCTION) | {f"{name}-line" for name in TABBAR} | {f"{name}-fill" for name in TABBAR}
    missing = sorted(n for n in names if n not in text)
    if missing:
        fail(f"NAMING.md missing names: {missing}")
    return {"path": "docs/NAMING.md", "bytes": path.stat().st_size, "sha256": sha256(path), "unique_names": len(names)}


def main() -> int:
    function_files = [check_function_svg(n, l, cp) for n, (l, cp) in FUNCTION.items()]
    tabbar_svg = []
    tabbar_png = []
    for name, (label, line_color, fill_color) in TABBAR.items():
        tabbar_svg.append(check_tabbar_svg(name, label, line_color, "line"))
        tabbar_svg.append(check_tabbar_svg(name, label, fill_color, "fill"))
        tabbar_png.append(check_png(name, "line"))
        tabbar_png.append(check_png(name, "fill"))
    result = {
        "ok": not failures,
        "failures": failures,
        "counts": {
            "function_svg": len(function_files),
            "tabbar_svg": len(tabbar_svg),
            "tabbar_png": len(tabbar_png),
            "unique_icon_names": len(FUNCTION) + len(TABBAR) * 2,
        },
        "files": {
            "function": function_files,
            "tabbar_svg": tabbar_svg,
            "tabbar_png": tabbar_png,
        },
        "checks": {
            "function_svg_spec": not failures,
            "tabbar_svg_spec": not failures,
            "tabbar_png_spec": not failures,
            "iconfont": check_iconfont(),
            "demo": check_demo(),
            "naming": check_naming(),
        },
    }
    result["ok"] = not failures
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if failures:
        print(f"FAIL {len(failures)} issue(s); see {OUT.relative_to(ROOT)}")
        return 1
    print(f"PASS 16 SVG + 10 SVG + 10 PNG + 16 glyphs + 26 names; wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())