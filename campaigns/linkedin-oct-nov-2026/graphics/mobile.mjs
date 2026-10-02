// Mobile preview: each graphic at 375 px wide, the width of a typical phone feed.
import { chromium } from 'playwright';
import { readdirSync, readFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const here = dirname(fileURLToPath(import.meta.url));
const pngs = readdirSync(join(here, 'png')).filter(f => f.endsWith('.png')).sort();
const imgs = pngs.map(f => `<figure><img src="data:image/png;base64,${readFileSync(join(here, 'png', f)).toString('base64')}"><figcaption>${f.slice(0, 10)}</figcaption></figure>`).join('');
const html = `<!doctype html><html><body style="margin:0;background:#e9e6ef;font:14px sans-serif;display:flex;gap:24px;padding:24px">
<style>figure{margin:0;width:375px;background:#fff;padding-bottom:10px}img{width:375px;height:375px;display:block}figcaption{padding:8px 12px;color:#555}</style>${imgs}</body></html>`;
const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const p = await b.newPage({ viewport: { width: 24 + pngs.length * 399, height: 460 } });
await p.setContent(html);
await p.waitForLoadState('load');
await p.screenshot({ path: join(here, 'mobile-preview.png'), fullPage: true });
await b.close();
console.log('mobile preview built');
