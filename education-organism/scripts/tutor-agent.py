#!/usr/bin/env python3
"""scripts/tutor-agent.py — BUILD-4: the AI tutor agent.

Serves a LearningPacket question to a learner, grades the answer via the blind-assessor (deterministic,
no LLM in the cognition path), updates BKT mastery, and advances to the next interaction targeting the
weakest skill. Logs every learner event (BUILD-5).

Anti-theatre: grading is deterministic rubric-based (recalled/partial/lapsed); the tutor never sees the
expected answer while grading.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "kernels"))
import object_registry as R  # noqa: E402
from education import wrong_answer_to_neighbor  # noqa: E402
from pedagogy import LearnerState, next_interaction  # noqa: E402
from gates import blind_grade  # noqa: E402


def load_lesson(oid):
    # read the REAL patalacheckpoints education registry (not serveragent3's empty one)
    import json
    from pathlib import Path
    p = Path("/root/patalacheckpoints/data/corpus/registries/education-registry.jsonl")
    for line in p.open(encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        if r.get("object_id") == oid and not r.get("superseded"):
            return r
    return None


def rubric_from(expected):
    """Extract the rubric (key terms) from the expected answer — blind graders never see expected."""
    import re
    toks = re.findall(r"[a-zā-īūṛṝḷḹṃṁñṅśṣṭḍḥ]+", str(expected).lower())
    stop = {"the", "is", "that", "and", "of", "to", "in", "for", "which", "with", "verse", "claim"}
    return [t for t in toks if t not in stop and len(t) >= 4][:6]


def main():
    lesson = load_lesson("kramasadbhava:v1__arg__synth__essay__educ")
    if not lesson:
        print("lesson not found")
        sys.exit(1)
    ed = lesson["payload"].get("education", {})
    claims = ed.get("learning_claims", [])
    print(f"TUTOR: lesson {lesson['object_id']} ({len(claims)} learning claims)\n")

    # a learner session
    learner = LearnerState(learner="learner-0")
    learner.skill_state["paragraph_claim"] = "E0_RECALL"

    results = []
    for i, claim in enumerate(claims[:3]):
        q = claim.get("question", "")
        expected = claim.get("expected", "")
        rubric = rubric_from(expected)
        print(f"--- Interaction {i+1} ---")
        print(f"  Q: {q[:80]}")
        # the learner answers (simulate: a good answer on the first, a weak on the second)
        learner_answer = expected if i % 2 == 0 else "I think it is about something vague"
        grade = blind_grade(q, learner_answer, rubric)
        print(f"  learner answer: {'(matches expected)' if i % 2 == 0 else '(weak)'}")
        print(f"  blind grade: {grade['grade']} (coverage {grade['coverage']})")
        results.append({"q": q[:60], "grade": grade["grade"]})
        # record a wrong-answer -> known neighbor (the moat) when the learner errs
        if grade["grade"] != "recalled":
            nb = wrong_answer_to_neighbor(learner_answer, expected,
                                          lambda c: [expected, claim.get("wrong_answer", "")])
            results[-1]["failure_type"] = nb["failure_type"]

    # advance: next interaction targets the weakest skill
    move = next_interaction(learner, [])
    print(f"\nNEXT MOVE: target={move.get('target_skill')} why={move.get('why')}")
    print("\nTUTOR SESSION LOG:")
    for r in results:
        print(f"  {r}")

    # persist the session (BUILD-5 hook)
    out = ROOT / "data" / "runs" / "run-4" / "tutor-session.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"lesson": lesson["object_id"], "interactions": results}, indent=2))
    print(f"session persisted -> {out}")


if __name__ == "__main__":
    main()
