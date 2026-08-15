# LIVE RUN 1 — autonomous translation run, fully logged (2026-08-15 ~14:36–14:42)

*A frozen record of a 5-minute live autonomous translation run on kramasadbhava, with all logs + the
monitoring report. This is the evidence that the pipeline runs end-to-end with observability.*

## What this run was
- **Work:** kramasadbhava (248 T1). **Pass:** deterministic L0 (`--max-model-calls 0 --per-layer 20`).
- **Monitor:** status board sampled every 30s for 5 min (11 snapshots).
- **Result:** L0 **168 → 180** (12 real validated commits, ~2.4/min, 0 model calls, 0 errors).
- **Memory:** factory stable at **~550MB** (the 4.5GB→545MB streaming fix holds); RAM ~5.2GB free.

## Files
| File | What |
|---|---|
| `MONITOR-REPORT-2026-08-15.md` | the full review (timeline, perf, findings) |
| `samples-30s.jsonl` | the 11 status-board snapshots (every 30s) |
| `status-constant.jsonl` | the perpetual status logger snapshots |
| `factory-pass.log` | the actual factory pass log |
| `fullchain-watchdog.log` | the full-chain watchdog log |

## Key findings captured
1. **One-owner violation caught + fixed** (two factory passes at 14:36; duplicate killed) — action item:
   tighten the watchdog's `_factory_running()` race.
2. **L2 is the thin layer** (3) — the model-bound readable-prose layer is the remaining bottleneck to the
   full chain.
3. **`per_layer` is the L0 throughput lever** (20 → ~6× faster than 2).
4. **Memory fix holds** — no OOM risk; the streaming lookup keeps RSS ~550MB.

*Replayable: any agent can re-read these logs + the report to confirm the run. The plan state is in
`data/plans/build-plan-2026-08-15.json`; the trace log in `data/ops/traces.jsonl`.*
