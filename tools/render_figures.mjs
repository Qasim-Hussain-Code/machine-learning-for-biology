// Render drawn figures (figures/svg/*.svg) as they will appear in the book, for checking: each in the light and the
// dark theme, at the desktop text width (660 px) and at a phone width (358 px), with its caption from the chapter.
// usage: node tools/render_figures.mjs <out_dir> figures/svg/fig-1-1.svg [more.svg ...]
// Writes <out_dir>/<name>-<theme>-<width>.png and prints a JSON report (sizes, smallest rendered text, overflow).
import { createServer } from 'node:http';
import { readFile, writeFile, mkdir, mkdtemp, rm, readdir, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join, extname, resolve, normalize, basename } from 'node:path';
import { tmpdir } from 'node:os';
import { spawn, spawnSync } from 'node:child_process';

const [outDir, ...svgs] = process.argv.slice(2);
if (!outDir || !svgs.length) { console.error('usage: node tools/render_figures.mjs <out_dir> figures/svg/a.svg ...'); process.exit(2); }
const ROOT = resolve(join(import.meta.dirname, '..'));
const CHROME = ['C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  `${process.env.LOCALAPPDATA}/Google/Chrome/Application/chrome.exe`, '/usr/bin/google-chrome', '/usr/bin/chromium'].find((p) => p && existsSync(p));
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const FONTS = 'https://fonts.googleapis.com/css2?family=STIX+Two+Text:ital,wght@0,400..700;1,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap';

async function page(svgPath, theme) {
  const svg = (await readFile(join(ROOT, svgPath), 'utf8')).replace(/<\?xml[^>]*\?>\s*/, '');
  const name = basename(svgPath);
  let caption = '';
  for (const f of (await readdir(join(ROOT, 'chapters'))).filter((f) => f.endsWith('.md'))) {
    const t = await readFile(join(ROOT, 'chapters', f), 'utf8');
    const m = t.match(new RegExp(`src="figures/svg/${name.replace('.', '\\.')}"[\\s\\S]*?<figcaption>([\\s\\S]*?)</figcaption>`));
    if (m) { caption = m[1]; break; }
  }
  return `<!doctype html><html lang="en-GB" data-theme="${theme}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link href="${FONTS}" rel="stylesheet"><link rel="stylesheet" href="/tools/theme/book.css">
<style>body{margin:0;padding:24px 16px;background:var(--bg)}.col{max-width:660px;margin:0;padding:0}</style></head>
<body class="lay-sidebar hs-smallcaps"><main class="col"><figure class="fig" id="f">${svg.replace(/<svg\b/, '<svg class="figsvg"')}
<figcaption>${caption}</figcaption></figure></main></body></html>`;
}

const pages = new Map();
const server = createServer(async (req, res) => {
  const url = new URL(req.url, 'http://x');
  if (url.pathname === '/__fig') { res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' }).end(pages.get(url.searchParams.get('k'))); return; }
  const path = normalize(join(ROOT, decodeURIComponent(url.pathname)));
  if (!path.startsWith(ROOT)) { res.writeHead(403).end(); return; }
  let body; try { body = await readFile(path); } catch { res.writeHead(404).end(); return; }
  res.writeHead(200, { 'content-type': extname(path) === '.css' ? 'text/css' : 'application/octet-stream' }).end(body);
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const port = server.address().port;
// Sweep only profiles left by earlier runs (older than 15 minutes), so renders running at the same time keep theirs.
for (const d of await readdir(tmpdir()).catch(() => [])) {
  if (!d.startsWith('mlb-fig-')) continue;
  const full = join(tmpdir(), d);
  const age = await stat(full).then((s) => Date.now() - s.mtimeMs, () => 0);
  if (age > 15 * 60 * 1000) await rm(full, { recursive: true, force: true }).catch(() => {});
}
const profile = await mkdtemp(join(tmpdir(), 'mlb-fig-'));
// Chrome picks a free debugging port and writes it to DevToolsActivePort, so parallel renders never share one.
const chrome = spawn(CHROME, ['--headless=new', '--remote-debugging-port=0', `--user-data-dir=${profile}`,
  '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });
let debugPort = 0;
for (let i = 0; i < 120 && !debugPort; i++) {
  try { debugPort = Number((await readFile(join(profile, 'DevToolsActivePort'), 'utf8')).split('\n')[0]) || 0; } catch {}
  if (!debugPort) await sleep(250);
}
let ws, id = 0; const pending = new Map(), waiters = [];
const send = (method, params = {}) => new Promise((ok, fail) => { const n = ++id; pending.set(n, { ok, fail }); ws.send(JSON.stringify({ id: n, method, params })); });
const once = (method) => new Promise((ok) => waiters.push({ method, ok }));
const report = {};
try {
  let target;
  for (let i = 0; i < 60 && !target; i++) {
    try { target = (await (await fetch(`http://127.0.0.1:${debugPort}/json/list`)).json()).find((t) => t.type === 'page'); } catch { await sleep(250); }
  }
  ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((ok, fail) => { ws.onopen = ok; ws.onerror = fail; });
  ws.onmessage = (e) => { const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.fail(new Error(m.error.message)) : p.ok(m.result); }
    else if (m.method) for (let i = waiters.length - 1; i >= 0; i--) if (waiters[i].method === m.method) { waiters[i].ok(m.params); waiters.splice(i, 1); } };
  await send('Page.enable'); await send('Runtime.enable');
  await mkdir(outDir, { recursive: true });
  for (const svgPath of svgs) {
    const name = basename(svgPath, '.svg');
    for (const theme of ['light', 'dark']) {
      for (const width of [692, 390]) {
        const key = `${name}-${theme}-${width}`;
        pages.set(key, await page(svgPath, theme));
        await send('Emulation.setDeviceMetricsOverride', { width, height: 1400, deviceScaleFactor: 1.5, mobile: width < 500 });
        const loaded = once('Page.loadEventFired');
        await send('Page.navigate', { url: `http://127.0.0.1:${port}/__fig?k=${encodeURIComponent(key)}` });
        await loaded;
        const r = await send('Runtime.evaluate', { awaitPromise: true, returnByValue: true, expression: `(async () => {
          await document.fonts.ready; await new Promise((r) => setTimeout(r, 150));
          const f = document.getElementById('f').getBoundingClientRect();
          const svg = document.querySelector('#f svg'), sb = svg.getBoundingClientRect();
          const sizes = [...svg.querySelectorAll('text')].map((t) => t.getBoundingClientRect().height).filter((h) => h > 0);
          const outside = [...svg.querySelectorAll('text')].filter((t) => { const b = t.getBoundingClientRect();
            return b.left < sb.left - 1 || b.right > sb.right + 1 || b.top < sb.top - 1 || b.bottom > sb.bottom + 1; }).map((t) => t.textContent.slice(0, 40));
          const unstyled = [...svg.querySelectorAll('rect,circle,path,line,polyline,polygon,ellipse,text')].filter((el) =>
            !el.getAttribute('class') && !el.closest('[class]:not(svg)')).length;
          return { x: f.left, y: f.top, w: f.width, h: f.height, svgW: Math.round(sb.width), svgH: Math.round(sb.height),
            minText: sizes.length ? Math.round(Math.min(...sizes) * 10) / 10 : null, texts: sizes.length, outside, unstyled };
        })()` });
        const v = r.result.value;
        const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true,
          clip: { x: 0, y: 0, width, height: Math.ceil(v.y + v.h + 24), scale: 1 } });
        await writeFile(join(outDir, `${key}.png`), Buffer.from(shot.data, 'base64'));
        report[key] = { svg: `${v.svgW}x${v.svgH}`, smallest_text_px: v.minText, text_items: v.texts, text_outside_figure: v.outside, unclassed_shapes: v.unstyled };
      }
    }
  }
  console.log(JSON.stringify(report, null, 1));
} catch (e) { console.error(String(e && e.stack || e)); process.exitCode = 1; }
finally {
  try { ws && ws.close(); } catch {}
  if (process.platform === 'win32') spawnSync('taskkill', ['/PID', String(chrome.pid), '/T', '/F'], { stdio: 'ignore' }); else chrome.kill('SIGKILL');
  server.closeAllConnections?.(); server.close();
  await sleep(500);
  await Promise.race([rm(profile, { recursive: true, force: true }).catch(() => {}), sleep(4000)]);
  process.exit(process.exitCode || 0);
}
