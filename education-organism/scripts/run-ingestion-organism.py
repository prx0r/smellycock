#!/usr/bin/env python3
"""scripts/run-ingestion-organism.py — the priority-driven refinery (sense→commit→feedback).

Wires ingestion_organism.py (the validated refinery): a Sanskrit doc enters the priority queue
(next_action formula), is ingested (rights check), refined through the LAYERS chain, verified (integrity
gate), committed, then a learner probe re-prioritizes. Demonstrates the organism's "attention"
recomputes each cycle. Deterministic, gated, versioned, append-only ledger.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "kernels"))
import ingestion_organism  # noqa: E402


def main():
    org = ingestion_organism.IngestionOrganism()
    # SENSE + PRIORITIZE: two works, one with high downstream load + question demand
    doc_a = ingestion_organism.SanskritDoc("tantraloka-ahnika-1", "Tantraloka Ahnika 1",
                                           "gretil", rights="CC-BY-NC-SA", tradition="kashmir_shaivism")
    doc_b = ingestion_organism.SanskritDoc("cidgaganacandrika-10", "Cidgaganacandrika cont 10",
                                           "muktabodha", rights="CC-BY-NC-SA", tradition="trika")
    org.add(doc_a, downstream=8, uncertainty=0.7, question_demand=4, review_deficit=2)
    org.add(doc_b, downstream=3, uncertainty=0.4, question_demand=1, review_deficit=0)
    print("PRIORITY QUEUE (the organism's attention, recomputed):")
    for q in org.queue():
        print(f"  {q['work']} prio={q['priority']} status={q['status']}")

    # INGEST -> REFINE -> VERIFY -> COMMIT one doc through the whole chain
    print("\nRUN ONE doc through the organism:")
    result = org.run_one("tantraloka-ahnika-1")
    print(f"  tantraloka-ahnika-1: {result}")

    # FEEDBACK: a learner probe re-prioritizes (raises question-demand)
    print("\nLEARNER PROBE (consumer-as-sensor feedback):")
    org.learner_probe("cidgaganacandrika-10", "why does the pulse precede differentiation?")
    for q in org.queue():
        print(f"  {q['work']} prio={q['priority']} status={q['status']}")

    # the append-only ledger (the organism's event-log truth)
    print(f"\nevent log (append-only): {len(org.event_log)} events")

    report = {"queue": org.queue(), "run_one": result,
              "events": len(org.event_log),
              "ledger": {k: {"status": v.status, "layers": v.layers_done} for k, v in org.ledger.items()}}
    out = ROOT / "data" / "runs" / "run-3" / "ingestion-organism.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, default=str))
    print(f"report -> {out}")


if __name__ == "__main__":
    main()
