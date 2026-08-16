# BENCHMARK VISIONS — the full spec for the Sanskrit translation benchmark + science lab

*2026-08-15 · the complete vision + spec for the benchmark system: the science lab, the fixed gold control,
per-tradition specialist benchmarks, the model leaderboard, and the product. Everything we've built +
everything we're heading toward, in one spec.*

---

## 1. THE VISION (one sentence)
> **A reproducible Sanskrit translation benchmark + science lab that measures ANY model on cost × speed ×
> quality, on FIXED control golds, per specialist tradition — so we (and the world) can see exactly how
> good each model is at translating Sanskrit, and the factory can pick the best model per layer.**

## 2. THE FOUNDATION (built — the reproducible core)
| Piece | What | Where |
|---|---|---|
| **Science lab** | fixed test set + config runner + durable registry + kanban + logs | `experiment_lab.py` |
| **Fixed gold control** | 8 IPVV scholarly exemplars reused for every experiment | `sanskrit_gold.py` |
| **Model data** | pricing/context (deepseek) + the deal-radar (3,773 models, arXiv LinUCB) | `model_registry.py`, `deepseek_pricing.py`, `deal-radar` |
| **Progress registry** | every translation + experiment, model-tagged, JSONL | `translation_db.py` |
| **Per-layer agents** | each layer a stage with its own queue + model | `layer_agent.py`, `kanban_translation.py` |

## 3. THE THREE MEASURED AXES (per experiment — the comparison surface)
| Axis | Metric | Source |
|---|---|---|
| **Speed** | time, sec/verse, verses/100s | the experiment run |
| **Cost** | $/verse (cache-miss vs hit), per-layer pricing | `deepseek_pricing` / deal-radar |
| **Quality** | LLM-judge score vs the gold (0-1) | `sanskrit_gold.score_vs_gold` |

Every experiment records all three on the SAME fixed control data → the leaderboard is honest.

## 4. THE CONTROL VARIABLE (the science method)
- A **small fixed gold test set** (8 IPVV exemplars now; more per tradition later) reused for EVERY
  experiment → results are comparable (same input, different config/model).
- The lab never compares apples to oranges — same data, one variable changed at a time.

## 5. PER-TRADITION SPECIALIST BENCHMARKS (our own — the differentiator)
| Tradition | Scope | Gold source |
|---|---|---|
| **Pratyabhijñā / Trika** | recognition, IPVV | the 8 committed IPVV C1 golds ✓ |
| **Krama** | Kālīkrama (kramasadbhava, tantraloka) | raw-material + Sāmayik/Itihāsa |
| **Śaiva Siddhānta** | the control group | GRETIL Siddhānta texts |

**The idea:** assess frontier models on **specialist schools**, not just general Sanskrit — "which model
is best at Krama terminology?" A model good at general Sanskrit may be weak on a specific philosophical
school. We can build our own per-tradition golds (from raw-material + the source survey).

## 6. THE MODEL COMPARISON (the product — the leaderboard)
- Run the **same fixed control golds through multiple models** (flash, pro, the deal-radar's free picks,
  frontier models) → a per-verse cost × speed × quality table.
- **No public LLM-vs-LLM Sanskrit translation leaderboard exists** (verified: IndicParam is MCQ, not
  translation) → this is the opening.
- The Sāmayik/Itihāsa/MITRA golds (BLEU/chrF) provide a general benchmark; our per-tradition golds provide
  the specialist angle.

## 7. THE LAB WORKFLOW (how an agent uses it)
1. **State the goal** (e.g. "fastest T1 build").
2. **Review** the layer profile + `--plan <LAYER>` (which models to test + why, from the deal-radar +
   model registry).
3. **Run** the experiment variants on the fixed control data.
4. **Collect** the hermes logs + the registry results.
5. **Compare** on speed × cost × quality; keep the winner; record the decision + why.

## 8. THE FACTORY LOOP (the model selection closes)
```
deal-radar /layer-config (per-layer model + why)
   ──▶ layer_agent uses it (HERMES_MODEL) ──▶ runs the layer
   ──▶ progress registry (outcome: cost/time/quality) ──▶ LinUCB learns ──▶ re-recommends
```
Plus the **eval_sanskrit** measured quality (IndicParam) feeds the router's quality axis.

## 9. THE PRODUCT SURFACES
- **The leaderboard** (`/benchmarks` — per-model cost × speed × quality, per tradition).
- **The estimator** (`project_translation.py` — "load a stack → this model costs X, takes Y").
- **The specialist reports** (per-tradition frontier-model assessment).
- **A public "translate my Sanskrit work" estimate** (the projector as an API).

## 10. THE ROADMAP
| P | Build |
|---|---|
| P1 | **Quality into the lab report** — `experiment_lab --report` shows speed × cost × quality per run |
| P2 | **Per-tradition assessor** — `benchmark_traditions.py` runs a model on each tradition's golds + scores |
| P3 | **The leaderboard** — run flash/pro/deal-radar free on the control golds → the cost × speed × quality table |
| P4 | **More golds per tradition** — Sāmayik/Itihāsa import + per-school golds |
| P5 | **The product** — serve the leaderboard + estimator on openpatala |

## 11. BOTTOM LINE
> **The benchmark is now a reproducible science: fixed control golds, three measured axes (speed × cost ×
> quality), per-tradition specialist benchmarks, and a model leaderboard no one else has — driving the
> factory's per-layer model selection. The vision: anyone can see how good any model is at translating
> Sanskrit, and the system picks the best model per layer, per tradition, for every verse.**
