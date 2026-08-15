#!/usr/bin/env python3
"""scripts/seed-c1.py — ingest a grounded C1 floor (real IPVV content).

Seeds the serveragent3 registry with real grounded C1s (from the IPVV knowledge core / published
passages) so the POST-C1 spine has a real floor. Deterministic. Anti-theatre: carries evidence_quote.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "kernels"))
import object_registry as R  # noqa: E402

# real IPVV C1s from server3 (grounded floor)
IPVV = Path("/root/patalacheckpoints/data/published/ipvv")


def load_real_c1s():
    out = []
    for f in sorted(IPVV.glob("pt-passage-ipvv-*.json"))[:10]:
        try:
            d = json.load(open(f))
        except Exception:
            continue
        c1 = d.get("c1", {}) or {}
        body = c1.get("body") or ""
        if not body:
            continue
        pid = d.get("immutable_id") or f.stem
        oid = f"ipvv:{pid.split(':')[-1]}" if ":" in pid else f"ipvv-{pid}"
        payload = {"c1": {
            "summary": body[:200],
            "explanation": body[:400],
            "boundary": "passage-local IPVV commentary",
            "key_terms": [{"term": t.strip(), "meaning": ""} for t in str(c1.get("terms", "")).split("·") if t.strip()][:6],
            "related_passages": [s.strip() for s in str(c1.get("see_also", "")).split("·") if s.strip()],
            "evidence_quote": body[:200],
            "claim": body[:150],
            "passage_id": pid,
        }, "c1_status": "MACHINE_PROPOSED", "derived_by": "seed-c1"}
        if R.is_committed("C1", oid, R.input_hash(payload)):
            continue
        # red-team MEDIUM-10: the floor is NOT auto-promoted — commit as GENERATED/MACHINE_PROPOSED
        # (no gate ran; EV requires a real gate + human review). Consistent: registry GENERATED ==
        # object c1_status MACHINE_PROPOSED.
        R.commit("C1", oid, R.input_hash(payload), "seed-c1", status=R.GENERATED,
                 payload=payload, input_refs=[pid])
        out.append(oid)
    return out


if __name__ == "__main__":
    seeded = load_real_c1s()
    print(f"seeded {len(seeded)} grounded C1s")
    print(json.dumps(R.summary(), indent=2))
