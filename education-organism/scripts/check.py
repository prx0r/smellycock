#!/usr/bin/env python3
"""scripts/check.py — the drift validator (mirrors patalaorg check.py).

Gates the serveragent3 docs + registries:
  --status  resolve docs refs + reconcile registry counts + run the gates.
Exit non-zero on failure. A doc/claim that doesn't reconcile is flagged (docs are a projection).
"""
from __future__ import annotations
import json, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"


def _check_refs() -> list[str]:
    errors = []
    if MANIFEST.exists():
        m = json.load(open(MANIFEST))
        for doc in m.get("docs", {}):
            if not (ROOT / doc).exists():
                errors.append(f"manifest doc missing: {doc}")
    # scan .md for /root/... refs that must resolve (via alias map)
    aliases = {"/root/patalacheckpoints": "/root/patalacheckpoints",
               "/root/fuck-off": "/root/fuck-off", "/root/smellycock": "/root/smellycock"}
    for root, _dirs, files in os.walk(ROOT):
        if ".git" in root:
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            for line in open(path, encoding="utf-8", errors="ignore"):
                for ref in re.findall(r"`(/root/[^`]+)`", line):
                    if not os.path.exists(ref) and not os.path.exists(aliases.get(ref, "")):
                        errors.append(f"dangling ref in {os.path.relpath(path, ROOT)}: {ref}")
    return errors


def _check_counts() -> list[str]:
    sys.path.insert(0, str(ROOT / "kernels"))
    import object_registry as R
    errors = []
    for layer in R.LAYERS:
        # any committed object with input_refs must resolve (chain gate)
        for oid, vs in R._load(layer)["objects"].items():
            for v in vs:
                if v.get("superseded"):
                    continue
                if "gold" in oid or v.get("created_by", "").endswith("-golds"):
                    continue
                refs = v.get("input_refs") or []
                if layer != "C1" and not refs:
                    errors.append(f"{layer}:{oid} has no input_refs")
    return errors


def _run_gates() -> list[str]:
    sys.path.insert(0, str(ROOT / "kernels"))
    import gates
    import object_registry as R
    errors = []
    ok, fails = gates.chain()
    if not ok:
        errors += [f"chain: {f}" for f in fails]
    if not R.verify_event_chain():
        errors.append("event ledger tampered")
    # red-team MEDIUM-8: run the production gates on the REAL registries
    for layer in R.LAYERS:
        for oid, r in gates.load_current(layer).items():
            if "gold" in oid or r.get("created_by", "").endswith("-golds"):
                continue  # gold/external objects are upstream gold, not generated projections
            score, checks, verdict = gates.quality(r)
            if verdict != "PASS":
                errors.append(f"{layer}:{oid} quality {verdict} ({checks})")
    return errors


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--status"
    errors = []
    if mode in ("--status", "--refs"):
        errors += _check_refs()
    if mode in ("--status", "--counts"):
        errors += _check_counts()
    if mode in ("--status", "--gates"):
        errors += _run_gates()
    if errors:
        print(f"serveragent3 check: FAIL ({len(errors)} issues)")
        for e in errors[:15]:
            print(f"  ✗ {e}")
        sys.exit(1)
    print("serveragent3 check: PASS")


if __name__ == "__main__":
    main()
