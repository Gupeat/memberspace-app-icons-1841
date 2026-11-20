# MemberSpace App Icons · #1841

会员空间平台 App 的底部标签栏图标与功能入口图标组。任务编号 `#1841 / S3-BRAND-004`。

## 交付内容

| 类别 | 数量 | 路径 | 规格 |
|---|---:|---|---|
| 功能入口 SVG | 16 | `assets/function/icon-app-*.svg` | 24×24 网格、2 px 描边、圆角端点、品牌蓝 `#1F5EFF` |
| 底部标签栏 SVG | 10 | `assets/tabbar/icon-app-*-line.svg` / `-fill.svg` | 5 个图标 × 线性/面性，24×24 矢量源 |
| 底部标签栏 PNG | 10 | `artifacts/tabbar/icon-app-*-line.png` / `-fill.png` | 81×81、透明背景、RGBA |
| 本地 iconfont | 1 套 | `font/memberspace-icons-1841.ttf` / `.woff2` / `iconfont.css` | 16 个功能入口图标，PUA U+E001–U+E010 |
| 命名表 | 26 行 | `docs/NAMING.md` | 覆盖 16 个功能图标 + 10 个标签栏状态 |
| Figma 总览板（查看） | 1 个 | 见下方链接 | 单个 1280×1710 矢量总览板，非组件库；可编辑源是 SVG |
| 演示与截图 | — | `demo/index.html`、`artifacts/*.png` | 本地字体、无外部依赖 |

### 功能入口图标（16）

资源大厅、活动报名、会员权益、智能客服、资源地图、洽谈室、创始人播客、服务包、空间预订、航海日志、发布供需、我想对接、电子票、签到、消息、隐私设置。

对应文件与码位见 [docs/NAMING.md](docs/NAMING.md)。

### 底部标签栏图标（5 × 2）

首页、商机、活动、我的、学院（预留）。线性色 `#57677C`，面性色 `#1F5EFF`。

## 设计规格

- 网格：24×24；功能图标主体控制在 20×20 安全区内。
- 描边：2 px；端点 `round`；转角 `round`；线性图标 `fill="none"`。
- 功能入口色：品牌蓝 `#1F5EFF`。
- 标签栏线性色：`#57677C`；面性色：`#1F5EFF`。
- 标签栏 PNG：由 24×24 SVG 等比放大到 81×81，保留透明背景。
- 命名：`icon-<模块>-<名称>[-line|-fill]`。

## 本地 iconfont

```html
<link rel="stylesheet" href="font/iconfont.css">
<i class="ms-icon icon-app-hall"></i>
```

- 字体文件：`font/memberspace-icons-1841.woff2`（优先）、`font/memberspace-icons-1841.ttf`（回退）。
- CSS：`font/iconfont.css`，包含 `@font-face` 和 16 个 `.icon-app-*` class。
- 映射：`font/glyphs.json`（名称、码位、glyph 名）。
- 本地演示：`demo/index.html`；截图 `artifacts/iconfont-demo.png`。
- 页面不引用任何外部字体或图标 CDN。

## Figma

- 公开文件：<https://www.figma.com/design/8ZSviAfM6kyW5xHa9XugyG/MemberSpace-App-Icons-1841---v1?node-id=0-1>
- 文件名称：`MemberSpace App Icons 1841 - v1`
- 画板：`01 Icons Overview`，1280×1710，X=0，Y=0。
- 内容：上半部 16 个功能入口图标 + 24 网格 + 名称；下半部 5 个标签栏图标 × 线性/面性 + 81×81 标注。
- 权限：`Anyone · can view`（链接可查看）。
- 画布截图：`artifacts/figma-final.png`；分享权限截图：`artifacts/figma-share-public.png`。

说明：Figma 文件是用于验线、命名与评审的矢量总览板，不是 Figma 组件库；SVG 源文件是唯一可编辑源。Figma 中放置的是 `artifacts/figma-board-all.svg` 的导入副本。

## 验证

```powershell
python scripts/validate_assets.py
```

预期输出一行 `PASS`，并生成 `artifacts/validation.json`。检查项：

1. 16 个功能 SVG 均为 24×24、2 px 描边、圆角端点、品牌蓝。
2. 10 个标签栏 SVG 成对存在，线性/面性颜色正确。
3. 10 个 PNG 均为 81×81 RGBA、透明背景、非空像素。
4. TTF/WOFF2 均含 U+E001–U+E010；`glyphs.json` 与 CSS class 覆盖 16 个名称。
5. `docs/NAMING.md` 覆盖 26 个唯一图标名。
6. demo 不引用外部字体/图标服务。

## 复现

```powershell
# 1. SVG -> 81x81 PNG（Edge + playwright-core）
node scripts/render_assets.mjs

# 2. SVG -> TTF/WOFF2 + CSS + glyphs.json
python scripts/build_font.py

# 3. 生成 demo 与截图
python scripts/generate_demo.py

# 4. 生成两块 Figma 板并合并
python scripts/build_figma_board.py
python scripts/combine_board.py

# 5. 校验
python scripts/validate_assets.py
```

依赖：Python 3.12、Pillow、fontTools、skia-pathops；Node 24、playwright-core、Microsoft Edge。

`render_assets.mjs` 默认从 `node_modules/playwright-core/index.mjs` 加载，也可用 `PLAYWRIGHT_CORE` 指向已安装的 `index.mjs`；Edge 路径可用 `EDGE` 覆盖。

```powershell
$env:PLAYWRIGHT_CORE = "C:\path\to\playwright-core\index.mjs"
$env:EDGE = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
```

## 产物

- `artifacts/function-grid.png`：16 个功能图标 4×4 总览（1100×1288）。
- `artifacts/tabbar-preview.png`：5 个标签 × 线/面 81 px 总览（1100×300）。
- `artifacts/iconfont-demo.png`：本地 iconfont 演示页截图（1080×900）。
- `artifacts/figma-board-all.svg` / `.png`：Figma 导入用合并板（1280×1710）。
- `artifacts/figma-final.png`：Figma 画布最终截图（1600×1000）。
- `artifacts/figma-share-public.png`：Figma 分享权限截图。

## 限制

- 所有演示文案与数据均为合成/脱敏内容，不含真实客户或会员信息。
- Figma 为免费工作区，文件是单页矢量总览板；未制作组件变体、Auto Layout 或交互原型。
- 标签栏 SVG 源为 24×24，PNG 按 81×81 导出；如果设计侧需要 81×81 可编辑 SVG，可按同一路径缩放。
- 未在微信小程序运行时做真机渲染测试；本单交付为 SVG/PNG/iconfont 资产与本地 Web 演示。
