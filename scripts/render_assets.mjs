import fs from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname.replace(/^\//, "")), "..");
const EDGE = process.env.EDGE || "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe";
const PLAYWRIGHT_CORE = process.env.PLAYWRIGHT_CORE || path.join(ROOT, "node_modules", "playwright-core", "index.mjs");
const { chromium } = await import(pathToFileURL(PLAYWRIGHT_CORE).href);
const ART = path.join(ROOT, "artifacts");
const NS = "http://www.w3.org/2000/svg";

const functionNames = [
  "hall", "event-signup", "benefits", "service", "map", "meeting", "podcast",
  "package", "booking", "log", "publish", "connect", "ticket", "checkin",
  "message", "privacy",
];
const tabNames = ["home", "opportunity", "event", "mine", "academy"];
const labels = {
  hall: "资源大厅", "event-signup": "活动报名", benefits: "会员权益",
  service: "智能客服", map: "资源地图", meeting: "洽谈室", podcast: "创始人播客",
  package: "服务包", booking: "空间预订", log: "航海日志", publish: "发布供需",
  connect: "我想对接", ticket: "电子票", checkin: "签到", message: "消息",
  privacy: "隐私设置", home: "首页", opportunity: "商机", event: "活动",
  mine: "我的", academy: "学院",
};

function svgText(name, dir = "function") {
  return fs.readFileSync(path.join(ROOT, "assets", dir, name + ".svg"), "utf8");
}

const browser = await chromium.launch({ executablePath: EDGE, headless: true });
const page = await browser.newPage({ viewport: { width: 81, height: 81 }, deviceScaleFactor: 1 });

for (const state of ["line", "fill"]) {
  for (const slug of tabNames) {
    const name = `icon-app-${slug}-${state}`;
    const svg = svgText(name, "tabbar");
    await page.setContent(
      `<!doctype html><html><head><style>html,body{margin:0;padding:0;background:transparent;width:81px;height:81px;overflow:hidden}svg{display:block;width:81px;height:81px}</style></head><body>${svg}</body></html>`,
    );
    const out = path.join(ART, "tabbar", name + ".png");
    fs.mkdirSync(path.dirname(out), { recursive: true });
    await page.screenshot({ path: out, omitBackground: true });
    console.log("rendered", name);
  }
}

// 16 function icons on a 24x24 grid, 4 columns.
const tiles = functionNames.map((slug) => {
  const svg = svgText("icon-app-" + slug).replace("<svg ", '<svg class="icon" ');
  return `<figure class="tile"><div class="canvas">${svg}</div><figcaption>icon-app-${slug} · ${labels[slug]}</figcaption></figure>`;
}).join("");
const gridSvg = `
<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box}body{margin:0;background:#f7f8fb;font:13px/1.45 "Segoe UI","Microsoft YaHei",sans-serif;color:#1b2433;padding:24px}
h1{font-size:18px;margin:0 0 4px}p{margin:0 0 18px;color:#5b6577}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.tile{margin:0;background:#fff;border:1px solid #e3e7ef;border-radius:10px;padding:12px;display:flex;flex-direction:column;align-items:center}
.canvas{width:216px;height:216px;background-image:linear-gradient(to right,#e8edf7 1px,transparent 1px),linear-gradient(to bottom,#e8edf7 1px,transparent 1px);background-size:9px 9px;display:flex;align-items:center;justify-content:center;outline:1px solid #dbe2ee}
canvas{display:none}
.icon{width:216px;height:216px;display:block}
figcaption{margin-top:9px;text-align:center;font-size:12px;color:#4a5568}
.note{font-size:12px;color:#667085;margin-top:16px}
</style></head><body>
<h1>24 × 24 网格 · 2 px 描边 · 16 个功能入口图标</h1>
<p>每格背景为 24 等分网格（每格 1 px ≈ 9 px），图标主体落在 20 × 20 安全区。</p>
<div class="grid">${tiles}</div>
<p class="note">命名与文件一一对应；源文件为 assets/function/*.svg。</p>
</body></html>`;
const gridPage = await browser.newPage({ viewport: { width: 1100, height: 1120 }, deviceScaleFactor: 1 });
await gridPage.setContent(gridSvg);
await gridPage.waitForTimeout(200);
await gridPage.screenshot({ path: path.join(ART, "function-grid.png"), fullPage: true });
console.log("rendered function-grid.png");

// Tabbar visual preview: 5 columns x 2 rows, 81px at 1x plus labels.
const cells = tabNames.map((slug) => {
  const line = svgText("icon-app-" + slug + "-line", "tabbar");
  const fill = svgText("icon-app-" + slug + "-fill", "tabbar");
  return `<div class="cell"><div class="pair"><div class="state">${line}<span>线性</span></div><div class="state">${fill}<span>面性</span></div></div><div class="name">${labels[slug]} · icon-app-${slug}-line / -fill</div></div>`;
}).join("");
const tabHtml = `
<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box}body{margin:0;background:#fff;font:13px/1.4 "Segoe UI","Microsoft YaHei",sans-serif;color:#1b2433;padding:24px}
h1{font-size:18px;margin:0 0 16px}.cells{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
.cell{border:1px solid #e3e7ef;border-radius:10px;padding:12px;text-align:center}
.pair{display:flex;gap:6px;justify-content:center}.state{display:flex;flex-direction:column;align-items:center;gap:4px;font-size:11px;color:#667085}
svg{width:81px;height:81px;display:block}.name{font-size:11px;color:#4a5568;margin-top:8px}
</style></head><body><h1>底部标签栏 · 5 个图标 × 线性/面性（81 × 81 px PNG）</h1><div class="cells">${cells}</div></body></html>`;
const tabPage = await browser.newPage({ viewport: { width: 1100, height: 300 }, deviceScaleFactor: 1 });
await tabPage.setContent(tabHtml);
await tabPage.waitForTimeout(200);
await tabPage.screenshot({ path: path.join(ART, "tabbar-preview.png"), fullPage: true });
console.log("rendered tabbar-preview.png");

// Local iconfont demo page.
const demoUrl = "file:///" + path.join(ROOT, "demo", "index.html").replace(/\\/g, "/");
const demoPage = await browser.newPage({ viewport: { width: 1080, height: 900 }, deviceScaleFactor: 1 });
await demoPage.goto(demoUrl);
await demoPage.evaluate(() => document.fonts.ready);
await demoPage.waitForTimeout(500);
const fontCheck = await demoPage.evaluate(() => ({
  ready: document.fonts.check("56px 'MemberSpace Icons 1841'"),
  count: document.querySelectorAll(".ms-icon").length,
  widths: Array.from(document.querySelectorAll(".ms-icon")).slice(0, 3).map((el) => el.getBoundingClientRect().width),
}));
console.log("font check", JSON.stringify(fontCheck));
await demoPage.screenshot({ path: path.join(ART, "iconfont-demo.png"), fullPage: true });
console.log("rendered iconfont-demo.png");

await browser.close();
