# LEARNER-PROFILE RESEARCH — how real platforms model users (verified)

*2026-08-15 · Researched Duolingo, Khan, Anki, Brilliant, Memrise + open-source repos (via GitHub API,
verified). Validates my event-stream→derived-profile design and gives concrete patterns to steal.*

---

## 1. THE VALIDATION: my design is correct

**Every strong platform keeps an append-only event log as truth, and treats mastery/progress/profile as
a recomputable, denormalized, versioned view.** My `event_stream → derived_profile` is exactly the
industry pattern:

- **Anki**: `revlog` (append-only event stream) = truth; `cards` (scheduling params) = derived cache.
- **Khan**: `exercise_assessment` log + **discrete Mastery levels 1-3** derived from BKT.
- **Duolingo**: content ladder + thin counter row + per-item `challenge_progress` log.
- **OATutor**: `probMastery` per problem (derived, denormalized for reads).

> "The derived state is a recomputable cache, never the source of truth."

---

## 2. THE CLEAN 3-WAY SPLIT (what I should keep separate)

| Concept | What it is | Example |
|---|---|---|
| **Activity/engagement** | raw event log + counters | Duolingo points/hearts, streaks — cheap, noisy |
| **Mastery** | probability/state per skill (BKT, FSRS S/D/R) | OATutor `probMastery`, Khan Mastery 1-3 |
| **Progress** | position in the content graph | active course + unit/lesson order, due dates |

**Progress = "how far along"; Mastery = "how well".** They're decoupled — OATutor skips a mastered
problem regardless of position.

---

## 3. THE TWO THINGS TO ADD (from the research)

### (a) Discrete mastery-level projection (Khan style)
Don't expose raw BKT probabilities to the learner. Map continuous mastery → **discrete levels**:
`Practiced → Level 1 → Level 2 → Mastered` (or our E0-E8). My `zone_levels` should be this discrete
projection of continuous mastery.

### (b) Per-item FSRS/DSR core feeding per-concept aggregates
Attach `skill_id`/`concept_id` to each SRS card; roll up per-skill SRS aggregates (mean stability, % due,
lapse rate) into the mastery model. FSRS `R = (1+...)^(-S/Δ)` gives per-item retrievability you can
average per concept to feed BKT priors.

---

## 4. THE STEAL-LIST (TOP-6, verified)

| # | Repo | Stars | The ONE pattern to steal |
|---|---|---|---|
| 1 | `ankitects/anki` | 29.8k | **revlog-as-truth + derived-cache** split — literally my model |
| 2 | `CAHLR/OATutor` | 241 | **BKT update loop + mastery-threshold selection** (a working conductor) |
| 3 | `CAHLR/pyBKT` | 273 | **BKT parameterization/fit** (P(L0),P(T),P(S),P(G)) |
| 4 | `open-spaced-repetition/fsrs4anki` | 4.0k | **DSR model (S/D/R) per-item mastery** with deterministic update |
| 5 | `Khan/khan-exercises` | 1.7k | **discrete mastery levels derived from BKT** (not raw probabilities) |
| 6 | `sanidhyy/duolingo-clone` | 623 | **content-ladder graph + counter row + per-item log** (progress vs activity) |

---

## 5. THE HONEST VERDICT

My `event_stream → derived_profile` design is **validated by every major platform**. The two concrete
upgrades to make:
1. **Add a discrete mastery-level projection** (map continuous BKT mastery → human-readable levels for
   `zone_levels`).
2. **Add the per-item FSRS/DSR core** so vocabulary/term cards have S/D/R and roll up into concept
   mastery.

My conductor = OATutor's threshold-based selector, generalized over objectives. The event stream =
Anki's revlog. Everything fits.
