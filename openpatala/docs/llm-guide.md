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

*Fast, deterministic, one-request answers. For the full grammar see `docs/api-reference.md`; for the
meaning of entities `docs/entity-model.md`; for failures `docs/errors.md`.*
