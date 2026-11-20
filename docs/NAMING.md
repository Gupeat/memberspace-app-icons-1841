# 命名表 · MemberSpace App Icons 1841

统一命名规则：`icon-<模块>-<名称>[-状态]`

- 模块：`app`（会员空间 App）。
- 名称：小写英文，单词之间用 `-`。
- 状态：仅底部标签栏使用 `-line` / `-fill`；功能入口图标无状态后缀。
- 功能入口 SVG：`assets/function/icon-app-<name>.svg`
- 标签栏 SVG：`assets/tabbar/icon-app-<name>-line.svg`、`assets/tabbar/icon-app-<name>-fill.svg`
- 标签栏 PNG：`artifacts/tabbar/icon-app-<name>-line.png`、`artifacts/tabbar/icon-app-<name>-fill.png`
- iconfont class：`.icon-app-<name>`，码位见 `font/glyphs.json`。

## 1. 功能入口图标 · 16 个

24×24 网格、2 px 描边、圆角端点，导出 SVG；同时进入本地 iconfont。

| # | 图标名 | 中文用途 | 源文件 | iconfont 码位 |
|---:|---|---|---|---|
| 1 | `icon-app-hall` | 资源大厅 | `assets/function/icon-app-hall.svg` | U+E001 |
| 2 | `icon-app-event-signup` | 活动报名 | `assets/function/icon-app-event-signup.svg` | U+E002 |
| 3 | `icon-app-benefits` | 会员权益 | `assets/function/icon-app-benefits.svg` | U+E003 |
| 4 | `icon-app-service` | 智能客服 | `assets/function/icon-app-service.svg` | U+E004 |
| 5 | `icon-app-map` | 资源地图 | `assets/function/icon-app-map.svg` | U+E005 |
| 6 | `icon-app-meeting` | 洽谈室 | `assets/function/icon-app-meeting.svg` | U+E006 |
| 7 | `icon-app-podcast` | 创始人播客 | `assets/function/icon-app-podcast.svg` | U+E007 |
| 8 | `icon-app-package` | 服务包 | `assets/function/icon-app-package.svg` | U+E008 |
| 9 | `icon-app-booking` | 空间预订 | `assets/function/icon-app-booking.svg` | U+E009 |
| 10 | `icon-app-log` | 航海日志 | `assets/function/icon-app-log.svg` | U+E00A |
| 11 | `icon-app-publish` | 发布供需 | `assets/function/icon-app-publish.svg` | U+E00B |
| 12 | `icon-app-connect` | 我想对接 | `assets/function/icon-app-connect.svg` | U+E00C |
| 13 | `icon-app-ticket` | 电子票 | `assets/function/icon-app-ticket.svg` | U+E00D |
| 14 | `icon-app-checkin` | 签到 | `assets/function/icon-app-checkin.svg` | U+E00E |
| 15 | `icon-app-message` | 消息 | `assets/function/icon-app-message.svg` | U+E00F |
| 16 | `icon-app-privacy` | 隐私设置 | `assets/function/icon-app-privacy.svg` | U+E010 |

## 2. 底部标签栏图标 · 5 个 × 2 态 = 10 个

81×81 PNG；源 SVG 为 24×24 矢量，导出时等比放大到 81×81。线性色 `#57677C`，面性色 `#1F5EFF`。

| # | 图标名 | 中文用途 | 线性源 | 线性 PNG | 面性源 | 面性 PNG |
|---:|---|---|---|---|---|---|
| 1 | `icon-app-home` | 首页 | `assets/tabbar/icon-app-home-line.svg` | `artifacts/tabbar/icon-app-home-line.png` | `assets/tabbar/icon-app-home-fill.svg` | `artifacts/tabbar/icon-app-home-fill.png` |
| 2 | `icon-app-opportunity` | 商机 | `assets/tabbar/icon-app-opportunity-line.svg` | `artifacts/tabbar/icon-app-opportunity-line.png` | `assets/tabbar/icon-app-opportunity-fill.svg` | `artifacts/tabbar/icon-app-opportunity-fill.png` |
| 3 | `icon-app-event` | 活动 | `assets/tabbar/icon-app-event-line.svg` | `artifacts/tabbar/icon-app-event-line.png` | `assets/tabbar/icon-app-event-fill.svg` | `artifacts/tabbar/icon-app-event-fill.png` |
| 4 | `icon-app-mine` | 我的 | `assets/tabbar/icon-app-mine-line.svg` | `artifacts/tabbar/icon-app-mine-line.png` | `assets/tabbar/icon-app-mine-fill.svg` | `artifacts/tabbar/icon-app-mine-fill.png` |
| 5 | `icon-app-academy` | 学院（预留） | `assets/tabbar/icon-app-academy-line.svg` | `artifacts/tabbar/icon-app-academy-line.png` | `assets/tabbar/icon-app-academy-fill.svg` | `artifacts/tabbar/icon-app-academy-fill.png` |

## 3. 合计

- 功能入口图标：16 个 SVG。
- 标签栏图标：5 个 × 2 态 = 10 个 SVG + 10 个 81×81 PNG。
- 总计：26 个唯一图标名、26 个源 SVG、10 个 PNG。
