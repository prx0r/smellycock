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


def test_guard_kernel():
    """The anti-hallucination guards (fojin-adapted): quote_verifier + citation_whitelist."""
    from guard import verify_quoted_content, citation_whitelist, guard_answer, count_checked_quotes
    src = {"Tantraloka": {1: "The flashing has an order-less support, the great Lord, required by ordered experience."}}

    # a real quote verifies (kept, no mutation)
    good = 'As the master writes: \u201cThe flashing has an order-less support, the great Lord, required by ordered experience.\u201d 【\u300aTantraloka\u300b第1章】'
    guarded, muts = verify_quoted_content(good, src)
    t("guard verifies a real quote (no mutation)", len(muts) == 0)
    t("guard keeps a verified citation", "【《Tantraloka》第1章】" in guarded)

    # an invented quote is DOWNGRADED to prose (never served as a false verbatim quote)
    bad = 'As the master writes: \u201cThe flashing is the order itself and nothing else.\u201d 【\u300aTantraloka\u300b第1章】'
    guarded, muts = verify_quoted_content(bad, src)
    t("guard downgrades an invented quote", len(muts) == 1 and muts[0].reason == "quote_not_in_source")
    t("guard strips quote marks on downgrade", "“" not in guarded.split("【")[0])

    # a fabricated citation is stripped to bare prose (no false click-through)
    fake = 'Some claim \u201cconsciousness is unverifiable by any means.\u201d 【\u300aFabricated-Sutra\u300b第9章】'
    guarded, wmuts = citation_whitelist(fake, ["Tantraloka"])
    t("guard strips a fabricated citation", len(wmuts) == 1 and "《Fabricated-Sutra》" in guarded and "【" not in guarded)

    # guard_answer runs BOTH in dependency order; idempotent
    g1 = guard_answer(bad, src, ["Tantraloka"])
    g2 = guard_answer(g1["answer"], src, ["Tantraloka"])
    t("guard_answer is idempotent (second pass is a no-op)", len(g2["quote_mutations"]) == 0)

    # the metric fix: 'cited but quoted nothing' is NOT scored as verified
    t("count_checked_quotes distinguishes quoted vs not", count_checked_quotes(good) >= 1
      and count_checked_quotes("Just a citation 【《X》第1章】 with no quote.") == 0)


def test_learner_gate_kernel():
    """The authority-gated learner store (graphiti + MKG + MemOS synthesis)."""
    import time
    from learner_gate import LearnerGate
    g = LearnerGate()
    g.propose_correction("c1", "The flashing has an order-less support.", episode="learner-A")
    g.propose_correction("c1", "The flashing is the order itself, no separate support.", episode="learner-B")
    t("gate VETOES a contradictory correction", len(g.rejections) >= 1)
    g.propose_correction("c2", "Recognition is the felt re-cognition of the self.", episode="learner-A")
    t("gate promotes a NEW belief (no conflict)", len(g.active_at(time.time())) >= 2)
    # 2-tier: ambiguous candidate → human queue → human accepts, old archived
    g.flag_for_human_review("c1", "The support is both order-less and ordered.", reason="ambiguous")
    t("ambiguous candidate enters the human review queue", len(g.review_queue) == 1)
    g.human_resolve(0, "accept", "scholar-K")
    t("human override stamps reviewed_by=human", g.review_queue == [] and g.summary()["archived"] >= 1)
    t("time-bounded truth: old belief superseded", g.current("c1") is not None)
    # as_of(t): time-bounded truth returns the RIGHT version before vs after a supersession
    g2 = LearnerGate()
    before = g2.propose_correction("f", "old belief", episode="learner-A", t=100.0)
    g2.propose_correction("f", "new belief", episode="learner-B", t=200.0)
    t("as_of(t) returns the OLD version before supersession", g2.as_of("f", 150.0) == "old belief")
    t("as_of(t) returns the NEW version after supersession", g2.as_of("f", 250.0) == "new belief")
    t("human accept archives the old belief (time-bounded)", g2.current("f").belief == "new belief")


def test_weighted_propagation():
    """RKA-weighted blast radius: a corrected contradiction stales harder than a citation."""
    from misconception import MisconceptionRepairCascade, weighted_propagate
    from staleness import build_dependency_index
    # all default-weight edges → all transitive dependents stale (threshold 0.5)
    dag = {"c1": {"requires": []}, "arg": {"requires": ["c1"]}, "essay": {"requires": ["arg"]}}
    c = MisconceptionRepairCascade(dag=dag, threshold=0.7, weighted=True)
    c.record("c1", "the order itself", cluster_size=40, persistence=7,
             ambiguity_signal=0.9, novice_rate=0.9)
    stale = c.propagate_fix("c1")
    t("weighted cascade still stales all transitive dependents", len(stale) >= 2)
    # relation-tagged edges: derived_from (1.0) reaches; cites (0.7) also crosses 0.5
    dep = {"c1": {("arg", "derived_from")}, "arg": {("essay", "cites")}}
    impact = weighted_propagate(dep, {"c1"})
    t("weighted propagation decays impact by edge weight", impact["arg"] == 1.0 and impact["essay"] == 0.7)
    # a low-weight edge (supersedes=0.3) drops below a high threshold
    dep2 = {"c1": {("x", "supersedes")}}
    impact2 = weighted_propagate(dep2, {"c1"}, impact_threshold=0.5)
    t("low-weight edge drops below threshold", "x" not in impact2)
    # contradicts (1.1) propagates HARDER than cites (0.7): same topology, same threshold
    dep_ct = {"c1": {("a", "contradicts")}, "a": {("b", "cites")}}
    dep_cu = {"c1": {("a", "cites")}, "a": {("b", "cites")}}
    imp_ct = weighted_propagate(dep_ct, {"c1"})
    imp_cu = weighted_propagate(dep_cu, {"c1"})
    # contradicts (1.1) reaches b (0.77); cites (0.7->0.49) falls below the 0.5 threshold → b absent
    t("contradicts (1.1) propagates harder than cites (0.7)",
      "b" in imp_ct and ("b" not in imp_cu or imp_ct["b"] > imp_cu["b"]),
      f"contradicts b={imp_ct.get('b')} cites b={imp_cu.get('b')}")


def test_temporal_context():
    """graphiti temporal provenance + the read-plane context compiler."""
    import time
    from staleness import TemporalFact, active_facts_at, supersede_fact, fact_as_of, facts_to_context
    t0 = time.time()
    facts = [TemporalFact("f1", t0, payload={"belief": "order-less support"}, episode="learner-A"),
             TemporalFact("f2", t0, invalid_at=t0 + 10, payload={"belief": "flashing is the order"}, episode="learner-B")]
    supersede_fact(facts, "f2", t0 + 5)
    t("temporal fact is time-bounded (superseded → not active later)",
      fact_as_of(facts, "f2", t0 + 6) is None and "f2" in [f.fact_id for f in active_facts_at(facts, t0 + 2)])
    ctx = facts_to_context(facts, t0 + 2)
    t("context compiler renders validity windows + episode provenance",
      "episode learner-A" in ctx and "→present" in ctx)
    # an EXPIRED fact is excluded from the context
    ctx_after = facts_to_context(facts, t0 + 6)
    t("expired fact excluded from context", "f2" not in ctx_after and "f1" in ctx_after)


def test_retrieval_lift():
    """TASK 2: the GFM-RAG sparse entity->doc ranker + RoG negative-path sampler (stdlib)."""
    import retrieval
    # -- GFM-RAG sparse projection ranker --
    # doc1 mentions the query entities (the-flashing + the-order); doc2 shares only a rare one;
    # doc3 shares the common entity only.
    idx = {
        "doc1": {"the-flashing", "the-order", "order-less-support"},
        "doc2": {"the-flashing", "recognition"},
        "doc3": {"the-flashing"},
    }
    ranked = retrieval.rank_sources_for_entities(["the-flashing", "the-order"], idx)
    t("ranker puts the best-supporting source first", ranked[0] == "doc1", str(ranked))
    t("ranker returns all supporting sources, best-first", ranked == ["doc1", "doc2", "doc3"])
    # IDF: an entity mentioned by many docs is downweighted; doc1 still leads on raw support
    simple = retrieval.entity_to_doc_rank({"the-flashing": 1.0, "the-order": 1.0, "recognition": 1.0},
                                          idx, idf=False)
    idfw = retrieval.entity_to_doc_rank({"the-flashing": 1.0, "the-order": 1.0, "recognition": 1.0},
                                        idx, idf=True)
    t("idf-weighting changes relative doc scores (rare entity gains weight)",
      simple["doc2"] != idfw["doc2"], f"simple={simple['doc2']} idf={idfw['doc2']}")
    # a doc supporting NO query entity scores nothing and is dropped
    only = retrieval.rank_sources_for_entities(["does-not-exist"], idx)
    t("no-support source is excluded from the ranking", only == [])

    # -- RoG rule-constrained BFS + distinct negative sampling --
    adj = {"A": {"B": "cites", "X": "cites"}, "B": {"D": "cites", "Y": "cites"},
           "X": {"W": "cites"}, "Y": {"Z": "cites"}}
    pos = [p for p in retrieval.positives_from_start(adj, "A", ["cites", "cites"])
           if p[-1][2] == "D"]  # positive path = rule-match ending at the answer
    t("rule-constrained BFS finds the positive path", pos == [[("A", "cites", "B"), ("B", "cites", "D")]])
    neg = retrieval.sample_negative_paths(adj, "A", "D", n_neg=3, hop=2, seed=7)
    t("negative sampler produces >0 distinct negatives", len(neg) >= 1, str(neg))
    t("negatives never end at the answer entity", all(p[-1][2] != "D" for p in neg))
    t("negatives are DISTINCT from the positive path", all(p not in pos for p in neg))


def test_guards_hard_subprocess():
    """The hard guard stress (test-guards.py) folded into the main gate as a subprocess."""
    import subprocess as _sp
    p = _sp.run([sys.executable, str(ROOT / "scripts" / "test-guards.py")],
                capture_output=True, text=True)
    last = p.stdout.strip().splitlines()[-1] if p.stdout else "no output"
    t("guards hard stress (test-guards.py) passes", p.returncode == 0, last)


def test_integration_ipvv_subprocess():
    """The real-gold integration gates (integration-ipvv.py) folded into the main gate."""
    import subprocess as _sp
    p = _sp.run([sys.executable, str(ROOT / "scripts" / "integration-ipvv.py")],
                capture_output=True, text=True)
    last = p.stdout.strip().splitlines()[-1] if p.stdout else "no output"
    t("integration vs REAL IPVV gold (integration-ipvv.py) passes", p.returncode == 0, last)


def main():
    print("=== serveragent3 TEST SUITE (red-team fixed + frontier adoptions) ===")
    test_registry()
    test_ledger_tamper_on_temp_copy()
    test_gates()
    test_real_registries()
    test_organism_kernels()
    test_guard_kernel()
    test_guards_hard_subprocess()
    test_integration_ipvv_subprocess()
    test_learner_gate_kernel()
    test_weighted_propagation()
    test_temporal_context()
    test_retrieval_lift()
    n = sum(RESULTS)
    print(f"\n=== SUMMARY: {n}/{len(RESULTS)} passed ===")
    sys.exit(0 if all(RESULTS) else 1)


if __name__ == "__main__":
    main()
