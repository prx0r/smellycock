#!/usr/bin/env python3
"""kernels/progress.py — the DERIVED progress reducer (sanskrithelp navigator pattern).

The profile-as-data realization: progress is NOT stored — it's DERIVED from the granular event stream.
This reducer computes the sanskrithelp-style progress view:
  zone_levels       — mastered level per zone (from assessments passed)
  retry_counts      — how many times a zone+level was attempted/failed (3 → remedial)
  weekly_arc        — a weekly plan: which zones to advance, one session per day
  streak            — consecutive days with activity

This is the "whole-site tracking of progress" — a PLAN (weekly arc) derived from events, not a stored
number. Deterministic + stdlib. Reads the EventStream.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class LearnerProgress:
    user_id: str
    zone_levels: dict = field(default_factory=dict)      # zone -> mastered level
    retry_counts: dict = field(default_factory=dict)     # {zone_level: n}
    weekly_arc: list = field(default_factory=list)       # the 7-day plan
    streak_days: int = 0
    zones: dict = field(default_factory=dict)            # zone metadata
    # the discrete mastery projection (Khan style — from LEARNER-PROFILE-RESEARCH.md):
    # map continuous BKT mastery (0..1) to human-readable levels, NOT raw probabilities.
    mastery_levels: dict = field(default_factory=dict)   # skill -> 'Practiced'|'Level 1'|'Level 2'|'Mastered'

    def to_dict(self):
        return {"user_id": self.user_id, "zone_levels": self.zone_levels,
                "retry_counts": self.retry_counts, "weekly_arc": self.weekly_arc,
                "streak_days": self.streak_days, "mastery_levels": self.mastery_levels}


# the discrete mastery projection (Khan Mastery-1/2/3 pattern)
def mastery_level(p: float) -> str:
    """Map a continuous BKT mastery probability to a discrete, human-readable level.

    <0.3 Practiced (seen) · 0.3-0.5 Level 1 · 0.5-0.7 Level 2 · 0.7-0.85 Level 3 · >=0.85 Mastered.
    Learners/users read LEVELS, not raw probabilities (Khan's canonical design)."""
    if p >= 0.85:
        return "Mastered"
    if p >= 0.7:
        return "Level 3"
    if p >= 0.5:
        return "Level 2"
    if p >= 0.3:
        return "Level 1"
    return "Practiced"


class ProgressReducer:
    """Reduce the event stream → LearnerProgress (the derived, not-stored view)."""

    def __init__(self, events=None):
        self.events = events

    def reduce(self, user_id: str, *, zones: dict | None = None) -> LearnerProgress:
        """Derive progress from the event stream."""
        p = LearnerProgress(user_id=user_id, zones=zones or {})
        # read the events
        learner_events = self.events.learner_events_for(user_id) if self.events else []
        assessments = [dict(r) for r in self.events.con.execute(
            "SELECT * FROM assessments WHERE learner=? ORDER BY ts", (user_id,)).fetchall()] if self.events else []

        # zone_levels from passed assessments
        for a in assessments:
            zone, level = a.get("zone", ""), a.get("level", 0)
            if a.get("passed") and zone and level > p.zone_levels.get(zone, 0):
                p.zone_levels[zone] = level
            elif not a.get("passed") and zone:
                key = f"{zone}_{level}"
                p.retry_counts[key] = p.retry_counts.get(key, 0) + 1

        # streak: consecutive days with learner activity
        if learner_events:
            days = {datetime.fromtimestamp(e["ts"], tz=timezone.utc).date() for e in learner_events if e.get("ts")}
            p.streak_days = self._streak(days)

        # discrete mastery levels (Khan style): derive a per-skill probability from grades, then
        # project to a human-readable level (NOT raw BKT output).
        skill_ps = {}
        for e in learner_events:
            skill = e.get("skill") or e.get("content") or ""
            if not skill:
                continue
            grade = e.get("grade", "partial")
            # a simple mastery accumulator: recalled +0.2, partial +0.0, lapsed -0.1, clamped [0,1]
            delta = 0.2 if grade == "recalled" else (-0.1 if grade == "lapsed" else 0.0)
            skill_ps[skill] = max(0.0, min(1.0, skill_ps.get(skill, 0.3) + delta))
        p.mastery_levels = {s: mastery_level(prob) for s, prob in skill_ps.items()}

        # weekly arc: plan next advances (sanskrithelp navigator pattern)
        p.weekly_arc = self._weekly_arc(p)
        return p

    def _streak(self, days) -> int:
        if not days:
            return 0
        today = datetime.now(timezone.utc).date()
        n = 0
        d = today
        while d in days:
            n += 1
            d -= timedelta(days=1)
        return n

    def _weekly_arc(self, p: LearnerProgress) -> list:
        """Build a 7-day plan: advance each zone ~2 levels, one session per day."""
        if not p.zones:
            return []
        ordered = sorted(p.zones.items(), key=lambda x: x[1].get("order", 99))
        goals = []
        for zone, meta in ordered:
            current = p.zone_levels.get(zone, 0)
            max_level = meta.get("level_count", 5)
            if current < max_level:
                goals.append({"zone": zone, "from_level": current,
                              "to_level": min(current + 2, max_level),
                              "focus": meta.get("label", zone)})
        slots = []
        for day in range(7):
            if goals:
                g = goals[day % len(goals)]
                slots.append({"day": day, "zone": g["zone"],
                              "level": g["from_level"] + 1, "focus": g["focus"]})
        return slots


if __name__ == "__main__":
    from events import EventStream
    es = EventStream()
    # a learner who passed kriya lvl 1-2, failed lvl 3 once
    es.assessment("learner-1", zone="kriya", level=1, rubric_score=0.9, passed=True)
    es.assessment("learner-1", zone="kriya", level=2, rubric_score=0.8, passed=True)
    es.assessment("learner-1", zone="kriya", level=3, rubric_score=0.5, passed=False)
    es.learner_event("learner-1", skill="kriya", grade="lapsed", content="kriya lvl 3")
    zones = {"kriya": {"order": 1, "label": "The action-power", "level_count": 5},
             "jnana": {"order": 2, "label": "The knowledge-power", "level_count": 4}}
    prog = ProgressReducer(es).reduce("learner-1", zones=zones)
    print("=== DERIVED PROGRESS (from the event stream) ===")
    print("  zone_levels:", prog.zone_levels)
    print("  retry_counts:", prog.retry_counts)
    print("  weekly_arc:")
    for s in prog.weekly_arc[:3]:
        print(f"    day {s['day']}: {s['focus']} level {s['level']}")
    print("  streak_days:", prog.streak_days)
