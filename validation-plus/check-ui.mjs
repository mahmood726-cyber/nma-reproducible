// Release UI smoke contract; not a numerical plus suite or a PR test count.
// Uses the unchanged shipped app and its existing, hash-verified R corpus.
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const expected = JSON.parse(readFileSync(new URL('../expected/paper_values.json', import.meta.url), 'utf8')).values;
const browser = await chromium.launch({ headless: true, ...(process.env.PW_CHANNEL ? { channel: process.env.PW_CHANNEL } : {}) });
let passed = 0;
try {
  const page = await browser.newPage();
  page.setDefaultTimeout(30000);
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('requestfailed', r => errors.push(r.url() + ': ' + r.failure()?.errorText));
  page.on('response', r => { if (r.status() >= 400) errors.push(r.url() + ': HTTP ' + r.status()); });
  await page.goto('http://127.0.0.1:8000/nma/index.html', { waitUntil: 'networkidle' });
  const input = await page.locator('#f-data').inputValue();
  const compute = () => page.evaluate(() => window.__almNmaCompute(document.getElementById('f-data').value, undefined, {}));
  const first = await compute();
  assert.ok(first.analysis && !first.error, 'Default example must produce a network analysis');
  assert.ok((await page.locator('#stats-wrap').innerText()).trim(), 'Summary must be populated');
  assert.deepEqual(errors, []);
  passed++; console.log('UI 1/5: page loads and default example computes');

  await page.locator('#btn-run').click();
  assert.deepEqual(await compute(), first, 'Rerun changes the numerical result');
  passed++; console.log('UI 2/5: default example rerun is identical');

  await page.locator('#f-data').fill(input + '\nMalformedStudy, A, B, oops, 0.1');
  await page.locator('#btn-run').click();
  assert.match((await compute()).error || '', /MalformedStudy|finite number|Row/);
  assert.match(await page.locator('#warn-banner').innerText(), /MalformedStudy/);
  for (const id of ['stats-wrap', 'svg-host', 'sucra-host', 'league-host', 'het-host', 'ref-host'])
    assert.equal((await page.locator('#' + id).innerHTML()).trim(), '', id + ' retains stale results');
  await page.locator('#btn-json').click();
  assert.match(await page.locator('#warn-banner').innerText(), /No valid results to export/);
  passed++; console.log('UI 3/5: malformed contrast refuses the whole network and clears results');

  await page.locator('#f-data').fill(input);
  await page.locator('#btn-run').click();
  assert.deepEqual(await compute(), first);
  for (const [id, filename] of [['btn-json', 'nma-state.json'], ['btn-league', 'nma-league.csv']]) {
    const pending = page.waitForEvent('download');
    await page.locator('#' + id).click();
    const download = await pending;
    assert.equal(download.suggestedFilename(), filename);
    assert.equal(await download.failure(), null);
  }
  passed++; console.log('UI 4/5: valid inputs restore results and both exports');

  const result = await page.evaluate(async () => {
    const adapter = window.AlmNmaValidateAdapter;
    const files = {};
    for (const spec of adapter.corpus.files) {
      const response = await fetch(spec.path);
      if (!response.ok) throw new Error('Corpus HTTP ' + response.status);
      const bytes = await response.arrayBuffer();
      const hash = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)), x => x.toString(16).padStart(2, '0')).join('');
      if (hash !== spec.sha256) throw new Error('Corpus SHA-256 mismatch');
      files[spec.path] = JSON.parse(new TextDecoder().decode(bytes));
    }
    return adapter.corpus.run(files);
  });
  assert.equal(result.checks, expected.checks_total.value);
  assert.equal(result.passed, expected.checks_passed.value);
  assert.equal(result.analyses, expected.analyses.value);
  assert.equal(result.refusals.matched, expected.refusals_matched.value);
  assert.deepEqual(result.failed, []);
  assert.deepEqual(errors, []);
  passed++; console.log('UI 5/5: archived R corpus replay ' + result.passed + '/' + result.checks);
  console.log('UI SMOKE: ' + passed + '/5 passed (separate from numerical extras)');
} finally {
  await browser.close();
}
