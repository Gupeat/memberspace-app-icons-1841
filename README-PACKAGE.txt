MemberSpace App Icons · #1841 / S3-BRAND-004
Version: 1.0.1
Prepared: 2026-11-21

CONTENTS
- README.md, README-PACKAGE.txt
- docs/NAMING.md ................ 26-name naming table
- docs/FIGMA.md ................. public Figma link and verification
- assets/function/*.svg ......... 16 function-entry icons (24x24, 2 px stroke)
- assets/tabbar/*.svg ........... 10 tab-bar icons (5 x line/fill)
- artifacts/tabbar/*.png ........ 10 exported PNGs (81x81, transparent)
- font/memberspace-icons-1841.ttf / .woff2
- font/iconfont.css ............. 16 local iconfont classes
- font/glyphs.json .............. name / codepoint / glyph map
- demo/index.html ............... local iconfont demo
- artifacts/function-grid.png ... 16-icon overview (1100x1288)
- artifacts/tabbar-preview.png .. tab-bar overview (1100x300)
- artifacts/iconfont-demo.png ... demo screenshot (1080x900)
- artifacts/figma-board-all.svg / .png (1280x1710 import board)
- artifacts/figma-final.png ..... final Figma canvas screenshot
- artifacts/figma-share-public.png (Anyone can view)
- artifacts/validation.json ..... machine-readable validation result
- artifacts/privacy-scan.json .. text privacy scan (0 hits)
- scripts/* .................... SVG generator, PNG renderer, font builder, demo, Figma board, validator

VALIDATION
Command: python scripts/validate_assets.py
Result: PASS
- 16 function SVGs: 24x24, 2 px stroke, round cap/join, #1F5EFF
- 10 tab-bar SVGs: 5 line (#57677C) + 5 fill (#1F5EFF)
- 10 PNGs: 81x81 RGBA, transparent background, non-empty
- 16 iconfont glyphs: U+E001-U+E010 in TTF and WOFF2
- 26 unique icon names covered by docs/NAMING.md
- demo references only local font files

FIGMA
Name: MemberSpace App Icons 1841 - v1
URL: https://www.figma.com/design/8ZSviAfM6kyW5xHa9XugyG/MemberSpace-App-Icons-1841---v1?node-id=0-1
Frame: 01 Icons Overview, 1280x1710, X=0, Y=0
Access: Anyone can view

REPRODUCE
node scripts/render_assets.mjs
python scripts/build_font.py
python scripts/generate_demo.py
python scripts/build_figma_board.py
python scripts/combine_board.py
python scripts/validate_assets.py

NOTES
- All demo text and data are synthetic/desensitized.
- Figma is a single-page vector overview board for review, not a component library.
- SVG is the only editable source; the Figma board is a view-only copy of artifacts/figma-board-all.svg.
- Tab-bar SVG sources are 24x24 vectors; PNGs are exported at 81x81.
- No WeChat runtime device test is claimed for this package.

