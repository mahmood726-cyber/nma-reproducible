# Changelog

## Validated version

This repository validates the allmeta NMA app at **allmeta commit `6e753c68644834ce4588c4bdf89366452da3159e`**, the merge of
[allmeta PR #78](https://github.com/mahmood726-cyber/allmeta/pull/78). `app/` is byte-identical to that commit.

## Earlier versions of the app (history)

Versions of the app before PR #78 had known issues. All were found by this repository's first validation run, against allmeta `76d3e9d`, and fixed in PR #78. The core estimates (common and DerSimonian–Laird random effects, with multi-arm studies) already matched netmeta to about 10⁻¹⁴.

| Issue | Before PR #78 | Since PR #78 |
|---|---|---|
| Incomplete multi-arm study | Dropped from the network, with a note, and the rest fitted (Dong2013, study 33: two arms without deaths, so one comparison is undefined). netmeta refuses the network. Duplicated comparisons were silently ignored and inconsistent multi-arm estimates not checked. | Refused and named, as netmeta's checks: incomplete or duplicated comparisons, inconsistent effects (tolerance 0.001), negative implied arm variances. |
| League table | Headed "rows vs columns" but each cell was column minus row (also in the CSV export). | Row versus column, as the heading and netmeta. |
| Ranking | Simulated SUCRA, assuming smaller effects are better, with no way to change the direction. | P-scores as netmeta's `netrank` (closed form), in the direction the user chooses; the simulated probability of ranking first kept alongside (fixed seed). |
| Greek label | "τ²" uppercased to capital tau (reads as "T²"). | Labels shown as written. |
| Network graph | The reference treatment was not highlighted when the reference changed; small labels; labels of crossing edges overlapped. | Highlighted from the reference used; larger labels placed off the crossing point. |
| Missing outputs | No p-values, t-based CIs, prediction intervals, p-value of Q, I² CI or decomposition of Q. | All reported, as netmeta. |

PR #78 also adds netmeta's datasets as examples and a parity test over the full grid used here (`hub/shared/tests/nma-netmeta-parity.spec.mjs`).

## This repository

- **Unreleased:** validation of allmeta `6e753c6` against netmeta 3.7-0 on all 13 of its datasets with normal and t-based CIs. All 26 analyses agree: 24 within 10⁻⁹ and the same 2 refusals; 410/410 checks pass.
