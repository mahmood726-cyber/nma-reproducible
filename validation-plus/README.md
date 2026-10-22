# NMA extras scope for v1.1.0

**No numerical plus validation applies.** APP.txt identifies paper 4, NMA,
netmeta 3.7-0, and PR #164 usability changes that refuse partial networks
without a new numerical validation claim. The supplied nma/validate directory
contains adapter.js, MANIFEST.json, README.md and two corpus JSON files, but
no files or folders named *plus*. Those runtime dependencies are copied
unchanged under app/nma/validate, preserving their relative paths.

Expected numerical extras count: **N/A**. A numerical extras count is
not applicable to this app and is not an unresolved numerical claim.
The original benchmark remains 410/410 expected checks against netmeta 3.7-0.
The browser live-R option uses netmeta 3.4-0, as disclosed by its unchanged
upstream adapter; it is not substituted for the benchmark.

A separate release UI smoke contract checks page loading, deterministic rerun,
whole-network refusal after malformed input, recovery and JSON/CSV exports,
and the existing hash-verified R corpus replay. Its expected five groups
(5/5) are defined by check-ui.mjs; they are not a PR-stated extra-check count.
No generated R references or fabricated research data are included.

From the archive root, with Playwright available via PLAYWRIGHT_MODULE:

    python scripts/recut_run.py ui

The wrapper serves app/ at http://127.0.0.1:8000, runs the browser check, and
closes only its own server/browser. Use RUN_PLAN.cmd to run the original
benchmark and all integrity checks as well. **2026-10-22 release run: UI SMOKE: 5/5 passed; archived R corpus replay 410/410.**
See the [final release log](../provenance/run_plan-2026-10-22-release.log).
The original numerical run passed 410/410 checks; numerical extras remain N/A.
