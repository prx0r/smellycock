#!/usr/bin/env python3
"""scripts/test-e2e.py — BUILD-6: the end-to-end audit trail test (source → customer).

Proves the organism works on REAL data: an EDUCATION claim → the AI tutor serves it → a learner answers
→ blind-grade + log → then trace the claim ALL THE WAY back to SOURCE. This is the audit trail from
source material through L0 to the customer.

Anti-theatre: every object is a REAL committed record; the resolution walks the real chain; nothing is
hand-fed.
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "kernels"))
import object_registry as R  # noqa: E402
from gates import blind_grade  # noqa: E402

PATALA = Path("/root/patalacheckpoints")
REG = PATALA / "data/corpus/registries"
RESULTS = []


def t(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


def read_layer(layer, oid):
    p = REG / f"{layer.lower()}-registry.jsonl"
    if not p.exists():
        return None
    for line in p.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("object_id") == oid and not r.get("superseded"):
            return r
    return None


def resolve_to_source(object_id):
    """Walk EDUCATION→ESSAY→...→C1 via refs, then the bare id down to SOURCE."""
    # upper: follow input_refs/depends_on to find the bare C1 base
    def find_base(oid, seen):
        if oid in seen:
            return None
        seen.add(oid)
        if "__" not in oid:
            return oid  # bare work:verse = the C1 floor
        for layer in ["EDUCATION", "ESSAY", "SYNTHESIS", "ARGUMENT", "THEME"]:
            r = read_layer(layer, oid)
            if not r:
                continue
            refs = list(r.get("input_refs") or [])
            for lc in (r.get("payload", {}).get("education", {}) or {}).get("learning_claims", []):
                refs += list(lc.get("depends_on") or [])
            for sec in (r.get("payload", {}).get("essay", {}) or {}).get("sections", []):
                for par in sec.get("paragraphs", []):
                    refs += list(par.get("depends_on") or [])
            for ref in refs:
                b = find_base(ref, seen)
                if b:
                    return b
        return None
    base = find_base(object_id, set())
    if not base:
        return []
    # lower: the bare id through SOURCE..C1
    chain = []
    for layer in ["C1", "L200", "L2", "L1", "L0", "T1", "SOURCE"]:
        if read_layer(layer, base):
            chain.append((layer, base))
    return chain


def main():
    print("=== E2E AUDIT TRAIL: source → L0 → ... → EDUCATION → customer ===\n")
    # pick a real education object from the REAL patalacheckpoints registry
    educ = []
    for line in (REG / "education-registry.jsonl").open():
        r = json.loads(line)
        if not r.get("superseded"):
            educ.append(r["object_id"])
    if not educ:
        print("no education objects")
        sys.exit(1)
    oid = educ[0]
    lesson = read_layer("EDUCATION", oid)
    t("EDUCATION object committed", lesson is not None, oid)
    claims = (lesson["payload"].get("education", {}) or {}).get("learning_claims", [])
    t("EDUCATION has real learning claims", len(claims) > 0, f"{len(claims)} claims")

    # 1. the tutor serves a question + grades (no LLM in path)
    claim = claims[0]
    q, expected = claim.get("question", ""), claim.get("expected", "")
    import re
    rubric = [t for t in re.findall(r"[a-zā-īūṛṝḷḹṃṁñṅśṣṭḍḥ]+", str(expected).lower())
              if len(t) >= 4][:6]
    grade = blind_grade(q, expected, rubric)
    t("tutor serves a question + blind-grades a good answer", grade["grade"] == "recalled")

    # 2. log the learner event
    import hashlib
    ev = {"ts": time.time(), "learner": "e2e-test", "question": q[:40], "grade": grade["grade"]}
    (ROOT / "data/learner/learner-events.jsonl").open("a").write(json.dumps(ev, ensure_ascii=False) + "\n")
    t("learner event logged (append-only)", (ROOT / "data/learner/learner-events.jsonl").exists())

    # 3. THE AUDIT TRAIL: trace this education claim back to SOURCE
    chain = resolve_to_source(oid)
    print("\n  AUDIT TRAIL:")
    for layer, ref in chain:
        print(f"    {layer:8s} {ref}")
    t("education claim resolves to SOURCE (full audit trail)",
      any(l == "SOURCE" for l, _ in chain), f"{len(chain)} layers")

    n = sum(RESULTS)
    print(f"\n=== E2E: {n}/{len(RESULTS)} passed ===")
    sys.exit(0 if all(RESULTS) else 1)


if __name__ == "__main__":
    main()
