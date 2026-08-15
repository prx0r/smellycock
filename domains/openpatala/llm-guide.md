# OpenPāṭala — LLM / Agent Quick Reference

*Status: v1.0 (live). One page for AI agents: the one-rule, the ID scheme, the fastest ways to answer
the questions a Sanskrit-scholarship agent actually asks. Optimized for token efficiency — one agent
question = one request (SPEC-00 §23).*

---

## 1. The one rule

> **Compute on write, read from bytes.** The Atlas is a compiler producing immutable, independently
> addressable read artifacts; the API + site serve those bytes. `ETag`/`304` means a cached answer is
> free. Never reconstruct the record set at request time.

## 2. What Pāṭala is

OpenAlex-style grammar over the **Sanskrit textual record**. It indexes **textual transmission**
(work→edition→witness→surrogate→e-text→source→factory), not just published scholarship. Native
identity (`PTW_...`) + crosswalk-outward external IDs. Authority is a per-dimension vector, never one
collapsed `verified=true`.

## 3. Fastest answers

| Question | One request |
|---|---|
| "What works do you have?" | `GET /works?per_page=50` |
| "Find Tantrāloka" | `GET /search?q=tantraloka` (diacritic-insensitive) |
| "Which works are fully translated?" | `GET /works?filter=translation_status:complete` |
| "Which have editions?" | `GET /works?filter=edition_count:>0&select=id,title,edition_count` |
| "Breakdown by status" | `GET /works?group_by=translation_status` |
| "Type-ahead 'mal' titles" | `GET /autocomplete?q=mal` |
| "Full record for a work" | `GET /works/{id}?select=id,title,traditions,period,text_sources,translations,scholarship` |
| "What's the live registry state?" | `GET /openpatala` |
| "One layer's count" | `GET /openpatala/l0` |
| "Resolve a title/author externally" | `GET /resolve?title=Tantraloka&author=Abhinavagupta` |

## 4. ID scheme (never fuzzy-join)

- Works: `PTW_...` (typed UUIDv7). Legacy readable id: `malinivijayottara`.
- Object vs version: `object_id` = the thing; `version_id` = one exact immutable formulation
  (`PTSRC_...@v17`). Cite the version when you need reproducibility.
- Resolver: `https://patala.org/id/PTW_...`

**Join on the object/version id — NEVER on fuzzy string similarity.**

## 5. Authority — read the vector, not a boolean

A work's trustworthiness is a **per-dimension vector** (`WORK_IDENTITY · AUTHORSHIP · DATE ·
EDITION_IDENTITY · WITNESS_IDENTITY · TEXT_DERIVATION · RIGHTS`), plus an explicit eligibility
predicate. Do not treat `verified: "true"` as proof of a reading; it is an audit flag. Check the
source-identity ladder for how far a source was confirmed.

## 6. Token-efficient responses

- `?select=` project only the fields you need — don't pull the whole object.
- `?filter=`/`?search=` narrow server-side; don't page through 254 records and filter locally.
- `cursor=` for deep paging; `group_by=` for aggregates — one request, small payload.
- On `304`, reuse the cached bytes — a free answer.

## 7. External identity — crosswalk, not canon

External IDs (VIAF, ORCID, ROR, ISNI, CTS URN, GRETIL/SARIT/PANDiT/Muktabodha) are **crosswalk
evidence**, never canonical identity. A crosswalk hit does not promote authority by itself.

## 8. The three truths (storage)

`Postgres` = entity truth (what things ARE) · `R2` = artifact truth (the exact immutable bytes,
SHA-256) · event log = history truth. Everything else (site, search index, snapshots) is a rebuildable
projection.

---

## 9. DO / DON'T (borrowed from the OpenAlex LLM guide — the agent footguns)

The OpenAlex API docs teach agents how NOT to misuse a scholarly-graph API. Pāṭala has the same grammar,
so the same rules apply.

### ❌ DON'T
- **Don't** sample by random `page=` numbers (`?page=5&page=17` is NOT random and biases results).
- **Don't** filter by entity *name* (`?filter=author_name:Abhinavagupta`) — names are ambiguous.
- **Don't** loop sequential ID calls for a known list — slow.
- **Don't** retry immediately on failure — makes rate-limit/500 worse.
- **Don't** fetch all fields when you need two — wasteful.
- **Don't** `group_by` multiple dimensions in one call.

### ✅ DO
- **Do** use a canonical ID (`PTW_...`), not a name — resolve first, then filter by ID (two-step).
- **Do** batch ID lookups with the pipe `|` operator (`?filter=openalex_id:W123|W456`) — up to 50/request.
- **Do** `per_page` to the max for bulk, `select=` only the fields you need.
- **Do** implement exponential backoff on 429/500.
- **Do** `group_by` one dimension per call; combine client-side for multi-dimensional.
- **Do** respect `304` — a cached answer is free.

### Two-step ID lookup (the identity genius)
```text
1. RESOLVE the name → canonical id:   /resolve?title=Tantraloka → PTW_...
2. FILTER by the canonical id:        /works?filter=work_id:PTW_...
```
Never fuzzy-join on display names.

### The 10 common mistakes (mirrors OpenAlex)
1. Page-number sampling → use `select`/`filter`/`cursor`, not random pages.
2. Name filtering → two-step ID lookup.
3. Default page size → `per_page` max.
4. Sequential ID calls → `|` batch.
5. No error handling → retry with backoff.
6. Ignoring rate limits in threads → global rate limiter.
7. Multi-field `group_by` → one per call + combine.
8. No `mailto`-style identity → include your agent id for polite access.
9. Fetching all fields → `select=`.
10. No timeouts → add request timeouts.

---

*Fast, deterministic, one-request answers. For the full grammar see `docs/api-reference.md`; for the
meaning of entities `docs/entity-model.md`; for failures `docs/errors.md`.*
