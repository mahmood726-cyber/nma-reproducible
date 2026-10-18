'use strict';
// Synthetic data only; checks the real repository statistical engine.
const test = require('node:test');
const assert = require('node:assert/strict');
const engine = require('../app/shared/nma-multiarm-v1.js');

const rows = () => [
  { study: 'Trial-1', t1: 'A', t2: 'B', est: 0.2, se: 0.2 },
  { study: 'Trial-2', t1: 'B', t2: 'C', est: 0.3, se: 0.25 },
  { study: 'Trial-3', t1: 'A', t2: 'C', est: 0.5, se: 0.2 },
];

const wrong = [
  ['NaN estimate', 'est', NaN],
  ['positive infinity estimate', 'est', Infinity],
  ['negative infinity estimate', 'est', -Infinity],
  ['NaN standard error', 'se', NaN],
  ['infinite standard error', 'se', Infinity],
  ['negative standard error', 'se', -0.2],
  ['zero standard error', 'se', 0],
  ['underflowed variance', 'se', 1e-250],
  ['overflowed variance', 'se', 1e250],
  ['string estimate', 'est', '0.2'],
  ['null standard error', 'se', null],
];
for (const [name, key, value] of wrong) {
  test('fail-closed ' + name, () => {
    const bad = rows();
    bad[0][key] = value;
    for (const run of [
      () => engine.fit(bad, { model: 'fe' }),
      () => engine.analyse(bad, {}),
    ]) {
      const actual = run();
      assert.equal(actual.ok, false);
      assert.match(actual.error, /contrast row 1:.*finite numbers.*positive finite variance/);
    }
  });
}

test('invalid second row is named and not discarded', () => {
  const bad = rows();
  bad[1].se = NaN;
  const actual = engine.analyse(bad, {});
  assert.equal(actual.ok, false);
  assert.match(actual.error, /contrast row 2/);
});

test('malformed row fails closed rather than throwing', () => {
  const bad = rows();
  bad[0] = null;
  const actual = engine.fit(bad, {});
  assert.equal(actual.ok, false);
  assert.match(actual.error, /contrast row 1/);
});

test('finite three-treatment network retains contrasts and rankings', () => {
  const a = engine.analyse(rows(), {});
  assert.equal(a.ok, true, a.error);
  assert.deepEqual(a.treatments, ['A', 'B', 'C']);
  const near = (x, y) => assert.ok(Math.abs(x - y) < 1e-10, x + ' != ' + y);
  near(a.common.TE[0][1], -0.2);
  near(a.common.TE[1][2], -0.3);
  near(a.common.TE[0][2], -0.5);
  assert.ok(a.pscore.common.every(x => Number.isFinite(x) && x >= 0 && x <= 1));
});

test('deterministic synthetic networks retain finite estimates and rankings', () => {
  let seed = 92301;
  const rand = () => {
    seed = (Math.imul(1664525, seed) + 1013904223) >>> 0;
    return seed / 4294967296;
  };
  for (let k = 0; k < 200; k++) {
    const e1 = (rand() - 0.5) * 1.4;
    const e2 = (rand() - 0.5) * 1.4;
    const input = rows().map((r, i) => ({
      ...r,
      est: i === 0 ? e1 : i === 1 ? e2 : e1 + e2,
      se: 0.11 + 0.26 * rand(),
    }));
    const out = engine.analyse(input, {});
    assert.equal(out.ok, true, out.error);
    assert.ok(out.pscore.common.every(Number.isFinite));
    assert.ok(out.pscore.random.every(Number.isFinite));
  }
});
