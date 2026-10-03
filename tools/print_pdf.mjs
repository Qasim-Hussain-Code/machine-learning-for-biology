// Print one page of the built book to PDF with headless Chrome, using the page's own @page size and margins.
// usage: node tools/print_pdf.mjs <docs_dir> <page.html> <out.pdf>
// Needs Node 22 or later (built-in WebSocket) and an installed Chrome. Nothing is installed or downloaded.
import { createServer } from 'node:http';
import { readFile, writeFile, mkdtemp, rm, readdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join, extname, resolve, normalize } from 'node:path';
import { tmpdir } from 'node:os';
import { spawn, spawnSync } from 'node:child_process';

const [docs, pageName, out] = process.argv.slice(2);
if (!docs || !pageName || !out) { console.error('usage: node tools/print_pdf.mjs <docs_dir> <page.html> <out.pdf>'); process.exit(2); }
const ROOT = resolve(docs);
const CHROME = ['C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  `${process.env.LOCALAPPDATA}/Google/Chrome/Application/chrome.exe`, '/usr/bin/google-chrome', '/usr/bin/chromium',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'].find((p) => p && existsSync(p));
if (!CHROME) { console.error('Chrome was not found'); process.exit(2); }
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.jpeg': 'image/jpeg',
  '.jpg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.json': 'application/json' };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const server = createServer(async (req, res) => {
  const path = normalize(join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname)));
  if (!path.startsWith(ROOT)) { res.writeHead(403).end(); return; }
  let body;
  try { body = await readFile(path); } catch { res.writeHead(404).end(); return; }
  res.writeHead(200, { 'content-type': TYPES[extname(path).toLowerCase()] || 'application/octet-stream' }).end(body);
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const port = server.address().port;
// clear profiles left by earlier runs (one may still be locked for a moment after its Chrome ended)
for (const d of await readdir(tmpdir()).catch(() => [])) {
  if (d.startsWith('mlb-print-')) await rm(join(tmpdir(), d), { recursive: true, force: true }).catch(() => {});
}
const profile = await mkdtemp(join(tmpdir(), 'mlb-print-'));
const debugPort = 9600 + (process.pid % 300);
const chrome = spawn(CHROME, ['--headless=new', `--remote-debugging-port=${debugPort}`, `--user-data-dir=${profile}`,
  '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--hide-scrollbars', 'about:blank'], { stdio: 'ignore' });

let ws, id = 0;
const pending = new Map(), waiters = [];
function send(method, params = {}) {
  return new Promise((ok, fail) => { const n = ++id; pending.set(n, { ok, fail }); ws.send(JSON.stringify({ id: n, method, params })); });
}
function once(method) { return new Promise((ok) => waiters.push({ method, ok })); }
try {
  let target;
  for (let i = 0; i < 60 && !target; i++) {
    try { target = (await (await fetch(`http://127.0.0.1:${debugPort}/json/list`)).json()).find((t) => t.type === 'page'); }
    catch { await sleep(250); }
  }
  if (!target) throw new Error('Chrome did not start');
  ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((ok, fail) => { ws.onopen = ok; ws.onerror = fail; });
  ws.onmessage = (e) => {
    const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.fail(new Error(m.error.message)) : p.ok(m.result); }
    else if (m.method) for (let i = waiters.length - 1; i >= 0; i--) if (waiters[i].method === m.method) { waiters[i].ok(m.params); waiters.splice(i, 1); }
  };
  await send('Page.enable');
  await send('Runtime.enable');
  const loaded = once('Page.loadEventFired');
  await send('Page.navigate', { url: `http://127.0.0.1:${port}/${pageName}` });
  await loaded;
  const ready = await send('Runtime.evaluate', { awaitPromise: true, returnByValue: true, expression: `(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map((i) => i.complete ? 0 : new Promise((r) => { i.onload = i.onerror = r; })));
    return { fonts: [...document.fonts].filter((f) => f.status === 'loaded').map((f) => f.family + ' ' + f.weight + ' ' + f.style),
             broken: [...document.images].filter((i) => !i.naturalWidth).map((i) => i.getAttribute('src')) };
  })()` });
  const info = ready.result.value;
  if (info.broken.length) throw new Error('images failed to load: ' + info.broken.join(', '));
  await sleep(400);
  const pdf = await send('Page.printToPDF', { preferCSSPageSize: true, printBackground: true, generateDocumentOutline: true,
    generateTaggedPDF: true, displayHeaderFooter: false });
  await writeFile(out, Buffer.from(pdf.data, 'base64'));
  console.log(JSON.stringify({ out, fonts: [...new Set(info.fonts)].length }));
} catch (e) {
  console.error(String(e && e.stack || e));
  process.exitCode = 1;
} finally {
  try { ws && ws.close(); } catch {}
  // Chrome's helper processes outlive the main one unless the whole tree is ended, and they hold the server open.
  if (process.platform === 'win32') spawnSync('taskkill', ['/PID', String(chrome.pid), '/T', '/F'], { stdio: 'ignore' });
  else chrome.kill('SIGKILL');
  server.closeAllConnections?.();
  server.close();
  await sleep(800);
  // a profile file can stay locked for a moment after Chrome ends; never let the clean-up hold the build
  await Promise.race([rm(profile, { recursive: true, force: true, maxRetries: 3, retryDelay: 300 }).catch(() => {}), sleep(4000)]);
  process.exit(process.exitCode || 0);
}
