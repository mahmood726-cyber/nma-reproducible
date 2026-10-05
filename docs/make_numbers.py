"""Write docs/numbers.json: every number printed in docs/paper.md, its value as printed, and the stats key it comes from.

  python docs/make_numbers.py outputs/full/stats.json "<source description>"
Fails if a printed value is not what the run gives after rounding as printed.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# (quantity, as printed, stats key, how the printed text is derived from the value)
N = [
    ("Datasets distributed with netmeta", "13", "datasets", "int"),
    ("Studies in those datasets", "364", "studies_total", "int"),
    ("Study contrasts", "506", "contrasts_total", "int"),
    ("Multi-arm studies", "52", "multiarm_total", "int"),
    ("Fewest treatments in a network", "3", "treatments_min", "int"),
    ("Most treatments in a network", "22", "treatments_max", "int"),
    ("Analyses (datasets x two CI methods)", "26", "analyses", "int"),
    ("Analyses agreeing", "26", "within_tolerance", "int"),
    ("Analyses netmeta completes", "24", "netmeta_fitted", "int"),
    ("Analyses netmeta refuses", "2", "netmeta_refused", "int"),
    ("Refusals the app matches", "2", "refusals_matched", "int"),
    ("Individual checks", "410", "checks_total", "int"),
    ("Individual checks passed", "410", "checks_passed", "int"),
    ("Estimates and intervals within 10^-12", "yes", "estimates_below_1e-12", "flag"),
    ("Every quantity within 10^-10", "yes", "all_below_1e-10", "flag"),
    ("Worked example: studies", "24", "ex_studies", "int"),
    ("Worked example: three-arm studies", "2", "ex_multiarm", "int"),
    ("Worked example: tau^2", "0.60", "ex_tau2", "2dp"),
    ("Worked example: I^2 (%)", "88.6", "ex_I2", "1dp"),
    ("Worked example: I^2 lower limit (%)", "84.4", "ex_I2_lo", "1dp"),
    ("Worked example: I^2 upper limit (%)", "91.7", "ex_I2_hi", "1dp"),
    ("Worked example: Q between designs", "15.2", "ex_Qbetween", "1dp"),
    ("Worked example: df between designs", "7", "ex_dfbetween", "int"),
    ("Worked example: p between designs", "0.03", "ex_pbetween", "2dp"),
    ("Worked example: OR group counselling vs no intervention", "2.47", "ex_or_D", "2dp"),
    ("Worked example: its lower 95% limit", "1.10", "ex_or_D_lo", "2dp"),
    ("Worked example: its upper 95% limit", "5.52", "ex_or_D_hi", "2dp"),
    ("Worked example: prediction interval lower", "0.40", "ex_or_D_pi_lo", "2dp"),
    ("Worked example: prediction interval upper", "15.11", "ex_or_D_pi_hi", "2dp"),
    ("Worked example: treatment with the highest P-score", "D", "ex_best", "D"),
    ("Worked example: its P-score", "0.84", "ex_best_pscore", "2dp"),
]


def shown(v, how):
    if how == "int": return str(int(round(v)))
    if how == "flag": return "yes" if v == 1 else "no"
    if how.endswith("dp"): return f"{v:.{int(how[0])}f}".replace("-", "−")
    return how if v == how else f"MISMATCH {v}"


st = json.loads(Path(sys.argv[1]).read_text())
src = sys.argv[2] if len(sys.argv) > 2 else "reproduce.py full run"
out, bad = [], []
for q, printed, k, how in N:
    s = shown(st[k], how)
    if s != printed: bad.append(f"{q}: printed {printed}, run gives {s}")
    out.append({"quantity": q, "printed": printed, "stats_key": k, "value": st[k]})
if bad: sys.exit("numbers.json NOT written:\n  " + "\n  ".join(bad))
(ROOT / "docs" / "numbers.json").write_text(json.dumps({"source": src, "numbers": out}, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"docs/numbers.json: {len(out)} numbers, all as printed")
