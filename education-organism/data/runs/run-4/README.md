# RUN 4 — the education-serving organism (end-to-end, auditable)

*2026-08-15. The run that builds + tests the ACTUAL organism infra: derivation audit trail, education
serving site, AI tutor, learner logging — connected into one tested path on real data.*

---

## What was built (this run)

| Build | What | Evidence |
|---|---|---|
| BUILD-1 | derivation-edge linker (SOURCE→L200→C1 input_refs) | 48 lower-chain objects linked |
| BUILD-2 | audit/resolve resolver (trace any object to source) | EDUCATION→SOURCE, 7 layers |
| BUILD-3 | education serving (compile-on-write → static JSON + Astro pages) | 3 lessons compiled to immutable bytes |
| BUILD-4 | AI tutor agent (serves LearningPackets, blind-grades, no LLM in path) | recalled/lapsed grading |
| BUILD-5 | learner data logging (events/mastery/misconceptions, append-only) | persisted |
| BUILD-6 | end-to-end audit trail test | **5/5 PASS** |

## The end-to-end audit trail (proven on real data)

```
EDUCATION kramasadbhava:v3__arg__synth__essay__educ
  → ESSAY → SYNTHESIS → ARGUMENT → C1
  → L200 → L2 → L1 → L0 → T1 → SOURCE kramasadbhava:v3
```

An education claim traces back to its source Sanskrit through the full chain. This is the audit trail
from source material through L0 to the customer.

## Tests (all recorded)

- **run-tests.py: 17/17** (incl. organism flywheel, procedural memory, ingestion, gates on real data)
- **test-e2e.py: 5/5** (the audit trail end-to-end)
- **check.py: PASS** (all gates on real data)
- **audit-resolve.py**: EDUCATION→SOURCE full trail
- **compile-education.py**: 3 lessons → immutable static bytes

## Performance (AXIOMS §7)

- 17/17 in **0.07s**, max RSS **~22 MB** (streaming, far under the 8GB budget)

## Files

`data/runs/run-4/`: `e2e.log` · `tests.log` · `check.log` · `audit-resolve.log` · `compile-education.log`

*Replayable: any agent can re-run these scripts. The organism now has a real, auditable source→customer
path — not just kernels.*
