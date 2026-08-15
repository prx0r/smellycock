# OpenPāṭala API Reference — the OpenAlex grammar over the Sanskrit record

*Status: v1.0 (live). Base URL: `https://patala.org` (dev: `http://localhost:8787`).*

This is the **wire mechanics** reference — how to filter, search, sort, group, page, select, and fetch
single entities. It does **not** re-explain what a Work/Edition/Witness is (see
`docs/entity-model.md`). It is deliberately modeled on OpenAlex's API grammar so that anyone who knows
OpenAlex can use Pāṭala immediately — *"OpenAlex for Sanskrit"*.

> **One rule:** compute on write, read from bytes. Every read is a compiled-bytes cache hit
> (`ETag`/`304`); nothing reconstructs the record set at request time.

---

## 1. The query grammar

Every list endpoint (`/works`) shares the same mechanics. Parameters are URL query strings.

| Param | What it does | Example |
|---|---|---|
| `filter=` | attribute:value pairs, comma = AND, `!` = NOT, `<`/`>` = numeric | `filter=translation_status:complete` |
| `search=` | full-text across title/id | `search=tantraloka` |
| `sort=` | `field` or `field:desc`, comma-separated multi-key | `sort=translation_status,id` |
| `cursor=` | opaque deep-paging token (`*` to start) | `cursor=*` then `cursor=<next>` |
| `per_page=` | page size (1–500) | `per_page=100` |
| `select=` | root-level fields only, comma-separated | `select=id,title,traditions` |
| `group_by=` | aggregate counts by a field | `group_by=translation_status` |

### filter= operators

```bash
curl "http://localhost:8787/works?filter=translation_status:complete"     # AND
curl "http://localhost:8787/works?filter=verified:true"                    # equality
curl "http://localhost:8787/works?filter=translation_status:!complete"     # NOT
curl "http://localhost:8787/works?filter=edition_count:>0"                 # numeric > / <
```

### search= (folded, diacritic-insensitive)

```bash
curl "http://localhost:8787/search?q=tantraloka"        # → "Tantrāloka" (diacritic-insensitive)
curl "http://localhost:8787/works?search=abhinavagupta"
```
Search matches `id` + `title` with diacritics folded to ASCII (`ā→a`, `ś→s`, `ṇ→n`, …), so a query is
a cheap substring probe over a **precomputed folded index** — never a per-request scan of the record set.

### sort= (multi-key)

```bash
curl "http://localhost:8787/works?sort=translation_status,id"
curl "http://localhost:8787/works?sort=edition_count:desc"
```
Comma-separated keys, each optional `:desc` (or leading `-`). The leftmost key is dominant (stable
per-key sort applied in reverse order).

### cursor= paging (deep, opaque)

```bash
curl "http://localhost:8787/works?per_page=100&cursor=*"          # first page
curl "http://localhost:8787/works?per_page=100&cursor=<next_cursor>"   # next
```
`cursor` is an opaque base64 offset — not `?page=97321`. Repeat until `next_cursor` is `null`.

### select= (projection)

```bash
curl "http://localhost:8787/works/malinivijayottara?select=id,title,traditions,translations"
```
Root-level fields only. Supports the enriched work fields (§entity-model).

### group_by= (aggregation)

```bash
curl "http://localhost:8787/works?group_by=translation_status"
```
Returns `group_by: [{"key": "complete", "count": 30}, ...]`.

### autocomplete (type-ahead)

```bash
curl "http://localhost:8787/autocomplete?q=mal"
```
Returns title matches ranked prefix-over-substring, for type-ahead UI/agents.

---

## 2. Get single entities

```bash
curl "http://localhost:8787/works/malinivijayottara"        # key only
curl "http://localhost:8787/works/malinivijayottara?select=id,title"
```
- IDs are the Pāṭala-native legacy id (e.g. `malinivijayottara`); the typed `PTW_...` scheme is the
  canonical identity layer (see `docs/entity-model.md`).
- External-ID lookups and merged-entity `301`s are the forward path (once crosswalks are populated).

---

## 3. The response envelope

Every list endpoint returns the same shape:

```json
{
  "count": 5,
  "total": 254,
  "next_cursor": "MQ==",
  "works": [ { "id": "malinivijayottara", ... } ],
  "provenance": { "api_version": "1.0", "backend": "postgres" }
}
```

Single-entity endpoints return `{ "data": {...}, "provenance": {...} }`.

---

## 4. Caching (the performance contract)

- **Every endpoint** emits `ETag: "sha256-..."` + `Cache-Control: public, max-age=31536000, immutable`.
- Conditional `If-None-Match` → **304 Not Modified** (client sends nothing; the bytes are immutable).
- All p95 latencies are far under the SPEC-00 §23 budget (<50ms): `/search` ~10ms, `/works` ~10ms,
  `/openpatala` ~8ms.

---

## 5. Endpoints

| Route | Method | Purpose |
|---|---|---|
| `/health` | GET | adapter backend + work count |
| `/works` | GET | list/filter/search/sort/group/select/cursor/paging |
| `/works/{id}` | GET | one work |
| `/works/{id}/identifiers` | GET | the external-ID crosswalk (PANDIT/GRETIL/SARIT/MUKTABODHA/CTS) — the resolver surface |
| `/works/{id}/bundle` | GET | one-request projection: work + editions + identifiers + related (`?depth=0|1|2`, ETag/304) |
| `/persons/{id}` | GET | one person + external authority ids (VIAF/Wikidata/ORCID) |
| `/institutions` | GET | list institutions (ROR crosswalk) |
| `/institutions/{id}` | GET | one institution |
| `/search` | GET | alias for `/works?search=` |
| `/autocomplete` | GET | title type-ahead |
| `/editions` | GET | real editions (editor/year/provider/tier/coverage, filterable by `filter=work:X`) |
| `/openpatala` | GET | live registry summary (counts + root hash) |
| `/openpatala/{layer}` | GET | one compiled layer projection |
| `/openpatala/{layer}/latest` | GET | short-TTL pointer to the newest compiled artifact |
| `/openpatala/{layer}/{sha}` | GET | immutable content-addressed artifact (stale sha → `X-Superseded-By`, not 404) |
| `/openpatala/search-index` | GET | compiled concept search index |
| `/resolve` | GET | identity crosswalk (OpenAlex/Crossref) — RESOLVED/NOT_FOUND/UNAVAILABLE |

---

*The grammar is the OpenAlex contract; the data is Pāṭala's. For the meaning of each entity and field,
see `docs/entity-model.md`. For what can go wrong and the exact error JSON, see `docs/errors.md`. For
agents, see `docs/llm-guide.md`.*
