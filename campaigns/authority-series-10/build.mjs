// Builds the 10 Payroll Authority Series graphics (1200 x 1200 PNG),
// a contact sheet and a 375 px mobile preview.
// Usage: node build.mjs   (needs the playwright npm package)
import { chromium } from 'playwright';
import { writeFileSync, readFileSync, mkdirSync, rmSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const fonts = pathToFileURL(join(here, '..', 'linkedin-oct-nov-2026', 'graphics', 'fonts')).href;
const outDir = join(here, 'png');
mkdirSync(outDir, { recursive: true });

const css = `
@font-face{font-family:Fraunces;font-weight:400;font-style:normal;src:url(${fonts}/fraunces-latin-400-normal.woff2)}
@font-face{font-family:Fraunces;font-weight:500;font-style:normal;src:url(${fonts}/fraunces-latin-500-normal.woff2)}
@font-face{font-family:Fraunces;font-weight:400;font-style:italic;src:url(${fonts}/fraunces-latin-400-italic.woff2)}
@font-face{font-family:Fraunces;font-weight:500;font-style:italic;src:url(${fonts}/fraunces-latin-500-italic.woff2)}
@font-face{font-family:Inter;font-weight:400;src:url(${fonts}/inter-latin-400-normal.woff2)}
@font-face{font-family:Inter;font-weight:500;src:url(${fonts}/inter-latin-500-normal.woff2)}
@font-face{font-family:Inter;font-weight:600;src:url(${fonts}/inter-latin-600-normal.woff2)}
:root{--cream:#FAF7F2;--plum:#312644;--clay:#D98C6F;--deepclay:#C97C63;--lav:#B7A7DA;--blush:#ECD5C8}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1200px;height:1200px;background:var(--cream);overflow:hidden}
.card{position:relative;width:1200px;height:1200px;padding:104px 104px 84px;display:flex;flex-direction:column;color:var(--plum);font-family:Inter,sans-serif}
.blob{position:absolute;top:-250px;right:-230px;width:600px;height:600px;z-index:0;transform:rotate(-18deg)}
.cool .panel{background:rgba(183,167,218,.3)}
.card>*:not(.blob){position:relative;z-index:1}
.label{font:600 22px/1 Inter;letter-spacing:.2em;color:var(--deepclay);text-transform:uppercase}
.rule{width:72px;height:3px;background:var(--clay);margin-top:26px;border-radius:2px}
.main{flex:1;display:flex;flex-direction:column;justify-content:center}
.hook{font-family:Fraunces,serif;font-weight:400;font-size:80px;line-height:1.1;letter-spacing:-.015em}
.hook .em{color:var(--deepclay);display:block;margin-top:6px}
.hook.sm{font-size:70px}
.support{font:400 36px/1.4 Inter;color:rgba(49,38,68,.82);margin-top:48px}
.panel{background:var(--blush);border-radius:20px;padding:34px 44px;margin-top:56px;font:400 35px/1.4 Inter;color:var(--plum)}
.quote{font-family:Fraunces,serif;font-style:italic;font-size:72px;line-height:1.14;letter-spacing:-.01em}
.verdict{font-family:Fraunces,serif;font-weight:500;font-size:62px;line-height:1.16;color:var(--deepclay);margin-top:40px}
.qrule{width:72px;height:3px;background:var(--clay);margin-top:52px;border-radius:2px}
.footer{display:flex;align-items:center;justify-content:space-between;border-top:1px solid rgba(49,38,68,.14);padding-top:30px}
.brand{display:flex;align-items:center;gap:18px}
.mono{width:56px;height:56px;border-radius:15px;background:var(--plum);color:var(--cream);display:flex;align-items:center;justify-content:center;font:500 33px/1 Fraunces;padding-bottom:3px}
.word{font:500 31px/1 Fraunces}
.tag{font:500 19px/1 Inter;letter-spacing:.16em;text-transform:uppercase;color:rgba(49,38,68,.7)}
.method{display:flex;align-items:center;gap:12px;margin-top:56px}
.pill{font:600 19px/1 Inter;letter-spacing:.12em;padding:18px 20px;border-radius:999px;background:var(--lav);color:var(--plum)}
.pill.key{background:var(--deepclay);color:var(--cream)}
.arrow{font:400 26px/1 Inter}
.methodline{font:600 21px/1 Inter;letter-spacing:.14em;color:rgba(49,38,68,.72);margin-top:56px}
.close{font:500 italic 38px/1.3 Fraunces;margin-top:40px}
.flow{margin-top:68px;position:relative;height:96px}
.flow .line{position:absolute;left:14px;right:14px;top:13px;height:3px;background:var(--clay)}
.flow .stop{position:absolute;top:0;display:flex;flex-direction:column;gap:22px}
.flow .dot{width:30px;height:30px;border-radius:50%;border:3px solid var(--clay);background:var(--cream)}
.flow .dot.on{background:var(--deepclay);border-color:var(--deepclay)}
.flow .cap{font:600 19px/1 Inter;letter-spacing:.16em;color:rgba(49,38,68,.75)}
.flow .cap.on{color:var(--deepclay)}
.grid{display:grid;grid-template-columns:repeat(24,14px);gap:12px;margin-top:60px}
.grid i{width:14px;height:14px;border-radius:50%;background:rgba(49,38,68,.16)}
.grid i.on{background:var(--deepclay);transform:scale(1.5)}
`;

// Restrained organic shape, top right, partly off canvas.
const blob = (fill, op) => `<svg class="blob" viewBox="0 0 600 600"><path fill="${fill}" fill-opacity="${op}" d="M438 58c62 36 116 94 128 166 13 76-27 140-58 208-34 74-76 140-160 152-86 12-150-46-214-96C70 440 16 392 22 312 28 226 92 182 150 128 214 68 266 22 336 26c38 2 72 14 102 32z"/></svg>`;
const warm = blob('#ECD5C8', 0.75);
const cool = blob('#B7A7DA', 0.32);
const footer = `<div class="footer"><div class="brand"><div class="mono">K</div><div class="word">Khafayah.AI</div></div><div class="tag">AI Made Friendly</div></div>`;
const head = (label) => `<div><div class="label">${label}</div><div class="rule"></div></div>`;
const page = (shape, label, body) => `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body><div class="card${shape === cool ? ' cool' : ''}">${shape}${head(label)}<div class="main">${body}</div>${footer}</div></body></html>`;
const method = `<div class="method"><span class="pill">INVESTIGATE</span><span class="arrow">→</span><span class="pill key">VALIDATE</span><span class="arrow">→</span><span class="pill">TRANSLATE</span><span class="arrow">→</span><span class="pill">ANTICIPATE</span></div>`;
const dots = Array.from({ length: 72 }, (_, i) => `<i${i === 41 ? ' class="on"' : ''}></i>`).join('');

export const posts = [
  ['01_payroll-control-note_errors-start-before-payroll', page(warm, 'Payroll Control Note', `
    <div class="hook">Most payroll errors start <span class="em">before payroll starts.</span></div>
    <div class="flow"><div class="line"></div>
      <div class="stop" style="left:0;align-items:flex-start"><div class="dot on"></div><div class="cap on">INPUT</div></div>
      <div class="stop" style="left:50%;transform:translateX(-50%);align-items:center"><div class="dot"></div><div class="cap">CALCULATION</div></div>
      <div class="stop" style="right:0;align-items:flex-end"><div class="dot"></div><div class="cap">PAYSLIP</div></div></div>
    <div class="support">Control the input, not only the output.</div>`)],
  ['02_payroll-control-note_reconciliation-is-a-control', page(warm, 'Payroll Control Note', `
    <div class="hook">A reconciliation is not a tick-box. <span class="em">It is a control.</span></div>
    <div class="panel">Matching totals is only the beginning.</div>`)],
  ['03_payroll-leadership_ask-sarah', page(warm, 'Payroll Leadership', `
    <div class="quote">“Ask Sarah. She knows how that works.”</div>
    <div class="verdict">That is not a payroll control.</div>`)],
  ['04_payroll-control-note_inbox-is-operational-data', page(warm, 'Payroll Control Note', `
    <div class="hook">Your payroll inbox <span class="em">is operational data.</span></div>
    <div class="panel">Do not only answer the query. Learn from it.</div>`)],
  ['05_payroll-control-note_not-checking-everything', page(warm, 'Payroll Control Note', `
    <div class="hook sm">Strong payroll control is not checking everything.</div>
    <div class="grid">${dots}</div>
    <div class="support">It is knowing what deserves attention.</div>`)],
  ['06_payroll-leadership_hr-or-payroll', page(warm, 'Payroll Leadership', `
    <div class="quote">“Is this HR or Payroll?”</div>
    <div class="verdict">If employees keep asking, the process probably needs work.</div>`)],
  ['07_responsible-ai_investigate-not-decide', page(cool, 'Responsible AI in Payroll', `
    <div class="hook sm">AI should help payroll investigate. <span class="em">It should not make the payroll decision.</span></div>
    ${method}
    <div class="close">AI assists. The professional validates.</div>`)],
  ['08_responsible-ai_not-upload-the-file', page(cool, 'Responsible AI in Payroll', `
    <div class="hook sm">Responsible AI in payroll does not start with: <span class="em" style="font-style:italic">“Upload the payroll file.”</span></div>
    <div class="panel">It starts with the data question.</div>`)],
  ['09_payroll-transformation_automation-bad-data', page(cool, 'Payroll Transformation', `
    <div class="hook">Automation does not fix <span class="em">bad payroll data.</span></div>
    <div class="panel">Sometimes it moves the error faster.</div>`)],
  ['10_responsible-ai_better-questions', page(cool, 'Responsible AI in Payroll', `
    <div class="hook">Payroll does not need better prompts first. <span class="em">It needs better questions.</span></div>
    <div class="methodline">INVESTIGATE → VALIDATE → TRANSLATE → ANTICIPATE</div>`)],
];

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const ctx = await browser.newContext({ viewport: { width: 1200, height: 1200 } });
const files = [];
for (const [name, html] of posts) {
  const htmlPath = join(outDir, name + '.html');
  writeFileSync(htmlPath, html);
  const pg = await ctx.newPage();
  await pg.goto(pathToFileURL(htmlPath).href);
  await pg.evaluate(() => document.fonts.ready);
  const over = await pg.evaluate(() => {
    const c = document.querySelector('.card');
    const m = document.querySelector('.method');
    return c.scrollHeight > 1200 || (m && m.scrollWidth > 992);
  });
  if (over) console.warn('OVERFLOW:', name);
  await pg.screenshot({ path: join(outDir, name + '.png') });
  await pg.close();
  rmSync(htmlPath);
  files.push(name + '.png');
  console.log('built', name);
}

const b64 = (f) => 'data:image/png;base64,' + readFileSync(join(outDir, f)).toString('base64');
const shot = async (html, w, h, out) => {
  const p = await ctx.newPage();
  await p.setViewportSize({ width: w, height: h });
  await p.setContent(html);
  await p.waitForLoadState('load');
  await p.screenshot({ path: join(here, out), fullPage: true });
  await p.close();
};

// Contact sheet: 5 x 2 grid.
await shot(`<body style="margin:0;padding:40px;background:#EFEAE3;font:16px Inter,sans-serif;display:grid;grid-template-columns:repeat(5,360px);gap:28px">
  ${files.map((f) => `<figure style="margin:0"><img src="${b64(f)}" style="width:360px;height:360px;display:block;box-shadow:0 1px 4px rgba(0,0,0,.12)"><figcaption style="padding-top:10px;color:#312644">${f.slice(0, 2)}  ${f.slice(3, -4).replace(/_/g, ' · ').replace(/-/g, ' ')}</figcaption></figure>`).join('')}
</body>`, 2000, 900, 'contact-sheet.png');

// Mobile preview: each graphic at 375 px, a typical phone feed width.
await shot(`<body style="margin:0;padding:24px;background:#e9e6ef;display:grid;grid-template-columns:repeat(5,375px);gap:24px">
  ${files.map((f) => `<img src="${b64(f)}" style="width:375px;height:375px;display:block">`).join('')}
</body>`, 2019, 860, 'mobile-preview.png');

await browser.close();
console.log('contact sheet and mobile preview built');
