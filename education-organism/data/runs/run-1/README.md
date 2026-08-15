# RUN 1 — serveragent3 POST-C1 spine, fully logged (2026-08-15)

*A frozen record of the complete serveragent3 run: the Hermes-driven POST-C1 spine build (generate →
gate → commit) over a grounded IPVV C1 floor, plus the full test suite and drift-validator evidence.
This is the anti-cheat record — every log is captured, nothing is hidden.*

---

## 1. SETUP (the run being recorded)

- **Floor:** 10 grounded IPVV C1s (real commentary content, evidence_quote anchored) seeded via
  `scripts/seed-c1.py`.
- **Run:** `scripts/build-spine.py` — Hermes (deepseek-v4-flash via opencode-go) derives THEME →
  ARGUMENT → SYNTHESIS → ESSAY → EDUCATION from each real C1; the deterministic gates validate; the
  registry commits (superseding stale). Fail-closed: an empty model result abstains (never fabricates).
- **Gates:** the 10-test suite (`run-tests.py`) + the drift validator (`check.py --status`) +
  the event-ledger tamper check.

## 2. THE RESULT (registry summary)

| Layer | Objects | Versions |
|---|---|---|
| C1 | 10 | 10 |
| THEME | 10 | 10 |
| ARGUMENT | 10 | 10 |
| SYNTHESIS | 10 | 10 |
| ESSAY | 10 | 10 |
| EDUCATION | 10 | 10 |

**50 upper-layer objects committed (10 × 5), 0 abstains/failures.** Every object is ENGINEERING_VALIDATED
or GENERATED, derived from a real C1.

## 3. THE MONITOR (live samples)

| ts | procs | rss_mb | C1 | THEME | ARG | SYNTH | ESSAY | EDUC |
|---|---|---|---|---|---|---|---|---|
| 16:32:03 | 1 | 19 | 10 | 10 | 10 | 10 | 10 | 10 |
| 16:32:05 | 1 | 19 | 10 | 10 | 10 | 10 | 10 | 10 |
| 16:32:07 | 1 | 19 | 10 | 10 | 10 | 10 | 10 | 10 |

Memory ~19MB (the kernels are tiny; the heavy work was the model call, now done).

## 4. THE TEST SUITE (all logs in `tests.log`)

```
SUMMARY: 10/10 passed
  [PASS] registry loads + CANONICAL-DAG compiles
  [PASS] event ledger pristine
  [PASS] event ledger DETECTS tamper
  [PASS] nyaya gate rejects unfalsifiable
  [PASS] nyaya gate accepts sound claim w/ falsifier
  [PASS] nyaya flags universal-without-vyapti
  [PASS] blind_grade recalls a good answer
  [PASS] chain gate (proof path to C1)
  [PASS] quality gate PASSes a grounded C1
  [PASS] quality gate BLOCKs a hollow argument
```

## 5. THE DRIFT VALIDATOR (in `check.log`)

```
serveragent3 check: PASS
```

## 6. EVENT-LEDGER INTEGRITY (in `ledger.log`)

```
event chain intact: True
```

## 7. ANTI-CHEAT VERIFICATION

- Inspected a committed ARGUMENT payload: **real model-derived content** ("After the maṅgala is
  completed, Abhinavagupta's exposition begins with the first kārikā on the Lord's spontaneity
  (svācchandya)...") — NOT an empty fabrication. `_raw` empty = False.
- The build commit count (50) matches the registry summary (10/layer × 5).
- The event ledger detects tampering (test proves it).

## 8. FILES

| File | What |
|---|---|
| `tests.log` | the full test suite output (10/10) |
| `check.log` | the drift validator output (PASS) |
| `ledger.log` | event-chain integrity (True) |
| `registry.log` | the registry summary |
| `monitor-snapshots.jsonl` | live system samples |
| `README.md` (this) | the run record |

*Replayable: any agent can re-read these logs to confirm the run. Lineage: no git repo (serveragent3 is
a working prototype), so lineage = the registry hashes + created_by + this log.*
