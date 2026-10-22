# NMA archive v1.1.0 recut preparation

## Status and application boundary

The coordinator applied the prepared archive and completed RUN_PLAN.cmd on
2026-10-22, with runner exit 0. This finalization reviews that final log and
the generated reports, updates publication metadata, records privacy actions,
and regenerates the archive's own integrity manifest using Python.

The initial preparation had been staged in the sibling prepared-archive
directory after a write denial. That application blocker is historical and
resolved for this task. No source checkout or archive/.git content was changed.
This task does not publish, deploy, or change portfolio/submission status.

## Ingredients and identity

- APP.txt: app=nma, paper 4, reference netmeta 3.7-0; PR #164 usability;
  no numerical plus suite; paper cuts simulated P(best).
- TASK.md supplies allmeta release v1.8.0, commit
  1cb3f8409c7af75ed41f7e1811f9c502f900fc79, release DOI
  10.5281/zenodo.23515177, concept DOI 10.5281/zenodo.20516880.
  The checked-in upstream CITATION.cff also says v1.8.0.
- Original archive README/CHANGELOG identify validated source 6e753c6
  (full commit 6e753c68644834ce4588c4bdf89366452da3159e).
- Current copied shared/build-info.js is unmodified and says v1.8.0 but records
  build commit 42a94da2110a02200d0b5bff4c56f636b9cbffa9. That is not the release
  tag commit. APP_SOURCE.json and release prose explicitly record the supplied
  release-tag identity. No build stamp was rewritten.
- Archive release date 2026-10-22 comes from TASK_finalize2.md, not the upstream release
  date. Creators/authors were compared before and after and are unchanged.
- Existing v1.0.0 archive DOI 10.5281/zenodo.23203451 and all existing related
  identifiers are retained. No v1.1.0 archive DOI was supplied or invented.

## Original build and verification contract

There is no validate.R or original archive file manifest/regenerator.
reproduce.py is the entry point. It checks R 4.6.0, netmeta 3.7.0, meta 8.5.0,
Node 24.15.0 and requirements.txt, then:
1. bench/build_corpus.R constructs contrasts from all 13 netmeta datasets.
2. bench/reference_netmeta.R computes both normal and t-based reference fits.
3. bench/run_engine.mjs invokes app/shared/nma-multiarm-v1.js on those contrasts.
4. analysis/make_outputs.py compares results and builds reports, tables and
   figures against expected/paper_values.json (48 paper-number expectations).
5. analysis/compare_runs.py provides the existing cross-platform comparison;
   a single Windows rerun does not constitute new cross-platform evidence.

The original full-run expectations are 13 datasets, 364 studies, 506 contrasts,
26 analyses, 24 successful fits, two matched Dong2013 refusals and 410/410
checks. They are read from the unchanged expected/paper_values.json:
26 fit/refusal checks plus 16 numerical families for each successful fit.
The original relative/absolute 1e-9 comparisons, 1e-10 and 1e-12 discrepancy
threshold indicators and all expected paper values remain byte-identical.
Quick mode retains its original two datasets/four analyses/eight paper values.

The originally supplied archive contained no results/ or outputs/ corpus/reference files. Those
are generated at runtime from the unchanged R scripts and packages. The new
page's upstream packaged corpus is additional runtime evidence, not a
replacement for the original benchmark. Its own manifest hashes verify;
the available provenance entries for expected/paper_values.json and
analysis/make_outputs.py also match their original source-byte hashes.
The historical results/full provenance files are not present and are not
falsely reported as verified.

## Runtime dependency closure and extras

All 11 pre-existing app files were recopied from matching upstream paths.
Six changed and five were already byte-identical. Every script src and link
href in nma/index.html was parsed, then shared JS/CSS examined for literal
fetch/import paths and computed resources. Added resources include the
analysis-lifecycle and PDF export helpers/vendor, validation widget/runner,
unchanged NMA adapter/manifest/corpus and the computed webR runtime.

webr-runner.js dynamically resolves r-shiny/shinylive/webr, imports webr.mjs,
fetches repo/manifest.json and recursively loads packages. The copied runtime
includes its VFS lazy resources and the 67 packages reachable from netmeta
in that unchanged manifest. Unrelated package archives are not copied;
their records remain in the byte-identical full upstream manifest.
The package closure's SHA-256 values and sizes were verified before copying.
The optional live widget uses netmeta 3.4-0; the archived corpus and original
benchmark use netmeta 3.7-0. No version substitution or tolerance relaxation.

No *plus* source files exist in allmeta/nma/validate. There is therefore no
numerical extras N/N, no R plus generation command and no invented plus corpus.
validation-plus documents N/A and contains a separate five-group UI smoke
contract. Its browser corpus replay checks the original 410-check corpus,
not additional numerical validation. Live webR execution and all PDF/TIFF
export variants are outside that smoke contract; their assets are byte checked.
Links to sibling allmeta apps remain navigation links, not copied application
dependencies.

## Integrity and protected originals

PROTECTED_ORIGINALS.json captures 25 pre-edit hashes covering all bench/ and
analysis/ scripts, reproduce.py, expected values, original environment pins,
docs/numbers.json and screenshot evidence. All 25 match. No line-ending
exception was required; protected files retain their original bytes.
The existing .gitattributes rule (* -text) preserves byte-level checkouts.

APP_SOURCE.json records all 208 app source-file hashes and copy reasons.
scripts/recut_integrity.py verifies protected originals, app inventory, NMA
corpus manifest and netmeta webR package closure. Its --write mode creates
SOURCE_SHA256.json deterministically; ordinary mode verifies the complete
release file set. Generated results, outputs, raw logs, caches, PROGRESS.md,
temporary directories and every *.prev-* backup are excluded. Redacted
provenance logs are included. The manifest is regenerated after finalization.

## Preparation checks and completed release verification

Python preparation QA: 9/9 checks PASS via python -X utf8 _verify_recut.py
from the parent workspace. Covers original-file preservation, upstream byte
equality, creators/version/DOI/date metadata, static dependencies/Python
syntax, run-plan portability/failure stops, hash-tampering rejection, backup
preservation, and application refusal on drift/unsafe paths.

The first QA attempt encountered Python TemporaryDirectory's owner-only
Windows ACL behavior (three test-setup errors); the test harness now uses
ordinary workspace directories and all nine checks pass. Three empty
inaccessible temporary directories remain outside the prepared release:
tmpej8fxgr7, tmps_98szes and tmp05hb1jcz. They are not publication inputs.

The release runner used the coordinator's explicit --allow-version-mismatch
exception. The final log records all deviations below; the protected pins,
expected values, numerical tolerances and corpus were not changed.

Numerical release result: 410/410 checks; 26/26 analyses agree; 2/2 refusals
matched; 48/48 numbers reproduced: ALL PASS. UI release result: 5/5 passed,
with archived R corpus replay 410/410. Numerical extras: N/A.
The final log and generated report agree. Original screenshots/numbers remain
historical v1.0.0 evidence.

## Static versus dynamic disclosure

| Item | Static or dynamic | Evidence / treatment |
|---|---|---|
| Release version/date/commit/DOIs | Static supplied identity | TASK_finalize2.md, TASK.md, APP.txt and local metadata; no invented DOI |
| Original expectations/tolerances | Static protected contract | Original expected JSON, R/analysis scripts and pre-edit hashes |
| Copied runtime and packaged corpus | Static source evidence | Exact upstream bytes and manifest hashes |
| File inventory and SHA-256 | Derived during preparation | Python byte reads; no cached or simulated values |
| Numerical results and N/N | Dynamic, observed | Final release log cross-checked against outputs/full/stats.json and reproduction_report.md |
| UI smoke outcome | Dynamic, observed | Final release log: 5/5 passed; no PR-count attribution |
| Historical screenshots/numbers | Static prior-run evidence | Unchanged original bytes; not a new release run |

## Remaining placeholders and unknowns

- All release-result statements are filled from the final 2026-10-22 log.
- New archive v1.1.0 DOI is unassigned. Prior-release DOI remains correctly
  labeled; CITATION.cff does not assign the old DOI to the new version.
- Numerical extras are explicitly N/A, not an unknown result.
- Inherited docs/paper.md editorial placeholders remain: ORCID/corresponding
  email, affiliation, competing-interest confirmation, grant information,
  acknowledgements. No authorship or personal details were fabricated.
- The copied upstream adapter's paper DOI is null and its run link is generic
  Actions, as in its README; upstream code remains byte-identical.
- Release-tag identity was supplied by TASK.md, not re-resolved with Git.
- Final external R/Node/browser results are recorded below; previous failed
  attempts are excluded from release evidence.

## Complete release-file change inventory

Paths below are relative to archive after human-side application.

Added: 207; changed: 12; removed: 0.

| Status | Path | Why |
|---|---|---|
| Changed | .gitignore | Exclude recovery progress and every *.prev-* backup folder. |
| Changed | .zenodo.json | Version/date, completed-result description, preserved creators/old relations, new allmeta release and prior archive links. |
| Changed | CHANGELOG.md | v1.1.0 entry and explicit historical v1.0.0 section. |
| Changed | CITATION.cff | Version 1.1.0/date 2026-10-22; preserve authors and prior DOI, add allmeta v1.8.0; avoid labeling old DOI as new release. |
| Changed | README.md | What's new, current source, portable rerun, historical versus reproduced results, no numerical extras. |
| Changed | app/hub/app-style.css | existing archived app file |
| Changed | app/nma/index.html | existing archived app file |
| Changed | app/shared/build-info.js | existing archived app file |
| Changed | app/shared/forced-colors.css | existing archived app file |
| Changed | app/shared/ma-comparisons-v1.js | existing archived app file |
| Changed | app/shared/nma-multiarm-v1.js | existing archived app file |
| Changed | docs/paper.md | Identify completed recut and historical results; remove simulated P(best) from the paper figure claim; resolve known old archive DOI. |
| Added | APP_SOURCE.json | Exact per-file upstream hashes, dependency reasons, release identity and upstream build-stamp discrepancy. |
| Added | PROTECTED_ORIGINALS.json | Hashes captured before edits; original validation/scripts/expectations and historical generated evidence. |
| Added | RECUT_NOTES.md | Preparation evidence, provenance, blockers, placeholders and complete file inventory. |
| Added | RUN_PLAN.cmd | Portable fail-closed validation, backup rotation, count reporting, UI smoke and integrity checks. |
| Added | RUN_PLAN_EXPECTED.md | Source-backed expected counts, variables, prerequisites and second-pass interpretation. |
| Added | SOURCE_SHA256.json | Complete deterministic release-file manifest, excluding generated output and itself. |
| Added | app/hub/shared/analysis-lifecycle.js | runtime dependency of nma/index.html |
| Added | app/hub/shared/plot-export.js | runtime dependency of nma/index.html |
| Added | app/hub/shared/vendor/jspdf.min.js | plot-export.js new URL('vendor/jspdf.min.js', script.src) |
| Added | app/nma/validate/MANIFEST.json | validation adapter and its unchanged manifest/corpus/provenance |
| Added | app/nma/validate/README.md | validation adapter and its unchanged manifest/corpus/provenance |
| Added | app/nma/validate/adapter.js | runtime dependency of nma/index.html |
| Added | app/nma/validate/corpus/paper-values.json | validation adapter and its unchanged manifest/corpus/provenance |
| Added | app/nma/validate/corpus/reference.json | validation adapter and its unchanged manifest/corpus/provenance |
| Added | app/r-shiny/shinylive/webr/R.js | webR runtime and source maps loaded from computed base URL |
| Added | app/r-shiny/shinylive/webr/R.wasm | webR runtime and source maps loaded from computed base URL |
| Added | app/r-shiny/shinylive/webr/libRblas.so | webR runtime and source maps loaded from computed base URL |
| Added | app/r-shiny/shinylive/webr/libRlapack.so | webR runtime and source maps loaded from computed base URL |
| Added | app/r-shiny/shinylive/webr/library.data.gz | webR runtime and source maps loaded from computed base URL |
| Added | app/r-shiny/shinylive/webr/library.js.metadata | webR runtime and source maps loaded from computed base URL |
| Added | app/r-shiny/shinylive/webr/packages/MASS/MASS_7.3-65.tgz | webR netmeta dependency: MASS |
| Added | app/r-shiny/shinylive/webr/packages/Matrix/Matrix_1.7-5.tgz | webR netmeta dependency: Matrix |
| Added | app/r-shiny/shinylive/webr/packages/RColorBrewer/RColorBrewer_1.1-3.tgz | webR netmeta dependency: RColorBrewer |
| Added | app/r-shiny/shinylive/webr/packages/S7/S7_0.2.2.tgz | webR netmeta dependency: S7 |
| Added | app/r-shiny/shinylive/webr/packages/bit/bit_4.6.0.tgz | webR netmeta dependency: bit |
| Added | app/r-shiny/shinylive/webr/packages/bit64/bit64_4.8.0.tgz | webR netmeta dependency: bit64 |
| Added | app/r-shiny/shinylive/webr/packages/boot/boot_1.3-32.tgz | webR netmeta dependency: boot |
| Added | app/r-shiny/shinylive/webr/packages/clipr/clipr_0.8.0.tgz | webR netmeta dependency: clipr |
| Added | app/r-shiny/shinylive/webr/packages/crayon/crayon_1.5.3.tgz | webR netmeta dependency: crayon |
| Added | app/r-shiny/shinylive/webr/packages/dplyr/dplyr_1.1.4.tgz | webR netmeta dependency: dplyr |
| Added | app/r-shiny/shinylive/webr/packages/farver/farver_2.1.2.tgz | webR netmeta dependency: farver |
| Added | app/r-shiny/shinylive/webr/packages/generics/generics_0.1.4.tgz | webR netmeta dependency: generics |
| Added | app/r-shiny/shinylive/webr/packages/ggplot2/ggplot2_4.0.3.tgz | webR netmeta dependency: ggplot2 |
| Added | app/r-shiny/shinylive/webr/packages/gtable/gtable_0.3.6.tgz | webR netmeta dependency: gtable |
| Added | app/r-shiny/shinylive/webr/packages/hms/hms_1.1.4.tgz | webR netmeta dependency: hms |
| Added | app/r-shiny/shinylive/webr/packages/isoband/isoband_0.3.0.tgz | webR netmeta dependency: isoband |
| Added | app/r-shiny/shinylive/webr/packages/labeling/labeling_0.4.3.tgz | webR netmeta dependency: labeling |
| Added | app/r-shiny/shinylive/webr/packages/lattice/lattice_0.22-9.tgz | webR netmeta dependency: lattice |
| Added | app/r-shiny/shinylive/webr/packages/mathjaxr/mathjaxr_2.0-0.tgz | webR netmeta dependency: mathjaxr |
| Added | app/r-shiny/shinylive/webr/packages/metadat/metadat_1.4-0.tgz | webR netmeta dependency: metadat |
| Added | app/r-shiny/shinylive/webr/packages/metafor/metafor_4.8-0.tgz | webR netmeta dependency: metafor |
| Added | app/r-shiny/shinylive/webr/packages/mvtnorm/mvtnorm_1.2-4.tgz | webR netmeta dependency: mvtnorm |
| Added | app/r-shiny/shinylive/webr/packages/nlme/nlme_3.1-169.tgz | webR netmeta dependency: nlme |
| Added | app/r-shiny/shinylive/webr/packages/numDeriv/numDeriv_2016.8-1.1.tgz | webR netmeta dependency: numDeriv |
| Added | app/r-shiny/shinylive/webr/packages/pbapply/pbapply_1.7-4.tgz | webR netmeta dependency: pbapply |
| Added | app/r-shiny/shinylive/webr/packages/pillar/pillar_1.11.1.tgz | webR netmeta dependency: pillar |
| Added | app/r-shiny/shinylive/webr/packages/pkgconfig/pkgconfig_2.0.3.tgz | webR netmeta dependency: pkgconfig |
| Added | app/r-shiny/shinylive/webr/packages/purrr/purrr_1.2.2.tgz | webR netmeta dependency: purrr |
| Added | app/r-shiny/shinylive/webr/packages/readr/readr_2.2.0.tgz | webR netmeta dependency: readr |
| Added | app/r-shiny/shinylive/webr/packages/scales/scales_1.4.0.tgz | webR netmeta dependency: scales |
| Added | app/r-shiny/shinylive/webr/packages/stringi/stringi_1.8.7.tgz | webR netmeta dependency: stringi |
| Added | app/r-shiny/shinylive/webr/packages/stringr/stringr_1.6.0.tgz | webR netmeta dependency: stringr |
| Added | app/r-shiny/shinylive/webr/packages/tibble/tibble_3.3.1.tgz | webR netmeta dependency: tibble |
| Added | app/r-shiny/shinylive/webr/packages/tidyselect/tidyselect_1.2.1.tgz | webR netmeta dependency: tidyselect |
| Added | app/r-shiny/shinylive/webr/packages/tzdb/tzdb_0.5.0.tgz | webR netmeta dependency: tzdb |
| Added | app/r-shiny/shinylive/webr/packages/utf8/utf8_1.2.6.tgz | webR netmeta dependency: utf8 |
| Added | app/r-shiny/shinylive/webr/packages/vctrs/vctrs_0.6.5.tgz | webR netmeta dependency: vctrs |
| Added | app/r-shiny/shinylive/webr/packages/viridisLite/viridisLite_0.4.3.tgz | webR netmeta dependency: viridisLite |
| Added | app/r-shiny/shinylive/webr/packages/vroom/vroom_1.6.5.9000.tgz | webR netmeta dependency: vroom |
| Added | app/r-shiny/shinylive/webr/packages/xml2/xml2_1.5.2.tgz | webR netmeta dependency: xml2 |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/CompQuadForm_1.4.4.tgz | webR netmeta dependency: CompQuadForm |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/R6_2.6.1.tgz | webR netmeta dependency: R6 |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/RcppEigen_0.3.4.0.2.tgz | webR netmeta dependency: RcppEigen |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/Rcpp_1.1.1-1.1.tgz | webR netmeta dependency: Rcpp |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/Rdpack_2.6.6.tgz | webR netmeta dependency: Rdpack |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/abind_1.4-8.tgz | webR netmeta dependency: abind |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/cli_3.6.6.tgz | webR netmeta dependency: cli |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/colorspace_2.1-2.tgz | webR netmeta dependency: colorspace |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/cpp11_0.5.4.tgz | webR netmeta dependency: cpp11 |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/digest_0.6.39.tgz | webR netmeta dependency: digest |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/glue_1.8.1.tgz | webR netmeta dependency: glue |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/igraph_2.1.4.tgz | webR netmeta dependency: igraph |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/lifecycle_1.0.5.tgz | webR netmeta dependency: lifecycle |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/lme4_2.0-1.tgz | webR netmeta dependency: lme4 |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/magic_1.6-1.tgz | webR netmeta dependency: magic |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/magrittr_2.0.5.tgz | webR netmeta dependency: magrittr |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/meta_8.3-0.tgz | webR netmeta dependency: meta |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/metabook_0.2-0.tgz | webR netmeta dependency: metabook |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/minqa_1.2.8.tgz | webR netmeta dependency: minqa |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/netmeta_3.4-0.tgz | webR netmeta dependency: netmeta |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/nloptr_2.2.1.9000.tgz | webR netmeta dependency: nloptr |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/prettyunits_1.2.0.tgz | webR netmeta dependency: prettyunits |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/progress_1.2.3.tgz | webR netmeta dependency: progress |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/rbibutils_2.4.1.tgz | webR netmeta dependency: rbibutils |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/reformulas_0.4.4.tgz | webR netmeta dependency: reformulas |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/rlang_1.2.0.tgz | webR netmeta dependency: rlang |
| Added | app/r-shiny/shinylive/webr/repo/bin/emscripten/contrib/4.5/withr_3.0.2.tgz | webR netmeta dependency: withr |
| Added | app/r-shiny/shinylive/webr/repo/manifest.json | webr-runner.js package manifest fetch |
| Added | app/r-shiny/shinylive/webr/vfs/etc/fonts/fonts.conf | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/etc/ssl/cert.pem | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/doc.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/doc.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/demo.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/demo.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/help.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/help.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/html.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/base/html.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/compiler/help.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/compiler/help.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/compiler/html.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/compiler/html.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/datasets/help.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/datasets/help.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/datasets/html.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/datasets/html.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/afm.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/afm.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/demo.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/demo.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/enc.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/enc.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/fonts.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/fonts.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/help.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/help.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/html.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/html.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/libs.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grDevices/libs.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/demo.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/demo.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/help.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/help.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/html.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/graphics/html.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/doc.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/doc.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/help.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/help.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/html.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/grid/html.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/help.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/help.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/html.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/methods/html.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/parallel.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/parallel.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/help.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/help.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/html.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/splines/html.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/demo.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/demo.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/doc.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/doc.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/help.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/help.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/html.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats/html.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/help.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/help.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/html.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/stats4/html.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tcltk.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tcltk.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/help.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/help.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/html.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/tools/html.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/translations/DESCRIPTION | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/doc.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/doc.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/help.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/help.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/html.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/html.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/misc.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/utils/misc.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/webr/help.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/webr/help.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/webr/html.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/library/webr/html.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/share.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/lib/R/share.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Bold.ttf | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-BoldItalic.ttf | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Italic.ttf | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSans-Regular.ttf | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSansMono-Bold.ttf | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSansMono-Regular.ttf | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Bold.ttf | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-BoldItalic.ttf | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Italic.ttf | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/fonts/NotoSerif-Regular.ttf | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/gdal.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/gdal.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/proj.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/proj.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/udunits.data.gz | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/usr/share/udunits.js.metadata | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/var/cache/fontconfig/3830d5c3ddfd5cd38a049b759396e72e-le32d8.cache-9 | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/vfs/var/cache/fontconfig/CACHEDIR.TAG | webR virtual filesystem lazy assets |
| Added | app/r-shiny/shinylive/webr/webr-worker.js | webR runtime and source maps loaded from computed base URL |
| Added | app/r-shiny/shinylive/webr/webr-worker.js.map | webR runtime and source maps loaded from computed base URL |
| Added | app/r-shiny/shinylive/webr/webr.cjs | webR runtime and source maps loaded from computed base URL |
| Added | app/r-shiny/shinylive/webr/webr.cjs.map | webR runtime and source maps loaded from computed base URL |
| Added | app/r-shiny/shinylive/webr/webr.mjs | webR runtime and source maps loaded from computed base URL |
| Added | app/r-shiny/shinylive/webr/webr.mjs.map | webR runtime and source maps loaded from computed base URL |
| Added | app/shared/alm-validate.js | runtime dependency of nma/index.html |
| Added | app/shared/webr-runner.js | runtime dependency of nma/index.html |
| Added | scripts/recut_integrity.py | Python-only source, corpus, package, protected-original and release manifest generation/verification. |
| Added | scripts/recut_run.py | Non-destructive backup rotation, actual-count reporting and owned loopback UI server. |
| Added | validation-plus/README.md | Document NMA's no-numerical-extras scope and the separate UI contract. |
| Added | validation-plus/check-ui.mjs | Five browser smoke groups using real default input and existing R corpus, with no new numerical reference values. |

No files were removed. Existing unchanged files, including protected originals, are retained.


## Tool-version deviation (coordinator, 2026-10-22)
The release run calls `reproduce.py --allow-version-mismatch` (1 line(s) of RUN_PLAN.cmd), as P3 dta-sroc v1.1.0 did: the runner has node 24.16.0 (pinned 24.15.0), contourpy 1.3.3 (1.4.0), fonttools 4.63.0 (4.66.1), kiwisolver 1.5.0 (1.5.1), numpy 2.4.6 (2.4.4), packaging 26.2 (26.3), pillow 12.2.0 (pinned 12.3.0) and pyparsing 3.3.2 (pinned 3.3.3). The pins are unchanged and the mismatch is printed in the run log; numerical checks, tolerances and expected values are unchanged.

## Finalize (2026-10-22)

Evidence is the final ../run_plan.log and RUN_EXIT 0 in ../run_plan.exit,
archived as [provenance/run_plan-2026-10-22-release.log](provenance/run_plan-2026-10-22-release.log).
Earlier attempts are not evidence. The provenance copy preserves every byte
except the two runner-profile path prefixes, replaced with <LOCAL>.
No runtime was rerun during this Python-only finalization.

Exact final runner results:

    48/48 numbers reproduced: ALL PASS
    corpus: 13 datasets, 364 studies, 506 contrasts (netmeta 3.7.0)
    ORIGINAL VALIDATION: 410/410 checks; 26/26 analyses agree; 2/2 refusals matched
    NUMERICAL EXTRAS: N/A (APP.txt: no numerical plus suite for NMA; no extra N/N claimed)
    UI 5/5: archived R corpus replay 410/410
    UI SMOKE: 5/5 passed (separate from numerical extras)
    INPUT INTEGRITY: 25/25 protected originals; 208/208 app source hashes; 67 webR package hashes/sizes verified
    RELEASE MANIFEST: 259/259 files verified
    === RUN_PLAN completed successfully

Expected-count differences: none. All 48 logged expected/reproduced rows
report PASS; the rounding differences in worked-example values are handled
by the unchanged original tolerances. The finalization file count increases
only because publication evidence is added. The corpus, R references,
expected values and tolerances remain unchanged.

Actual environment (copied from the final log):

    environment: R 4.6.0 (netmeta 3.7.0, meta 8.5.0), Node 24.16.0, Python 3.13.13, Windows AMD64

All logged tool-version deviations:

| Tool | Actual | Pinned |
|---|---|---|
| node | 24.16.0 | 24.15.0 |
| contourpy | 1.3.3 | 1.4.0 |
| fonttools | 4.63.0 | 4.66.1 |
| kiwisolver | 1.5.0 | 1.5.1 |
| numpy | 2.4.6 | 2.4.4 |
| packaging | 26.2 | 26.3 |
| pillow | 12.2.0 | 12.3.0 |
| pyparsing | 3.3.2 | 3.3.3 |

The coordinator's --allow-version-mismatch change is retained and disclosed.
This is one Windows run; historical cross-platform claims are not promoted
to new cross-platform evidence. Archive release date is 2026-10-22; the
allmeta v1.8.0 date and all v1.0.0 dates remain unchanged.

Publication privacy actions and every detected occurrence are listed in
[provenance/publication-scan-2026-10-22.json](provenance/publication-scan-2026-10-22.json).
Upstream matches are listed without rewriting any copied source file.
Public author/repository attribution and functional generic identifiers are
retained explicitly; local runner profile information is redacted.

Finalization changes: release dates/results in README.md, CITATION.cff,
.zenodo.json, CHANGELOG.md, RUN_PLAN_EXPECTED.md, RECUT_NOTES.md, docs/paper.md
and validation-plus/README.md; publication exclusions in .gitignore;
provenance-log/temporary-directory handling in scripts/recut_integrity.py;
the redacted log, privacy inventory and regenerated SOURCE_SHA256.json.
The original preparation change inventory above is historical.

Publication scan: 262 publishable files, including binaries and decompressed
gzip/tgz streams. The inventory records 8826 overlapping pattern matches
across 134 files; 121 matching files are exact upstream copies and remain
unchanged. Each hit has a rule, file, stream, line, byte offset, action and
reason. Raw bytes and the first gzip layer were scanned; nested formats inside
those streams were not recursively unpacked. No credential was identified
among the scanned token-prefix matches: the PEM hits are public certificates
and a license separator; the other prefixes are code, text or binary
substrings. Public author/repository attribution and the standard CI bot
address remain functional attribution, not private runner information.
No backup or temporary file is included in the publishable inventory.

Python integrity regeneration and verification (from archive root), exit 0:

    python -X utf8 scripts/recut_integrity.py --write
    INPUT INTEGRITY: 25/25 protected originals; 208/208 app source hashes; 67 webR package hashes/sizes verified
    WROTE SOURCE_SHA256.json: 261 files

    python -X utf8 scripts/recut_integrity.py
    INPUT INTEGRITY: 25/25 protected originals; 208/208 app source hashes; 67 webR package hashes/sizes verified
    RELEASE MANIFEST: 261/261 files verified

The 261 hashed files plus SOURCE_SHA256.json itself are the 262 publishable
files. Compared with the runner's 259-file manifest, the two additions are
the redacted final release log and this finalization's privacy inventory.

Independent Python finalization review (parent-workspace helper; exit 0):

    python -X utf8 _finalize2_verify.py
    FINALIZATION REVIEW: 8/8 checks passed

The review cross-checks all 48 logged rows against the original expectations,
generated report and statistics; verifies exact log redaction; compares all
208 copied files with the supplied allmeta bytes and all 25 protected hashes;
checks dates, identities, preserved authors/DOIs, all eight tool deviations,
publication/manifest coverage, scan locations and local documentation/assets.
The earlier integrity-selection check also passed for provenance inclusion,
raw-log exclusion and temporary-folder exclusion.
