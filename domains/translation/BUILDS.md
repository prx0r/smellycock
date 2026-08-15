# translation — BUILD REVIEW (the canonical comparison + the best)

*2026-08-15 · the canonical, agent-readable review of every translation build. One rule: **the kanban build
is the production architecture** — a durable, resumable, auditable work queue. The others are proof/benchmark
tools or building blocks it uses. Read `layers/` for the per-layer contracts + `ORCHESTRATION.md` for ops.*

---

## THE BUILD (the production architecture = the KANBAN build)
```
DAG eligibility ──feed()──▶ kanban board (BUILD_<LAYER>: <work> cards)
   └── per-layer agent claims → drains that layer's queue (90%-context Hermes call) → commits → completes → chains
```
- `pipeline/kanban_translation.py` (feed / work-once / daemon) · `pipeline/layer_agent.py` (the worker) ·
  `pipeline/model_registry.py` (dynamic 90%-context batch).
- **Why it's best:** durable (cards = rows in `~/.hermes/kanban.db`) · resumable (crash → reclaim) ·
  auditable (every handoff a row) · per-layer + per-model · observable (`hermes kanban --board translation stats`).
- **Current (logged):** daemon running, 32 ready / 1 done; gated by T1 generation speed + verse recovery.

## THE COMPARISON (all builds)
| # | Build | File | Role | Verdict |
|---|---|---|---|---|
| 1 | E2E harness | `test_full_chain_timing.py` | 1-verse RAW→C1 proof | prove the chain (live-run-5) |
| 2 | translate_work | `translate_work.py` | 1-verse + logged benchmark | benchmark/proof |
| 3 | factory_scheduler | `factory_scheduler.py` | DAG backlog, chunk 50, parallel 4 | **most proven at committing** |
| 4 | per-layer agents | `layer_agent.py` | independent worker per layer, 90%-context | the building block |
| 5 | streaming worker | `stream_worker.py` + `chat_stream` | commit-per-verse as model generates | responsive infra |
| 6 | **KANBAN** ⭐ | `kanban_translation.py` | durable work queue, agents claim/complete/chain | **THE PRODUCTION BUILD** |

## THE VERDICT
- **Best = #6 (kanban)** — the only durable/resumable/auditable work queue; subsumes #4 (workers) + #5
  (streaming) + the 90%-context batching; base for per-layer/per-model optimization.
- **Most proven at committing = #3 (factory_scheduler)** — the kanban build uses the same generators.
- **Limits (not infra):** T1 generation speed (model wall) + verse recovery (SOURCE payloads metadata-only).

## HOW TO RUN THE KANBAN BUILD
```bash
python3 pipeline/kanban_translation.py --feed          # mirror the DAG queue into cards
python3 pipeline/kanban_translation.py --daemon --calls 2 --model deepseek-v4-flash   # the worker loop
hermes kanban --board translation list / stats         # the queue
```
