#!/usr/bin/env python3
"""scripts/audit-resolve.py — BUILD-2: the audit/resolve resolver (follows real input_refs).

Upper chain uses suffixed ids (kramasadbhava:v1__arg) linked by input_refs. Lower chain uses the bare
work:verse id (kramasadbhava:v1) across SOURCE..C1. This resolver:
  1. follows input_refs/depends_on up the upper chain (EDUCATION -> ... -> C1),
  2. at the C1 (bare work:verse), walks that SAME id through the lower layers (L200->...->SOURCE).
This yields the TRUE audit trail from an educational claim back to source Sanskrit.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

PATALA = Path("/root/patalacheckpoints")
REG = PATALA / "data/corpus/registries"
LOWER = ["L200", "L2", "L1L2", "L1", "L0", "T1", "SOURCE"]


def layer_ids(layer):
    p = REG / f"{layer.lower()}-registry.jsonl"
    ids = set()
    if not p.exists():
        return ids
    for line in p.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        if not r.get("superseded"):
            ids.add(r["object_id"])
    return ids


def follow_upper(object_id, visited):
    """Follow input_refs/depends_on up the upper chain. Returns the id that reaches the bare work:verse C1."""
    if object_id in visited:
        return None
    visited.add(object_id)
    # this id is an EDUCATION/ESSAY/SYNTHESIS/ARGUMENT object
    for layer in ["EDUCATION", "ESSAY", "SYNTHESIS", "ARGUMENT", "THEME"]:
        p = REG / f"{layer.lower()}-registry.jsonl"
        if not p.exists():
            continue
        for line in p.open(encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get("superseded") or r["object_id"] != object_id:
                continue
            # input_refs + depends_on both point at parents
            refs = list(r.get("input_refs") or [])
            for sec in (r.get("payload", {}).get("essay", {}) or {}).get("sections", []):
                for par in sec.get("paragraphs", []):
                    refs += list(par.get("depends_on") or [])
            for lc in (r.get("payload", {}).get("education", {}) or {}).get("learning_claims", []):
                refs += list(lc.get("depends_on") or [])
            for ref in refs:
                # a bare work:verse id (no '__') = the C1 floor
                if "__" not in ref:
                    return ref
                sub = follow_upper(ref, visited)
                if sub:
                    return sub
    return None


def main():
    educ_ids = layer_ids("EDUCATION")
    if not educ_ids:
        print("no EDUCATION objects")
        return
    for oid in sorted(educ_ids)[:1]:
        visited = set()
        base = follow_upper(oid, visited)
        print(f"RESOLVE {oid} (EDUCATION) down to SOURCE:")
        if not base:
            print("  ✗ could not find the C1 floor")
            continue
        # walk the bare base id through the lower chain
        chain = ["C1"] + LOWER
        lineage = []
        for layer in chain:
            if base in layer_ids(layer):
                lineage.append((layer, base))
        print(f"  upper ref reached C1 base: {base}")
        for layer, ref in lineage:
            print(f"  {layer:8s} {ref}")
        reached = any(l == "SOURCE" for l, _ in lineage)
        print(f"\n  → {'RESOLVES TO SOURCE ✅ (full audit trail)' if reached else 'PARTIAL — lower chain gap ⚠️'}")


if __name__ == "__main__":
    main()
