# USER PROFILE AS DATA — brainstorming the granular progress model

*2026-08-15 · What is the user profile actually, as data? And how do we track granular progress through
the whole system (games, content, media)? Synthesized from: our current store, sanskrithelp's
conductor/navigator/profile, and the organism vision.*

---

## 1. THE REALIZATION: the profile is DERIVED, not stored

The vision (educationmain §9) is explicit: **the profile is derived from MasteryEvidence[] events, never
mutated directly.** It's the `ReviewEvent[] → DerivedState` pattern. So:

> The user profile is NOT a row you update. It's a **derived projection over a stream of granular events**.

This is the key architectural truth. You don't store "Tom knows prakāśa = 0.84." You store the EVENTS
that let you compute it.

---

## 2. THE GRANULAR EVENT STREAM (what actually gets tracked)

Every learner action is a tiny event. The granular data:

### The event types
```
LEARNER_EVENT   {ts, learner, question, grade(recalled/partial/lapsed), response, failure_type, skill, surface}
INQUIRY         {ts, learner, question, answer, surface, object_ids}
GAME_EVENT      {ts, learner, game, format, score, outcome, difficulty, ai_layer}
ASSESSMENT      {ts, learner, zone, level, rubric_score, passed, feedback}
MEDIA_EVENT     {ts, learner, media_id, type, watched/read, duration}
```

### The dimensions each event carries
| Dimension | What it tracks |
|---|---|
| **skill** | which skill axis (recall/argument/crux/grounding) |
| **content** | which concept/zone/lesson |
| **grade** | the outcome (recalled/partial/lapsed) |
| **failure_type** | the misconception mapped (wrong-answer→neighbor) |
| **surface** | where (game/lesson/media/api) |
| **session** | which session/arc |
| **timestamp** | when (for the longitudinal curve) |

---

## 3. THE DERIVED LAYERS (what you compute from the events)

```
EVENT STREAM (append-only, the truth)
  └── derived view 1: MASTERY     (BKT P(mastery) per skill×content)
  └── derived view 2: PROGRESS    (zone_levels, weekly arc, retry counts)  ← sanskrithelp navigator
  └── derived view 3: PROFILE     (UserKnowledgeState: interests, confusions, depth)  ← the personalizer
  └── derived view 4: DEMAND      (question clusters → the organism's research signal)
  └── derived view 5: TRAJECTORY  (the longitudinal learning curve over time)
```

The events are the ONLY stored truth. Everything else is a recomputable projection. This is the
`object_registry` + `ReviewEvents → DerivedState` pattern applied to learners.

---

## 4. THE USER PROFILE AS DATA (the full shape)

```json
UserKnowledgeState {
  identity:    {user_id, created_at, preferred_depth, tradition_scope}
  mastery:     {skill×concept: {P(mastery), evidence_level(E0-E8), last_seen}}
  progress:    {zone_levels: {zone: level}, retry_counts, weekly_arc, streak}
  confusions:  [{wrong, correct, failure_type, count, first/last_seen}]
  interests:   {topic: engagement_strength}
  trajectory:  [{ts, skill, level}]     // the learning curve
  sessions:    [{session_id, arc, daily_slot, outcomes}]
}
```

**The profile is the aggregation of: mastery (BKT) + progress (zones/arc) + confusions + interests +
trajectory + sessions.** It's the central node that games/content/media read.

---

## 5. THE GRANULAR TRACKING MODEL (the schema)

```sql
-- THE EVENT STREAM (append-only truth)
CREATE TABLE learner_events (
  id INTEGER PRIMARY KEY, ts REAL, learner TEXT,
  skill TEXT, content TEXT, grade TEXT,      -- recalled/partial/lapsed
  response TEXT, failure_type TEXT, surface TEXT, session_id TEXT
);
CREATE TABLE game_events (
  id INTEGER PRIMARY KEY, ts REAL, learner TEXT,
  game TEXT, format TEXT, score INTEGER, outcome TEXT,
  difficulty REAL, ai_layer INTEGER, content TEXT
);
CREATE TABLE assessments (
  id INTEGER PRIMARY KEY, ts REAL, learner TEXT,
  zone TEXT, level INTEGER, rubric_score REAL, passed INTEGER, feedback TEXT
);
CREATE TABLE media_events (
  id INTEGER PRIMARY KEY, ts REAL, learner TEXT,
  media_id TEXT, type TEXT, duration REAL
);

-- THE DERIVED LAYER (recomputed from events)
CREATE TABLE derived_progress (
  user_id TEXT, zone TEXT, level INTEGER, retries INTEGER, last_updated REAL
);
```

---

## 6. WHAT THIS UNLOCKS

1. **Whole-site progress** — one event stream across games/media/content/lessons → one coherent profile
   (sanskrithelp's `weekly_arc` + `zone_levels` over OUR content).
2. **The closed loop** — an event → re-derive profile → personalizer picks next game/content → event.
3. **The organism** — the event stream IS the demand signal (misconceptions → source-repair).
4. **Honesty** — the profile is always a recomputable projection of real events, never a stale stored
   number. Per the anti-theatre doctrine.

---

## 7. THE NEXT BUILD (what I'm implementing)

1. **The event-stream schema** (above) — store every learner action as a granular event.
2. **The derived-progress reducer** — compute zone_levels + weekly_arc (sanskrithelp navigator pattern)
   from the events.
3. **The conductor** — a session loop: profile → pick game/content → conduct → assess (Hermes rubric) →
   emit event → re-derive profile.
4. **The profile as the API** — `/api/profile/{uid}` returns the DERIVED profile (all views), not a
   stored row.
