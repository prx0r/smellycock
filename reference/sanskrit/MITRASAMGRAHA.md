# MITRASAMGRAHA — the translation-gate calibration gold (Sanskrit→English)

*2026-08-16 · the spec for using Mitrasamgraha as the calibration gold for the translation gate. The most
important Sanskrit→English quality benchmark for the factory — independent of Postgres, both lanes use it.
Saved here for later reference + alignment on the metric.*

---

## WHAT IT IS
- **391,548 Sanskrit–English bitext pairs** (3,000+ years, multiple genres).
- **5,552 post-corrected test pairs** + **5,587 post-corrected val pairs** (human-reviewed gold).
- **Designed to expose translation error families:**
  - compound semantic loss
  - scope loss
  - case-role inversion
  - negation loss
  - implicit-subject error
  - metaphor literalisation

## WHERE IT IS
- **HuggingFace** (`buddhist-nlp/mitrasamgraha-released-data-only`) — parquet files:
  - `test-00000-of-00001.parquet` (5,552) · `validation-00000-of-00001.parquet` (5,587) ·
    `train-00000-of-00001.parquet` (391K, 69MB)
- **R2** (`patala` bucket): `source/ingestion/MITRASAMGRAHA/snapshots/mitrasamgraha-2026-08-16/`
  (`test.jsonl` + `val.jsonl` + manifest).
- **Local**: `data/corpus/mitrasamgraha/test.parquet` + `test.jsonl` (5,552 pairs, verified).

## HOW TO USE IT (the eval + the gate)
1. **Sample test pairs** → call a model to translate the Sanskrit → score vs gold English.
2. **Metric (aligned):** `chrF` (character n-gram, right for Sanskrit morphology) + **LLM-judge semantic
   fidelity** (0-1). BLEU/chrF *understates* good Sanskrit translations (wording diverges but meaning is
   right) — so the honest score is **chrF + LLM-judge**, calibrated consistently across both lanes.
3. **Wiring:** the error families map directly to the L200 audit + translation_proof checks — running
   translation_proof against the post-corrected test pairs shows whether the gate catches the known error
   families.

## FIRST MEASURED RUN (deepseek-v4-flash, n=4 — the calibration baseline)
- **avg chrF 0.539 · bleu1 0.368** — but the qualitative output is **semantically strong** (meaning right,
  wording diverges). So surface n-gram understates quality → we need the LLM-judge semantic score alongside.

## THE ONE-RULE LINK
> Mitrasamgraha is the **calibration gold for the translation gate** — it's what makes "our L2 is good"
> verifiable. A green gate on the post-corrected test pairs = the ONE-RULE quality gate is real.

## NEXT (when we return to it)
- Wire `eval_mitrasamgraha.py` (the patalacheckpoints tool) into our lab as the L2/translation_proof gate.
- Run L2/translation_proof against the test pairs; confirm it catches the documented error families.
- Agree the final metric (chrF + LLM-judge) across both lanes so the gate is calibrated consistently.

*Source: buddhist-nlp/mitrasamgraha (HF) · R2 · the server2 lane's `tools/eval_mitrasamgraha.py`.*
