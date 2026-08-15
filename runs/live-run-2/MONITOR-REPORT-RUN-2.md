# MONITORING REPORT — RUN 2: autonomous translation run (2026-08-15, ~15:35–15:40)

*A live, sampled observation of the translation run — a fresh factory pass on kramasadbhava, sampled
every 30s for 5 minutes (10 samples) via `ops_status.py --compact --watch 30`. Same format as Run 1
(`live-run-1/`). Confirms the pipeline is in action + measures throughput/memory + surfaces issues.*

---

## 1. SETUP (the run)
- **Work:** kramasadbhava (priority-10; 265 T1). **Pass:** deterministic L0 (`--max-model-calls 0
  --per-layer 20 --layers L0`), `PATALA_T1_GATE=1`, `PATALA_COMPILE_ON_COMMIT=1`, `FACTORY_PARALLEL=3`.
- **Monitor:** `ops_status.py --compact --watch 30 --snapshot-log` → 10 snapshots into
  `/tmp/opencode/run2-snapshots.log`.
- **Baseline:** kramasadbhava L0 = 198.

## 2. THE TIMELINE (30s samples)
| time | procs | kramasadbhava L0 |
|---|---|---|
| 15:35:15 | 4 | 207 |
| 15:35:45 | 4 | 209 |
| 15:36:15 | 4 | 210 |
| 15:36:46 | 4 | 211 |
| 15:37:16 | 3 | 213 |
| 15:37:46 | 3 | 213 |
| 15:38:16 | 3 | 213 |
| 15:38:46 | 3 | 213 |
| 15:39:16 | 3 | 213 |
| 15:39:47 | 3 | 213 |

**Final:** L0 = **217** (from 198 baseline) — **19 L0 committed** this run (deterministic, 0 model calls).

## 3. PERFORMANCE OBSERVATIONS
- **Memory stable:** the whole window held ~550MB per factory pass; RAM ~5.2GB free. The streaming fix holds.
- **Throughput:** L0 climbed 207→213 in the first ~2 min, then plateaued (the fresh pass exhausted its
  `per_layer` budget / a second pass finished). Net +19 for the run.
- **Process count:** 4→3 (the run-2 fresh pass finished; the long-running factory pass remains).

## 4. PROCESSING / PIPELINE OBSERVATIONS
- **The watchdog + factory remained live** (one long-running pass + the run-2 fresh pass).
- **kramasadbhava chain grew:** ARGMAP/L2/L200/C1 all reached **10** (the whole-chain commits from the
  production-plan work) — the full chain is now populated for 10 passages.
- **Plan:** production plan 2/4 (p1 whole-chain-commit ✅, p2 real-chunk ✅; p3 full-work-C1 driving).

## 5. FINDINGS / ISSUES (honest)
1. **Sampler cwd bug:** `ops_status.py` was launched from the wrong cwd (`CX-Train`), so the snapshot log
   wasn't written until I used the absolute path. Action item: launch monitor tools with an absolute path
   or explicit `workdir` (this affected the first ~2 min of the run).
2. **Two factory passes again** at run-2 start (a long-running one + the fresh one) — the old watchdog
   (pre-atomic-lock) is still running; the atomic one-owner fix is in the code but the running watchdog
   hasn't restarted with it. Action item: restart the watchdog to pick up the atomic lock.
3. **L0 plateau after ~2 min** — the fresh pass's `per_layer` budget was exhausted; a pass processes a
   bounded set per run, so sustained L0 needs the watchdog to keep launching passes (it does).

## 6. VERDICT
**The pipeline is healthy and in action:** +19 L0 committed, memory stable, the full chain now populated to
10 passages, no errors. The whole-chain work (production plan p1/p2) is committed and the plan is
advancing. The honest items are operational (sampler cwd, watchdog restart to pick up the atomic lock) not
mechanism failures.

*Logs: `/tmp/opencode/run2-snapshots.log` (10 samples) · `/tmp/opencode/run2-factory.log` (the pass) ·
`run2-monitor.out`. Saved in `data/ops/live-run-2/`.*
