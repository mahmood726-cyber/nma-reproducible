// Run the app's JavaScript engine (app/shared/nma-multiarm-v1.js, loaded unchanged) on every dataset of the
// corpus: analyse() with both random-effects CI methods ("classic", "t-dist") and both directions of benefit
// for the P-scores. The page app/nma/index.html calls the same function. The analyses are fixed here
// (identical to bench/reference_netmeta.R), so this output depends only on the corpus and the engine.
// Convention: netmeta's TE is treat1 - treat2; the app's estimate is treatment2 - treatment1, so each contrast
// is passed with treatment1 = treat2 and treatment2 = treat1. Output: one JSON object per dataset per line.
//
//   node bench/run_engine.mjs results/full/corpus.csv results/full/engine.jsonl
import { readFileSync, writeFileSync, mkdirSync } from "fs";
import { createHash } from "crypto";
import { createRequire } from "module";
import { dirname, join } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const require = createRequire(import.meta.url);
const ENGINE = join(ROOT, "app", "shared", "nma-multiarm-v1.js");
const E = require(ENGINE);
const sha = (f) => createHash("sha256").update(readFileSync(f)).digest("hex");

function parseCSV(text) {
  const rows = []; let row = [], cur = "", q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { cur += '"'; i++; } else q = false; } else cur += c; }
    else if (c === '"') q = true;
    else if (c === ",") { row.push(cur); cur = ""; }
    else if (c === "\n") { row.push(cur); rows.push(row); row = []; cur = ""; }
    else if (c !== "\r") cur += c;
  }
  if (cur.length || row.length) { row.push(cur); rows.push(row); }
  const h = rows.shift();
  return rows.filter((r) => r.length > 1).map((r) => Object.fromEntries(h.map((k, i) => [k, r[i]])));
}

const [corpusFile, out] = process.argv.slice(2);
const corpus = parseCSV(readFileSync(corpusFile, "utf8"));
const lines = [];
for (const ds of [...new Set(corpus.map((r) => r.dataset))]) {
  const rows = corpus.filter((r) => r.dataset === ds).map((r) => ({ study: r.studlab, t1: r.treat2, t2: r.treat1, est: +r.TE, se: +r.seTE }));
  const fits = ["classic", "t-dist"].map((ci) => {
    const a = E.analyse(rows, { randomCi: ci });
    if (!a.ok) return { method_random_ci: ci, ok: false, error: a.error };
    const b = E.analyse(rows, { randomCi: ci, smallValues: "undesirable" });
    const L = (x) => ({ TE: x.TE.flat(), seTE: x.seTE.flat(), lower: x.lower.flat(), upper: x.upper.flat(), pval: x.pval.flat() });
    return { method_random_ci: ci, ok: true, trts: a.treatments, k: a.k, m: a.m, n: a.n, Q: a.Q, df: a.df, pvalQ: a.pvalQ, tau2: a.tau2,
      I2: a.I2, lowerI2: a.lowerI2, upperI2: a.upperI2, common: L(a.common), random: L(a.random),
      predict: a.predict ? { lower: a.predict.lower.flat(), upper: a.predict.upper.flat() } : null, decomp: a.decomp,
      pscoreDesirable: a.pscore, pscoreUndesirable: b.pscore, multiArmStudies: a.multiArmStudies.length };
  });
  lines.push(JSON.stringify({ dataset: ds, fits }));
}
mkdirSync(dirname(out), { recursive: true });
writeFileSync(out, lines.join("\n") + "\n");
console.log(`engine (${process.version}): ${lines.length} datasets -> ${out}; nma-multiarm-v1.js sha256 ${sha(ENGINE).slice(0, 16)}`);
