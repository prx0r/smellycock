# SANSKRIT MODEL EVALUATION — the measured benchmark + router integration

*2026-08-15 · imported from the patalacheckpoints research lane. Import the IndicParam benchmark
(arXiv 2512.00333) and run ANY model against its real Sanskrit questions to get a MEASURED "how good at
Sanskrit" number → model-quality.json → the model router uses MEASURED quality (not just the paper's) to
route translation intelligently (cheap model for simple verses, strong for hard, free-first).*

---

## 1. WHAT WAS IMPORTED (IndicParam, the real benchmark)
| Artifact | What | Location |
|---|---|---|
| `data.csv` | 13,207 human-curated UGC-NET questions, 11 langs incl. **1,315 Sanskrit + 971 Sa-En** | `data/benchmarks/indicparam/` |
| `IndicParam-paper.pdf` | the paper (arXiv 2512.00333) | `data/benchmarks/indicparam/` |
| `llama4-scout-outputs.json` | their raw predictions (validates methodology) | `data/benchmarks/indicparam/` |

**Methodology:** zero-shot MCQ ("respond ONLY with A/B/C/D"), temp 0, regex letter extraction, typed by
format (MCQ/Assertion-Reason/List-Matching/Fill-Blank/Incorrect/Ordering), LU vs GK labels.
**Validated:** reproduced llama4-scout's Sanskrit score (46.0% vs paper ~44% — small delta is Mix-subset).

## 2. THE EVAL HARNESS (`pipeline/eval_sanskrit.py`)
```bash
python3 pipeline/eval_sanskrit.py --model deepseek-v4-flash --provider opencode-go --limit 50 --save
```
`--save` writes the measured accuracy to `data/model-quality.json`, which the router reads.

## 3. MEASURED RESULTS (our own numbers, not the paper's)
| Model | Sanskrit accuracy | Provider |
|---|---|---|
| llama-4-scout-17b | **60.0%** (n=50) | Cloudflare (free) |
| llama-3.2-3b | **26.7%** (n=30) | Cloudflare (free) |

**Confirmed the thesis with our own data:** small models (3b) are weak (26.7%); larger MoE (scout 17b)
much better (60%).

## 4. THE ROUTER INTEGRATION (measured quality → intelligent selection)
`model_router.py` reads `model-quality.json`:
- **Simple verses** → cheapest free model clearing a low floor (llama-3.2-3b if floor low, else scout)
- **Hard/rare verses** → strong model (floor 50 → scout 60%; floor 60+ → needs gemini/pro)
- **Free-first** → Cloudflare → opencode-go → OpenRouter, auto-swap on quota/429
- **Measured over paper** — the eval can rerun anytime to refresh a model's true score

## 5. THE LEGITIMACY LOOP (the vision)
```
Import gold (IndicParam) ──► eval_sanskrit.py runs a model
     ──► measured score ──► model-quality.json ──► model_router.py
          ──► quality-aware selection (hard→strong, simple→cheap) + live cost + free-first
          ──► BATCH TRANSLATION (smart, cheap, quality-guarded)
```

## 6. NEXT
- Evaluate more free models (gemma-4, qwen3, gpt-oss) to build a real leaderboard.
- Wire the eval into the batch-translation path (route per-verse by measured quality).
- Run at scale (2,286 questions/model) for statistically-solid scores.

*This connects to our science lab: eval_sanskrit gives the MEASURED per-model Sanskrit quality, which the
lab's plan_for_layer + the deal-radar can use as the quality axis.*
