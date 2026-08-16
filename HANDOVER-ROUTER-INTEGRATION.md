# HANDOVER — per-layer router integration + openpatala/translation (the state + the seam)

*2026-08-15 · the handover for the agent-2 lane. What's built, what the OTHER agent's per-layer
translation stack needs from the deal-radar, and the openpatala/translation work. This preps smellycock
for handover — the coordination point between the deal-radar (model selection) and the translation
factory (per-layer execution).*

---

## 1. THE PER-LAYER TRANSLATION INTEGRATION (the seam)

The translation factory now runs **each layer as its own stage** (`domains/translation/layers/`):
T1/ARGMAP/L2/L200/C1 each have a queue + Hermes call + generator + validator, and **each can use a
different model** (`HERMES_MODEL` per worker). The deal-radar recommends the best model per layer.

**The deal-radar produces `layer_config()` → the worker config:**
```
T1    poolside/laguna-xs-2.1:free          task=extraction   # high-volume rough batch → free+cheap
ARGMAP nvidia/nemotron-3-ultra-550b-a55b:free  task=reasoning  # structural analysis
L2    poolside/laguna-xs-2.1:free          task=research     # prose quality
L200  nvidia/nemotron-3-ultra-550b-a55b:free  task=reasoning  # bounded audit
C1    poolside/laguna-xs-2.1:free          task=research     # commentary depth
```
**How the worker consumes it:** call the deal-radar `/layer-config` (or the MCP
`recommend_model_for_layer`) → set `HERMES_MODEL` per layer worker.

**Why these models:** cost-first (free wins), then value (quality/cost), rate-limit-aware (a free model
with a tiny quota is penalized for batch work). The recommendation is the ALGORITHM's reasoning (tension
scores + utility + value) — the worker can trust it or reason further.

**The arXiv basis:** RouteProfile/BELLA utility argmax (cold-start) + LinUCB with benchmark surrogate +
exploration (PILOT/2607.09015) — in `patalacheckpoints/deal-radar/app/routing.py`.

---

## 2. WHAT'S BUILT (verified, all gated)

### The deal-radar (the model-selection layer)
| Capability | Where | Tests |
|---|---|---|
| Canonical model DB (3,773 models) | deal-radar normalize.py | ✅ |
| Real pricing + rate limits + speed | HF-router + OpenRouter + models.dev | ✅ |
| Measured benchmarks (1,185 models) | benchmark_quality.py | ✅ |
| Tension engine (9 tensions × 6 profiles) | tensions.py | ✅ |
| Rate-limit-aware routing | routing.py + free_limits.py | ✅ |
| arXiv algorithms (utility + LinUCB) | routing.py | ✅ |
| Per-layer recommendation | layer_recommend.py | ✅ |
| LLM data structure + NL query | model_data.py + advanced_query.py | ✅ |
| API (16 endpoints) + MCP (6 tools) | api.py + mcp/server.py | ✅ |
| Lean Astro homepage | web/ | ✅ |

### The openpatala / translation work (the earlier lane)
- **Translation-availability index** — for each work, which translations exist + where + missing
  (254 works, 192 untranslated). API `/works/{id}/translations`.
- **The per-layer stack** (the other agent's): each layer = stage with its own model.
- **The assess flow** — deterministic decision engine routing works to translate/OCR/scholar-queue.

---

## 3. THE SEAM (what each lane needs from the other)

| The deal-radar needs | The translation stack needs |
|---|---|
| The translation layers' measured productivity (to tune per-layer model choice) | The deal-radar's `/layer-config` (HERMES_MODEL per layer) |
| Real per-layer quality outcomes (for the LinUCB learning) | The recommended model per layer + why |

**The loop:** the factory runs a layer with the recommended model → logs the outcome (quality + cost +
time) → the deal-radar's LinUCB learns → re-recommends a better model per layer.

---

## 4. THE OPEN ITEMS (for the next agent)

1. **Wire `/layer-config` into the layer workers** — set `HERMES_MODEL` per worker from the deal-radar.
2. **Feed per-layer outcomes back** — the progress registry (layers[]) → `routing.log_feedback()` so the
   LinUCB learns real quality/cost.
3. **openpatala**: the `/benchmarks` + `/recommend` projections are ready to serve as a public page.
4. **Postgres**: the documented future canonical store (the compiled-JSON read layer is current).

---

## 5. THE GATES (run after any change — both repos)

```bash
# deal-radar
cd /root/dealradar && python3 app/test.py  # 7/7  (and the other test_*.py → 65 total)
# smellycock
cd /root/smellycock && python3 check.py --status
```

*This is the handover. The deal-radar provides the per-layer model recommendation (cost-first, then
value, rate-limit-aware, arXiv-based); the translation stack consumes it per layer. The seam is the
progress-registry → feedback → LinUCB loop. Nothing is real without a gate.*
