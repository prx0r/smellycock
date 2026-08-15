#!/usr/bin/env python3
"""scripts/link-derivation-chain.py — BUILD-1: backfill input_refs on the lower chain (fast, targeted).

The lower chain (SOURCE→T1→L0→L1→L2→L200→C1) has empty input_refs. This backfills them for the
works that have an EDUCATION object (the real customer-facing path) + all L200/C1, using the payload
refs + shared object_id. Single-pass per layer (fast — no O(n) re-save). Additive.

Operates on the REAL patalacheckpoints registries. Deterministic.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

PATALA = Path("/root/patalacheckpoints")
REG = PATALA / "data/corpus/registries"
sys.path.insert(0, str(PATALA / "pipeline"))
import object_registry as R  # noqa: E402


def load_all(layer):
    return [v for oid, vs in R._load(layer)["objects"].items() for v in vs]


def parent_ref(layer, obj):
    oid = obj["object_id"]
    p = obj.get("payload", {})
    if layer in ("T1", "L0"):
        return [oid]
    if layer == "L1":
        return [oid]  # ref the L0 object by object_id
    if layer == "L1L2":
        return [oid]
    if layer == "L2":
        return [oid]  # ref the L1 object by object_id
    if layer == "L200":
        return [oid]  # ref the L2 object by object_id
    if layer == "C1":
        # ref the L200 object by its OBJECT_ID (kramasadbhava:v1), not the version string
        return [oid]
    return []


def main():
    # fix L200 dual-superseded (mark earlier dup superseded)
    for oid, vs in R._load("L200")["objects"].items():
        cur = [v for v in vs if not v.get("superseded")]
        if len(cur) > 1:
            for v in cur[:-1]:
                v["superseded"] = True
            R._save("L200", R._load("L200"))

    # build the list of works to link (those with EDUCATION, so the e2e customer path is linked)
    edu_works = set()
    for obj in load_all("EDUCATION"):
        for r in obj.get("input_refs") or []:
            # e.g. kramasadbhava:v3__arg__synth__essay -> extract kramasadbhava:v3
            if "__" in r:
                edu_works.add(r.split("__")[0])
    print(f"works with EDUCATION (the customer path): {sorted(edu_works)}")

    linked = 0
    for layer in ["T1", "L0", "L1", "L1L2", "L2", "L200", "C1"]:
        for obj in load_all(layer):
            if obj.get("superseded"):
                continue
            oid = obj["object_id"]
            work = oid.split(":")[0] if ":" in oid else oid
            # link C1/L200 always; link lower only for the customer-path works
            if layer not in ("C1", "L200") and work not in edu_works:
                continue
            refs = parent_ref(layer, obj)
            if not refs:
                continue
            if obj.get("input_refs") == refs:
                continue
            R.supersede(layer, oid)
            R.commit(layer, oid, R.input_hash(obj["payload"]), "link-derivation-chain",
                     status=obj.get("status", R.GENERATED), payload=obj["payload"], input_refs=refs)
            linked += 1
    print(f"\nlinked {linked} lower-chain objects (the audit trail from SOURCE up to C1)")


if __name__ == "__main__":
    main()
