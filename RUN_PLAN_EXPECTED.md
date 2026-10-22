# v1.1.0 runner expectations

Release date: 2026-10-22. **Final release run passed.** The expected-stage
contract below is unchanged; the observed result is recorded separately below.

The coordinator applied the prepared archive and completed the final release
run. To repeat the run, use the prepared archive root:

    call RUN_PLAN.cmd > ..\run_plan.log 2>&1

Review the exit code as well as the log. Every failed stage stops the plan.
The source clone, original reference scripts and all expected values must stay
unchanged. Do not use analysis/set_expected.py to resolve a failed recut.

## Prerequisites and environment variables

Use the original README/Dockerfile pins: R 4.6.0, netmeta 3.7-0 (R reports
3.7.0), meta 8.5-0 (R reports 8.5.0), Node 24.15.0, Python 3.12 or 3.13, and
requirements.txt. Install missing packages separately using the original
bench/install_r_packages.R and requirements.txt instructions. The plan does not
download or silently change the runner environment. The coordinator explicitly
added --allow-version-mismatch for the release runner; the final log records
every mismatch. The original pins, expectations and tolerances are unchanged.
See RECUT_NOTES.md for actual versions and the complete deviation list.

| Variable | Meaning |
|---|---|
| R_BIN | Optional R binary directory; prepend to PATH when defined. Otherwise Rscript must already be on PATH. |
| PATH | Inherited command search path for Python, Node and Rscript; only R_BIN is optionally prepended. |
| R_HOME | Optional inherited R home; if set, it must match R_BIN. Never assigned a machine path in the plan. |
| R_LIBS_USER, R_LIBS | Inherited R library locations. Preserve the runner's values; R verifies the installed package versions. |
| R_ENVIRON_USER | Set to NUL, as specified by RENV.txt, to prevent a user Renviron overriding the runner. |
| PYTHONUTF8 | Set to 1 for UTF-8 output. |
| PLAYWRIGHT_MODULE | Existing Playwright module directory or entry file, passed to Node require(). If unset, playwright must resolve normally. Browser binaries must already be available. |
| PW_CHANNEL | Optional installed Chromium channel, for example chrome; unset uses Playwright's default Chromium. |

RENV.txt is informational and outside the published tree. Its local R/library
and Playwright paths are deliberately not copied into this plan.

## Expected output for each stage

| RUN_PLAN label | Expected behavior / evidence |
|---|---|
| Enter archive root | cd succeeds, independently of the caller's working directory. |
| Use inherited R binary directory | PATH is updated only when R_BIN is defined. |
| Use inherited libraries; disable user Renviron | Library values remain unchanged; R_ENVIRON_USER=NUL. |
| Use UTF-8 Python console output | PYTHONUTF8=1. |
| Verify before running | 25/25 protected originals, 208/208 app source hashes, 67 webR package hashes/sizes; SOURCE_SHA256 file count is read dynamically. Exit 0. |
| Preserve prior full results and outputs | Each existing results/full and outputs/full moves to the first unused full.prev-N; otherwise a no-previous-output message. No deletion. |
| Original full validation | Corpus: 13 datasets, 364 studies, 506 contrasts. Reference: 26 analyses. Engine: 13 datasets. Expected paper report: 48/48 numbers reproduced: ALL PASS. Exit 0. |
| Report actual original-validation N/N | ORIGINAL VALIDATION: 410/410 checks; 26/26 analyses agree; 2/2 refusals matched. Values are read from the new outputs/full/stats.json and checked against the unchanged expected/paper_values.json. |
| Numerical extras scope | NUMERICAL EXTRAS: N/A. APP.txt states no numerical plus suite for NMA; no plus N/N exists or is claimed. |
| Browser usability smoke | UI SMOKE: 5/5 passed; existing archived R corpus replay 410/410. These five groups are this archive's smoke contract, not a PR #164 count or added numerical validation. |
| Verify after the run | Same protected/source/manifests checks; generated results and outputs are excluded from the release manifest. Exit 0. |
| RUN_PLAN completed successfully | Reached only after all stages return zero. |

The original denominator is 26 fit/refusal checks plus 16 numerical families
for each of the 24 successful analyses: 410. The 48 paper-number expectations
are stored independently in expected/paper_values.json. No new tolerance was
introduced. The browser widget's historical corpus also uses netmeta 3.7-0;
its optional live R mode uses netmeta 3.4-0 and is not the original benchmark.

Port 127.0.0.1:8000 must be free. The Python UI wrapper owns the server and closes
it afterward; it never reuses an unrelated server or kills other browsers.
The browser check does not boot the optional live webR session or exercise
every export format. Those runtime files are byte/hash checked.

After a reviewed documentation-only second-pass edit, regenerate and verify:

    python scripts/recut_integrity.py --write
    python scripts/recut_integrity.py

Keep generated results, outputs, raw logs, temporary directories and every
*.prev-* folder out of the published tree. The redacted final log under
provenance/ is intentional publication evidence and is covered by the release
manifest.

## Observed final release run (2026-10-22)

Source: [redacted final log](provenance/run_plan-2026-10-22-release.log);
runner exit: 0. Earlier attempts are not evidence.

| Measure | Observed |
|---|---|
| Corpus | 13 datasets, 364 studies, 506 contrasts |
| Original validation | 410/410 checks; 26/26 analyses agree; 2/2 refusals matched |
| Paper-number reproduction | 48/48 numbers reproduced: ALL PASS |
| Numerical extras | N/A |
| UI smoke | 5/5 passed; archived R corpus replay 410/410 |
| Protected originals | 25/25 |
| App source hashes | 208/208 |
| webR packages | 67 hashes/sizes verified |
| Release manifest during numerical run | 259/259 files verified before and after |
| Completion | RUN_PLAN completed successfully |

No expected count differs from the final log. The finalization manifest has
additional publication evidence; its new file count is recorded in
RECUT_NOTES.md, without changing the original validation expectations.
