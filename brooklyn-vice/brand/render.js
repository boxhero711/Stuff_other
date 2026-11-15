// Renders brand assets from templates.html to PNG.
//
//   node brand/render.js                 render every asset to brand/export/
//   node brand/render.js thumbnail --text "Brooklyn|*rules*|in Leonida" \
//        --bg path/frame.png --host path/host.png --out out/thumb.png
//
// Headline markup: |  line break, *word* gold, _word_ pink, ~word~ cyan.
// Never pass a GTA/Rockstar logo, key art, or game character as --bg or --host.
const { chromium } = require("playwright");
const path = require("path");
const fs = require("fs");

const TEMPLATE = "file://" + path.join(__dirname, "templates.html");
const EXPORT = path.join(__dirname, "export");

function parseArgs(argv) {
  const out = { assets: [], opts: {} };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith("--")) out.opts[argv[i].slice(2)] = argv[++i];
    else out.assets.push(argv[i]);
  }
  return out;
}

async function render(page, asset, opts) {
  const params = new URLSearchParams({ asset });
  for (const [k, v] of Object.entries(opts)) {
    if (k === "out") continue;
    params.set(k, ((k === "bg" || k === "host") && v !== "none") ? "file://" + path.resolve(v) : v);
  }
  await page.goto(TEMPLATE + "#" + params.toString());
  await page.reload(); // hash-only navigation does not re-run scripts
  await page.evaluate(() => document.fonts.ready);
  await page.waitForLoadState("networkidle");
  const size = await page.evaluate(() => window.ASSET_SIZE);
  await page.setViewportSize({ width: size.w, height: size.h });
  const out = opts.out || path.join(EXPORT, `${asset}.png`);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  await page.locator("#stage").screenshot({ path: out, omitBackground: size.transparent });
  console.log("wrote", path.relative(process.cwd(), out), `${size.w}x${size.h}`);
}

(async () => {
  const { assets, opts } = parseArgs(process.argv.slice(2));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 2560, height: 1440 } });
  let list = assets;
  if (!list.length) {
    await page.goto(TEMPLATE + "#asset=avatar");
    list = await page.evaluate(() => window.ASSET_LIST);
  }
  for (const a of list) await render(page, a, assets.length ? opts : {});
  await browser.close();
})();
