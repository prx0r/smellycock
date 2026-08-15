# openpatala — the OpenAlex-of-Sanskrit surface (complete reference)

*The clean, canonical reference for the **openpatala** read plane — the OpenAlex-grammar Atlas API + the
deployed edge site. This is the counterpart to `domains/translation/`: patala PRODUCES translation,
openpatala SERVES the scholarly record (including the live translation-status + content).*

## The doc map (read in order)

| Doc | What it is | Read when |
|---|---|---|
| **this README** | the index + the one-line + the integration seam | orienting |
| `api-reference.md` | the wire mechanics — the OpenAlex query grammar (`filter/search/sort/group_by/select/cursor/autocomplete`), endpoints, response envelope, caching | calling the API |
| `entity-model.md` | the semantics — the `PT*` identity scheme, the textual-transmission chain, per-dimension authority, external-ID crosswalks, rights | knowing what an entity/field means |
| `errors.md` | the failure modes — status codes, error JSON, retryability | a request failed / writing a client |
| `llm-guide.md` | one page for agents — fastest answers, token efficiency, identity rules | you're an LLM/agent using the API |

## The one-line
> **OpenAlex for Sanskrit**: a live identity/reconciliation + read plane over the Pāṭala record —
> OpenAlex-grammar API (compiled bytes, ETag/304 + immutable, p95<50ms), edge-deployed, with the live
> translation-status + content surfaced per work. Crosswalks are identity MAPPING, never corroboration.

## The integration seam (openpatala ↔ translation)
- **Translation-status:** `GET /openpatala/translation` · `GET /openpatala/translation/{work_id}` ·
  `GET /openpatala/translation/{work_id}/content` (committed T1/L2/L200/C1) · `GET /openpatala/status`
  (the live ops board). Served as compiled bytes, ETag/304 + immutable.
- **Bibliography↔translation linkage:** `enrich_bibliography.py` adds `rec['translation']` (committed
  counts + content); served via `?select=translation`.
- **Edge:** `https://patala.tradesprior.workers.dev/` (R2 `patala-site`, KV `patala-aliases`).

## The performance doctrine (how it stays fast)
`performance/ip-graph-perf-doctrine.md` — compute-on-write, immutable versioned URLs, one-question-one-
request, 0-JS Astro, ETag/304, cache aggressively. Budgets: cached p95 < 50ms · DB p95 < 200ms · reader JS
< 80KB · LCP < 1.5s.

## Non-negotiables (AXIOMS §: never violate)
- Crosswalk = identity MAPPING, never external corroboration.
- Native identity is canonical (`PTW`/`PTP` + `object_id`); external ids are `external_identifier` rows.
- Rights firewall: PANDiT CC BY-NC-SA (discovery/index only), Muktabodha CC BY-NC, GRETIL/SARIT per-file.
- Docs are a projection; the registry + ledger are the truth.
