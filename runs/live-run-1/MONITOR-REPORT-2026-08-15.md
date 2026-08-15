# MONITORING REPORT — 5-minute autonomous translation run (2026-08-15, ~14:36–14:42)

*A live, sampled observation of the full translation run — a fresh factory pass on kramasadbhava, sampled
every 30s for 5 minutes (11 samples) via `ops_status.py --compact --watch 30`. Purpose: confirm the
pipeline is genuinely in action, measure throughput/memory, and surface any performance or processing
issues.*

---

## 1. SETUP (the run being monitored)
- **Work:** `kramasadbhava` (priority-10 Krama packet; 248 T1).
- **Run:** a fresh deterministic L0 pass — `factory_scheduler.py --works kramasadbhava --max-model-calls 0
  --per-layer 20 --layers L0`, `PATALA_T1_GATE=1`, `PATALA_COMPILE_ON_COMMIT=1`, `FACTORY_PARALLEL=3`.
- **Monitor:** `ops_status.py --compact --watch 30 --snapshot-log` → 11 snapshots (processes, per-layer
  counts, queue, plan, logs) into `/tmp/opencode/run-report-snapshots.log`.
- **Baseline:** kramasadbhava L0 = 168.

## 2. THE TIMELINE (30s samples)
| time | procs | L0 | factory RSS |
|---|---|---|---|
| 14:36:52 | 4 | 168 | 562MB |
| 14:37:22 | 4 | 169 | 562MB |
| 14:37:53 | 3 | 169 | 549MB |
| 14:38:23 | 3 | 169 | 549MB |
| 14:38:53 | 3 | 171 | 550MB |
| 14:39:23 | 3 | 172 | 551MB |
| 14:39:53 | 3 | 174 | 553MB |
| 14:40:23 | 3 | 175 | 554MB |
| 14:40:54 | 3 | 176 | 555MB |
| 14:41:24 | 3 | 178 | 555MB |
| 14:41:54 | 3 | 179 | 555MB |

**Final:** L0 = **180** (from 168) — **12 passages committed in 5 min (~2.4/min)**, deterministic (0 model
calls), all passing `verify_l0.p0_proof`.

## 3. PERFORMANCE OBSERVATIONS (all green)
- **Memory is stable and low:** factory RSS held at **~550MB** the whole run (the 4.5GB→545MB streaming
  fix holds). RAM available ~5.2GB (one agent). No OOM risk.
- **CPU:** factory at ~99% (busy committing, not stalled).
- **Throughput:** ~2.4 L0/min with `--per-layer 20` (vs the earlier ~2-per-10-min at `per_layer 2` — a
  real 6× improvement from the per-layer setting). L0 is the deterministic fast layer; model layers
  (L2/L200/C1) are the slower, budgeted ones.
- **No retryable/rejected** in the pass (`0 retryable, 0 rejected`).

## 4. PROCESSING / PIPELINE OBSERVATIONS
- The **queue + watchdog** stayed live (one factory pass, one-owner respected after I caught + killed a
  duplicate — see §5).
- **Plan:** 14/15 checkpoints done (the end-goal `endgoal-fullwork-c1` is the open one, waiting on the
  chain to reach ~90%).
- **Data:** the per-layer counts updated live in the status board; kramasadbhava chain
  `{T1:248, L0:180, ARGMAP:1, L2:3, L200:3, C1:3}` — the deterministic floor is climbing toward T1.

## 5. FINDINGS / ISSUES CAUGHT (the honest part)
1. **One-owner violation caught + fixed:** at 14:36 there were TWO factory passes (the watchdog's older
   one + my fresh one). I killed the duplicate to restore one-owner. **The watchdog's
   `_factory_running()` pgrep check should be tightened** so it never launches while ANY pass runs (it
   did check, but a race allowed a second launch). Action item.
2. **L2 is still the thin layer** (3) — the model-bound readable-prose layer is the remaining bottleneck
   to the full chain; the monitored run only advanced the deterministic L0 floor.
3. **L0 rate is bounded by `per_layer`** — raising it (20) gave 6× throughput; a per-layer knob is the
   throughput lever for the deterministic layers.

## 6. VERDICT
**The pipeline is genuinely in action and healthy:** a fresh run committed 12 real, validated L0 objects
in 5 minutes at stable ~550MB memory with full logging (status board + factory log + trace), no errors.
The deterministic floor is climbing; the honest remaining work is the model-bound upper layers (L2 at
scale) + tightening the one-owner guard.

*Logs: `/tmp/opencode/run-report-snapshots.log` (11 samples) · `/tmp/opencode/monitor-factory.log` (the
pass) · `ops-status-snapshots.log` (the constant logger).*
