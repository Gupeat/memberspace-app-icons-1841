#!/usr/bin/env python3
"""Generate iconfont CSS and the local demo page."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "font" / "glyphs.json").read_text(encoding="utf-8"))
ICONS = DATA["icons"]
FAMILY = DATA["family"]

css_lines = [
    "/* Local iconfont for #1841. No external font service. */",
    "@font-face {",
    f"  font-family: '{FAMILY}';",
    "  src: url('../font/memberspace-icons-1841.woff2') format('woff2'),",
    "       url('../font/memberspace-icons-1841.ttf') format('truetype');",
    "  font-weight: normal;",
    "  font-style: normal;",
    "  font-display: block;",
    "}",
    "",
    ".ms-icon {",
    f"  font-family: '{FAMILY}';",
    "  font-style: normal;",
    "  font-weight: normal;",
    "  font-variant: normal;",
    "  text-transform: none;",
    "  line-height: 1;",
    "  display: inline-block;",
    "  speak: never;",
    "  -webkit-font-smoothing: antialiased;",
    "  -moz-osx-font-smoothing: grayscale;",
    "}",
    "",
]
for name, item in ICONS.items():
    css_lines.append(f".{name}::before {{ content: '\\{item['codepoint']:04x}'; }}")
(ROOT / "font" / "iconfont.css").write_text("\n".join(css_lines) + "\n", encoding="utf-8")

cards = "\n".join(
    f'''      <div class="card">
        <span class="ms-icon {name}" aria-hidden="true"></span>
        <div class="label">{name}</div>
        <div class="cp">U+{item['codepoint']:04X}</div>
      </div>'''
    for name, item in ICONS.items()
)
html = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>本地 iconfont 示例 · #1841</title>
<link rel="stylesheet" href="../font/iconfont.css">
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: #f6f8fc; color: #1b2433; font: 14px/1.5 "Segoe UI", "Microsoft YaHei", sans-serif; }}
  main {{ width: 1080px; margin: 0 auto; padding: 32px 28px 36px; }}
  h1 {{ font-size: 22px; margin: 0 0 6px; }}
  p {{ margin: 0 0 22px; color: #5b6577; font-size: 13px; }}
  .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }}
  .card {{ background: #fff; border: 1px solid #e3e7ef; border-radius: 12px; padding: 22px 16px 16px; text-align: center; }}
  .ms-icon {{ font-size: 56px; line-height: 1; color: #1F5EFF; }}
  .label {{ margin-top: 14px; font-size: 13px; font-weight: 600; }}
  .cp {{ margin-top: 3px; font-size: 11px; color: #7a8496; font-family: Consolas, monospace; }}
  footer {{ margin-top: 22px; font-size: 12px; color: #667085; }}
  code {{ font-family: Consolas, monospace; }}
</style>
</head>
<body>
<main>
  <h1>本地 iconfont 示例</h1>
  <p>16 个功能入口图标全部来自本地 TTF/WOFF2 字体文件，页面不引用任何外部字体或图标服务。</p>
  <div class="grid">
{cards}
  </div>
  <footer>字体：<code>font/memberspace-icons-1841.woff2</code>、<code>font/memberspace-icons-1841.ttf</code>；CSS：<code>font/iconfont.css</code>；字形数与映射见 <code>font/glyphs.json</code>。</footer>
</main>
</body>
</html>
'''
(ROOT / "demo" / "index.html").write_text(html, encoding="utf-8")
print("wrote font/iconfont.css and demo/index.html")
