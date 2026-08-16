#!/usr/bin/env python3
"""kernels/conductor.py — the SESSION CONDUCTOR (sanskrithelp pattern, closes the loop).

The conductor is the brain that closes the organism loop:
  profile → pick a game/content/session → conduct turns → assess (Hermes rubric) → emit events → re-derive progress

This is the sanskrithelp `conductor.py` pattern adapted to our organism: objective-driven sessions with
retry-then-remedial, over OUR games + content packs.

The loop (fully closed):
  LearnerProgress (zone_levels/arc)
    → conductor picks the next session (the weekly arc's next slot)
    → projects a game over a content pack (the projection)
    → the learner answers
    → assess (Hermes rubric; .py fallback)
    → emit a learner_event + assessment to the EventStream
    → re-derive LearnerProgress → the profile updates → next session

Deterministic loop + Hermes for the rubric assessment. The events are the truth; everything is derived.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 3 retries then remedial (sanskrithelp rule)
MAX_RETRIES = 3


@dataclass
class Session:
    session_id: str
    user_id: str
    zone: str
    level: int
    objective: str
    game: str
    content: str
    challenge: str
    status: str = "pending"


class Conductor:
    """Run objective-driven sessions; conduct turns, assess, update progress, retry-then-remedial."""

    def __init__(self, events, progress_reducer, studio=None):
        self.events = events
        self.progress = progress_reducer
        self.studio = studio

    def next_session(self, user_id: str, *, zones: dict | None = None) -> Session | dict:
        """Pick the next session from the weekly arc (the plan → next move)."""
        prog = self.progress.reduce(user_id, zones=zones)
        arc = prog.weekly_arc
        if not arc:
            return {"note": "all zones complete — no next session"}
        slot = arc[0]  # today's slot (the plan's first)
        zone, level = slot["zone"], slot["level"]
        # retry-then-remedial: if this level has been failed MAX_RETRIES, offer remedial
        key = f"{zone}_{level}"
        if prog.retry_counts.get(key, 0) >= MAX_RETRIES:
            return {"remedial": True,
                    "message": "3 attempts failed — review prerequisite material first",
                    "zone": zone, "level": level,
                    "next": self._prerequisite_zone(zones, zone)}
        # project a game over a content pack (if studio given)
        challenge = ""
        if self.studio:
            ch = self.studio.play("ipvv", "textlogic", "crux_hunt")
            challenge = getattr(ch, "prompt", str(ch))[:80]
        return Session(session_id=f"{user_id}_{zone}_{level}_{__import__('time').time()}",
                       user_id=user_id, zone=zone, level=level,
                       objective=f"master {zone} level {level}", game="textlogic",
                       content=zone, challenge=challenge)

    def conduct_and_assess(self, session: Session, answer: str, *, rubric_score: float = 0.0,
                           passed: bool = False, feedback: str = "") -> dict:
        """Record the turn: emit a learner_event + assessment, return the updated state."""
        # emit the learner event (the granular truth)
        self.events.learner_event(session.user_id, skill=session.zone, content=session.content,
                                  grade="recalled" if passed else "lapsed",
                                  response=answer, surface="session", session_id=session.session_id)
        # emit the assessment (rubric score → progress)
        self.events.assessment(session.user_id, zone=session.zone, level=session.level,
                               rubric_score=rubric_score, passed=passed, feedback=feedback)
        # re-derive progress (the loop closes)
        prog = self.progress.reduce(session.user_id)
        return {"session": session.session_id, "passed": passed, "feedback": feedback,
                "zone_levels": prog.zone_levels, "retries": prog.retry_counts,
                "next": self.next_session(session.user_id).session_id if hasattr(self.next_session(session.user_id), "session_id") else "done"}

    def _prerequisite_zone(self, zones, zone):
        return (zones or {}).get(zone, {}).get("prerequisites", [])


if __name__ == "__main__":
    from events import EventStream
    from progress import ProgressReducer
    es = EventStream()
    prog = ProgressReducer(es)
    cond = Conductor(es, prog)
    zones = {"kriya": {"order": 1, "label": "The action-power", "level_count": 5},
             "jnana": {"order": 2, "label": "The knowledge-power", "level_count": 4}}
    print("=== THE CONDUCTOR (the closed loop) ===")
    s = cond.next_session("learner-1", zones=zones)
    print("  next session:", s.objective if hasattr(s, "objective") else s)
    if hasattr(s, "session_id"):
        r = cond.conduct_and_assess(s, "the action-power manifests order", rubric_score=0.85, passed=True,
                                    feedback="solid")
        print("  after assess:", {k: v for k, v in r.items() if k != "next"})
        print("  zone_levels now:", r["zone_levels"])
