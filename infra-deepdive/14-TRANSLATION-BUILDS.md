# TRANSLATION BUILDS — the kanban build (saved) + the full comparison + the best

*2026-08-15 · the alternative kanban-driven translation build, saved as the production architecture, plus
the honest comparison of every translation build we've done and which is best and why.*

---

## 1. THE KANBAN BUILD (the alternative / production architecture) — saved here
**Drive translation through the Hermes kanban board (the smart, durable queue).** Not a script that grinds —
a **work queue** where every card is a row, every handoff is durable, and per-layer agents are the workers.

### How it works
```
DAG eligibility ──feed()──▶ kanban board: BUILD_<LAYER>: <work> cards (BUILD_T1: kulasara, BUILD_L0: netratantra, ...)
                              └── per-layer agent (layer_agent.py) claims → drains that layer's queue (90%-context
                                   Hermes call) → commits → completes the card → chains to the next layer's card
```

### The commands
```bash
python3 pipeline/kanban_translation.py --feed          # mirror the real DAG queue into cards
python3 pipeline/kanban_translation.py --daemon --calls 2 --model deepseek-v4-flash   # the worker loop
hermes kanban --board translation list                 # the queue
hermes kanban --board translation stats                # ready/running/done
```

### Why this is the production build
- **Durable + resumable + crash-safe** — cards are rows in `~/.hermes/kanban.db`; a crash → card reclaims.
- **Audit trail** — every card + handoff is a durable row (the "logged run").
- **Smart queue** — `feed()` mirrors the real DAG eligibility (no empty/duplicate work).
- **Per-layer + per-model** — each card is one layer of one work; agents can use a different model per layer.
- **Observable** — `stats` shows ready/running/done; productivity per card.

### Current state (logged)
- Daemon running, claimed `BUILD_T1: kulasara`, 32 ready / 1 done. Slow because **T1 generation is the model wall**
  (~2 min/call) + the **verse-recovery gap** (SOURCE payloads metadata-only) — fixed via `_source_objects`.

---

## 2. ALL THE TRANSLATION BUILDS (what we've done this session) + the comparison

| Build | File(s) | How it translates | RAM | Model calls | Crash-safe | Audit | Best for |
|---|---|---|---|---|---|---|---|
| **1. E2E harness** | `test_full_chain_timing.py` | 1 verse at a time, `batch_size=1`, RAW→C1 proof | low | **5/verse** (slow) | no | e2e-trace | **proving** the chain works (live-run-5) |
| **2. translate_work** | `translate_work.py` | 1 verse RAW→C1, logged, benchmark | low | 5/verse | no | progress registry | **benchmark/proof**, not throughput |
| **3. factory_scheduler** | `factory_scheduler.py` | DAG backlog scheduler: chunks of 50, parallel 4, per-layer queues | low (after OOM fix) | **~1/50 verses** | retry | per-pass | **the efficient DAG grinder** |
| **4. per-layer agents** | `layer_agent.py` | independent worker per layer, drains queue, 90%-context | low | ~1/big-batch | partial | layer log | **the building block** (parallel agents) |
| **5. streaming worker** | `stream_worker.py` + `chat_stream` | commit-per-verse as the model generates | low | 1 call | yes | per-commit | **responsive infra** (no blocking) |
| **6. KANBAN build** ⭐ | `kanban_translation.py` | cards per layer-work on the Hermes board; agents claim/complete/chain | low | ~1/big-batch | **YES** | **durable rows** | **the production architecture** |

## 3. WHICH IS BEST + WHY — **the KANBAN build**

**Best = #6 (kanban).** It's the only one that's a *durable, resumable, auditable work queue* — every card is
a row that survives crashes, is reclaimable, and leaves an audit trail. It subsumes the others:
- it **uses** the per-layer agents (#4) as workers,
- it **sizes batches to 90% context** like #3/#4,
- it's **crash-safe + auditable** (unlike #1-#4),
- and it's **the right base for per-layer/per-model optimization** (each card can run a different model).

**Most proven at committing = #3 (factory_scheduler)** — it actually batches + commits (the assembly-line),
and after the `_source_objects` streaming fix it's low-RAM. The kanban build uses the same layer generators,
so it inherits that proven committing.

**The honest dependencies:** the kanban build's *rate* is still gated by (a) **T1 generation speed** (the
model wall) and (b) **verse recovery** (SOURCE payloads metadata-only). Those are the real throughput limits —
the infra (kanban + agents + streaming) is done.

## 4. BOTTOM LINE
> **The KANBAN build is the best translation build: a durable, crash-safe, auditable work queue driven by
> per-layer agents (90%-context Hermes calls, per-model per layer). It supersedes the E2E/proof harnesses
> and the scheduler, and is the base for per-layer model optimization. What still gates its throughput is
> the model's generation speed + verse recovery — not the infra.**
