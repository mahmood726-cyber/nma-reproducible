"""Write expected/*.json from a run's stats.json (used once, to record the canonical run).

  python analysis/set_expected.py outputs/full/stats.json expected/paper_values.json full
  python analysis/set_expected.py outputs/quick/stats.json expected/quick_values.json quick
Each number is stored rounded to the precision at which the paper prints it. Discrepancy maxima, which
differ between platforms in their last digits, enter only as threshold indicators (0/1).
"""
import json
import sys

# quantity -> decimals
FULL = {"datasets": 0, "studies_total": 0, "contrasts_total": 0, "multiarm_total": 0, "datasets_with_multiarm": 0,
        "analyses": 0, "netmeta_fitted": 0, "netmeta_refused": 0, "refusals_matched": 0, "app_refused_netmeta_fitted": 0,
        "app_fitted_netmeta_refused": 0, "within_tolerance": 0, "all_within_tolerance": 0, "checks_total": 0, "checks_passed": 0,
        "all_below_1e-10": 0, "estimates_below_1e-12": 0, "treatments_min": 0, "treatments_max": 0,
        "ex_studies": 0, "ex_multiarm": 0, "ex_n": 0, "ex_tau2": 2, "ex_I2": 1, "ex_I2_lo": 1, "ex_I2_hi": 1, "ex_Q": 1, "ex_df": 0,
        "ex_Qwithin": 1, "ex_dfwithin": 0, "ex_Qbetween": 1, "ex_dfbetween": 0, "ex_pbetween": 2,
        "ex_or_D": 2, "ex_or_D_lo": 2, "ex_or_D_hi": 2, "ex_or_D_pi_lo": 2, "ex_or_D_pi_hi": 2, "ex_or_C": 2, "ex_or_C_lo": 2, "ex_or_C_hi": 2,
        "ex_or_B": 2, "ex_or_B_lo": 2, "ex_or_B_hi": 2, "ex_best": "str", "ex_best_pscore": 2, "ex_pscore_A": 2, "ex_netmeta_or_D": 2}
QUICK = {"datasets": 0, "analyses": 0, "netmeta_fitted": 0, "all_within_tolerance": 0, "all_below_1e-10": 0,
         "ex_tau2": 2, "ex_or_D": 2, "ex_best": "str"}

stats, out, mode = sys.argv[1:4]
st = json.load(open(stats))
spec = FULL if mode == "full" else QUICK
vals = {}
for k, d in spec.items():
    if d == "str":
        vals[k] = {"value": st[k], "decimals": 0}
        continue
    v = round(float(st[k]), d)
    vals[k] = {"value": int(v) if d <= 0 else v, "decimals": d}
json.dump({"source": f"Canonical run ({mode} mode): values as printed in the paper.", "values": vals}, open(out, "w"), indent=1)
print(f"wrote {len(vals)} expected values to {out}")
