# BUILD DEV PLAN — smellycock / openpatala / ingestor (what's done, what didn't finish, what's next)

*2026-08-15 · the honest build plan for the smellycock (reference), openpatala (serve), and ingestor
(assess/translation) work. What's BUILT + verified, what's UNFINISHED, and the next build steps in
priority order. Every item maps to a real module + gate.*

---

## 1. THE ARCHITECTURE (the three planes)

```
INGESTOR (assess/translation) → OPENPATALA (serve) → SMELLYCOCK (reference)
   pipeline/assess.py            atlas api.py            domains/ docs/
   translation_availability      /works /translations    MANIFEST + check.py
   translation_locator           /recommend /benchmarks
   project_translation           /recommend-layer
```

---

## 2. WHAT'S BUILT + VERIFIED (done, all gated)

### The ingestor (assess/translation pipeline)
| Capability | Module | Gate |
|---|---|---|
| Translation-availability index (254 works, 192 untranslated) | `translation_availability.py` | 11/11 |
| Live translation-location (OpenAlex/Crossref/Unpaywall) | `translation_locator.py` | 10/10 |
| Materialized translation-status (compute-on-write) | `translation_status.py`, `build_translation_index.py` | ✅ |
| Ingestion-ROI projector (cost/time/calls to translate) | `project_translation.py` | 10/10 |
| The ASSESS decision engine (T0-T5 + routing table) | `assess.py` | 16/16 |
| Red-team hardening (2 rounds, real vulns fixed) | source_ready/assess/reconcile/api | ✅ |

### openpatala (serve)
| Capability | Module | Gate |
|---|---|---|
| Atlas API (OpenAlex grammar, ETag/304, 254 works) | `patala_core/atlas/api.py` | ALL PASS |
| Translation-availability endpoints | `/works/{id}/translations`, `/translations` | ✅ |

### The deal-radar (model selection — the new layer)
| Capability | Module | Gate |
|---|---|---|
| 3,773 canonical models (real prices + speed) | `deal-radar/app/normalize.py` | ✅ |
| Tension engine + arXiv routing + per-layer rec | `tensions.py`, `routing.py`, `layer_recommend.py` | 65 tests |
| MCP server (6 tools) + API (16 endpoints) + Astro | `mcp/`, `api.py`, `web/` | ✅ |

---

## 3. WHAT DIDN'T GET FINISHED (the honest gaps)

### 3.1 smellycock / reference
- **Not fully reconciled with the other agent's concurrent MANIFEST edits** — the MANIFEST merge was
  fought; the clean handover doc is committed but the full build-docs set from my earlier commits was
  reset (re-derivable, in my notes + deal-radar).
- **The per-layer router integration doc** is done (`HANDOVER-ROUTER-INTEGRATION.md`) but the translation
  **workers don't yet consume `/layer-config`** (the HERMES_MODEL-per-layer wiring is the next build).

### 3.2 openpatala / serve
- **Atlas Postgres is not up** (the documented future canonical store) — the compiled-JSON read layer
  is current, Postgres deferred.
- **`/recommend` + `/benchmarks` projections not yet served as a public openpatala page** (the deal-radar
  data could be surfaced).
- **`fastapi`/deps are in a venv**, not system — the API runs from `.venv-atlas`, not deployed.

### 3.3 ingestor / translation
- **The actual T1/L0/L2 translation generation** is the OTHER agent's lane (Hermes-driven); the assess
  + availability + projector feed it, but the generation worker isn't mine.
- **The per-layer model auto-load** — the deal-radar recommends per-layer models, but the workers
  haven't been rewired to use them yet.
- **Mitrasaṃgraha benchmark import** (the Tantrāloka 4,550 gold) was spec'd (sanskritbenchplan) but not
  imported + wired as a quality gate.

---

## 4. THE NEXT BUILD (priority order)

### P1 — Wire the per-layer model into the translation workers (the seam)
- Have the layer workers read `/layer-config` (or MCP `recommend_model_for_layer`) → set `HERMES_MODEL`.
- Feed per-layer outcomes → `routing.log_feedback()` → LinUCB learns.
- **Why:** this is the highest-value unfinished piece — the deal-radar → translation-stack integration.

### P2 — Serve the deal-radar on openpatala
- Expose `/recommend`, `/benchmarks`, `/recommend-layer` as public openpatala projections (additive).
- Surface the per-layer config + the model leaderboard.

### P3 — Import Mitrasaṃgraha gold + quality gate
- Download the Tantrāloka 4,550 pairs → score our L2/C1 output → a real translation-quality number.
- Gate promotion on the benchmark score (the ONE-RULE quality gate).

### P4 — Atlas Postgres
- Stand up the canonical store when the read layer demands it (perf rule 6: measure first).

---

## 5. THE GATES (run after any change)

```bash
# deal-radar (the model layer)
cd /root/dealradar && python3 app/test.py  # 7/7 (all test_*.py → 65)
# ingestor (patalacheckpoints)
cd /root/patalacheckpoints && for p in assess translation_availability translation_locator project_translation; do PYTHONPATH=pipeline python3 pipeline/${p}_test.py | grep SUMMARY; done
# smellycock (reference)
cd /root/smellycock && python3 check.py --status
```

---

## 6. THE PUSH STATUS (honest)

| Repo | Local | Remote | Unpushed | Pushable? |
|---|---|---|---|---|
| smellycock | 501582b | 3ed810c | 1 (handover doc) | ✅ safe (clean, on top of remote) |
| patalacheckpoints | ec9807a | b5b9b50 | 20 (all my work) | ⚠️ 20 commits, but it's my own lane — likely safe |
| dealradar | df615b3 | (no remote) | n/a | ⚠️ standalone, no remote yet |

---

*This is the build plan. The core (assess/availability/locator/projector + the deal-radar model layer) is
built + verified. The unfinished pieces are: P1 wire per-layer model into workers, P2 serve on openpatala,
P3 Mitrasaṃgraha gold gate, P4 Postgres. P1 is the highest-value next build.*
