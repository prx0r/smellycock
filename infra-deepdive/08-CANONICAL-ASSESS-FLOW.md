# CANONICAL ASSESS-FLOW — how every Sanskrit work is assessed + routed (the decision engine)

*2026-08-15 · the authoritative, deterministic process for deciding what to do with each Sanskrit work —
from raw acquisition through to queueing for translation. The decision is **deterministic Python, not
Hermes** (AXIOM 3: "Eligibility is deterministic Python, never an LLM judgment"; AXIOM 2: "Hermes for
GENERATION, .py for REDUCTION"). Hermes generates content/rationale; the `.py` engine decides. This is
fast, cheap, and reproducible — the same evidence standard as the confirmed RAW→C1 run.*

---

## 1. THE ANSWER TO "IS IT HERMES? IS IT TOO SLOW?"
**No.** The assessment is a **deterministic `.py` decision engine** — a regex + dict scan over each work's
source bytes + the ledger, completed in milliseconds per work, with **zero LLM calls**. Hermes is only ever
used for GENERATION (a verse translation, an argument map, a rationale), never for the eligibility/route
decision. This is enforced by AXIOM 3. Existing pieces already do this:
- `pipeline/source_ready.py` — CLEAN / READY / PRIORITY signals (pure regex + registry reads).
- `pipeline/corpus_state.py:35` — `detect_source_format` (AND_GLOSS / RAW_SANSKRIT / UNKNOWN) + `next_valid_action` (the per-work state machine).
- `pipeline/translation_targets.py` — the priority registry (KRAMA packet first, then tiers).
- `pipeline/sivaqueue_targets.py` — period/tradition/genre metadata for the second corpus.
- `source-evidence/.../entity_reconciliation.py` — identity EXACT/PROBABLE/POSSIBLE/CONFLICT/UNRESOLVED.

**The only place Hermes MAY be used in the decision:** generating the *rationale* for an ambiguous case
(route it to the scholar queue with a written note) — never to make the routing call itself.

## 2. THE CANONICAL DECISION TABLE (per work — one deterministic pass → one `{state, route, tag, priority}`)
Every work goes through exactly one pass. The output is a machine-readable record (cached to
`data/corpus/source-ready.json` + the ledger) so the decision is auditable.

| Stage | Input | Deterministic check | Output |
|---|---|---|---|
| **T0 CATEGORY** | work id + `sivaqueue_targets` + source-format | which corpus/period/tradition | `tag ∈ {KRAMA_PACKET, TIER1, E_TEXT_READY, SCANNED_MANUSCRIPT, IDENTITY_PENDING, COPYRIGHT_RESTRICTED}` |
| **T1 STATE** | on-disk source bytes | `source_ready._clean_signal` (IAST/Devanagari density, verse markers, size) | `state ∈ {CLEAN_ETEXT, NEEDS_OCR, LACUNA_BLOCKED, AMBIGUOUS, NO_SOURCE}` |
| **T2 FORMAT** | source text | `corpus_state.detect_source_format` | `format ∈ {AND_GLOSS, RAW_SANSKRIT, UNKNOWN}` |
| **T3 VERSE** | SOURCE registry | `payload.verse` present + non-empty (else verse-recovery P0) | `verse ∈ {PRESENT, RECOVERABLE, BLOCKED}` |
| **T4 IDENTITY** | adapter `ExternalRecord` | `entity_reconciliation` | `identity ∈ {EXACT, PROBABLE, POSSIBLE, CONFLICT, UNRESOLVED}` |
| **T5 PRIORITY** | translation coverage + source urls | `source_ready._priority_for` (copyright-aware) + `translation_targets.priority` | `priority ∈ {HIGH, MEDIUM, LOW, BLOCKED}` |

## 3. THE ROUTING (the decision table that maps tag/state/format → the process)
| state | format | identity | → process (the route) |
|---|---|---|---|
| CLEAN_ETEXT | RAW_SANSKRIT | EXACT/PROBABLE | **NORMALIZE → SOURCE(with verse) → QUEUE → TRANSLATE** (the confirmed stack) |
| CLEAN_ETEXT | AND_GLOSS | EXACT | **EXTRACT the Sanskrit** (strip the `[and]-GLOSS`) → re-assess |
| CLEAN_ETEXT | RAW_SANSKRIT | POSSIBLE/CONFLICT | **scholar-queue** (adjudicate identity first — never auto-merge) |
| NEEDS_OCR | any | any | **OCR integrator** (Kraken/eScriptorium/Vidyut per SPEC-18) → re-assess |
| LACUNA_BLOCKED / empty verse | RAW_SANSKRIT | EXACT | **verse-recovery (P0)** → `harvest_to_factory` → re-assess |
| UNKNOWN | UNKNOWN | any | **scholar-queue** (classify the source) |
| COPYRIGHT_RESTRICTED | any | any | **register only** — never publish |
| NO_SOURCE | any | any | **ACQUIRE** (choose adapter) → re-ingest |

## 4. THE QUEUE ENTRY (the seam to the confirmed translation stack)
A work is **promoted into the translation queue only after**: T0 tag + T1 state + T2 format + T3 verse
present + T5 priority all resolve to a "proceed" route (i.e. the CLEAN_ETEXT→RAW_SANSKRIT→EXACT row above).
Then `factory_scheduler._eligible_jobs` picks it up (SOURCE committed → T1 eligible), ranked by
`translation_targets.priority` + `source_ready` priority. This makes `queue=N` reflect **assessed,
verse-carrying, priority-ranked** works — not raw discoveries.

## 5. THE AUDIT TRAIL (logged-run evidence, same as translation)
The decision engine is itself evidenced:
- every work's `{tag, state, format, verse, identity, priority, route}` is written to a machine-readable
  cache + the ledger;
- `source_ready --write-cache` recomputes the full corpus signal into `source-ready.json`;
- a re-run is idempotent (same bytes → same decision), so the assessment is reproducible like the E2E.

## 6. WHERE TO BUILD (what exists vs what's consolidated)
| Piece | Exists | Consolidate into |
|---|---|---|
| CLEAN signal | `source_ready._clean_signal` | a single `assess.py` (T0→T5 in one deterministic pass) |
| FORMAT signal | `corpus_state.detect_source_format` | above |
| IDENTITY | `entity_reconciliation` | above (as a sub-call) |
| PRIORITY | `source_ready._priority_for` + `translation_targets` | above |
| CATEGORY tag | ❌ net-new (no work taxonomy exists) | add T0 to `assess.py` |
| ROUTE decision table | ⚠️ scattered across schedulers | add the table to `assess.py` |
| VERSE recovery | `harvest_to_factory` + `register_harvest_sources` (exists, not run for all) | wire into S8 (P0) |

## 7. BOTTOM LINE
**The assessment is a fast, deterministic, reproducible `.py` decision engine — Hermes is NOT in the loop**
(and would be too slow + rate-limited + non-deterministic to be). The canonical flow is one deterministic
pass per work producing `{tag, state, format, verse, identity, priority, route}`, mapped through the routing
table into the correct process, gated into the translation queue only when verse-carrying and ready, and
audited to a machine-readable cache — the same evidence standard as the confirmed RAW→C1 logged run.
