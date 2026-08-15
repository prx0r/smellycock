# LIVE RUN 2 — autonomous translation run, fully logged (2026-08-15 ~15:35–15:40)

Frozen record of a 5-minute live autonomous translation run on kramasadbhava (same format as Run 1).
**Result:** L0 198 → 217 (+19, deterministic), memory stable (~550MB, RAM 5.2GB free), full chain now
populated to 10 passages, production plan 2/4.

## Files
- `MONITOR-REPORT-RUN-2.md` — the full review (timeline, perf, findings)
- `samples-30s.jsonl` — the 10 status snapshots (every 30s)
- `factory-pass.log` — the run-2 factory pass
- `monitor.out` — the sampler stdout
- `EXPERIMENT-COMPARISON.md` — the 3-build comparison (Build 1 whole-chain is the winner)

## Key findings
1. Sampler cwd bug (needed absolute path) — operational, not mechanism.
2. Old watchdog still running pre-atomic-lock — restart to pick up the one-owner fix.
3. L0 plateaus when a pass's per_layer budget is exhausted — the watchdog re-launches.
