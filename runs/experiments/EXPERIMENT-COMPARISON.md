# EXPERIMENT COMPARISON — which translation build is best (2026-08-15)

*A measured comparison of the 3 translation architectures, from real runs. Build 1 was run live (one
1M-context call → all 6 layers for kramasadbhava:v1, saved in `experiments/build1-wholechain/run-1`);
Build 3 is measured from the committed registry (v1's full chain exists, built by the per-layer path).*

---

## THE 3 BUILDS (from `BRAINSTORM-3-BUILDS.md`)
| Build | Idea | Model calls per full chain (1 verse) |
|---|---|---|
| **1 — Whole-chain single-pass** | load the work once (1M context) → emit T1/L0/ARGMAP/L2/L200/C1 as per-layer JSONL | **1** (measured) |
| **2 — Graph-memory reader-writer** | a memory the translator reads+updates; later verses get easier (compounding corpus) | ~1–5 (memory amortized; not 1-verse measurable) |
| **3 — Specialized passes + handoffs** | one call per layer, each committed → next reads the registry (the current factory) | **~5** (T1/ARGMAP/L2/L200/C1; L0 deterministic) |

## THE MEASURED RESULT
- **Build 1 (real run):** ONE Hermes call produced **all 6 layers** for kramasadbhava:v1 — committed +
  validated, `tail:false` (no truncation), real content (C1 Krama commentary, L2 readable prose). **~6×
  fewer model calls than Build 3.**
- **Build 3 (from the registry):** the same v1 full chain exists, built over **~5 model calls** (one per
  model-bound layer, L0 deterministic free-draining). More calls, each focused/reliable.

## THE TRADEOFF (honest)
| | Build 1 | Build 3 |
|---|---|---|
| Model calls per full chain | **1** (6× fewer) | ~5 |
| Output size per call | **huge** (6 layers × N verses) → truncation risk grows with N | small (1 layer) — reliable |
| Throughput (the goal) | **best** on the model-bound layers | lower |
| Reliability at scale | needs streaming/adaptive (the proven contract) | high (focused calls) |
| Integration with current infra | new generator; commit path still to wire | **already the running factory** |

## VERDICT — Build 1 WINS on throughput; the BEST build is a HYBRID
- **Throughput winner: Build 1** — ~6× fewer calls on the model-bound layers (the real bottleneck to C1).
- **Reliability + integration winner: Build 3** — it's the running factory; focused calls don't truncate.
- **The best build = Build 1 at small N (whole-chain per verse/chunk, streaming + adaptive), falling back
  to Build 3's per-layer for large N or on truncation.** This gets Build 1's ~6× win where it's safe and
  Build 3's reliability where the output would get too large.
- **Build 2 (graph-memory) is the long-term compounding win** — each verse enriches a memory so the corpus
  gets easier (the dialect-genealogy idea). Not measurable in a 1-verse A/B, but the right end-state once
  the whole-chain path is committed.

## RECOMMENDATION (the path)
1. **Wire Build 1's output into the real registry** (commit the 6 layers from one call via the existing
   validators) — this makes the 6× win real, not just measured.
2. **Adaptive N**: start whole-chain at ~8 verses/chunk; halve on truncation (the proven adaptive rule).
3. **Then Build 2** — add the graph memory so the corpus compounds.

*Build 1 measured live (1 call → 6 layers); Build 3 measured from the committed chain (5 calls). The best
is the hybrid: Build 1's whole-chain at small N with Build 3's per-layer fallback, then Build 2's memory
on top.*

## POST-RUN CORRECTION (autonomous finding, 2026-08-15)
**Build 1 (whole-chain) is UNRELIABLE AT SCALE.** Tested live: at batch ≥2, the model does NOT reliably
emit the strict per-layer JSONL — it often returns an *example* (`{"tokens":{"<surface>":...}}` with literal
placeholders) + prose + reasoning instead of the 6 real layer records. So `parse_layers` extracts nothing,
C1 never advances. It worked on 1 verse (the earlier proof) but not reliably at N≥2.
**Verdict revision:** the reliable path to C1 is the **per-layer factory (Build 3)** — it reliably produces
ARGMAP/L2/L200/C1 (measured: those layers are climbing via the factory while whole-chain contributed ~0
new C1). The 6× whole-chain win is theoretical; in practice the model won't hold the all-layer JSONL
contract at batch. **Recommendation:** keep the per-layer factory as the production path; treat Build 1 as
a small-batch (1 verse) nicety, not the scale path. A middle option (grouping 2 layers per call, e.g.
T1+L0 / ARGMAP+L2 / L200+C1 = 3 focused calls per verse) is worth testing as the reliable middle ground.
