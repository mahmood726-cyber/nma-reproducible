# Figure 1: using the app, step by step

Data: the app's built-in copy of netmeta's smokingcessation dataset (24 studies, 2 of them three-arm; A = no intervention, B = self-help, C = individual counselling, D = group counselling; outcome: successful smoking cessation). App: allmeta commit 6e753c6.

## How the images were captured
- **Browser:** Google Chrome, driven by Playwright (`capture.mjs`), light theme.
- **Window:** 640 × 900 CSS px (the page's single-column layout).
- **Resolution:** 4 device pixels per CSS pixel (at least the 3× asked for; 4 so that every panel is at least 300 dpi at 170 mm with text of at least 8 pt). No image is enlarged.
- **Cropping:** each image is cropped tightly to the panels it shows.
- **Composites:** steps 3–6 are labelled composites (A, B, C) of regions of one page state, stacked by `compose.py`. Steps 1 and 2 are single crops.
- **Formats:** final width 2392–2683 px, lossless PNG plus uncompressed TIFF at 357–401 dpi for a 170 mm print width.
- **Legibility:** text measured in the page prints at 8.3 pt or larger at 170 mm. See `legibility.json`.

## Steps
- **step1: Data entry.** One row per study contrast (`study, treatment1, treatment2, estimate, SE`, the estimate being treatment2 − treatment1 on the log odds ratio scale), here smokingcessation loaded from the list of netmeta's datasets.
- **step2: Model options.** Random effects (DerSimonian–Laird τ²); normal confidence intervals (netmeta's default); larger estimates better (quitting); odds ratios shown.
- **step3: Network and summary (composite).**
  - (A) Network graph: the number on each edge is the number of studies comparing the two treatments; the reference treatment (A) in yellow.
  - (B) Studies, contrasts, treatments, reference, τ² = 0.5989 and I² = 88.6%.
- **step4: Heterogeneity, inconsistency and estimates (composite).**
  - (A) τ² and τ; I² 88.6% (84.4% to 91.7%); Q = 202.62 (23 df); within designs Q = 187.40 (16 df); between designs Q = 15.22 (7 df, p = 0.0333).
  - (B) Odds ratios against A with 95% CIs, 95% prediction intervals and p-values, e.g. D: 2.47 (1.10 to 5.52), prediction interval 0.40 to 15.11.
- **step5: Ranking and league table (composite).**
  - (A) P-scores (larger better): D 83.8%, C 71.0%, B 40.4%, A 4.8%, with the simulated probability of ranking first.
  - (B) League table, row treatment versus column treatment, odds ratios with 95% CIs.
- **step6: t-based intervals, a refusal, and export (composite).**
  - (A) Estimates with t-based confidence intervals (df of Q), e.g. D: 2.47 (1.05 to 5.78).
  - (B) After deleting one of the three comparisons of the three-arm study 1, the network is refused and the study named, as netmeta does.
  - (C) Export and data buttons.

## To regenerate
Serve the repository root, for example `python -m http.server 8000`, then:

```bash
node docs/screenshots/capture.mjs work http://localhost:8000/app/nma/index.html
python docs/screenshots/compose.py work docs/screenshots
```
