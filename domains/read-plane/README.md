# read-plane — the compiled read plane (complete reference)

*The clean, canonical reference for the **read plane** — the projection compiler + immutable-bytes serving
that turns the canonical graph + registry into fast static surfaces (the SPEC-49 / SPEC-00 build). This is
the SERVED side; `domains/factory/` produces, `openpatala` is the API/site surface.*

## The one model (compute-on-write, read from bytes)
```text
canonical graph + object_registry ──compile──► immutable projections (R2 + site/)
   ──► Astro (humans, JSON-LD) + compiled bundles/MCP (agents) + Postgres FTS (search)
```
A reader NEVER reconstructs at request time — it serves precomputed bytes.

## The pieces (all real)
| Piece | File | Role |
|---|---|---|
| Perf doctrine (10 rules) | `performance/ip-graph-perf-doctrine.md` | the binding rules |
| Projection compiler | `ip-graph/scripts/build-static-site.py` | graph → works/concepts/openpatala layers |
| Translation-status compiler | `ip-graph/scripts/compile-translation-status.py` | per-work committed counts (live, compile-on-commit) |
| Dyczkowski gold keyer | `ip-graph/scripts/build-dyczkowski-gold.py` | kārikā-level gold (431 verses) |
| Gold scorer | `ip-graph/scripts/score-vs-gold.py` | committed T1/L2 vs gold (honest metric) |
| Atlas API | `python/patala_core/atlas/api.py` | the OpenAlex-grammar read API (ETag/304) |
| Edge deploy | Workers + R2 `patala-site` + KV | `https://patala.tradesprior.workers.dev/` |

## The budgets (SPEC-00 §23)
`cached p95 < 50ms · DB p95 < 200ms · reader JS < 80KB · LCP < 1.5s`.

## The invariants
- **Immutable versioned URLs** (`/concept/x/v17`, `/openpatala/{layer}/{sha}`), `Cache-Control: immutable`.
- **ETag from hashes → 304**; `?select=`/`?depth=` bounded; one question = one request.
- **Compute on write** — a change recompiles only what's stale (per-artifact).
- **Postgres FTS first; Tantivy only if profiled hot; Rust only as a compiled wheel.**

## Run it
```bash
python3 scripts/compile-translation-status.py       # refresh the live translation projection
python3 scripts/score-vs-gold.py --work <w>          # score committed output vs kārikā gold
```
