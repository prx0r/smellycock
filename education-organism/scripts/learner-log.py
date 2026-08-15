#!/usr/bin/env python3
"""scripts/learner-log.py — BUILD-5: the data logging store.

Persists learner interactions (responses, blind grades, mastery, misconceptions) append-only + streamed.
This is the organism's sensory data: every learner event feeds the misconception graph + the flywheel.

Stores (all append-only / streamed, low-RAM):
  learner-events.jsonl   — every interaction (learner, question, grade, response)
  mastery-state.json     — per learner per concept (BKT-style mastery)
  misconceptions.jsonl   — wrong-answer -> known epistemic neighbor (the demand signal)
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "learner"
DATA.mkdir(parents=True, exist_ok=True)


def append_event(learner, question, grade, response, failure_type=""):
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ"), "learner": learner,
           "question": question, "grade": grade, "response": response,
           "failure_type": failure_type}
    with (DATA / "learner-events.jsonl").open("a") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fh.flush()
    return rec


def update_mastery(learner, concept, delta):
    p = DATA / "mastery-state.json"
    state = {}
    if p.exists():
        state = json.loads(p.read_text())
    m = state.setdefault(learner, {}).setdefault(concept, 0.0)
    state[learner][concept] = round(max(0.0, min(1.0, m + delta)), 3)
    p.write_text(json.dumps(state, indent=2))
    return state[learner][concept]


def record_misconception(wrong, correct, failure_type, n=1):
    p = DATA / "misconceptions.jsonl"
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ"), "wrong": wrong, "correct": correct,
           "failure_type": failure_type, "count": n}
    with p.open("a") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fh.flush()
    return rec


def summary():
    out = {}
    for f in ["learner-events.jsonl", "misconceptions.jsonl"]:
        p = DATA / f
        out[f] = sum(1 for _ in p.open()) if p.exists() else 0
    p = DATA / "mastery-state.json"
    out["mastery-state.json"] = len(json.loads(p.read_text())) if p.exists() else 0
    return out


if __name__ == "__main__":
    # a demo session: log 3 learner events + mastery + a misconception
    append_event("learner-0", "What is the order-less support?", "recalled", "the great Lord")
    append_event("learner-0", "Is the flashing the order?", "lapsed", "yes it is", "wrong_technical_sense")
    update_mastery("learner-0", "orderless_support", +0.1)
    update_mastery("learner-0", "orderless_support", -0.2)
    record_misconception("the flashing is the order", "the order-less support", "wrong_technical_sense")
    print("learner data logged:", json.dumps(summary(), indent=2))
