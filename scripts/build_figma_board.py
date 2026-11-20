#!/usr/bin/env python3
"""Build SVG boards used as the Figma source frame for #1841."""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT = ROOT / "artifacts"
OUT.mkdir(exist_ok=True)
NS = "{http://www.w3.org/2000/svg}"

FUNCTIONS = [
    ("hall", "资源大厅"), ("event-signup", "活动报名"),
    ("benefits", "会员权益"), ("service", "智能客服"),
    ("map", "资源地图"), ("meeting", "洽谈室"),
    ("podcast", "创始人播客"), ("package", "服务包"),
    ("booking", "空间预订"), ("log", "航海日志"),
    ("publish", "发布供需"), ("connect", "我想对接"),
    ("ticket", "电子票"), ("checkin", "签到"),
    ("message", "消息"), ("privacy", "隐私设置"),
]
TABBAR = [
    ("home", "首页"), ("opportunity", "商机"), ("event", "活动"),
    ("mine", "我的"), ("academy", "学院"),
]


def read_paths(path: Path) -> list[tuple[str, dict[str, str]]]:
    tree = ET.parse(path)
    root = tree.getroot()
    out = []
    for el in root.iter():
        if el.tag == NS + "path":
            out.append((el.attrib.get("d", ""), dict(el.attrib)))
    return out


def path_markup(paths: list[tuple[str, dict[str, str]]], scale: float) -> str:
    parts = []
    for d, attrs in paths:
        attrs = dict(attrs)
        attrs.pop("d", None)
        style = " ".join(f'{k.replace(":", "-")}="{v}"' for k, v in attrs.items())
        parts.append(f'<path d="{d}" {style}/>')
    return "\n".join(parts)


def grid(x: float, y: float, size: float, step: float) -> str:
    lines = []
    n = int(round(size / step))
    for i in range(n + 1):
        p = x + i * step
        q = y + i * step
        weight = "0.8" if i % 6 == 0 else "0.4"
        color = "#CBD5E1" if i % 6 == 0 else "#E2E8F0"
        lines.append(f'<line x1="{p:.2f}" y1="{y}" x2="{p:.2f}" y2="{y+size}" stroke="{color}" stroke-width="{weight}"/>')
        lines.append(f'<line x1="{x}" y1="{q:.2f}" x2="{x+size}" y2="{q:.2f}" stroke="{color}" stroke-width="{weight}"/>')
    lines.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="none" stroke="#94A3B8" stroke-width="0.8"/>')
    return "\n".join(lines)


def build_functions() -> None:
    W, H = 1280, 1100
    icon_size = 144.0
    scale = icon_size / 24.0
    cards = []
    for i, (slug, cn) in enumerate(FUNCTIONS):
        col, row = i % 4, i // 4
        x = 40 + col * 300
        y = 128 + row * 232
        paths = read_paths(ASSETS / "function" / f"icon-app-{slug}.svg")
        body = path_markup(paths, scale)
        cards.append(f'''<g>
  <rect x="{x}" y="{y}" width="280" height="212" rx="14" fill="#FFFFFF" stroke="#E2E8F0"/>
  {grid(x + 68, y + 24, icon_size, icon_size / 24)}
  <g transform="translate({x + 68} {y + 24}) scale({scale})">{body}</g>
  <text x="{x+20}" y="{y+192}" font-family="Inter, Segoe UI, sans-serif" font-size="14" font-weight="700" fill="#0F172A">icon-app-{slug}</text>
  <text x="{x+20}" y="{y+207}" font-family="Noto Sans SC, Microsoft YaHei, sans-serif" font-size="12" fill="#64748B">{cn}</text>
</g>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="#F8FAFC"/>
<text x="40" y="58" font-family="Inter, Segoe UI, sans-serif" font-size="30" font-weight="800" fill="#0F172A">MemberSpace App · Function Entry Icons</text>
<text x="40" y="88" font-family="Noto Sans SC, Microsoft YaHei, sans-serif" font-size="15" fill="#475569">16 个功能入口图标 · 24×24 网格 · 2 px 描边 · 圆角端点 · 画布放大 6× 以便验线</text>
<text x="40" y="112" font-family="Inter, Segoe UI, sans-serif" font-size="12" fill="#64748B">Each cell is 24×24; the 24 grid lines are drawn at 1 unit = 6 px. Source SVG: assets/function/*.svg</text>
{''.join(cards)}
<text x="40" y="1070" font-family="Inter, Segoe UI, sans-serif" font-size="12" fill="#64748B">Brand #1F5EFF · stroke #1F5EFF · round cap/join · transparent background · synthetic demo data only</text>
</svg>'''
    (OUT / "figma-board-function.svg").write_text(svg, encoding="utf-8")


def build_tabbar() -> None:
    W, H = 1280, 560
    size = 81.0
    scale = size / 24.0
    cards = []
    for i, (slug, cn) in enumerate(TABBAR):
        x = 40 + i * 244
        y = 118
        line_paths = read_paths(ASSETS / "tabbar" / f"icon-app-{slug}-line.svg")
        fill_paths = read_paths(ASSETS / "tabbar" / f"icon-app-{slug}-fill.svg")
        line_body = path_markup(line_paths, scale)
        fill_body = path_markup(fill_paths, scale)
        cards.append(f'''<g>
  <rect x="{x}" y="{y}" width="224" height="360" rx="16" fill="#FFFFFF" stroke="#E2E8F0"/>
  <text x="{x+20}" y="{y+34}" font-family="Inter, Segoe UI, sans-serif" font-size="14" font-weight="700" fill="#0F172A">icon-app-{slug}</text>
  <text x="{x+20}" y="{y+52}" font-family="Noto Sans SC, Microsoft YaHei, sans-serif" font-size="12" fill="#64748B">{cn}</text>
  <g transform="translate({x+31} {y+82}) scale({scale})">{line_body}</g>
  <g transform="translate({x+132} {y+82}) scale({scale})">{fill_body}</g>
  <text x="{x+53}" y="{y+190}" text-anchor="middle" font-family="Noto Sans SC, Microsoft YaHei, sans-serif" font-size="12" fill="#64748B">线性 81×81</text>
  <text x="{x+154}" y="{y+190}" text-anchor="middle" font-family="Noto Sans SC, Microsoft YaHei, sans-serif" font-size="12" fill="#64748B">面性 81×81</text>
  <text x="{x+20}" y="{y+224}" font-family="Inter, Segoe UI, sans-serif" font-size="11" fill="#94A3B8">line: #57677C</text>
  <text x="{x+20}" y="{y+240}" font-family="Inter, Segoe UI, sans-serif" font-size="11" fill="#94A3B8">fill: #1F5EFF</text>
  <text x="{x+20}" y="{y+262}" font-family="Inter, Segoe UI, sans-serif" font-size="11" fill="#94A3B8">PNG exported at 81×81</text>
</g>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="#F8FAFC"/>
<text x="40" y="58" font-family="Inter, Segoe UI, sans-serif" font-size="30" font-weight="800" fill="#0F172A">MemberSpace App · Bottom Tab Bar Icons</text>
<text x="40" y="88" font-family="Noto Sans SC, Microsoft YaHei, sans-serif" font-size="15" fill="#475569">5 个标签 · 线性/面性两态 · 10 个 81×81 PNG · 线性 #57677C / 面性 #1F5EFF</text>
{''.join(cards)}
<text x="40" y="530" font-family="Inter, Segoe UI, sans-serif" font-size="12" fill="#64748B">Sources: assets/tabbar/*.svg · exports: artifacts/tabbar/*.png · synthetic demo data only</text>
</svg>'''
    (OUT / "figma-board-tabbar.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    build_functions()
    build_tabbar()
    print("wrote artifacts/figma-board-function.svg and artifacts/figma-board-tabbar.svg")
