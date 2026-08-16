#!/usr/bin/env python3
"""kernels/events.py — the granular EVENT STREAM (the user-profile-as-data foundation).

The realization (PROFILE-AS-DATA.md): the user profile is NOT a stored row — it's a DERIVED projection
over an append-only stream of granular learner events. This is the `ReviewEvent[] → DerivedState`
pattern applied to learners.

The event stream is the ONLY stored truth. Every learner action across games/media/content/lessons is
one event. Everything else (mastery, progress, profile, demand) is a recomputable projection.

Event types:
  learner_event  — a graded answer (skill, content, grade, failure_type, surface, session)
  game_event     — a game played (game, format, score, outcome, difficulty, ai_layer)
  assessment     — a session assessed (zone, level, rubric_score, passed, feedback)
  media_event    — media consumed (media_id, type, duration)

Deterministic + stdlib. Append-only, streamed (never bulk-loaded). SQLite.
"""
from __future__ import annotations
import json
import sqlite3
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "events.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS learner_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts REAL, learner TEXT, skill TEXT, content TEXT,
  grade TEXT, response TEXT, failure_type TEXT, surface TEXT, session_id TEXT
);
CREATE TABLE IF NOT EXISTS game_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts REAL, learner TEXT, game TEXT, format TEXT,
  score INTEGER, outcome TEXT, difficulty REAL, ai_layer INTEGER, content TEXT
);
CREATE TABLE IF NOT EXISTS assessments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts REAL, learner TEXT, zone TEXT, level INTEGER,
  rubric_score REAL, passed INTEGER, feedback TEXT
);
CREATE TABLE IF NOT EXISTS media_events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts REAL, learner TEXT, media_id TEXT, type TEXT, duration REAL
);
CREATE INDEX IF NOT EXISTS idx_le_learner ON learner_events(learner, ts);
CREATE INDEX IF NOT EXISTS idx_ge_learner ON game_events(learner, ts);
CREATE INDEX IF NOT EXISTS idx_as_learner ON assessments(learner, ts);
"""


class EventStream:
    """The append-only granular event stream (the truth behind every profile)."""

    def __init__(self, db: str | Path = DB):
        self.db = Path(db)
        self.db.parent.mkdir(parents=True, exist_ok=True)
        self.con = sqlite3.connect(str(self.db), check_same_thread=False)
        self.con.row_factory = sqlite3.Row
        self.con.executescript(SCHEMA)
        self.con.commit()

    # ── append events (the only writes) ────────────────────────────────────
    def learner_event(self, learner, *, skill="", content="", grade="partial",
                      response="", failure_type="", surface="", session_id="") -> int:
        cur = self.con.execute(
            "INSERT INTO learner_events(ts, learner, skill, content, grade, response, failure_type, surface, session_id) "
            "VALUES(?,?,?,?,?,?,?,?,?)",
            (time.time(), learner, skill, content, grade, response, failure_type, surface, session_id))
        self.con.commit()
        return cur.lastrowid

    def game_event(self, learner, *, game="", format="", score=0, outcome="",
                   difficulty=0.5, ai_layer=0, content="") -> int:
        cur = self.con.execute(
            "INSERT INTO game_events(ts, learner, game, format, score, outcome, difficulty, ai_layer, content) "
            "VALUES(?,?,?,?,?,?,?,?,?)",
            (time.time(), learner, game, format, score, outcome, difficulty, ai_layer, content))
        self.con.commit()
        return cur.lastrowid

    def assessment(self, learner, *, zone="", level=1, rubric_score=0.0, passed=False,
                   feedback="") -> int:
        cur = self.con.execute(
            "INSERT INTO assessments(ts, learner, zone, level, rubric_score, passed, feedback) "
            "VALUES(?,?,?,?,?,?,?)",
            (time.time(), learner, zone, level, rubric_score, 1 if passed else 0, feedback))
        self.con.commit()
        return cur.lastrowid

    def media_event(self, learner, *, media_id="", type="", duration=0.0) -> int:
        cur = self.con.execute(
            "INSERT INTO media_events(ts, learner, media_id, type, duration) VALUES(?,?,?,?,?)",
            (time.time(), learner, media_id, type, duration))
        self.con.commit()
        return cur.lastrowid

    # ── read the stream (for the derived reducers) ─────────────────────────
    def learner_events_for(self, learner, limit=200):
        return [dict(r) for r in self.con.execute(
            "SELECT * FROM learner_events WHERE learner=? ORDER BY ts LIMIT ?", (learner, limit)).fetchall()]

    def game_events_for(self, learner, limit=100):
        return [dict(r) for r in self.con.execute(
            "SELECT * FROM game_events WHERE learner=? ORDER BY ts LIMIT ?", (learner, limit)).fetchall()]

    def all_events(self, learner):
        return {"learner_events": self.learner_events_for(learner),
                "game_events": self.game_events_for(learner)}

    def counts(self):
        return {t: self.con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
                for t in ("learner_events", "game_events", "assessments", "media_events")}


if __name__ == "__main__":
    es = EventStream()
    es.learner_event("learner-1", skill="vimarśa", content="svācchandya",
                     grade="recalled", response="the spontaneity of the Lord", surface="game")
    es.game_event("learner-1", game="millionaire", format="question", score=100,
                  outcome="correct", difficulty=0.3, content="svācchandya")
    es.assessment("learner-1", zone="kriya", level=1, rubric_score=0.85, passed=True,
                  feedback="solid understanding of the action-power")
    es.media_event("learner-1", media_id="ipvv:v3a", type="read", duration=240)
    print("event stream counts:", es.counts())
    print("learner-1 events:", len(es.learner_events_for("learner-1")))
