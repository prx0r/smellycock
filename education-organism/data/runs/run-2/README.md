# RUN 2 — serveragent3 post-red-team rebuild (2026-08-15)

*A re-logged run after the red-team fixes + the smellycock gold integration. Honest per-object gate
verdicts, no overclaims.*

---

## What changed (vs run-1, which was red-teamed)

| Flaw | Fix |
|---|---|
| CRITICAL-1 (no gate before EV) | gates wired into build; EV only on gate pass |
| CRITICAL-2 (junk EDUCATION) | quality gate inspects real content; EDUCATION = real LearningClaims |
| CRITICAL-3 (authority invariant unenforced) | `assert_authority_invariant` enforced in commit |
| CRITICAL-4 (multi-parent DAG) | `eligible()` checks every required parent |
| HIGH-5 (input_hash = self) | `derivation_hash` over parent inputs |
| HIGH-6 (forgeable ledger) | keyed (HMAC) + payload-digested event chain |
| HIGH-7 (circular tests) | tests run gates on REAL registries; junk must FAIL |
| MEDIUM-8/9/10 | check runs all gates; commit rejects fake status; seed no auto-promote |
| **NEW (user's catch)** | EDUCATION + ORGANISM now real (not prose) |
| smellycock gold | real C1 golds + essay golds ingested (complete content, no truncation) |

## The result (real data)

| Layer | Objects | Gold | Content |
|---|---|---|---|
| C1 | 12 | 2 | real IPVV C1 golds (complete) |
| THEME | 10 | 0 | derived (GENERATED — invariant holds) |
| ARGUMENT | 10 | 0 | derived (GENERATED) |
| SYNTHESIS | 10 | 0 | derived (GENERATED) |
| ESSAY | 14 | 3 | real smellycock essays + derived |
| EDUCATION | 2 | 2 | **real LearningClaims + interactions** |

**Statuses are honest:** all derived objects are GENERATED (the authority invariant correctly refuses
EV over the GENERATED gold floor). No fake ENGINEERING_VALIDATED.

## The EDUCATION + ORGANISM fix (the user's catch)

EDUCATION is no longer model prose. It is the **interaction compiler** (`compile_interactions`) turning
each gold C1 into a LearningPacket: 6 LearningClaims + 6 interactions (Choice/SpanSelect/SpeakerClassify/
PremiseAttach/ArgumentAssemble/PremiseRetract) + distractors from real key terms + the
`wrong_answer_to_neighbor` moat. Plus the **ORGANISM**: UserKnowledgeState (3 learner profiles),
MisconceptionGraph (the demand signal), ConsumerSensor (questions → gaps → the research/pedagogy
backlog).

## Gates (recorded)

- **Test suite: 10/10 PASS** (incl. real-data regression: junk EDUCATION must FAIL, chain on real
  registries). See `tests.log`.
- **check.py: PASS** (runs all gates on real data). See `check.log`.
- **Event ledger: intact** (keyed scheme, tamper-detected). See `ledger.log`.

*Replayable: any agent can re-read these logs + the registries. Lineage = registry hashes + created_by +
this log.*
