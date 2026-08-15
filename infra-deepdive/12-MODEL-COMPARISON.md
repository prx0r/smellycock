# MODEL-COMPARISON — run different models on the same Sanskrit pipeline + review quality

*2026-08-15 · the design for comparing translation models (flash vs pro vs future) on the SAME pipeline,
verse by verse, on cost × speed × quality. Built on the formal progress registry (`translation_db.py`, JSONL per AXIOMS) — every
translation is tagged to its model, and the same verse can exist under multiple models (the
`UNIQUE(work, verse_id, model)` constraint). This is the foundation for a "how good are models at
translating Sanskrit" surface.*

---

## 1. WHY THIS WORKS (the DB is the enabler)
`translation_db.py` records every translation tagged to its **model** (via `HERMES_MODEL`). The same verse
`kramasadbhava:v9` can be translated by `deepseek-v4-flash` AND `deepseek-v4-pro` — both rows live in the DB
keyed by `(work, verse_id, model)`. So comparing models = querying the same verse under different models.

## 2. THE COMPARISON PROTOCOL (same input, per model)
1. **Fixed test set** — a stable set of verses: the `raw-material/` golds (T1 glosses, IPVV C1, ARGMAP
   golds — human-grounded) + a fixed kramasadbhava sample. Fixed input = apples-to-apples.
2. **Run the same pipeline per model** — `HERMES_MODEL=deepseek-v4-flash`, then `...pro`, on the SAME
   verses, via `translate_work.py`. Each commit is tagged to its model in the DB.
3. **Quality score** — the `quality_score` column, filled by a semantic scorer (embeddings/LLM-judge
   similarity of the produced C1/L2 vs the human gold), NOT Jaccard.
4. **Compare** — same verse, different models: time, model calls, cost, quality, side-by-side.

## 3. THE COMPARISON TABLE (the product surface)
| verse | model | total_s | calls | $/verse | quality_score |
|---|---|---|---|---|---|
| kramasadbhava:v9 | deepseek-v4-flash | 401 | 5 | 0.0009 | 0.72 |
| kramasadbhava:v9 | deepseek-v4-pro | 290 | 5 | 0.0027 | 0.81 |

The user reads: pro is 30% faster + 9pts higher quality, at 3× cost — a real, per-verse decision.

## 4. THE TEST DESIGN (the "design tests" part)
- **Fixed corpus**: the `raw-material/` golds — these have human-grounded answers, so quality is
  measurable, not vibes.
- **Metric**: semantic (embedding/LLM-judge) similarity vs gold, per layer (T1, L2, C1), not Jaccard 0.091.
- **Same input, multiple models, one DB** → the comparison is automatic + reproducible (git_commit is
  recorded on every row).
- **Splits**: a train/held-out verse split so a model's "quality" isn't fit to the test set.
- **Fail-closed**: a layer that doesn't commit (L200 hiccup) records status, doesn't fake a score.

## 5. NEXT STEPS (in order)
1. **Semantic quality scorer** → fill `quality_score` (the missing quality axis). — the biggest missing piece.
2. **Fixed test-set manifest** — the exact verses every model must translate.
3. **A `compare_models.py` runner** — run the same verses under N models, write to the DB, emit the table.
4. **A held-out gold split** so reported quality is honest.

## 6. BOTTOM LINE
The **speed + model-call + cost** axes are already recorded and tagged per model. Adding the **semantic
quality axis** completes the cost × speed × quality leaderboard for Sanskrit translation — a genuinely
novel surface (no common product does per-verse, multi-model, cost+quality Sanskrit benchmarking).

*Sources: `pipeline/translation_db.py`, `pipeline/deepseek_pricing.py`, `pipeline/translate_work.py`,
`raw-material/` (the human golds), `benchmark_translation.py`.*
