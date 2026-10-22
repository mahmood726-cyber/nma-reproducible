"""Generate/verify release hashes without Git, R, Node, or network access."""
from pathlib import Path
import argparse
import fnmatch
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "SOURCE_SHA256.json"
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "results", "outputs"}
SKIP_FILES = {"SOURCE_SHA256.json", "PROGRESS.md"}
TEMP_DIR_PATTERNS = ("tmp*", "temp", "temp-*", ".tmp", ".temp", "*.tmp", "*.temp", "_recut_test_*")
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path):
    return json.loads(path.read_text(encoding="utf-8"))
def release_files():
    result = {}
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and ".prev-" not in d
                         and not any(fnmatch.fnmatchcase(d, pattern) for pattern in TEMP_DIR_PATTERNS))
        for name in sorted(files):
            p = Path(base) / name
            rel = p.relative_to(ROOT).as_posix()
            if rel in SKIP_FILES or p.suffix in {".pyc", ".tif", ".sqlite"}: continue
            if p.suffix == ".log" and not rel.startswith("provenance/"): continue
            if name.startswith("_full_") and p.suffix == ".png": continue
            result[rel] = sha(p)
    return dict(sorted(result.items()))
def check_file(path, expected):
    p = ROOT / path
    if not p.is_file() or sha(p) != expected:
        raise ValueError("SHA-256 mismatch or missing file: " + path)
def verify_inputs():
    protected = load(ROOT / "PROTECTED_ORIGINALS.json")["files"]
    for path, expected in protected.items(): check_file(path, expected)
    source = load(ROOT / "APP_SOURCE.json")
    files = source["files"]
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / "app").rglob("*") if p.is_file()}
    if actual != {r["path"] for r in files}: raise ValueError("App source inventory differs")
    for record in files: check_file(record["path"], record["sha256"])
    manifest = load(ROOT / "app/nma/validate/MANIFEST.json")
    for record in manifest["files"]:
        check_file("app/nma/" + record["path"], record["sha256"])
    for record in manifest["provenance"]:
        if record["path"] in protected: check_file(record["path"], record["sha256"])
    base = "app/r-shiny/shinylive/webr/"
    packages = load(ROOT / (base + "repo/manifest.json"))
    records = {r["package"]: r for r in packages["packages"]}
    for name in source["webr_packages"]:
        r = records[name]
        rel = base + (r.get("path") or ("repo/" + packages["layout"] + r["file"]))
        check_file(rel, r["sha256"])
        if (ROOT / rel).stat().st_size != r["bytes"]: raise ValueError("Size mismatch: " + rel)
    print(f"INPUT INTEGRITY: {len(protected)}/{len(protected)} protected originals; "
          f"{len(files)}/{len(files)} app source hashes; {len(source['webr_packages'])} webR package hashes/sizes verified")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="regenerate after reviewed release edits")
    args = parser.parse_args()
    verify_inputs()
    current = release_files()
    if args.write:
        payload = {"schema": 1, "algorithm": "sha256", "archive_version": "1.1.0",
                   "note": "Exact file bytes, including redacted provenance logs. Excludes self, .git, runtime outputs, raw logs, caches, temporary directories, PROGRESS.md and *.prev-* backups.",
                   "files": current}
        MANIFEST.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"WROTE SOURCE_SHA256.json: {len(current)} files")
    else:
        recorded = load(MANIFEST)["files"]
        if recorded != current:
            bad = sorted(p for p in set(recorded) | set(current) if recorded.get(p) != current.get(p))
            raise ValueError("Release manifest differs: " + ", ".join(bad))
        print(f"RELEASE MANIFEST: {len(current)}/{len(current)} files verified")
if __name__ == "__main__":
    main()
