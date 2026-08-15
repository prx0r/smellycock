# RUN 4 — the education-serving organism (end-to-end, auditable)

*2026-08-15 · the run that built + verified the ACTUAL organism infrastructure: the derivation audit
trail, the education serving site, the AI tutor, and the learner data logging — connected into one
tested path on REAL data. All logs recorded, all gates run on real data, per the AXIOMS (ONE RULE:
nothing is real without a reproducible gate).*

---

## 1. THE HONEST STARTING STATE (before this run)

The context + derivation-chain audits found:
- **Upper chain (C1→THEME→ARGUMENT→SYNTHESIS→ESSAY→EDUCATION):** real + linked (`input_refs` populated,
  ENGINEERING_VALIDATED).
- **Lower chain (SOURCE→T1→L0→L1→L2→L200→C1):** DISCONNECTED — every `input_refs=[]`. No audit trail
  from source to C1.
- **No education site, no AI tutor, no learner data logging** — only kernels.

## 2. WHAT WAS BUILT + THE LOGS (each gated, on real data)

| Build | What | Log | Result |
|---|---|---|---|
| **B1** | derivation-edge linker (backfill `input_refs` SOURCE→L200→C1) | `scripts/link-derivation-chain.py` | 48 lower-chain objects linked |
| **B2** | audit/resolve resolver (trace any object to source) | `scripts/audit-resolve.py` | EDUCATION→SOURCE, 7 layers |
| **B3** | education serving (compile-on-write → static JSON + Astro `/education/` pages) | `scripts/compile-education.py` | 3 lessons compiled to immutable bytes |
| **B4** | AI tutor agent (serves LearningPackets, blind-grades, no LLM in path) | `scripts/tutor-agent.py` | recalled/lapsed grading |
| **B5** | learner data logging (events/mastery/misconceptions, append-only) | `scripts/learner-log.py` | persisted |
| **B6** | end-to-end audit-trail test | `scripts/test-e2e.py` | **5/5 PASS** |

## 3. THE END-TO-END AUDIT TRAIL (verified on real data)

```
EDUCATION kramasadbhava:v3__arg__synth__essay__educ
  → ESSAY kramasadbhava:v3__arg__synth__essay
  → SYNTHESIS kramasadbhava:v3__arg__synth
  → ARGUMENT kramasadbhava:v3__arg
  → C1 kramasadbhava:v3
  → L200 kramasadbhava:v3
  → L2 kramasadbhava:v3
  → L1 kramasadbhava:v3
  → L0 kramasadbhava:v3
  → T1 kramasadbhava:v3
  → SOURCE kramasadbhava:v3
```

An education claim traces back to its source Sanskrit through the full chain — the audit trail from
source material through L0 to the customer. **Resolves to SOURCE: ✅.**

## 4. THE FULL LOGS (recorded in this run)

| Log | Content |
|---|---|
| `e2e.log` | the end-to-end audit-trail test (5/5) |
| `tests.log` | the full test suite (17/17) |
| `check.log` | the drift validator (PASS — all gates on real data) |
| `audit-resolve.log` | the resolver trace (EDUCATION→SOURCE, 7 layers) |
| `compile-education.log` | the education projection (3 lessons) |
| `tutor-session.json` | a tutor session (question + blind grade) |
| `learner/` | the learner data logging (events/mastery/misconceptions) |

## 5. PERFORMANCE (AXIOMS §7 — RAM is the scarcest resource)

- Test suite: **17/17 in 0.07s**, max RSS **~22 MB** (streaming, far under the 8GB box budget).

## 6. THE GATES (all run on real data, per the ONE RULE)

- `run-tests.py`: 17/17 PASS (incl. organism flywheel, procedural memory, ingestion, gates on real data)
- `test-e2e.py`: 5/5 PASS (the audit trail end-to-end)
- `check.py`: PASS (all gates on real data)
- Event ledger: keyed + tamper-detected (verified in the test suite)

*Replayable: any agent can re-run the scripts in `serveragent3/scripts/`. This is the organism's real,
auditable source→customer path — not just kernels.*
