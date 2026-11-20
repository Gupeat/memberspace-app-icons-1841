#!/usr/bin/env python3
"""Combine the function and tab bar boards into one Figma frame."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"


def inner(name: str) -> str:
    text = (ART / name).read_text(encoding="utf-8")
    text = re.sub(r'^.*?<svg[^>]*>', '', text, flags=re.S)
    text = text.replace('</svg>', '')
    text = re.sub(r'<rect width="\d+" height="\d+" fill="#F8FAFC"/>', '', text, count=1)
    return text


W, H = 1280, 1710
body = inner("figma-board-function.svg")
body += '<g transform="translate(0 1110)">' + inner("figma-board-tabbar.svg") + '</g>'
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="#F8FAFC"/>
{body}
</svg>'''
(ART / "figma-board-all.svg").write_text(svg, encoding="utf-8")
print("wrote artifacts/figma-board-all.svg")
