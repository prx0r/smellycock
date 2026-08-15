#!/usr/bin/env python3
"""scripts/build-spine.py — the Hermes-driven POST-C1 spine build (generate -> gate -> commit).

PRODUCTION-GRADE (red-team fixed):
  - GATE EVERY LAYER before ENGINEERING_VALIDATED (CRITICAL-1): only a passing quality+layer gate
    promotes; otherwise GENERATED. A failing object is committed as GENERATED (honest), never EV.
  - MULTI-PARENT DAG eligibility (CRITICAL-4): a layer is derived for a C1 only when every required
    parent (per CANONICAL-DAG) is committed. Uses object_registry.eligible().
  - INPUT-HASH OF INPUTS (HIGH-5): derivation_hash over the parent records, not the output payload.
  - QUALITY GATE ON REAL CONTENT (CRITICAL-2): junk (single-word) content BLOCKs and is never EV.
  - AUTHORITY INVARIANT enforced by object_registry.commit (CRITICAL-3).
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "kernels"))
import object_registry as R  # noqa: E402
import gates  # noqa: E402
import generation  # noqa: E402

# layer -> the gate(s) that must pass to reach ENGINEERING_VALIDATED
LAYER_GATES = {
    "THEME": ("quality",),
    "ARGUMENT": ("quality", "nyaya", "cite"),
    "SYNTHESIS": ("quality", "chain"),
    "ESSAY": ("quality", "chain"),
    "EDUCATION": ("quality", "chain"),
}


def _layer_passes(layer: str, payload: dict, obj: dict) -> bool:
    """Run the layer's required gates on the fresh payload. All must pass for ENGINEERING_VALIDATED."""
    for gate_name in LAYER_GATES.get(layer, ("quality",)):
        if gate_name == "quality":
            _, _, verdict = gates.quality(obj)
            if verdict != "PASS":
                return False
        elif gate_name == "nyaya":
            a = payload.get("argument", {}) or payload.get("derived", {})
            concl = (a.get("conclusion", {}) or {}).get("text", "") if isinstance(a, dict) else ""
            g = gates.nyaya({"claim_text": concl, "pramana": "anumana",
                             "falsifier": (a.get("counterargument") if isinstance(a, dict) else None)})
            if g["verdict"] == "FAIL":
                return False
        elif gate_name == "cite":
            a = payload.get("argument", {}) or payload.get("derived", {})
            if isinstance(a, dict) and not a.get("conclusion", {}).get("source"):
                return False
        elif gate_name == "chain":
            ok, _ = gates.chain()
            if not ok:
                return False
    return True


def derive(layer: str, c1) -> dict:
    c = c1["payload"].get("c1", {})
    text = (c.get("summary") or c.get("evidence_quote") or c.get("claim") or "")[:400]
    system = (
        f"You are a Sanskrit philologist. Derive the {layer} from the given claim, strictly from its "
        "content. Give a SUBSTANTIVE multi-sentence answer (at least 30 words). Output ONLY JSON, no "
        "reasoning.")
    user = f"CLAIM: {text}\nOutput JSON for layer {layer}."
    for mt in (800, 1200):
        try:
            res = generation.generate_json(system, user, max_tokens=mt, timeout=120)
            if isinstance(res, dict) and res.get("_raw") == "":
                continue
            return res
        except Exception:
            time.sleep(2)
    return {"_raw": ""}


def build_layer(layer: str, eligible_c1s: list[str]) -> int:
    committed = 0
    for c1_oid in eligible_c1s:
        c1 = R.current("C1", c1_oid)
        if not c1:
            continue
        target = f"{c1_oid}__{layer.lower()}"
        res = derive(layer, c1)
        if not res or res.get("_raw") == "":
            print(f"  ✗ {layer} {target}: model empty — abstaining")
            continue
        payload = {"layer": layer, "source": c1_oid, "derived": res,
                   "derived_by": "model (generation.py)"}
        # provisional object for the gates
        obj = {"layer": layer, "payload": payload, "input_refs": [c1_oid]}
        # HIGH-5: input-hash over the parent record
        ih = R.derivation_hash([c1], f"{layer}:{c1_oid}")
        if R.is_committed(layer, target, ih):
            continue
        # CRITICAL-1: EV only if the layer's gates pass; else GENERATED (honest)
        status = R.ENGINEERING_VALIDATED if _layer_passes(layer, payload, obj) else R.GENERATED
        try:
            # authority invariant enforced inside commit (CRITICAL-3): if the parent floor is only
            # GENERATED, an upper EV is refused → fall back to GENERATED (honest, no over-claim).
            R.commit(layer, target, ih, "build-spine", status=status, payload=payload,
                     input_refs=[c1_oid])
        except ValueError:
            R.commit(layer, target, ih, "build-spine", status=R.GENERATED, payload=payload,
                     input_refs=[c1_oid])
            status = R.GENERATED
        committed += 1
        print(f"  ✓ {layer} {target}: committed ({status})")
    return committed


def main():
    if not generation.available():
        print("generation engine unavailable — fail-closed")
        sys.exit(1)
    total = 0
    for layer in ["THEME", "ARGUMENT", "SYNTHESIS", "ESSAY", "EDUCATION"]:
        # CRITICAL-4: only C1s whose required parents are all committed
        elig = R.eligible(layer)
        print(f"== {layer} (eligible C1s: {len(elig)}) ==")
        total += build_layer(layer, elig)
    print(f"\nDONE: +{total} objects committed")
    print(json.dumps(R.summary(), indent=2))


if __name__ == "__main__":
    main()
