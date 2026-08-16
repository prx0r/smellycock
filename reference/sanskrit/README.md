# reference/sanskrit — the canonical Sanskrit research references

*2026-08-15 · imported from the patalacheckpoints research lane. The verified Sanskrit benchmark,
evaluation, and source-repository references — grounding the science lab, the model router, and the
ingestion pipeline.*

## The docs
| Doc | What it is |
|---|---|
| `SANSKRIT-BENCHMARKS.md` | which models are best at Sanskrit + the translation benchmarks (Sāmayik, Itihāsa, MITRA) + the gold data |
| `SANSKRIT-EVAL-ROUTER.md` | the measured per-model eval (IndicParam) → model-quality.json → the router |
| `SANSKRIT-REPOSITORIES-SURVEY.md` | where to source Sanskrit texts (bulk/authoritative) for ingestion |

## How it feeds our work
- **Science lab** (`domains/translation/LAB.md`) — the quality axis + which models to test (from the benchmarks).
- **Deal-radar / model router** — measured Sanskrit quality (not assumed) → per-layer model choice.
- **Ingestion** — GRETIL/Muktabodha TEI e-texts for clean verse recovery; rights firewall per AXIOM 9.
