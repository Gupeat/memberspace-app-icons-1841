#!/usr/bin/env python3
"""Generate monochrome SVG icon sources for #1841.

All function icons share a 24x24 grid, 2 px stroke, round caps/joins.
Tabbar icons use the same grid and are rendered to 81x81 PNG elsewhere.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FUNCTION_DIR = ROOT / "assets" / "function"
TABBAR_DIR = ROOT / "assets" / "tabbar"

BRAND = "#1F5EFF"
MUTED = "#57677C"

LABELS = {
    "hall": "资源大厅",
    "event-signup": "活动报名",
    "benefits": "会员权益",
    "service": "智能客服",
    "map": "资源地图",
    "meeting": "洽谈室",
    "podcast": "创始人播客",
    "package": "服务包",
    "booking": "空间预订",
    "log": "航海日志",
    "publish": "发布供需",
    "connect": "我想对接",
    "ticket": "电子票",
    "checkin": "签到",
    "message": "消息",
    "privacy": "隐私设置",
}

TAB_LABELS = {
    "home": "首页",
    "opportunity": "商机",
    "event": "活动",
    "mine": "我的",
    "academy": "学院",
}


def circle(cx: float, cy: float, r: float) -> str:
    k = 0.5522847498307936
    return (
        f"M {cx + r} {cy} "
        f"C {cx + r} {cy + k * r} {cx + k * r} {cy + r} {cx} {cy + r} "
        f"C {cx - k * r} {cy + r} {cx - r} {cy + k * r} {cx - r} {cy} "
        f"C {cx - r} {cy - k * r} {cx - k * r} {cy - r} {cx} {cy - r} "
        f"C {cx + k * r} {cy - r} {cx + r} {cy - k * r} {cx + r} {cy} Z"
    )


FUNCTION_PATHS = {
    "hall": [
        "M3 9 L12 3 L21 9",
        "M4 9 H20",
        "M6 9 V18",
        "M10 9 V18",
        "M14 9 V18",
        "M18 9 V18",
        "M3 21 H21",
    ],
    "event-signup": [
        "M5 5 H19 C20.1 5 21 5.9 21 7 V19 C21 20.1 20.1 21 19 21 H5 C3.9 21 3 20.1 3 19 V7 C3 5.9 3.9 5 5 5 Z",
        "M3 9 H21",
        "M8 3 V6",
        "M16 3 V6",
        "M8 14 L11 17 L17 11",
    ],
    "benefits": [
        "M3 18 L3 7 L8.5 11 L12 5 L15.5 11 L21 7 L21 18 Z",
        "M3 21 H21",
    ],
    "service": [
        "M4 13 V11 C4 6.6 7.6 4 12 4 C16.4 4 20 6.6 20 11 V13",
        "M3 13 H6 V20 H5 C3.9 20 3 19.1 3 18 Z",
        "M21 13 H18 V20 H19 C20.1 20 21 19.1 21 18 Z",
        "M20 19 C20 21 18 22 15 22",
        "M17 22 H15",
    ],
    "map": [
        "M3 6 L9 4 L15 6 L21 4 V18 L15 20 L9 18 L3 20 Z",
        "M9 4 V18",
        "M15 6 V20",
    ],
    "meeting": [
        "M3 5 H15 V13 H9 L6 16 V13 H3 Z",
        "M14 10 H21 V17 H18 L16 19 V17 H14 Z",
    ],
    "podcast": [
        "M12 3 C9.8 3 8 4.8 8 7 V13 C8 15.2 9.8 17 12 17 C14.2 17 16 15.2 16 13 V7 C16 4.8 14.2 3 12 3 Z",
        "M5 11 C5 15 8 18 12 18 C16 18 19 15 19 11",
        "M12 18 V21",
        "M9 21 H15",
    ],
    "package": [
        "M3 8 L12 3 L21 8 V17 L12 22 L3 17 Z",
        "M3 8 L12 13 L21 8",
        "M12 13 V22",
    ],
    "booking": [
        "M5 21 V4 C5 3.4 5.4 3 6 3 H18 C18.6 3 19 3.4 19 4 V21",
        "M3 21 H21",
        circle(15, 12, 1.2),
    ],
    "log": [
        "M4 5 C4 3.9 4.9 3 6 3 H20 V21 H6 C4.9 21 4 20.1 4 19 Z",
        "M4 17 H20",
        "M8 8 H16",
        "M8 12 H14",
    ],
    "publish": [
        "M3 10 L14 5 V19 L3 14 Z",
        "M7 15 V19 C7 20.1 7.9 21 9 21 H10 V16",
        "M17 9 C18 10.5 18 13.5 17 15",
        "M20 7 C22 9.5 22 14.5 20 17",
    ],
    "connect": [
        "M10 14 L14 10",
        "M9 12 L6 15 C4.9 16.1 4.9 17.9 6 19 C7.1 20.1 8.9 20.1 10 19 L13 16",
        "M15 12 L18 9 C19.1 7.9 19.1 6.1 18 5 C16.9 3.9 15.1 3.9 14 5 L11 8",
    ],
    "ticket": [
        "M3 7 H21 V10 C19.9 10 19 10.9 19 12 C19 13.1 19.9 14 21 14 V17 H3 V14 C4.1 14 5 13.1 5 12 C5 10.9 4.1 10 3 10 Z",
        "M12 8 V10",
        "M12 12 V14",
        "M12 16 V17",
    ],
    "checkin": [
        "M5 5 H19 V21 H5 Z",
        "M9 3 H15 V6 H9 Z",
        "M8 13 L11 16 L16 10",
    ],
    "message": [
        "M3 5 H21 V17 H10 L5 21 V17 H3 Z",
        circle(8, 11, 1.0),
        circle(12, 11, 1.0),
        circle(16, 11, 1.0),
    ],
    "privacy": [
        "M12 3 L20 6 V12 C20 16.5 16.8 19.8 12 21 C7.2 19.8 4 16.5 4 12 V6 Z",
        circle(12, 10, 2.0),
        "M12 12 V15",
    ],
}

TAB_LINE_PATHS = {
    "home": [
        "M3 11 L12 3 L21 11",
        "M5 10 V21 H19 V10",
        "M10 21 V15 H14 V21",
    ],
    "opportunity": [
        "M3 8 H21 V20 H3 Z",
        "M9 8 V5 H15 V8",
        "M3 13 H21",
        "M11 13 V15 H13 V13",
    ],
    "event": [
        "M4 5 H20 V21 H4 Z",
        "M4 9 H20",
        "M8 3 V6",
        "M16 3 V6",
        "M8 13 H10",
        "M12 13 H14",
        "M16 13 H18",
        "M8 17 H10",
        "M12 17 H14",
    ],
    "mine": [
        circle(12, 8, 4),
        "M4 21 C4 16.7 7.6 14 12 14 C16.4 14 20 16.7 20 21",
    ],
    "academy": [
        "M2 9 L12 4 L22 9 L12 14 Z",
        "M6 11 V16 C6 18.2 9 20 12 20 C15 20 18 18.2 18 16 V11",
        "M22 9 V15",
    ],
}

TAB_FILL_PATHS = {
    "home": [
        "M12 2 L22 11 L20 13 L19 12 V21 H5 V12 L4 13 L2 11 Z M10 21 V14 H14 V21 Z",
    ],
    "opportunity": [
        "M4 8 H20 C21.1 8 22 8.9 22 10 V19 C22 20.1 21.1 21 20 21 H4 C2.9 21 2 20.1 2 19 V10 C2 8.9 2.9 8 4 8 Z",
        "M9 8 V6 C9 5.4 9.4 5 10 5 H14 C14.6 5 15 5.4 15 6 V8 H13 V7 H11 V8 Z",
    ],
    "event": [
        "M5 5 H19 C20.1 5 21 5.9 21 7 V19 C21 20.1 20.1 21 19 21 H5 C3.9 21 3 20.1 3 19 V7 C3 5.9 3.9 5 5 5 Z",
        "M7 3 H9 V6 H7 Z",
        "M15 3 H17 V6 H15 Z",
    ],
    "mine": [
        circle(12, 8, 4),
        "M4 21 C4 16.7 7.6 14 12 14 C16.4 14 20 16.7 20 21 Z",
    ],
    "academy": [
        "M2 9 L12 4 L22 9 L12 14 Z",
        "M6 11 V16 C6 18.2 9 20 12 20 C15 20 18 18.2 18 16 V11 L12 14 Z",
        "M21 10 H22 V15 H21 Z",
    ],
}


def svg_doc(title: str, paths: list[str], *, fill: str | None = None,
            stroke: str | None = None, evenodd: bool = False) -> str:
    if fill:
        d = " ".join(paths)
        rule = ' fill-rule="evenodd"' if evenodd else ""
        body = f'<path d="{d}" fill="{fill}"{rule}/>'
    else:
        assert stroke
        body = "\n".join(
            f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            for d in paths
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" '
        f'viewBox="0 0 24 24" role="img" aria-label="{title}">\n'
        f"  <title>{title}</title>\n  {body}\n</svg>\n"
    )


def main() -> None:
    FUNCTION_DIR.mkdir(parents=True, exist_ok=True)
    TABBAR_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {"function": {}, "tabbar": {}}
    for slug, paths in FUNCTION_PATHS.items():
        label = LABELS[slug]
        name = f"icon-app-{slug}"
        (FUNCTION_DIR / f"{name}.svg").write_text(
            svg_doc(label, paths, stroke=BRAND), encoding="utf-8")
        manifest["function"][name] = {"label": label, "path": paths}
    for slug, paths in TAB_LINE_PATHS.items():
        label = TAB_LABELS[slug]
        for state, paths_, fill, stroke in (
            ("line", paths, None, MUTED),
            ("fill", TAB_FILL_PATHS[slug], BRAND, None),
        ):
            name = f"icon-app-{slug}-{state}"
            (TABBAR_DIR / f"{name}.svg").write_text(
                svg_doc(label, paths_, fill=fill, stroke=stroke,
                        evenodd=(slug == "home" and state == "fill")),
                encoding="utf-8")
            manifest["tabbar"][name] = {"label": label, "state": state,
                                        "path": paths_}
    (ROOT / "assets" / "icons.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print(f"wrote {len(FUNCTION_PATHS)} function icons, "
          f"{len(TAB_LINE_PATHS) * 2} tabbar icons")


if __name__ == "__main__":
    main()
