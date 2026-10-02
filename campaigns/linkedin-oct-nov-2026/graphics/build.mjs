// Builds the five authority post graphics (1200 x 1200 PNG) for the
// October to November 2026 LinkedIn campaign.
// Usage: node build.mjs   (needs the playwright npm package)
import { chromium } from 'playwright';
import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const fonts = pathToFileURL(join(here, 'fonts')).href;
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
html,body{width:1200px;height:1200px;background:var(--cream)}
.card{width:1200px;height:1200px;padding:104px 104px 88px;display:flex;flex-direction:column;color:var(--plum);font-family:Inter,sans-serif}
.label{font:600 22px/1 Inter;letter-spacing:.2em;color:var(--deepclay);text-transform:uppercase}
.rule{width:72px;height:3px;background:var(--clay);margin-top:26px;border-radius:2px}
.main{flex:1;display:flex;flex-direction:column;justify-content:center}
.hook{font-family:Fraunces,serif;font-weight:400;font-size:82px;line-height:1.1;letter-spacing:-.015em;font-variation-settings:"SOFT" 100}
.hook .em{color:var(--deepclay);display:block;margin-top:6px}
.support{font:400 36px/1.4 Inter;color:rgba(49,38,68,.82);margin-top:48px}
.panel{background:var(--blush);border-radius:20px;padding:36px 44px;margin-top:56px;font:400 35px/1.4 Inter;color:var(--plum)}
.footer{display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:18px}
.mono{width:58px;height:58px;border-radius:16px;background:var(--plum);color:var(--cream);display:flex;align-items:center;justify-content:center;font:500 34px/1 Fraunces;padding-bottom:3px}
.word{font:500 32px/1 Fraunces;letter-spacing:-.005em}
.tag{font:500 19px/1 Inter;letter-spacing:.16em;text-transform:uppercase;color:rgba(49,38,68,.7)}
.method{display:flex;align-items:center;gap:12px;margin-top:60px;flex-wrap:nowrap}
.pill{font:600 19px/1 Inter;letter-spacing:.12em;padding:18px 20px;border-radius:999px;background:var(--lav);color:var(--plum)}
.pill.key{background:var(--deepclay);color:var(--cream)}
.arrow{font:400 26px/1 Inter;color:var(--plum)}
.close{font:500 italic 38px/1.3 Fraunces;margin-top:44px}
.flow{margin-top:72px;position:relative;height:96px}
.flow .line{position:absolute;left:14px;right:14px;top:13px;height:3px;background:var(--clay)}
.flow .stop{position:absolute;top:0;display:flex;flex-direction:column;align-items:center;gap:22px;transform:translateX(-50%)}
.flow .dot{width:30px;height:30px;border-radius:50%;border:3px solid var(--clay);background:var(--cream)}
.flow .dot.on{background:var(--deepclay);border-color:var(--deepclay)}
.flow .cap{font:600 19px/1 Inter;letter-spacing:.16em;color:rgba(49,38,68,.75)}
.flow .cap.on{color:var(--deepclay)}
.quote{font-family:Fraunces,serif;font-style:italic;font-weight:400;font-size:68px;line-height:1.14;letter-spacing:-.01em}
.verdict{font-family:Fraunces,serif;font-weight:500;font-size:66px;line-height:1.14;color:var(--deepclay);margin-top:36px}
.qrule{width:72px;height:3px;background:var(--clay);margin-top:56px;border-radius:2px}
`;

const footer = `<div class="footer"><div class="brand"><div class="mono">K</div><div class="word">Khafayah.AI</div></div><div class="tag">AI Made Friendly</div></div>`;
const head = (label) => `<div><div class="label">${label}</div><div class="rule"></div></div>`;
const page = (body) => `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body><div class="card">${body}${footer}</div></body></html>`;

const posts = [
  {
    file: '2026-10-09_payroll-control-note_busy-inbox.png',
    html: page(`${head('Payroll Control Note')}
      <div class="main">
        <div class="hook">A busy payroll inbox is not just a service problem. <span class="em">It is operational data.</span></div>
        <div class="panel">The stronger question is not how to answer faster. It is why the queries arrive at all.</div>
      </div>`),
  },
  {
    file: '2026-10-14_responsible-ai_investigate-not-decide.png',
    html: page(`${head('Responsible AI in Payroll')}
      <div class="main">
        <div class="hook">AI should help payroll investigate. <span class="em">It should not make the payroll decision.</span></div>
        <div class="method">
          <span class="pill">INVESTIGATE</span><span class="arrow">→</span>
          <span class="pill key">VALIDATE</span><span class="arrow">→</span>
          <span class="pill">TRANSLATE</span><span class="arrow">→</span>
          <span class="pill">ANTICIPATE</span>
        </div>
        <div class="close">AI assists. The professional validates.</div>
      </div>`),
  },
  {
    file: '2026-10-28_payroll-control-note_errors-start-before-payroll.png',
    html: page(`${head('Payroll Control Note')}
      <div class="main">
        <div class="hook">Most payroll errors start <span class="em">before payroll starts.</span></div>
        <div class="flow">
          <div class="line"></div>
          <div class="stop" style="left:15px;transform:none;align-items:flex-start"><div class="dot on"></div><div class="cap on">INPUT</div></div>
          <div class="stop" style="left:50%"><div class="dot"></div><div class="cap">CALCULATION</div></div>
          <div class="stop" style="right:15px;left:auto;transform:none;align-items:flex-end"><div class="dot"></div><div class="cap">PAYSLIP</div></div>
        </div>
        <div class="support">Control the input. Do not rely on checking the output.</div>
      </div>`),
  },
  {
    file: '2026-11-02_responsible-ai_automation-bad-data.png',
    html: page(`${head('Responsible AI in Payroll')}
      <div class="main">
        <div class="hook">Automation does not fix <span class="em">bad payroll data.</span></div>
        <div class="panel">Automate the right process. Not the existing one.</div>
      </div>`),
  },
  {
    file: '2026-11-06_payroll-control-note_ask-sarah.png',
    html: page(`${head('Payroll Control Note')}
      <div class="main">
        <div class="quote">“Ask Sarah. She knows how that one works.”</div>
        <div class="verdict">That is not a payroll control.</div>
        <div class="qrule"></div>
        <div class="support" style="margin-top:36px">Payroll resilience is a function that still works when any one person is away.</div>
      </div>`),
  },
];

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const ctx = await browser.newContext({ viewport: { width: 1200, height: 1200 }, deviceScaleFactor: 1 });
for (const p of posts) {
  const htmlPath = join(outDir, p.file.replace('.png', '.html'));
  writeFileSync(htmlPath, p.html);
  const pg = await ctx.newPage();
  await pg.goto(pathToFileURL(htmlPath).href);
  await pg.evaluate(() => document.fonts.ready);
  const overflow = await pg.evaluate(() => document.querySelector('.card').scrollHeight > 1200 || document.querySelector('.method')?.scrollWidth > 992);
  if (overflow) console.warn('OVERFLOW:', p.file);
  await pg.screenshot({ path: join(outDir, p.file) });
  await pg.close();
  console.log('built', p.file);
}
await browser.close();
