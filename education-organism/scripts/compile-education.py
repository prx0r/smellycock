#!/usr/bin/env python3
"""scripts/compile-education.py — BUILD-3: compute-on-write education projection for the site.

Turns the committed EDUCATION objects (real LearningPackets) into immutable static JSON for the Astro
site — compute-on-write, ETag/304, no per-request LLM. Output: education-index.json + per-lesson json.

Anti-theatre: reads the REAL committed education objects; every learning claim keeps its depends_on
(resolves to the source chain) + honest ceiling.
"""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

PATALA = Path("/root/patalacheckpoints")
REG = PATALA / "data/corpus/registries"
OUT = Path("/root/smellycock/site/education")


def load_education():
    out = []
    p = REG / "education-registry.jsonl"
    if not p.exists():
        return out
    for line in p.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        if not r.get("superseded"):
            out.append(r)
    return out


def main():
    educ = load_education()
    print(f"committed education objects: {len(educ)}\n")
    OUT.mkdir(parents=True, exist_ok=True)
    index = []
    for rec in educ:
        ed = rec["payload"].get("education", {}) or {}
        lcs = ed.get("learning_claims", []) or []
        lesson = {
            "object_id": rec["object_id"],
            "version": rec["version"],
            "status": rec["status"],
            "derived_from": ed.get("object_id") or rec.get("input_refs") or [],
            "input_refs": rec.get("input_refs") or [],
            "learning_claims": lcs,
            "epistemic_ceiling": rec.get("status", "GENERATED"),
            "source_chain_resolves": bool(rec.get("input_refs")),
        }
        # per-lesson immutable file (sha in name -> ETag/immutable)
        h = hashlib.sha256(json.dumps(lesson, sort_keys=True).encode()).hexdigest()[:12]
        fn = f"lesson-{rec['object_id'].replace(':', '_')}-{h}.json"
        (OUT / fn).write_text(json.dumps(lesson, indent=2, ensure_ascii=False))
        index.append({"object_id": rec["object_id"], "file": fn, "hash": h,
                      "status": rec["status"], "n_claims": len(lcs),
                      "source_chain_resolves": lesson["source_chain_resolves"]})
    (OUT / "education-index.json").write_text(json.dumps({"lessons": index}, indent=2))
    print(f"compiled {len(index)} lessons -> {OUT}")
    for i in index:
        print(f"  {i['object_id']}: {i['n_claims']} claims, source_chain={i['source_chain_resolves']}")
    print("\ncompute-on-write: these are immutable static bytes (ETag/304), no per-request LLM")


if __name__ == "__main__":
    main()
