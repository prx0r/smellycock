# BUILD-OPENPATALA-PERFECTING.md — docs quality + grammar completion + bibliography enrichment

*2026-08-14 · status: DONE (verified) · agentpatala's "go ham on perfecting the OpenPatala build"
pass. OpenAlex docs + grammar + data-model researched in parallel (4 subagents), then implemented.
Every change is deterministic, perf-spec-worthy (SPEC-00 §23), and verified by execution — no model
calls, no collision with agentgraph's factory.*

---

## 1. The research (4 parallel agents — what we learned)

| Agent | Finding |
|---|---|
| OpenAlex architecture | Split docs into reference (wire) / model (semantics) / recipes (tasks); document common attrs once; JSONL+Parquet snapshots with manifest-last; `id/ids/display_name` DRY model; **don't copy** ES/fuzzy/proximity/scale |
| openpatala audit | **0 native Pāṭala docs** (README + 92 imported OpenAlex files only); 254-work bibliography is a **4-field projection** discarding rich seeds; `group_by`/`autocomplete`/multi-key-sort missing; `/editions` stub |
| ip-graph perf benchmark | All endpoints p95 < 50ms budget (max ~10ms); site 0-JS; **only gap = `/works`+`/search` lack ETag/304** |
| legacy atlas + tooling | Identity model is OpenAlex-grade already (`PT*`, per-dimension authority, 14-scheme crosswalk); **only `LEGACY_ATLAS_ID` populated**; CTS/Stencila/ORCID/ROR declared not wired; SCHEMA-AUDIT flags 4× ReviewEvent/Authority drift |

## 2. What I built (all verified)

### 2.1 Performance — closed the only gap (`api.py`)
- Added `_conditional()` → **`/works`, `/works/{id}`, `/search` now emit `ETag: "sha256-..."` +
  `Cache-Control: public, max-age=31536000, immutable` + honor `If-None-Match` → 304**. Verified:
  all three return 304 on match. The only surface not honoring immutable-cache is now compliant.

### 2.2 OpenAlex grammar completion (`api.py`)
- **`group_by=`** — `?group_by=translation_status` → `[{key, count}]`. Verified.
- **multi-key `sort=`** — `?sort=translation_status,id` + per-key `:desc`/`-`. Stable reverse-order
  sort. Verified.
- **`/autocomplete`** — prefix-over-substring title type-ahead. Verified.
- All 9 `test_api.py` contracts still PASS.

### 2.3 Bibliography enrichment (`pipeline/enrich_bibliography.py`)
The 254-work cache was a 4-field stub. New compiler merges the rich `BibliographyRecord` depth from
`audited.ts` + `bibliographySeed.ts` into the work records: `traditions`, `period`, `text_sources`
(editions/etexts/scans), `translations` (language/translator/coverage/complete/type/year/url/tier),
`scholarship`, `related`, plus derived `edition_count`/`etext_count`. 68 works enriched, 254 total
maintained, contract fields untouched. Served through `?select=`/`sort=`. **This is the "make the
bibliography beautiful data-wise" ask — the Work becomes a real hub, not a stub.**

### 2.4 Native docs (`openpatala/docs/`) — the biggest gap, now filled
Pāṭala-native OpenAlex-quality docs (reference/model/recipes split):
- `api-reference.md` — the wire grammar (filter/search/sort/group/select/cursor/autocomplete,
  envelope, caching, endpoints)
- `entity-model.md` — the `PT*` identity scheme, textual-transmission chain, per-dimension authority,
  the enriched Work object, external-ID crosswalks, rights
- `errors.md` — status codes + exact error JSON + retryability
- `llm-guide.md` — one page for agents (fastest answers, token efficiency, identity rules)
- `README.md` — the docs index; linked from `openpatala/README.md`

## 3. Perf evidence (SPEC-00 §23 budget = cached p95 < 50ms)

| Endpoint | median | p95 |
|---|---|---|
| `/works` | 6.8ms | 9.9ms |
| `/works?group_by=translation_status` | 2.9ms | 5.7ms |
| `/search?q=tantraloka` | 3.8ms | 6.0ms |
| `/autocomplete?q=tan` | 4.3ms | 6.5ms |
| `/openpatala/l0` | 3.9ms | 5.9ms |

All well under budget. ETag/304 verified on `/works`, `/works/{id}`, `/search`.

## 4. Coordination (agentgraph)
- This is entirely the **write-side / Atlas-surface** lane (docs, API grammar, bibliography data
  model). No overlap with the Tantrāloka factory DAG or your kernels.
- The bibliography enrichment touches `data/corpus/atlas-bibliography.json` — if you regenerate the
  site, re-run `pipeline/enrich_bibliography.py` first so the compiled site serves the rich data.
- **Not done (flagged, not claimed):** CTS/Stencila adapters, ORCID/ROR/ISNI population, the
  SCHEMA-AUDIT convergence (Stencila as the canonical-schema compiler), `/editions` real data, the
  R2/edge deploy. These are coordinated follow-ups, not this pass.

## 5. Files
| File | Role |
|---|---|
| `openpatala/docs/{README,api-reference,entity-model,errors,llm-guide}.md` | the native docs |
| `python/patala_core/atlas/api.py` | ETag/304 + group_by + multi-key sort + autocomplete |
| `pipeline/enrich_bibliography.py` | the bibliography enrichment compiler |
| `data/corpus/atlas-bibliography.json` | the enriched compiled cache (68 works rich) |
| this file | the build record |

---

*Honest state: the Atlas API is now OpenAlex-grammar-complete (group/sort/autocomplete), fully
ETag/304-compliant, the bibliography carries real depth, and there is a native docs set to OpenAlex
quality. Nothing claimed "verified" that isn't — CTS/Stencila/identity-population and the R2 deploy
remain explicitly NOT done and coordinated.*
