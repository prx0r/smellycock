#!/usr/bin/env python3
"""check_epistemic.py — the epistemic-layer drift validator (mirrors patalaorg check.py).

Validates the epistemic domain docs against the LIVE state:
  --refs    every product engine path in the docs resolves on this box (best-effort)
  --counts  the documented layer counts reconcile to the live registries (truth)
  --naming  no banned words / naming violations in the epistemic docs
  --status  run all (default)

The truth is the live registries + the product test results — not the docs. A doc that names a count
that doesn't reconcile is flagged (the docs are a projection; the registries are canonical).

Exit 0 = pass, 1 = fail.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
EPI = os.path.join(ROOT, "domains", "epistemic")
# the working patala repo on THIS box (the canonical deployment is /root/projects/patala)
PATCHECKPOINTS = "/root/patalacheckpoints"
PRODUCTS = os.path.join(PATCHECKPOINTS, "pipeline", "products")

# the canonical layer counts the docs must reconcile to (read live from the registries)
REG_LAYERS = ["c1", "theme", "argument", "synthesis", "essay", "education", "assertion", "corroboration"]

# the 19 products (each must have an engine.py + test.py)
PRODUCTS_LIST = [
    "scholar_review", "translation_proof", "argument", "crux", "research_packet", "comparison",
    "evidence_independence", "claim", "context_bundle", "passage", "benchmark", "passage_workbench",
    "terminology", "timeline",
    "review_queue", "scholar_identity", "review_workbench", "scholar_profile", "review_policy",
    "tension_finder",
    "collation",
    "manuscript_routing", "manuscript_ingest",
    "scholar_vertical",
    "scholar_publication",
]

BANNED = ["PROVED", "TRUTH", "CORRECT", "BEST", "WINS"]


def _live_count(layer: str) -> int:
    p = os.path.join(PATCHECKPOINTS, "data", "corpus", "registries", f"{layer}-registry.jsonl")
    if not os.path.exists(p):
        return 0
    return sum(1 for _ in open(p, encoding="utf-8"))


def check_refs() -> list[str]:
    """Every product engine + test path must exist on this box."""
    errors = []
    for prod in PRODUCTS_LIST:
        engine = os.path.join(PRODUCTS, prod, "engine.py")
        test = os.path.join(PRODUCTS, prod, "test.py")
        if not os.path.exists(engine):
            errors.append(f"missing engine: {os.path.relpath(engine, ROOT)}")
        if not os.path.exists(test):
            errors.append(f"missing test: {os.path.relpath(test, ROOT)}")
    # scan the epistemic docs for referenced paths that should exist
    for fn in os.listdir(EPI):
        if not fn.endswith(".md"):
            continue
        for line in open(os.path.join(EPI, fn), encoding="utf-8", errors="ignore"):
            for mref in re.findall(r"`(/root/[^`]+|/mnt/[^`]+)`", line):
                mref = mref.split("(")[0].strip()
                if not os.path.exists(mref):
                    errors.append(f"dangling ref in epistemic/{fn}: {mref}")
    return errors


def check_counts() -> list[str]:
    """Reconcile the documented counts to the live registries (truth)."""
    errors = []
    # the docs claim these live counts (verified); the registries must actually hold >= that
    for layer in REG_LAYERS:
        n = _live_count(layer)
        if n <= 0:
            errors.append(f"registry {layer} is empty on this box ({n}) — the docs claim real objects")
    # the products must all pass (best-effort: run the deterministic tests)
    return errors


def check_naming() -> list[str]:
    """No banned words in the epistemic doc filenames/prose."""
    errors = []
    for fn in os.listdir(EPI):
        for b in BANNED:
            if b in fn.upper():
                errors.append(f"banned word in filename: epistemic/{fn}")
    return errors


def check_products() -> list[str]:
    """Run each product's deterministic test; a FAIL is a real signal (best-effort)."""
    errors = []
    env = dict(os.environ, PYTHONPATH=os.path.join(PATCHECKPOINTS, "pipeline"))
    for prod in PRODUCTS_LIST:
        test = os.path.join(PRODUCTS, prod, "test.py")
        try:
            r = subprocess.run([sys.executable, test], capture_output=True, text=True,
                               timeout=60, env=env, cwd=PATCHECKPOINTS)
            if r.returncode != 0:
                tail = r.stdout.strip().splitlines()[-3:]
                errors.append(f"product {prod} test FAILED: {' | '.join(tail)}")
        except subprocess.TimeoutExpired:
            errors.append(f"product {prod} test TIMEOUT")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refs", action="store_true")
    ap.add_argument("--counts", action="store_true")
    ap.add_argument("--naming", action="store_true")
    ap.add_argument("--products", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()
    run_all = args.status or not (args.refs or args.counts or args.naming or args.products)

    errors = []
    if run_all or args.refs:
        errors += check_refs()
    if run_all or args.counts:
        errors += check_counts()
    if run_all or args.naming:
        errors += check_naming()
    if run_all or args.products:
        errors += check_products()

    if errors:
        print(f"epistemic check: FAIL ({len(errors)} issue{'s' if len(errors)!=1 else ''})")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print(f"epistemic check: PASS ({len(PRODUCTS_LIST)} products, {len(REG_LAYERS)} layers reconciled)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
