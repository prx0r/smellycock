# BRAINSTORM — 3 ALTERNATIVE TRANSLATION BUILDS (1M-context whole-chain)

*2026-08-15. Three alternative architectures for the translation pipeline, exploiting Hermes's **1M
context** to do RAW→(T1…L200→C1) in as few calls as possible, with smart streaming handoffs + a graph
memory. Grounded in Hermes's real capabilities, the graph-agent memory ideas (cognee/graphiti/SAGE), and
our existing infra (canonical generator, factory, orchestration).*

## THE KEY INSIGHT (why this can be far faster)
Hermes has **1M context**. The expensive, non-vectorizable work is **loading the work's Sanskrit + term-
context packet once**. Today we load it once per LAYER per batch (6×). If we load it **once per work** and
produce MANY layers from that one loaded context, we collapse 6 model calls into 1 — a ~6× throughput win
on the model-bound layers (the real bottleneck).

**The risk that killed the old 50-verse approach:** output truncation (a giant single JSON). **The fix
(already proven):** streaming JSONL per-record + per-layer recovery + adaptive chunking. So the build must
load-once but *stream* layer-by-layer, committing each layer's complete records as they arrive.

## THE 3 BUILDS

### BUILD 1 — WHOLE-CHAIN SINGLE-PASS (load once, emit all layers) ⭐ most aggressive
- **One agentic Hermes session** per work (or per chunk): loads the whole work's Sanskrit + term-context
  packet into the 1M context.
- The model emits **per-layer JSONL** — for each verse, T1 glosses + L0 tokens + ARGMAP + L2 reading +
  L200 audit + C1 — as structured records.
- **Smart streaming handoff:** the response is parsed as a stream of layer-keyed records; each layer's
  complete records commit (via the existing validators) as they arrive; a truncated tail is retried by
  re-emission (adaptive), never losing committed layers.
- `.py` REDUCES: validates + commits T1, then L0 (deterministic), then ARGMAP/L2/L200/C1 from the SAME
  response — the whole chain from one context load.
- **Win:** ~6× fewer calls; the whole chain per verse from one load.
- **Risk:** the output is large (6 layers × N verses) → truncation. Mitigated by streaming + per-layer
  recovery + adaptive chunking (the proven contract).
- **Sources:** the canonical generator's JSONL contract + the 1M-context insight.

### BUILD 2 — GRAPH-MEMORY READER-WRITER (compounding corpus)
- A **graph memory** (cognee/graphiti/SAGE reader-writer): the term-context packet + every committed
  translation becomes nodes/facts the translator READS and UPDATES.
- As verses translate, their term-senses + readings feed back into the memory → later verses/corpus are
  easier (the dialect-genealogy / "lexicon compounding" idea — GEM 3).
- Hermes (1M context) reads the work's accumulated graph-memory + the current verse batch → produces the
  next layers, grounded in the evolving term-semantics.
- **Win:** compounding — the corpus gets easier over time; cross-work consistency.
- **Risk:** memory construction + retrieval overhead; the graph-memory must be real, not a promise.
- **Sources:** `lib/organism.py`, graphiti (valid_at/invalid_at), SAGE reader-writer, cognee entity-linked
  memory, EverOS user-vs-agent memory.

### BUILD 3 — SPECIALIZED PASSES WITH STRUCTURED HANDOFFS (safe, incremental)
- Chain specialized Hermes passes, one per layer, with each layer committed to the registry and the NEXT
  pass reading the committed context from the registry (the structured handoff — not re-reading raw).
- RAW→T1 (one call) → L0 (deterministic, free) → ARGMAP (one) → L2 (one) → L200 (one) → C1 (one).
- **Smart handoffs via the registry** (the committed object is the data handed to the next pass) +
  `delegate_task` parallel workers across passages/works.
- **Win:** focused calls (smaller, more reliable), clean tracked handoffs, integrates with the existing
  factory + orchestration + build-plan.
- **Risk:** more calls (one per layer); doesn't exploit the 1M-context-once win as fully.
- **Sources:** the existing factory DAG + orchestration + MCP verbs.

## RECOMMENDATION
**Build 1 (whole-chain single-pass) is the experiment to try first** — it directly delivers what you're
after (almost the whole chain in one call) and reuses the proven streaming/JSONL/adaptive machinery. It is
the highest-leverage: if it works at N verses/chunk, throughput jumps ~6× on the model-bound layers.
**Build 2** is the compounding long-term win (wire the graph memory once Build 1 works). **Build 3** is the
safe fallback that integrates with what's already running.

## THE MODEL + HERMES CAPABILITIES (deepseek-v4-flash, as configured)
- **Model:** `deepseek-v4-flash` / provider `opencode-go` (pinned in `pipeline/model.py` + the `patala`
  profile). Agentic call: `hermes chat -Q -q "…" --yolo --max-turns N -m deepseek-v4-flash
  --provider opencode-go -p patala`.
- **1M context** — load the whole file once; the hard work (Sanskrit + term senses) is done.
- **Agentic file access** — Hermes reads the work's Sanskrit from a path itself (never stuff it in).
- **Sessions** (`--resume`) — persist context across calls (Build 3's handoffs can reuse a session).
- **MCP verbs** (`patala_next_action`, `get_work_state`, etc.) — the orchestration surface.
- **delegate_task / kanban** — parallel workers across works (Build 3).
- **JSONL streaming + iter_jsonl_recover + adaptive chunking** (our proven contract) — the anti-truncation core.

*This is the brainstorm. Next: prototype Build 1 — a whole-chain single-pass generator that loads once
and emits per-layer JSONL, with `.py` committing each layer as it streams.*
