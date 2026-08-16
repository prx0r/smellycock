# translation — BUILD REVIEW (the canonical comparison + the best)

*2026-08-15 · the canonical, agent-readable review of every translation build. **STATUS: the KANBAN build is
the ACTIVE/CANONICAL translation build.** The others are `SUPERSEDED` (kept for reference/proof, per AXIOM 6:
archive, don't delete) or are building blocks the kanban build uses. One rule: the kanban build is the
production architecture — a durable, resumable, auditable work queue. Read `layers/` for the per-layer
contracts + `ORCHESTRATION.md` for ops.*

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
| # | Build | File | Role | Status |
|---|---|---|---|---|
| 6 | **KANBAN** ⭐ | `kanban_translation.py` | durable work queue, agents claim/complete/chain | **ACTIVE / CANONICAL** |
| 3 | factory_scheduler | `factory_scheduler.py` | DAG backlog, chunk 50, parallel 4 | SUPERSEDED (kanban uses its generators) |
| 4 | per-layer agents | `layer_agent.py` | independent worker per layer, 90%-context | BUILDING BLOCK (used by kanban) |
| 5 | streaming worker | `stream_worker.py` + `chat_stream` | commit-per-verse as model generates | BUILDING BLOCK (used by kanban) |
| 1 | E2E harness | `test_full_chain_timing.py` | 1-verse RAW→C1 proof | SUPERSEDED (proof only) |
| 2 | translate_work | `translate_work.py` | 1-verse + logged benchmark | SUPERSEDED (benchmark only) |

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

## CURRENT FACTORY STATE (experiment-driven — the science lab sets the config)
The factory's config now reflects the **science-lab experiment results** (`EXP-T1-speed-20260816`):
- **T1 build = `-z` streaming + ONE big context-saturating batch per call + flash** (the winning config,
  9.0s/verse, 1 call, 5/5 committed). `chunk_size` defaults to `max_verses_per_call()` (~2993) + `PATALA_T1_STREAM=1`.
- **Bigger batches are faster per-verse** (batch 5 → 22.6s/v, batch 10 → 10.2s/v) — so the factory batches big.
- **Vidyut OFF was faster** (10.0 vs 22.6s/v @ batch 5) — pending a quality check vs the gold before adoption.
- The report (`data/corpus/experiment-reports/EXP-T1-speed-20260816-report.json`) records the findings +
  decision + validation. **The factory's defaults ARE the experiment's winners** — change a config only after a
  new experiment justifies it (the lab gates it).
