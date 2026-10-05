# nma-reproducible

[![reproduce](https://github.com/mahmood726-cyber/nma-reproducible/actions/workflows/reproduce.yml/badge.svg)](https://github.com/mahmood726-cyber/nma-reproducible/actions/workflows/reproduce.yml)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/mahmood726-cyber/nma-reproducible?quickstart=1)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Latest verified run](https://img.shields.io/badge/latest%20verified%20run-results%20page-2c5e8a)](https://mahmood726-cyber.github.io/nma-reproducible/)

The [allmeta](https://github.com/mahmood726-cyber/allmeta) **NMA app** runs frequentist network meta-analysis offline in the browser
([live](https://mahmood726-cyber.github.io/allmeta/nma/)), as the R package netmeta does. It offers:

- **Models:** common effect, or random effects with netmeta's generalised DerSimonian–Laird τ²; multi-arm studies handled through their correlated contrasts. Studies with an incomplete, duplicated or internally inconsistent set of comparisons are refused, as in netmeta.
- **Intervals:** 95% confidence intervals from the normal or the t distribution (random effects); prediction intervals.
- **Outputs:** league table (row versus column, estimates with CIs and p-values), estimates against a reference treatment, Q, τ², I² with its CI, the design-based decomposition of Q into within-design heterogeneity and between-design inconsistency, P-scores in either direction of benefit, the network graph, and CSV and JSON export. netmeta's datasets are built in as examples.

This repository validates the app against **netmeta** on every dataset netmeta ships, and checks every number in the accompanying F1000Research article.

## Reproduce in one click

**1. See the latest verified run (nothing to run).** The [results page](https://mahmood726-cyber.github.io/nma-reproducible/) is republished by CI after every push to `main`: the PASS/FAIL table for every number in the paper, the result on Docker, Linux, Windows and macOS, the cross-platform comparison, and the figures.

**2. Open in GitHub Codespaces (one click).** Click the *Open in GitHub Codespaces* badge above, then *Create codespace*.
- The pinned environment is built from this repository's `Dockerfile`: R 4.6.0, the dated package snapshot, Node 24.15.0 and Python.
- The quick reproduction (2 datasets) then runs automatically. Its log ends with `QUICK RUN: ALL PASS`; the report is in `outputs/quick/reproduction_report.md`.
- For the full run, type `python reproduce.py` in the terminal (a few minutes; writes `outputs/full/`).

Limits: you need to be signed in to GitHub; the codespace uses your own Codespaces allowance (personal accounts get a free monthly quota; this uses a 2-core machine); the first build takes several minutes, mostly installing R packages. `codespaces-check` in Actions builds the same devcontainer and runs its automatic quick run on every relevant change.

**3. Re-run the CI yourself (one click in a fork).** Only maintainers can trigger workflows here, so use your own copy:
1. Click **Fork**.
2. In your fork, open the **Actions** tab and click *I understand my workflows, go ahead and enable them*.
3. Choose **reproduce**, then **Run workflow** (branch `main`).

The run is the full validation on Docker, Linux, Windows and macOS. Each job's **summary** shows its PASS/FAIL report; **Artifacts** hold `reproduction-report-<platform>` and the complete outputs (`full-<platform>`); the *compare* job shows the cross-platform check. Publishing to Pages happens only on this repository.

**On your own machine:**

```bash
git clone https://github.com/mahmood726-cyber/nma-reproducible && cd nma-reproducible
docker build -t nma . && docker run --rm -v "$PWD/outputs:/work/outputs" nma        # canonical
```

Without Docker you need R 4.6.0, Node 24.15.0 and Python 3.12 or 3.13:
1. `Rscript bench/install_r_packages.R`
2. `python -m pip install -r requirements.txt`
3. `python reproduce.py` (or `--quick`)

`make setup` and `make reproduce` do the same. **To use the app**, open `app/nma/index.html` in a browser.

## What it shows

The app is validated at **allmeta commit `6e753c6`** (the merge of [allmeta PR #78](https://github.com/mahmood726-cyber/allmeta/pull/78)). `app/` is byte-identical to that commit.

| | Result |
|---|---|
| All 13 netmeta datasets (364 studies, 506 contrasts, 52 multi-arm studies; 3–22 treatments) × normal and t-based random-effects CIs = 26 analyses | All 26 agree with netmeta: 24 within 10⁻⁹ and the same 2 refusals (Dong2013: a three-arm study has an undefined comparison). 410/410 checks pass. |
| Largest differences | Estimates, SEs, CIs and prediction intervals below 10⁻¹²; every reported quantity below 10⁻¹⁰. |
| Worked example: smoking cessation (24 studies, 2 three-arm) | τ² 0.60, I² 88.6% (84.4% to 91.7%); between-design inconsistency Q 15.2 (7 df, p = 0.03). Group counselling vs no intervention: OR 2.47 (1.10 to 5.52), prediction interval 0.40 to 15.11; highest P-score (0.84). |

Earlier versions of the app had known issues, found by this validation and fixed in allmeta PR #78; see [CHANGELOG.md](CHANGELOG.md).

Tolerances follow allmeta's own parity test (`hub/shared/tests/_nma_parity_check.mjs`, mirrored in `analysis/make_outputs.py`). netmeta's common-effect and DerSimonian–Laird analyses are closed form and the engine evaluates the same formulas, so every quantity must agree within 10⁻⁹: relative (max(1, |value|)) for estimates, SEs, CIs, prediction intervals, Q, τ² and the decomposition of Q; absolute for p-values, I² and its CI, and P-scores. Degrees of freedom must agree within 10⁻⁹ (netmeta computes them in floating point: on ARM they can differ from an integer in the last bit) and refusals must match. Treatments are matched by name (R and JavaScript sort names differently).

netmeta's REML and ML estimators of τ², node-splitting (`netsplit`, in a separate allmeta app) and arm-level input are not part of this comparison.

## Layout

| Path | Contents |
|---|---|
| `app/` | The app, byte-identical to allmeta commit `6e753c6` |
| `bench/build_corpus.R` | Builds the contrasts of the 13 datasets with netmeta's `pairwise()` |
| `bench/reference_netmeta.R` | netmeta reference analyses |
| `bench/run_engine.mjs` | Runs the app's JavaScript engine on the same contrasts |
| `analysis/make_outputs.py` | Tables, figures, statistics, PASS/FAIL |
| `analysis/compare_runs.py` | Cross-platform comparison |
| `expected/` | Every number as printed in the paper |
| `docs/` | Paper, `numbers.json`, Figure 1 screenshots and their capture script |
| `ci/build_site.py` | Builds the live results page from a CI run (reads outputs only) |
| `.devcontainer/` | Codespaces / dev-container definition; runs the quick reproduction on creation |

## Outputs and how they map to the paper

`python reproduce.py` writes to `outputs/full/`:

| File | Paper |
|---|---|
| `docs/screenshots/step1.png` … `step6.png` | Figure 1: using the app, step by step (`captions.md`) |
| `figure2_worked_example.png` (+ `.csv`) | Figure 2: smoking cessation, estimates and P-scores |
| `figure3_agreement.png` (+ `.csv`) | Figure 3: agreement by dataset and quantity |
| `table1_by_dataset.csv` | Table 1: agreement by dataset |
| `table2_by_quantity.csv` | Table 2: largest difference by quantity |
| `table3_all_analyses.csv` | Every analysis and every check (extended data) |
| `visual_abstract.png` | Visual abstract |
| `stats.json` | Every number quoted in the text |
| `reproduction_report.md` | Expected versus reproduced, PASS/FAIL per number |

## Environment and determinism

- **R 4.6.0.** The image is `rocker/r-ver:4.6.0`. netmeta 3.7-0, meta 8.5-0 and their dependencies come from the Posit Package Manager snapshot of 2026-10-01.
- **Node 24.15.0** (`.nvmrc`) runs the app's JavaScript engine. There are no npm dependencies.
- **Python** builds the tables and figures (numpy and matplotlib, pinned in `requirements.txt`).
- **Docker is the canonical environment.** CI runs the full validation on every push on Linux, Windows, macOS and Docker. `analysis/compare_runs.py` then requires the corpus and the engine's output to be bit-identical across the x86-64 runs; macOS on ARM is reported but not required to match (V8 there can differ in the last bit).
- **R's own values** differ between operating systems in the last bits. The printed numbers are chosen to be robust to this (discrepancy maxima enter only as threshold indicators), and are checked on every platform.

Run time: a few minutes, almost all of it netmeta itself.

## Data

`bench/build_corpus.R` builds the corpus at run time from the 13 datasets shipped with netmeta (GPL-2 | GPL-3), which documents each original source. parkinson is identical to Franchini2012 and is kept because netmeta ships both. The app's example list (`app/nma/example-datasets.js`, generated by `_make_examples.R` in allmeta) carries the same contrasts for 11 of them (without parkinson and Dong2013).

## Cite

Ahmad M. Network meta-analysis in the browser: a tool validated against the R package netmeta [software], v1.0.0. Zenodo; 2026. (DOI to be added on release.) Machine-readable metadata: `CITATION.cff`.

## Licence

MIT, the same as allmeta.
