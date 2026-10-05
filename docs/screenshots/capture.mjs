// Figure 1: step-by-step workflow of the NMA app, high resolution (Playwright + installed Google Chrome, headless).
// Viewport 640 x 900 CSS px (the page's single-column layout, every panel about 590 px wide), light theme,
// device scale factor 4 (at least 3x; 4 so that panels are >= 300 dpi at 170 mm with text >= 8 pt). compose.py
// lays the regions out (tight crops, labelled sub-panels) and checks legibility from the font sizes recorded here.
// Data: the app's built-in copy of netmeta's smokingcessation dataset (24 studies, 4 treatments).
//   node docs/screenshots/capture.mjs <work-dir> http://localhost:8000/app/nma/index.html
//   python docs/screenshots/compose.py <work-dir> docs/screenshots
import { chromium } from "playwright";
import { writeFileSync, mkdirSync } from "fs";
const [D, APP] = process.argv.slice(2);
const OUT = `${D}/regions`; mkdirSync(OUT, { recursive: true });
const DPR = 4;
const b = await chromium.launch({ channel: "chrome" });
const ctx = await b.newContext({ viewport: { width: 640, height: 900 }, colorScheme: "light", deviceScaleFactor: DPR });
const p = await ctx.newPage();
const errs = []; p.on("pageerror", (e) => errs.push(e.message));
const meta = { dpr: DPR, viewport: [640, 900], regions: {}, states: {} };
await p.goto(APP); await p.evaluate(() => { try { localStorage.clear(); } catch (e) {} }); await p.goto(APP); await p.waitForTimeout(500);
await p.addStyleTag({ content: "#hub-back{display:none!important}" });
const set = async (o) => { for (const [id, v] of Object.entries(o)) await p.selectOption("#" + id, v); await p.waitForTimeout(400); };
const state = async (name) => (meta.states[name] = await p.evaluate(() => ({ het: document.getElementById("het-host").innerText,
  ref: document.getElementById("ref-host").innerText, rank: document.getElementById("sucra-host").innerText, notes: document.getElementById("warn-banner").innerText })));
// page rectangle of an element, or of the panel / fieldset whose heading starts with `h2:<text>` / `legend:<text>`
const rect = (sel, opt = {}) => p.evaluate(([sel, opt]) => {
  const pick = (tag, t) => [...document.querySelectorAll(tag)].find((h) => h.textContent.trim().startsWith(t));
  let e = sel.startsWith("h2:") ? pick("h2", sel.slice(3)) : sel.startsWith("legend:") ? pick("legend", sel.slice(7)) : document.querySelector(sel);
  if (!e) throw new Error("missing " + sel);
  if (opt.closest) e = e.closest(opt.closest);
  const r = e.getBoundingClientRect(); return { x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height };
}, [sel, opt]);
async function region(name, r, pad = 6) {
  const c = { x: Math.max(0, Math.floor(r.x - pad)), y: Math.max(0, Math.floor(r.y - pad)), width: Math.ceil(r.w + 2 * pad), height: Math.ceil(r.h + 2 * pad) };
  await p.screenshot({ path: `${OUT}/${name}.png`, clip: c, fullPage: true });
  const fonts = await p.evaluate((c) => {
    const out = [];
    const inside = (rr) => rr.width > 0 && rr.height > 0 && rr.left + scrollX >= c.x - 1 && rr.right + scrollX <= c.x + c.width + 1 && rr.top + scrollY >= c.y - 1 && rr.bottom + scrollY <= c.y + c.height + 1;
    const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    for (let n = tw.nextNode(); n; n = tw.nextNode()) {
      const t = n.textContent.trim(); if (t.length < 2) continue;
      const el = n.parentElement; const cs = getComputedStyle(el); if (cs.visibility === "hidden" || cs.display === "none") continue;
      if (el.tagName === "TEXTAREA" || el.tagName === "SCRIPT" || el.tagName === "STYLE" || el.tagName === "OPTION") continue;
      const range = document.createRange(); range.selectNodeContents(n); const rr = range.getBoundingClientRect(); if (!inside(rr)) continue;
      let px = parseFloat(cs.fontSize);
      if (el.closest("svg") && el.getScreenCTM) { const m = el.getScreenCTM(); if (m) px = px * Math.hypot(m.a, m.b); }
      out.push([Math.round(px * 100) / 100, t.length]);
    }
    document.querySelectorAll("textarea, input[type=text], select").forEach((f) => { const rr = f.getBoundingClientRect(); if (inside(rr)) out.push([parseFloat(getComputedStyle(f).fontSize), 10]); });
    return out;
  }, c);
  meta.regions[name] = { clip: c, fonts };
}

// 1 data entry: netmeta's smokingcessation from the example list
await set({ "f-example": "smokingcessation" }); await p.click("#btn-example"); await p.waitForTimeout(700);
await p.evaluate(() => { document.getElementById("f-data").scrollTop = 0; });
await region("d1_data", await rect("legend:Data", { closest: "fieldset" }));
// 2 model options: random effects, normal CIs, larger odds ratios of quitting are better, odds ratios shown
await set({ "f-model": "re", "f-ci": "classic", "f-dir": "undesirable", "f-scale": "exp" }); await state("step2");
await region("d2_options", await rect("legend:Options", { closest: "fieldset" }));
// 3 network graph and summary cards
await region("d3_network", await rect("#svg-host svg"), 2);
await region("d3_stats", await rect("#stats-wrap .stats"));
// 4 heterogeneity, inconsistency and estimates versus the reference
await region("d4_het", await rect("h2:Heterogeneity", { closest: ".panel" }));
await region("d4_ref", await rect("h2:Estimates versus", { closest: ".panel" }));
// 5 ranking and league table
await region("d5_rank", await rect("h2:Ranking", { closest: ".panel" }));
await region("d5_league", await rect("h2:League table", { closest: ".panel" }));
// 6 t-based CIs; a multi-arm study with a missing comparison is refused, naming the study; export
await set({ "f-ci": "t-dist" }); await state("step6");
await region("d6_t", await rect("h2:Estimates versus", { closest: ".panel" }));
await region("d6_export", await rect(".actions"));
await p.evaluate(() => { const ta = document.getElementById("f-data"); ta.value = ta.value.split("\n").filter((l) => !/^1, D, C,/.test(l)).join("\n"); ta.dispatchEvent(new Event("input")); });
await p.waitForTimeout(500); await state("step6_refusal");
await region("d6_refuse", await rect("#warn-banner"));
meta.errors = errs;
writeFileSync(`${D}/regions_meta.json`, JSON.stringify(meta, null, 1));
console.log(JSON.stringify({ states: meta.states, regions: Object.keys(meta.regions), errors: errs }, null, 1));
await b.close();
