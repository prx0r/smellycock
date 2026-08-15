# OPTIMIZATION ANALYSIS — from Live Run 1 + the arxiv/github patterns

*2026-08-15. What the live run revealed + the concrete optimizations applied, cross-referenced to the
cloned agentic repos (`ip-graph/ecosystem/`) and the arXiv agent papers. Every finding is grounded in the
run's data (`data/ops/live-run-1/`).*

---

## 1. FINDINGS FROM THE RUN
| Signal | Evidence | Implication |
|---|---|---|
| **One-owner race** | two factory passes at 14:36 (watchdog `pgrep` race) | need an atomic owner claim |
| **L0 throughput** | 12 commits / 5 min = ~2.4/min (deterministic, CPU-bound Vidyut) | the deterministic floor is the fast layer; throughput is a `per_layer` knob |
| **L2 thin** | 3 committed (model-bound readable prose) | the real bottleneck to the full chain is the model layers, not L0 |
| **Memory stable** | factory ~550MB the whole run (4.5GB→545MB fix holds) | no OOM risk; the streaming lookup works |

## 2. OPTIMIZATIONS APPLIED (deterministic, safe)
| # | Fix | Pattern (source) | Where |
|---|---|---|---|
| 1 | **Atomic one-owner lock** — a pid-file created with `O_EXCL`; a second watchdog can never claim while the first is alive. Reclaims stale locks. | **herdr**'s registered-reducer/atomic-claim ("no arbitrary loops; ownership is registered") | `pipeline/watchdog_fullchain.py` (`_claim_owner`/`_release_owner`) |
| 2 | **`per_layer` throughput lever** — `--per-layer 20` gave ~6× L0 rate (2-per-10min → ~2.4/min) | the perf doctrine's "parallelize/batch CPU work" | scheduler CLI |

## 3. THE NEXT OPTIMIZATIONS (the honest plan)
| # | Optimization | Pattern (source) | Why |
|---|---|---|---|
| A | **L2 at scale via batch-input/chunk-output + parallel workers** — apply the T1 `canonical_translate` JSONL contract to L2, and use **`delegate_task`/parallel Hermes workers** for the model-bound prose | the translation doctrine ("batch the input, chunk the output") + **OpenHands SDK / delegate_task** | L2 (3) is the real gap to the full chain |
| B | **Bounded-process L0** — a `ProcessPoolExecutor` where each worker loads Vidyut once and processes a chunk of verses (amortizing the expensive Chedaka model load). **Cautious**: each worker loads the model → memory risk on the 8GB box; only if L0 becomes the bottleneck. | maestro/perf "parallelize CPU work" | L0 is not currently the bottleneck |
| C | **Failure-class-aware recovery** — record a structured trace per pass (memory/JSON/timeout/validator) and pick the recovery under a budget | **Self-Healing Orchestrators** (observable signal → failure class → budgeted recovery → verify) | the `trace_log` layer is wired; wire it to choose recovery |
| D | **Semantic gold scoring** — replace raw Jaccard (0.091) with semantic matching (embeddings / LLM-as-judge) | the docs' own finding + the gold scorer | makes the anti-theatre metric meaningful |

## 4. WHERE THE RUN PROVED THE SYSTEM
- A fresh run committed 12 real validated L0 in 5 min, memory stable, full logs + traces.
- The status board + trace log gave real observability (the herdr/self-healing structure).
- The one-owner fix closes the race the run exposed.

*This analysis lives in the working repo (not patalaorg — patalaorg is final docs only). The applied fixes
(one-owner lock) are live; A–D are the prioritized next optimizations.*
