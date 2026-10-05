# Network meta-analysis in a browser: a tool validated against the R package netmeta

**Mahmood Ahmad**¹ [AUTHOR TO COMPLETE: ORCID, corresponding-author e-mail]

¹ [AUTHOR TO COMPLETE: affiliation]

## Abstract

**Background:** Network meta-analysis compares several treatments at once and usually needs R, Stata or WinBUGS. We built a browser tool for it and validated it against R.

**Methods:** The allmeta NMA app fits common- and random-effects network meta-analysis of study contrasts, handling multi-arm studies, and reports a league table, prediction intervals, heterogeneity, the decomposition of Q into within- and between-design parts, and P-scores. We compared it with the R package netmeta on all 13 datasets netmeta distributes (364 studies, 52 multi-arm), with normal and t-based confidence intervals, in a containerised analysis run on four platforms.

**Results:** All 26 analyses agreed: 24 within 10⁻⁹ and the same 2 refusals. All 410 checks passed.

**Conclusions:** The app reproduces netmeta offline, without installation or programming.

**Keywords:** network meta-analysis; multi-arm trials; inconsistency; P-scores; netmeta; software validation; reproducibility; browser-based software

## Introduction

Network meta-analysis combines direct and indirect evidence on several treatments [1]. The frequentist model, fitted by weighted least squares with correlated contrasts from multi-arm studies [2], is implemented in the R package netmeta [3,4].

We describe the NMA app, a member of allmeta, a collection of offline browser tools for evidence synthesis [5], and validate it against netmeta.

## Methods

### Implementation

The app is a static web tool (https://mahmood726-cyber.github.io/allmeta/nma/). Its engine, `nma-multiarm-v1.js`, reproduces netmeta's estimation in pure JavaScript.

- **Data.** One row per study contrast: study, two treatments, estimate and standard error. A multi-arm study supplies every pair of its arms.
- **Checks.** Studies with incomplete, duplicated or internally inconsistent comparisons are refused and named, as in netmeta.
- **Estimation.** Common effect, or random effects with netmeta's generalised DerSimonian–Laird variance; confidence intervals from the normal or the t distribution.
- **Outputs.** League table with p-values; prediction intervals [8]; Q, τ² and I² with its confidence interval [9]; the design-based decomposition of Q [6]; P-scores in either direction [7]; network graph; CSV and JSON export.

### Operation

The app needs only a browser and works offline. A user (Figure 1):

1. pastes the contrasts or loads one of netmeta's datasets;
2. chooses the model, interval method, direction of benefit and scale;
3. inspects the network graph and summary statistics;
4. reviews heterogeneity, inconsistency and estimates against a reference treatment;
5. reads the P-scores and the league table;
6. switches to t-based intervals, sees a refusal for an incomplete multi-arm study, and exports results.

### Validation

We validated allmeta commit 6e753c6. The corpus was all 13 datasets in netmeta 3.7-0 [4], converted to contrasts with netmeta's `pairwise()` and each dataset's documented summary measure (364 studies, 506 contrasts, 52 multi-arm studies; 3–22 treatments; one dataset, parkinson, duplicates Franchini2012). netmeta analysed each with normal and t-based random-effects intervals: 26 analyses. The app's engine ran on the same contrasts. This validation found that earlier app versions dropped an incomplete multi-arm study instead of refusing the network, labelled the league table the wrong way round, and ranked by simulated probabilities assuming smaller effects were better; all were corrected (allmeta PR #78).

Agreement required identical refusals and every reported quantity within 10⁻⁹ (relative for estimates, intervals, Q and τ²; absolute for p-values, I² and P-scores).

One command (`python reproduce.py`) runs everything in a canonical Docker image (R 4.6.0, Node 24.15.0). Continuous integration repeats it on Linux, Windows, macOS and Docker and checks every reported number.

## Results

**Agreement.** netmeta analysed 24 networks and refused 2 (Dong2013, where one three-arm study has an undefined comparison). The app refused the same 2 and agreed on all 24 (Table 1; Figure 3). Estimates and intervals agreed within 10⁻¹², and every quantity within 10⁻¹⁰. All 410 checks passed.

**Worked example.** In smoking cessation (24 studies, 2 three-arm) [10], random effects gave τ² = 0.60 and I² = 88.6% (95% CI 84.4% to 91.7%). Between-design inconsistency was Q = 15.2 (7 df, p = 0.03). Against no intervention, group counselling had an odds ratio of quitting of 2.47 (95% CI 1.10 to 5.52; prediction interval 0.40 to 15.11) and the highest P-score (0.84) (Figure 2).

**Reproducibility.** Every number was reproduced on all four platforms.

## Discussion

The app gives reviewers netmeta's frequentist network meta-analysis in a browser, with results reproducible in one step.

Limitations: input is contrast-level (arm-level data must first be converted); random effects use the DerSimonian–Laird estimator only; node-splitting is in a separate allmeta app and was not compared here; and the test datasets are curated examples.

## Conclusions

A browser tool can reproduce standard network meta-analysis on published datasets.

## Data availability

**Underlying data:** datasets distributed with the R package netmeta 3.7-0 [4], built at run time.

**Extended data:** app, analysis code, expected values, figures and screenshots, archived at Zenodo: [DOI to be added on release] [11]. Licence: MIT.

## Software availability

- **Source code available from:** https://github.com/mahmood726-cyber/allmeta (`nma/`, `shared/nma-multiarm-v1.js`); validated version: commit 6e753c68644834ce4588c4bdf89366452da3159e
- **Archived source code at time of publication:** Zenodo. NMA app: reproducible validation against netmeta (v1.0.0). [DOI to be added on release] [11]
- **Licence:** MIT
- **Reproduction:** one click via GitHub Codespaces (free account), a fork's "Run workflow" button, or `python reproduce.py`; verified runs: https://mahmood726-cyber.github.io/nma-reproducible/

## Competing interests

The author develops allmeta. [AUTHOR TO CONFIRM: no other competing interests.]

## Grant information

[AUTHOR TO COMPLETE]

## Acknowledgements

[AUTHOR TO COMPLETE.] Claude (Anthropic), an AI assistant, helped write the software, the analysis code and the draft of this manuscript. The author checked all code, results and text.

## References

1. Lu G, Ades AE. Combination of direct and indirect evidence in mixed treatment comparisons. Stat Med. 2004;23(20):3105–24. https://doi.org/10.1002/sim.1875
2. Rücker G. Network meta-analysis, electrical networks and graph theory. Res Synth Methods. 2012;3(4):312–24. https://doi.org/10.1002/jrsm.1058
3. Balduzzi S, Rücker G, Nikolakopoulou A, Papakonstantinou T, Salanti G, Efthimiou O, et al. netmeta: an R package for network meta-analysis using frequentist methods. J Stat Softw. 2023;106(2):1–40. https://doi.org/10.18637/jss.v106.i02
4. Rücker G, Krahn U, König J, Efthimiou O, Davies A, Papakonstantinou T, et al. netmeta: Network Meta-Analysis using Frequentist Methods. R package version 3.7-0 [software]. CRAN; 2026. https://doi.org/10.32614/CRAN.package.netmeta
5. Ahmad M. allmeta — open browser-only tools for evidence synthesis (v1.1.1) [software]. Zenodo; 2026. https://doi.org/10.5281/zenodo.20584424
6. Krahn U, Binder H, König J. A graphical tool for locating inconsistency in network meta-analyses. BMC Med Res Methodol. 2013;13:35. https://doi.org/10.1186/1471-2288-13-35
7. Rücker G, Schwarzer G. Ranking treatments in frequentist network meta-analysis works without resampling methods. BMC Med Res Methodol. 2015;15:58. https://doi.org/10.1186/s12874-015-0060-8
8. Riley RD, Higgins JPT, Deeks JJ. Interpretation of random effects meta-analyses. BMJ. 2011;342:d549. https://doi.org/10.1136/bmj.d549
9. Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. Stat Med. 2002;21(11):1539–58. https://doi.org/10.1002/sim.1186
10. Dias S, Welton NJ, Sutton AJ, Caldwell DM, Lu G, Ades AE. Evidence synthesis for decision making 4: inconsistency in networks of evidence based on randomized controlled trials. Med Decis Making. 2013;33(5):641–56. https://doi.org/10.1177/0272989X12455847
11. Ahmad M. Network meta-analysis in the browser: a tool validated against the R package netmeta (v1.0.0) [software]. Zenodo; 2026. [DOI to be added on release]

## Figure and table legends

**Figure 1.** Using the app, step by step (smoking cessation data from netmeta; Google Chrome, light theme; high-resolution captures cropped to the relevant panels).
(1) Data entry, one row per study contrast, and the list of netmeta's datasets.
(2) Model options: random effects, normal intervals, larger odds ratios of quitting better, odds ratios shown.
(3) Network graph with the number of studies per comparison (A) and summary statistics (B).
(4) Heterogeneity and the decomposition of Q (A) and estimates against no intervention with prediction intervals (B).
(5) P-scores with the simulated probability of ranking first (A) and the league table, row versus column (B).
(6) Estimates with t-based intervals (A), the refusal when one comparison of a three-arm study is removed (B), and export buttons (C).
Panels 3–6 are labelled composites of regions of one page; panels 1 and 2 are single crops.

**Figure 2.** Worked example, smoking cessation: (A) random-effects odds ratios of quitting against no intervention with 95% confidence and prediction intervals; (B) P-scores (larger odds ratios better). The app (blue) is drawn over netmeta.

**Figure 3.** App versus netmeta for the 12 networks both analyse, normal and t-based intervals: largest difference in estimates and intervals, p-values, heterogeneity statistics and P-scores.

**Table 1.** Agreement with netmeta by dataset: measure, studies, contrasts, multi-arm studies, treatments, τ², I², Q, test for between-design inconsistency, and largest difference.

**Table 2.** Largest difference from netmeta for each reported quantity across all 24 analyses, with its tolerance.
