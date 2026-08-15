# THE BENCHMARK + PROJECTOR — full thesis, capabilities, and what it enables

*2026-08-15 · the spec for the translation estimator (projector) and the wider analysis surface built on
the translation-progress benchmark. EVERY number is backed by the actual logs (the progress registry +
`e2e-trace.json` + the DeepSeek pricing), not vibes. This is the foundation the other agent can use in
their openpatala work + ingestion pipeline.*

---

## 1. THE PROJECTOR (the estimator): "load a stack → this model costs X, takes Y"

### The thesis
We record, per verse, the real **time, model calls, cost, and quality** (tagged to the model). A work's
**verse count** is known from the SOURCE registry. So we can PROJECT any stack of works through any model:

```
per-verse (measured, per model)  ×  verse_count(work)  ×  scenario(batch, parallel)  =  cost + time + calls
```

### The math (backed by actual logs)
| Quantity | Value | Source |
|---|---|---|
| per-verse time | **385s** (5 logged verses) / 325s default | progress registry + `e2e-trace.json` |
| model calls/verse | **5** (T1, ARGMAP, L2, L200, C1) | the DAG (accurate counter) |
| cost/verse (flash) | **$0.000875** (cache-miss) / **$0.000361** (cache-hit) | `deepseek_pricing.py` on 15k-in/5k-out chars |
| verse count / work | streamed from `source-registry.jsonl` | e.g. kramasadbhava **573**, cidgagana **700** |
| scenarios | `batch N` verses/call · `parallel P` works | cuts calls + wall-clock |

### The projection output (`project_translation.py`)
```
=== PROJECTION: N works | model=deepseek-v4-flash (batch=1/call, parallel=1) ===
work        verses    calls   hours   $ (miss)    $ (hit)
kramasadbhava  573   2865     61.0    0.501       0.207
TOTAL: 1273 verses | 6365 model calls | ~135 hrs | $1.11 (cache-miss) / $0.46 (cache-hit)
```

### Use cases
1. **Budgeting a corpus** — "the whole 100-work sivaqueue at flash = $X, Y days" (a real planning number).
2. **Model selection** — same stack at pro = 3× cost; is the quality gain worth it? (the leaderboard decides).
3. **Pipeline planning** — batch 16 + parallel 3 cuts 135 hrs → ~3 hrs; the throughput scenario.
4. **A product** — a public "estimate my Sanskrit work" endpoint: pick a work + model → cost + time + quality range.

---

## 2. THE BENCHMARK — other things it enables (the analysis surface)

### A. The model leaderboard (cost × speed × quality) — the product
`translation_db.py --by-model` + `compile_benchmark.py` → the dashboard. Run flash AND pro on the same
verses → a real per-verse comparison: "for this verse, flash is $0.0004 + 325s + quality 0.72; pro is
$0.001 + 290s + quality 0.81." **No common product does this for Sanskrit** — it's the differentiated surface.

### B. Regression detection (is a model update getting worse?)
The benchmark is time-series (each verse logged with git_commit + ts). If a model updates and quality
drops on a **held-out verse set**, the benchmark catches it. The Sāmayik/Itihāsa golds give a stable
reference to regress against.

### C. Cost + cache optimization telemetry
The cache-hit vs cache-miss columns show the real cost lever: keep the system prompt + shared context as a
**stable leading prefix** → more cache-hit → up to 50× cheaper input. The benchmark measures the actual
cache benefit.

### D. Progress tracking (the registry)
Every verse: work, verse, model, time, calls, cost, quality, git_commit. Queryable (`--progress`,
`--by-work`, `--by-model`) → the "how much have we done + how long it's taking" DB.

### E. Gold-quality scoring (the quality axis)
`quality_score.py` — LLM-judge the produced C1/L2 against the `raw-material/` golds (0-1), reference-free
fallback. This is the "how good at translating Sanskrit" number, not Jaccard.

### F. Sourcing decisions (which source/manuscript to translate)
The projector, run per source, tells which manuscript gives the most verses for the least cost — feeding
the acquisition/ingestion pipeline (the other agent's lane).

---

## 3. FOR THE OTHER AGENT (openpatala + ingestion) — how to use this
- **openpatala:** the `/benchmarks` projection (`benchmark.json`) is ready to serve as a public page —
  per-model leaderboard + per-work progress. Add it to the read-plane.
- **ingestion pipeline:** the projector answers "is it worth ingesting this work?" — verse count ×
  per-verse cost = the ingestion ROI. Wire `project_translation.py --work <wid>` into the assess-flow
  (the T5 priority step).
- **The seam:** my progress registry (JSONL) → your `compile_benchmark.py` projection → the dashboard.
  Reuse it, don't rebuild.

## 4. THE FOUNDATION (why the numbers are honest)
- The progress registry is **JSONL** (per AXIOMS, no SQL), append-only, model-tagged, git-linked.
- Per-verse numbers are **measured from actual logged runs** (`e2e-trace.json` + the registry), not assumed.
- The DeepSeek pricing is a **documented reference** (the opencode-go provider may bill differently — noted).
- Everything is **compute-on-write** → the dashboard is a static projection, ETag/304, 0-JS (perf doctrine).

## 4b. THE ASSEMBLY-LINE FACTORY (the actual translation architecture — 2026-08-15)
**The background driver is now the PRODUCTION `factory_scheduler`, not the 1-verse-at-a-time harness.**
- Each layer (T1→L0→ARGMAP→L2→L200→C1) is an **assembly-line stage with its own queue** (the DAG backlog).
- **Big chunks:** `chunk_size=50` (`factory_scheduler.py`) → **1 model call per ~50 verses** (context-saving,
  the 1M-context win). Before, `translate_work` used `batch_size=1` → 5 calls/verse.
- **Parallel:** `FACTORY_PARALLEL=4` → chunks run concurrently (`ThreadPoolExecutor`).
- **Queue + stage telemetry:** `factory_status.py --layers` (committed vs pending per layer) +
  the per-layer avg stage time in the `/benchmarks` projection.
- **OOM fixed:** `factory_batch._source_objects` streams the SOURCE registry (was `R._load("SOURCE")` → 4.5GB).
- The background loop: `factory_long.sh` → `factory_scheduler --retry --per-layer 2 --max-model-calls 6
  --layers T1,ARGMAP,L0,L2,L200,C1` (chunk 50, parallel 4, NO intake flooding), logged to `log5long.log`.

## 5. BOTTOM LINE
> **The projector turns the per-verse benchmark into a planning + product tool: "load a stack of
> manuscripts → with this model, it costs this much and takes this long." And the benchmark itself is the
> model-leaderboard (cost × speed × quality), a regression detector, a cost optimizer, and the progress DB
> — all backed by actual logged runs, ready for the other agent's openpatala + ingestion work.**

*Sources: `pipeline/{project_translation,translation_db,quality_score,deepseek_pricing,translate_work}.py`,
`scripts/compile_benchmark.py`, `/tmp/opencode/e2e-trace.json`, `data/corpus/registries/*.jsonl`,
DeepSeek pricing docs, Sāmayik (arXiv 2305.14004) + Itihāsa (Sanskrit MT golds).*
