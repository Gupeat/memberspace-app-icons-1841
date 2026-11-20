# Figma 总览板与公开访问

## 文件

- 名称：`MemberSpace App Icons 1841 - v1`
- 链接：<https://www.figma.com/design/8ZSviAfM6kyW5xHa9XugyG/MemberSpace-App-Icons-1841---v1?node-id=0-1>
- 画板：`01 Icons Overview`
- 尺寸：1280×1710；位置 X=0，Y=0。
- 内容：上半部 16 个功能入口图标（24 网格、2 px 描边、名称与中文用途）；下半部 5 个标签栏图标 × 线性/面性（81×81 标注）。
- 权限：`Anyone · can view`。

## 截图

- 画布：`artifacts/figma-final.png`（1600×1000，含 Figma 工具栏、文件名、画板）。
- 分享权限：`artifacts/figma-share-public.png`（Share 对话框显示 `Anyone` / `can view`）。

## 匿名访问核验

公开链接在未登录的 HTTP 客户端下返回 200，并包含文件标题：

```powershell
curl.exe -sS -L -A "Mozilla/5.0" -o "$env:TEMP\figma-public.html" -w "%{http_code}\n" "https://www.figma.com/design/8ZSviAfM6kyW5xHa9XugyG/MemberSpace-App-Icons-1841---v1?node-id=0-1"
Select-String -Path "$env:TEMP\figma-public.html" -Pattern "MemberSpace App Icons 1841 - v1" -SimpleMatch
```

实测返回 `200`，HTML 中的 `twitter:title` 为 `MemberSpace App Icons 1841 - v1`。

## 说明

Figma 文件是验线、命名和评审用的矢量总览板，不是组件库；SVG 源文件是唯一可编辑源。Figma 中放置的是 `artifacts/figma-board-all.svg` 的导入副本，无外部图片或字体依赖。
