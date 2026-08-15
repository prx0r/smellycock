#!/usr/bin/env python3
"""scripts/run-tests.py — the deterministic test suite (red-team fixed).

Fixes:
  - HIGH-7: tests now run the gates against the REAL committed registries, not just synthetic dicts.
    A regression test asserts that a junk (single-word) EDUCATION object FAILS quality.
  - LOW-13: the event-ledger tamper test operates on a TEMP COPY, never the live ledger.
"""
from __future__ import annotations
import json, os, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "kernels"))
import object_registry as R  # noqa: E402
import gates  # noqa: E402

RESULTS = []


def t(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))


def test_registry():
    t("registry loads + CANONICAL-DAG compiles", len(R.PREREQS) >= 5)
    t("event ledger verifies under the keyed scheme", R.verify_event_chain())


def test_ledger_tamper_on_temp_copy():
    """LOW-13: operate on a temp copy, never the live ledger."""
    src = R.REG_DIR / "object-events.jsonl"
    if not src.exists():
        t("ledger tamper (temp copy) — no ledger present", True, "skip")
        return
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / "events.jsonl"
        tmp.write_text(src.read_text())
        lines = tmp.read_text().splitlines()
        if len(lines) >= 2:
            mid = len(lines) // 2
            rec = json.loads(lines[mid])
            rec["event"]["x"] = "TAMPER"
            lines[mid] = json.dumps(rec)
            tmp.write_text("\n".join(lines) + "\n")
            # copy the ledger KEY into the temp dir too (verify reads the key from ROOT/data)
            import object_registry as _R
            key = _R.ROOT / "data" / ".ledger-key"
            if key.exists():
                (Path(td) / ".ledger-key").write_bytes(key.read_bytes())
            orig_root = _R.ROOT
            _R.ROOT = Path(td)
            detected = not _R.verify_event_chain()
            _R.ROOT = orig_root
            t("event ledger DETECTS tamper (temp copy)", detected)
        else:
            t("event ledger tamper (temp copy) — too few events", True, "skip")
    # live ledger untouched
    t("live ledger intact after test", R.verify_event_chain())


def test_gates():
    t("nyaya gate rejects unfalsifiable",
      gates.nyaya({"claim_text": "consciousness cannot be verified"})["verdict"] == "FAIL")
    t("nyaya gate accepts sound claim w/ falsifier",
      gates.nyaya({"claim_text": "memory requires the one who remembers", "pramana": "anumana",
                   "falsifier": "if memory did not persist"})["verdict"] == "PASS")
    # quality: junk vs real content (CRITICAL-2 regression)
    junk = {"layer": "EDUCATION", "payload": {"derived": {"EDUCATION": "Postgraduate"}}, "input_refs": ["c1"]}
    real = {"layer": "EDUCATION",
            "payload": {"derived": {"text": "The learner can distinguish an author's own commitment from an objection the author is reporting."}},
            "input_refs": ["c1"]}
    t("quality BLOCKs junk (single-word EDUCATION)", gates.quality(junk)[2] == "BLOCK")
    t("quality PASSes substantive content", gates.quality(real)[2] == "PASS")


def test_real_registries():
    """HIGH-7: run the gates against the REAL committed data."""
    # every committed object must have substantive content (quality's core check)
    empty_content = []
    for layer in R.LAYERS:
        for oid, r in gates.load_current(layer).items():
            txt = gates._content_text(r.get("payload", {}))
            if not txt:
                empty_content.append(f"{layer}:{oid}")
    t("every committed object has substantive content", not empty_content,
      str(empty_content[:3]))
    # chain gate on real data
    ok, fails = gates.chain()
    t("chain gate passes on real registries", ok, str(fails[:2]))


def test_organism_kernels():
    """The closed organism flywheel + ingestion organism (validated kernels)."""
    import sys as _s
    _s.path.insert(0, str(ROOT / "kernels"))
    import organism, misconception, pedagogy, staleness, ingestion_organism

    # 1. wrong-answer moat (education)
    from education import wrong_answer_to_neighbor
    def neighbors(c): return ["the order-less support", "the great Lord"]
    r = wrong_answer_to_neighbor("the order itself", "the flashing is not the order", neighbors)
    t("wrong-answer maps to a KNOWN epistemic neighbor", r.get("maps_to_epistemic_neighbor") is not None)

    # 2. misconception likelihood + flag
    m = misconception.Misconception("c1", "the order itself", cluster_size=40, persistence=7,
                                    ambiguity_signal=0.9, novice_rate=0.9)
    t("misconception flagged above threshold", m.flagged, f"likelihood={m.likelihood}")

    # 3. the closed repair cascade: flag -> RKA propagate -> dissolve
    dag = {"c1": {"requires": []}, "arg": {"requires": ["c1"]}, "essay": {"requires": ["arg"]}}
    cascade = misconception.MisconceptionRepairCascade(dag=dag, threshold=0.7)
    cascade.record("c1", "the order itself", cluster_size=40, persistence=7,
                   ambiguity_signal=0.9, novice_rate=0.9)
    flagged = cascade.flag_for_review()
    stale = cascade.propagate_fix("c1") if flagged else set()
    t("repair cascade RKA-propagates staleness downstream", len(stale) >= 2, str(sorted(stale)))
    if flagged:
        cascade.measure_dissolution("c1", cluster_size=40, persistence=8,
                                    ambiguity_signal=0.2, novice_rate=0.1)
        t("confusion dissolves after repair", cascade.summary()["dissolved"] >= 1)

    # 4. ingestion organism (priority + commit)
    org = ingestion_organism.IngestionOrganism()
    d = ingestion_organism.SanskritDoc("w", "Work", "gretil", rights="CC-BY-NC-SA")
    org.add(d, downstream=8, uncertainty=0.7, question_demand=4)
    org.run_one("w")
    t("ingestion organism commits a doc (rights + refine + verify)", org.ledger["w"].status == "committed")

    # 5. procedural memory (evolving-memory dream-cycle)
    from memory import ProceduralMemory, Trace
    mem = ProceduralMemory()
    mem.add_trace(Trace("t1", "orderless_support",
                        "the flashing has an order-less support, the great Lord, required by ordered experience.", access=5))
    mem.add_trace(Trace("t2", "orderless_support",
                        "so basically the flashing is not the order and there is this support thing which is complicated and people discuss it at length.", access=1))
    mem.add_trace(Trace("t3", "recognition", "recognition is the felt re-cognition of the self.", access=4))
    mem.dream_cycle()
    compacted = [c for c in mem.consolidated if c.get("compacted")]
    t("procedural memory compacts verbose low-access traces", len(compacted) >= 1)
    t("procedural memory persists high-value traces", len(mem.recall("orderless_support")) >= 2)

    # 6. GEM-A: segment-anchor keying
    from segment_key import make_segment_key, provenance_key, object_id_from_segment, segment_of
    seg = make_segment_key("kramasadbhava", "v1")
    t("GEM-A segment key is stable", seg == "kramasadbhava:v1")
    t("GEM-A provenance key is layer-scoped", provenance_key(seg, "EDUCATION").endswith(":lesson"))
    t("GEM-A object_id recovers the segment", segment_of("kramasadbhava:v1__argument") == "kramasadbhava:v1")

    # 7. GEM-C: reconciliation gate
    from reconciliation import reconciliation_check
    src = "The flashing has an order-less support, the great Lord, required by ordered experience."
    good = "<claim>The flashing has an order-less support, the great Lord, required by ordered experience.</claim>"
    corrupt = "The flashing has an order-less support."
    t("GEM-C reconciliation PASSes a source-preserving derivation", reconciliation_check(src, good)["pass"])
    t("GEM-C reconciliation BLOCKs a source-dropping derivation", not reconciliation_check(src, corrupt)["pass"])


def main():
    print("=== serveragent3 TEST SUITE (red-team fixed) ===")
    test_registry()
    test_ledger_tamper_on_temp_copy()
    test_gates()
    test_real_registries()
    test_organism_kernels()
    n = sum(RESULTS)
    print(f"\n=== SUMMARY: {n}/{len(RESULTS)} passed ===")
    sys.exit(0 if all(RESULTS) else 1)


if __name__ == "__main__":
    main()
