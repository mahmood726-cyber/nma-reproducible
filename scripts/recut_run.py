"""Portable runner support: preserve earlier outputs, report actual counts, serve UI tests."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import json
import subprocess
import threading

ROOT = Path(__file__).resolve().parents[1]
def rotate():
    for rel in ["results/full", "outputs/full"]:
        path = ROOT / rel
        if path.exists():
            n = 1
            while path.with_name(path.name + f".prev-{n}").exists(): n += 1
            target = path.with_name(path.name + f".prev-{n}")
            path.rename(target)
            print(f"Preserved {rel} as {target.relative_to(ROOT).as_posix()}")
        else:
            print(f"No previous {rel}")
def summary():
    expected = json.loads((ROOT / "expected/paper_values.json").read_text())["values"]
    stats = json.loads((ROOT / "outputs/full/stats.json").read_text())
    for key in ["datasets", "analyses", "netmeta_fitted", "netmeta_refused", "refusals_matched",
                "within_tolerance", "checks_passed", "checks_total"]:
        if stats[key] != expected[key]["value"]:
            raise ValueError(f"{key}: actual {stats[key]!r} != original expected {expected[key]['value']!r}")
    print(f"ORIGINAL VALIDATION: {stats['checks_passed']}/{stats['checks_total']} checks; "
          f"{stats['within_tolerance']}/{stats['analyses']} analyses agree; "
          f"{stats['refusals_matched']}/{stats['netmeta_refused']} refusals matched")
    print("Expected-versus-reproduced paper numbers: see outputs/full/reproduction_report.md")
def ui():
    handler = partial(SimpleHTTPRequestHandler, directory=str(ROOT / "app"))
    with ThreadingHTTPServer(("127.0.0.1", 8000), handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            result = subprocess.run(["node", "validation-plus/check-ui.mjs"], cwd=ROOT, timeout=180)
        finally:
            server.shutdown()
            thread.join(timeout=5)
    raise SystemExit(result.returncode)
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["rotate", "summary", "extras", "ui"])
    args = parser.parse_args()
    if args.stage == "rotate": rotate()
    elif args.stage == "summary": summary()
    elif args.stage == "ui": ui()
    else:
        print("NUMERICAL EXTRAS: N/A (APP.txt: no numerical plus suite for NMA; no extra N/N claimed)")
if __name__ == "__main__": main()
