"""Compare the app's engine with netmeta and build every table, figure and number in the paper.

  python analysis/make_outputs.py --results results/full --outputs outputs/full --expected expected/paper_values.json

Every analysis is judged as in allmeta's own parity test (hub/shared/tests/_nma_parity_check.mjs; same
discrepancy measures and tolerances, mirrored below). Exit code 0 only if every number in the expected file is
reproduced (after rounding to its stated decimals).
"""
import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

LABEL = {"Baker2009": "COPD, exacerbations", "Dogliotti2014": "Atrial fibrillation, stroke", "Dong2013": "COPD, mortality",
         "Franchini2012": "Parkinson's disease, off-time", "Gurusamy2011": "Liver transplantation, mortality",
         "Linde2015": "Depression, response", "Linde2016": "Depression in primary care, response", "Senn2013": "Diabetes, HbA1c",
         "Stowe2010": "Parkinson's disease, off-time", "Woods2010": "Survival counts", "dietaryfat": "Dietary fat, mortality",
         "parkinson": "Parkinson's disease (= Franchini2012)", "smokingcessation": "Smoking cessation"}
TOL = {"TE_common": 1e-9, "seTE_common": 1e-9, "CI_common": 1e-9, "p_common": 1e-9, "TE_random": 1e-9, "seTE_random": 1e-9,
       "CI_random": 1e-9, "p_random": 1e-9, "Q": 1e-9, "df": 0, "pvalQ": 1e-9, "tau2": 1e-9, "I2": 1e-9, "predict": 1e-9,
       "pscore": 1e-9, "decomp": 1e-9}
GROUP = {"TE_common": "estimates", "seTE_common": "estimates", "CI_common": "estimates", "TE_random": "estimates",
         "seTE_random": "estimates", "CI_random": "estimates", "predict": "estimates", "p_common": "p-values", "p_random": "p-values",
         "pvalQ": "p-values", "Q": "heterogeneity", "tau2": "heterogeneity", "I2": "heterogeneity", "decomp": "heterogeneity",
         "df": "heterogeneity", "pscore": "P-scores"}


def jl(p):
    return {json.loads(l)["dataset"]: json.loads(l) for l in open(p, encoding="utf-8") if l.strip()}


# ---- mirror of allmeta hub/shared/tests/_nma_parity_check.mjs ----
def reorder(app, trts):
    n = len(trts)
    if sorted(app["trts"]) != sorted(trts):
        return None
    p = [app["trts"].index(t) for t in trts]
    M = lambda v: None if v is None else [v[p[i] * n + p[j]] for i in range(n) for j in range(n)]
    V = lambda v: [v[i] for i in p]
    L = lambda x: {k: M(x[k]) for k in ("TE", "seTE", "lower", "upper", "pval")}
    a = dict(app)
    a.update(common=L(app["common"]), random=L(app["random"]),
             predict=None if app["predict"] is None else {"lower": M(app["predict"]["lower"]), "upper": M(app["predict"]["upper"])},
             pscoreDesirable={k: V(app["pscoreDesirable"][k]) for k in ("common", "random")},
             pscoreUndesirable={k: V(app["pscoreUndesirable"][k]) for k in ("common", "random")})
    return a


def rel(a, b):
    return abs(a - b) / max(1.0, abs(b))


def mx(vals):
    return max([v for v in vals] or [0.0])


def compare(app_in, ref):
    n = len(ref["trts"])
    off = [i * n + j for i in range(n) for j in range(n) if i != j]
    allix = range(n * n)
    app = reorder(app_in, ref["trts"])
    if app is None:
        return {"treatments": math.inf}
    R = lambda a, b, ix: mx([rel(a[k], b[k]) for k in ix])
    A = lambda a, b, ix: mx([abs(a[k] - b[k]) for k in ix])

    def nul(a, b, f):
        return (0.0 if a is None else math.inf) if b is None else (math.inf if a is None else f(a, b))

    def vecs(a, b, f):
        return mx([(0.0 if x is None else math.inf) if y is None else f(x, y) for x, y in zip(a, b)])

    m = {"TE_common": R(app["common"]["TE"], ref["TE_common"], allix), "seTE_common": R(app["common"]["seTE"], ref["seTE_common"], allix),
         "CI_common": max(R(app["common"]["lower"], ref["lower_common"], off), R(app["common"]["upper"], ref["upper_common"], off)),
         "p_common": A(app["common"]["pval"], ref["pval_common"], off),
         "TE_random": R(app["random"]["TE"], ref["TE_random"], allix), "seTE_random": R(app["random"]["seTE"], ref["seTE_random"], allix),
         "CI_random": max(R(app["random"]["lower"], ref["lower_random"], off), R(app["random"]["upper"], ref["upper_random"], off)),
         "p_random": A(app["random"]["pval"], ref["pval_random"], off),
         "Q": nul(app["Q"], ref["Q"], rel), "df": 0.0 if app["df"] == ref["df_Q"] else math.inf,
         "pvalQ": nul(app["pvalQ"], ref["pval_Q"], lambda a, b: abs(a - b)), "tau2": nul(app["tau2"], ref["tau2"], rel),
         "I2": max(nul(app["I2"], ref["I2"], lambda a, b: abs(a - b)), nul(app["lowerI2"], ref["lower_I2"], lambda a, b: abs(a - b)),
                   nul(app["upperI2"], ref["upper_I2"], lambda a, b: abs(a - b)))}
    if ref.get("lower_predict"):
        m["predict"] = math.inf if app["predict"] is None else max(R(app["predict"]["lower"], ref["lower_predict"], off), R(app["predict"]["upper"], ref["upper_predict"], off))
    else:
        m["predict"] = math.inf if app["predict"] is not None else 0.0
    m["pscore"] = max(vecs(app["pscoreDesirable"]["common"], ref["pscore_desirable"]["common"], lambda a, b: abs(a - b)),
                      vecs(app["pscoreDesirable"]["random"], ref["pscore_desirable"]["random"], lambda a, b: abs(a - b)),
                      vecs(app["pscoreUndesirable"]["common"], ref["pscore_undesirable"]["common"], lambda a, b: abs(a - b)),
                      vecs(app["pscoreUndesirable"]["random"], ref["pscore_undesirable"]["random"], lambda a, b: abs(a - b)))
    if ref.get("Q_decomp"):
        d, r = app["decomp"], ref["Q_decomp"]
        m["decomp"] = math.inf if d is None else max(vecs(d["Q"], r["Q"], rel), vecs(d["df"], r["df"], rel), vecs(d["pval"], r["pval"], lambda a, b: abs(a - b)))
    else:
        m["decomp"] = math.inf if app["decomp"] is not None else 0.0
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True); ap.add_argument("--outputs", required=True); ap.add_argument("--expected", required=True)
    a = ap.parse_args()
    res, out = Path(a.results), Path(a.outputs)
    out.mkdir(parents=True, exist_ok=True)
    R, E = jl(res / "netmeta.jsonl"), jl(res / "engine.jsonl")
    corpus = list(csv.DictReader(open(res / "corpus.csv", encoding="utf-8")))
    DS = list(R)
    studies = {d: len({r["studlab"] for r in corpus if r["dataset"] == d}) for d in DS}
    contr = {d: sum(1 for r in corpus if r["dataset"] == d) for d in DS}
    multi = {}
    for d in DS:
        cnt = defaultdict(int)
        for r in corpus:
            if r["dataset"] == d: cnt[r["studlab"]] += 1
        multi[d] = sum(1 for v in cnt.values() if v > 1)
    st = {"datasets": len(DS), "studies_total": sum(studies.values()), "contrasts_total": sum(contr.values()),
          "multiarm_total": sum(multi.values()), "datasets_with_multiarm": sum(1 for d in DS if multi[d] > 0)}

    rows, checks, ok_checks, worst = [], 0, 0, defaultdict(float)
    for ds in DS:
        for f, g in zip(R[ds]["fits"], E[ds]["fits"]):
            assert f["method_random_ci"] == g["method_random_ci"]
            row = {"dataset": ds, "ci": f["method_random_ci"], "netmeta_ok": f["ok"], "app_ok": g["ok"]}
            checks += 1
            if f["ok"] and g["ok"]:
                ok_checks += 1
                m = compare(g, f)
                for k, v in m.items():
                    checks += 1; ok_checks += v <= TOL[k]; worst[GROUP[k]] = max(worst[GROUP[k]], v)
                row.update(m); row["within_tolerance"] = all(v <= TOL[k] for k, v in m.items())
                row.update(n=f["n"], netmeta_tau2=f["tau2"], netmeta_I2=f["I2"], netmeta_Q=f["Q"], netmeta_df_Q=f["df_Q"])   # distinct names: "Q", "tau2", "I2" are discrepancies
            else:
                same = f["ok"] == g["ok"]; ok_checks += same; row["within_tolerance"] = same
            rows.append(row)
    both = [r for r in rows if r["netmeta_ok"] and r["app_ok"]]
    st.update({"analyses": len(rows), "netmeta_fitted": sum(r["netmeta_ok"] for r in rows), "netmeta_refused": sum(not r["netmeta_ok"] for r in rows),
               "refusals_matched": sum(1 for r in rows if not r["netmeta_ok"] and not r["app_ok"]),
               "app_refused_netmeta_fitted": sum(1 for r in rows if r["netmeta_ok"] and not r["app_ok"]),
               "app_fitted_netmeta_refused": sum(1 for r in rows if not r["netmeta_ok"] and r["app_ok"]),
               "within_tolerance": sum(r["within_tolerance"] for r in rows), "all_within_tolerance": int(all(r["within_tolerance"] for r in rows)),
               "checks_total": checks, "checks_passed": ok_checks,
               "max_estimates": worst["estimates"], "max_pvalues": worst["p-values"], "max_heterogeneity": worst["heterogeneity"], "max_pscores": worst["P-scores"],
               "all_below_1e-10": int(max(worst.values()) < 1e-10), "estimates_below_1e-12": int(worst["estimates"] < 1e-12),
               "treatments_min": min(r["n"] for r in both), "treatments_max": max(r["n"] for r in both)})

    # ---- worked example: smoking cessation (random effects, normal CIs; quitting, so larger is better) ----
    ex = "smokingcessation"
    if ex in DS:
        f = next(x for x in R[ex]["fits"] if x["method_random_ci"] == "classic")
        g = reorder(next(x for x in E[ex]["fits"] if x["method_random_ci"] == "classic"), f["trts"])
        tr, n = f["trts"], len(f["trts"]); iA = tr.index("A")
        eff = {t: (math.exp(g["random"]["TE"][i * n + iA]), math.exp(g["random"]["lower"][i * n + iA]), math.exp(g["random"]["upper"][i * n + iA]),
                   math.exp(g["predict"]["lower"][i * n + iA]), math.exp(g["predict"]["upper"][i * n + iA])) for i, t in enumerate(tr) if t != "A"}
        ps = dict(zip(tr, g["pscoreUndesirable"]["random"]))
        best = max(ps, key=ps.get)
        dq = g["decomp"]
        st.update({"ex_studies": studies[ex], "ex_multiarm": multi[ex], "ex_n": n, "ex_tau2": g["tau2"], "ex_I2": 100 * g["I2"],
                   "ex_I2_lo": 100 * g["lowerI2"], "ex_I2_hi": 100 * g["upperI2"], "ex_Q": g["Q"], "ex_df": g["df"],
                   "ex_Qwithin": dq["Q"][1], "ex_dfwithin": dq["df"][1], "ex_Qbetween": dq["Q"][2], "ex_dfbetween": dq["df"][2], "ex_pbetween": dq["pval"][2],
                   "ex_or_D": eff["D"][0], "ex_or_D_lo": eff["D"][1], "ex_or_D_hi": eff["D"][2], "ex_or_D_pi_lo": eff["D"][3], "ex_or_D_pi_hi": eff["D"][4],
                   "ex_or_C": eff["C"][0], "ex_or_C_lo": eff["C"][1], "ex_or_C_hi": eff["C"][2], "ex_or_B": eff["B"][0], "ex_or_B_lo": eff["B"][1], "ex_or_B_hi": eff["B"][2],
                   "ex_best": best, "ex_best_pscore": ps[best], "ex_pscore_A": ps["A"],
                   "ex_netmeta_or_D": math.exp(f["TE_random"][tr.index("D") * n + iA])})

    # ---- tables ----
    def write(name, rws):
        with open(out / f"{name}.csv", "w", newline="", encoding="utf-8") as fh:
            fields = list(dict.fromkeys(k for r in rws for k in r))
            w = csv.DictWriter(fh, fieldnames=fields, restval=""); w.writeheader(); w.writerows(rws)
    T1 = []
    for ds in DS:
        rs = [r for r in rows if r["dataset"] == ds]; f = R[ds]["fits"][0]; b = [r for r in rs if r["netmeta_ok"] and r["app_ok"]]
        T1.append({"dataset": ds, "label": LABEL.get(ds, ds), "measure": R[ds]["sm"], "studies": studies[ds], "contrasts": contr[ds],
                   "multiarm_studies": multi[ds], "treatments": f.get("n", ""), "netmeta": "fits" if f["ok"] else "refuses",
                   "app": "fits" if E[ds]["fits"][0]["ok"] else "refuses", "tau2": f.get("tau2", ""), "I2": f.get("I2", ""),
                   "Q": f.get("Q", ""), "df": f.get("df_Q", ""),
                   "p_between_designs": (f["Q_decomp"]["pval"][2] if f.get("Q_decomp") else ""),
                   "max_discrepancy": max((max(v for k, v in r.items() if k in TOL) for r in b), default=""),
                   "all_within_tolerance": all(r["within_tolerance"] for r in rs)})
    write("table1_by_dataset", T1)
    T2 = []
    for k in TOL:
        vals = [r[k] for r in both]
        T2.append({"quantity": k, "group": GROUP[k], "analyses": len(vals), "max_discrepancy": max(vals), "tolerance": TOL[k],
                   "all_within": all(v <= TOL[k] for v in vals)})
    # the per-quantity summary must agree with the per-analysis verdicts (guards against overwriting a discrepancy)
    if all(t["all_within"] for t in T2) != bool(st["all_within_tolerance"]) or any(t["max_discrepancy"] > TOL[t["quantity"]] for t in T2 if t["all_within"]):
        sys.exit("internal inconsistency: table 2 disagrees with the per-analysis verdicts")
    write("table2_by_quantity", T2)
    write("table3_all_analyses", rows)

    # ---- figures ----
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "figure.facecolor": "white", "savefig.facecolor": "white"})
    meta = {"Software": None}
    C = {"app": "#1b6ca8", "ref": "#333333", "pi": "#999999"}
    if ex in DS:
        fig, axs = plt.subplots(1, 2, figsize=(9.4, 4.3), gridspec_kw={"width_ratios": [1.5, 1]})
        ax = axs[0]; others = [t for t in tr if t != "A"]
        names = {"A": "A: no intervention", "B": "B: self-help", "C": "C: individual counselling", "D": "D: group counselling"}
        for y, t in enumerate(reversed(others)):
            i = tr.index(t)
            lo, hi = math.exp(f["lower_random"][i * n + iA]), math.exp(f["upper_random"][i * n + iA])
            plo, phi = math.exp(f["lower_predict"][i * n + iA]), math.exp(f["upper_predict"][i * n + iA])
            ax.plot([plo, phi], [y, y], "-", color=C["pi"], lw=6, alpha=0.35, solid_capstyle="butt", label="netmeta: 95% prediction interval" if y == 0 else None)
            ax.plot([lo, hi], [y, y], "-", color=C["ref"], lw=1.8, label="netmeta: 95% CI" if y == 0 else None)
            ax.plot([math.exp(f["TE_random"][i * n + iA])], [y], "s", color=C["ref"], ms=7, label="netmeta: estimate" if y == 0 else None)
            e = eff[t]
            ax.plot([e[0]], [y], "o", color=C["app"], ms=4, label="App: estimate" if y == 0 else None)
            ax.plot([e[1], e[2], e[3], e[4]], [y] * 4, "|", color=C["app"], ms=11, mew=1.6, label="App: interval limits" if y == 0 else None)
        ax.axvline(1, color="#bbbbbb", lw=0.8); ax.set_xscale("log")
        from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
        tk = [0.25, 0.5, 1, 2, 4, 8, 16]; ax.xaxis.set_major_locator(FixedLocator(tk)); ax.xaxis.set_major_formatter(FixedFormatter([f"{t:g}" for t in tk])); ax.xaxis.set_minor_locator(NullLocator())
        ax.set_yticks(range(len(others)), [names[t] for t in reversed(others)]); ax.set_ylim(-0.6, len(others) - 0.4)
        ax.set_xlabel("Odds ratio of quitting versus A: no intervention (random effects)")
        ax.set_title("A. Network estimates", fontsize=9.5); ax.legend(fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.45, -0.2), ncol=3)
        ax = axs[1]
        order = sorted(tr, key=lambda t: -dict(zip(tr, f["pscore_undesirable"]["random"]))[t])
        for x, t in enumerate(order):
            ax.bar(x, dict(zip(tr, f["pscore_undesirable"]["random"]))[t], color="#cfd8e3", edgecolor=C["ref"], width=0.6, label="netmeta" if x == 0 else None)
            ax.plot(x, ps[t], "o", color=C["app"], ms=6, label="App" if x == 0 else None)
        ax.set_xticks(range(len(order)), [names[t].split(":")[0] for t in order]); ax.set_ylim(0, 1); ax.set_ylabel("P-score (larger odds ratio better)")
        ax.set_title("B. P-scores", fontsize=9.5); ax.legend(fontsize=7.5, frameon=False, loc="upper right")
        fig.suptitle(f"Figure 2. Worked example: smoking cessation ({studies[ex]} studies, {n} treatments); the app (blue) over netmeta", fontsize=10)
        fig.tight_layout(); fig.savefig(out / "figure2_worked_example.png", dpi=300, metadata=meta); plt.close(fig)
        with open(out / "figure2_worked_example.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh); w.writerow(["treatment", "OR_vs_A_app", "OR_vs_A_netmeta", "CI_low_app", "CI_high_app", "PI_low_app", "PI_high_app", "pscore_app", "pscore_netmeta"])
            for t in others:
                i = tr.index(t)
                w.writerow([t, eff[t][0], math.exp(f["TE_random"][i * n + iA]), eff[t][1], eff[t][2], eff[t][3], eff[t][4], ps[t], dict(zip(tr, f["pscore_undesirable"]["random"]))[t]])
    # Figure 3: agreement by dataset and quantity group
    groups = ["estimates", "p-values", "heterogeneity", "P-scores"]; mk = {"estimates": "o", "p-values": "s", "heterogeneity": "D", "P-scores": "^"}
    col = {"estimates": "#1b6ca8", "p-values": "#c27c0e", "heterogeneity": "#2c7a4b", "P-scores": "#8a4b9b"}
    fitted = [d for d in DS if R[d]["fits"][0]["ok"]]
    fig, ax = plt.subplots(figsize=(7.8, 0.34 * len(fitted) + 2.3))
    lg = lambda v: math.log10(max(v, 1e-17))   # exact agreement (0) is drawn at 1e-17
    for y, d in enumerate(fitted):
        rs = [r for r in both if r["dataset"] == d]
        for gi, gname in enumerate(groups):
            v = max(r[k] for r in rs for k in TOL if GROUP[k] == gname and k != "df")
            ax.plot(lg(v), y + (gi - 1.5) * 0.12, mk[gname], color=col[gname], ms=5, label=gname if y == 0 else None)
    ax.axvline(-9, color="#444444", ls="--", lw=0.8)
    ax.set_yticks(range(len(fitted)), [f"{d} ({R[d]['fits'][0]['n']} treatments)" for d in fitted]); ax.set_xlim(-17.5, -6)
    ax.set_xlabel("log10 largest difference from netmeta (exact agreement shown at -17)")
    ax.set_title(f"Figure 3. App versus netmeta: {len(fitted)} networks, normal and t-based CIs\n(dashed: tolerance 1e-9; Dong2013 is refused by both)", fontsize=9.5)
    ax.grid(axis="x", color="#eeeeee", lw=0.6); ax.legend(fontsize=7.5, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.11), ncol=4)
    fig.tight_layout(); fig.savefig(out / "figure3_agreement.png", dpi=300, metadata=meta); plt.close(fig)
    with open(out / "figure3_agreement.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["dataset", "ci", "quantity", "group", "discrepancy"])
        for r in both:
            for k in TOL: w.writerow([r["dataset"], r["ci"], k, GROUP[k], r[k]])
    # Visual abstract
    fig = plt.figure(figsize=(11, 4.6)); fig.patch.set_facecolor("white")
    boxes = [("Problem", "Network meta-analysis\nis usually run in R\n(netmeta), Stata\nor WinBUGS."),
             ("Tool", "allmeta NMA app:\noffline, in the browser.\nCommon and random\neffects, multi-arm studies,\nprediction intervals,\ninconsistency, P-scores."),
             ("Validation", f"Against R netmeta on all\n{st['datasets']} datasets it ships\n({st['studies_total']} studies, {st['multiarm_total']} multi-arm),\nnormal and t-based CIs:\n{st['analyses']} analyses."),
             ("Result", f"All {st['analyses']} agree: {st['netmeta_fitted']} within\n1e-9 and the same {st['refusals_matched']} refusals;\n{st['checks_passed']}/{st['checks_total']} checks pass.")]
    for i, (hh, txt) in enumerate(boxes):
        x = 0.02 + i * 0.245
        fig.patches.append(matplotlib.patches.FancyBboxPatch((x, 0.22), 0.22, 0.60, boxstyle="round,pad=0.01", transform=fig.transFigure, facecolor=["#f4ece8", "#e8f0f7", "#eaf4ec", "#fdf6e3"][i], edgecolor="#999"))
        fig.text(x + 0.11, 0.75, hh, ha="center", fontsize=13, weight="bold")
        fig.text(x + 0.11, 0.48, txt, ha="center", va="center", fontsize=10.5, linespacing=1.4)
        if i < 3: fig.text(x + 0.2325, 0.52, "→", ha="center", va="center", fontsize=18)
    fig.text(0.5, 0.09, "One command reproduces every number on Linux, Windows, macOS and Docker: github.com/mahmood726-cyber/nma-reproducible",
             ha="center", fontsize=9, color="#333333")
    fig.text(0.5, 0.91, "A browser tool for network meta-analysis, validated against R netmeta", ha="center", fontsize=13.5, weight="bold")
    fig.savefig(out / "visual_abstract.png", dpi=300, metadata=meta); plt.close(fig)
    (out / "stats.json").write_text(json.dumps(st, indent=1, default=float))

    # ---- PASS/FAIL ----
    exp = json.loads(Path(a.expected).read_text())
    rep = []
    for k, spec in exp["values"].items():
        g_ = st.get(k)
        if isinstance(spec["value"], str):
            okv = g_ == spec["value"]; shown = g_
        else:
            d = spec["decimals"]
            okv = g_ is not None and round(float(g_), d) == round(float(spec["value"]), d)
            shown = None if g_ is None else (int(round(float(g_), d)) if d <= 0 else round(float(g_), d + 2))
        rep.append((k, spec["value"], shown, "PASS" if okv else "FAIL"))
    npass = sum(r[3] == "PASS" for r in rep)
    md = ["| Quantity | Expected | Reproduced | Result |", "|---|--:|--:|---|"] + [f"| {a_} | {b} | {c} | {d} |" for a_, b, c, d in rep]
    (out / "reproduction_report.md").write_text(f"# Reproduction report\n\n{npass}/{len(rep)} numbers reproduced\n\n" + "\n".join(md) + "\n", encoding="utf-8")
    w = max(len(r[0]) for r in rep) if rep else 0
    for a_, b, c, d in rep: print(f"{a_.ljust(w)}  {str(b):>14}  {str(c):>16}  {d}")
    print(f"\n{npass}/{len(rep)} numbers reproduced: {'ALL PASS' if npass == len(rep) else 'FAILURES PRESENT'}")
    sys.exit(0 if rep and npass == len(rep) else 1)


if __name__ == "__main__":
    main()
