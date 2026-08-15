# OpenPāṭala Entity Model — the canonical Sanskrit research graph

*Status: v1.0 (live). The meaning of every entity and field. This is the semantics layer — the wire
mechanics live in `docs/api-reference.md`.*

**Thesis:** *OpenAlex indexes scholarship; Pāṭala indexes textual transmission and then continues
through meaning.* Every entity carries native identity (`PT*`), authority as a per-dimension vector
(never one collapsed `verified=true`), and crosswalk-outward external IDs (never canonical).

---

## 1. The identity model (Pāṭala-native)

Two identities, never conflated (from `docs/atlas-contracts/ids.md`):

- **`object_id`** — the thing across its entire history (`PTW_01J...`).
- **`version_id`** — one exact immutable formulation (`PTSRC_...@v17` + payload hash).

IDs are typed + self-describing (UUIDv7, sortable, opaque — **never encode mutable metadata in the
ID**):

| Prefix | Entity |
|---|---|
| `PTW` | Work |
| `PTP` | Person |
| `PTI` | Institution |
| `PTE` | Edition |
| `PTM` | Witness |
| `PTS` | Surrogate |
| `PTT` | Transcription |
| `PTX` | E-Text |
| `PTPASS` | Passage |
| `PTPROP` / `PTPROPV` | Proposition / Proposition-version |
| `PTARG` | Argument |
| `PTREV` | Review |
| `PTASSET` | Asset |
| `PTSRC` | Source |

Permanent resolver: `https://patala.org/id/PTW_...`

**The identity rule** (do not collapse): `Tantrāloka` = WORK · `Kaul edition` = EDITION · a specific
manuscript = WITNESS · a scan = SURROGATE · a GRETIL file = E-TEXT · the Pāṭala-selected text basis =
SOURCE. Each carries authority evidence (which catalogs/authorities matched, with confidence), not a
single collapsed boolean.

---

## 2. The textual-transmission chain (the moat)

```
WORK → EDITION → WITNESS → SURROGATE → TRANSCRIPTION → E-TEXT → SOURCE → factory
```

This is what OpenAlex does **not** model: OpenAlex indexes published scholarship; Pāṭala tracks the
**manuscript→edition→digital text** derivation that underlies a Sanskrit work.

---

## 3. The authority model (per-dimension, never a scalar boolean)

Authority is a **vector**, not a total order. Dimensions (from `docs/atlas-contracts/authority-vector.md`):

`WORK_IDENTITY · AUTHORSHIP · DATE · EDITION_IDENTITY · WITNESS_IDENTITY · TEXT_DERIVATION · RIGHTS`

Eligibility is via explicit predicates, never `ceiling >= N`:
- `eligible_for_publication()`
- `eligible_for_scholar_review()`
- `eligible_for_education()`

The source-identity ladder (for **sources only**, not propositions):
```
DISCOVERED → CATALOG_MATCHED → MULTI_SOURCE_MATCHED → COPY_INSPECTED → EDITION_VERIFIED
→ TEXT_DERIVATION_VERIFIED → SCHOLAR_CONFIRMED
```

---

## 4. The Work object (the hub)

The `Work` is the central entity. It is a real hub (not a 4-field stub) once enriched. Selectable /
sortable / filterable fields:

| Field | Type | Meaning |
|---|---|---|
| `id` | string | the stable legacy id (e.g. `malinivijayottara`) |
| `title` | string | the canonical title |
| `translation_status` | `complete\|partial\|none` | how far toward translation-readiness |
| `verified` | bool | audit flag (not authority) |
| `traditions` | string[] | the doctrinal traditions (e.g. `["Bhairava/Vidyāpīṭha","Trika"]`) |
| `period` | `{start,end,approximate}` | the compositional date range |
| `text_sources` | object[] | editions / etexts / scans (editor, year, tier, coverage, provider) |
| `translations` | object[] | translations (language, translator, coverage, complete, type, year, url, tier) |
| `scholarship` | object[] | secondary literature (author, work, year, url, tier, kind) |
| `related` | string[] | related work ids |
| `edition_count` | int | derived count of edition/critical-edition sources |
| `etext_count` | int | derived count of etext sources |

### The Work object — example (`malinivijayottara`)

```json
{
  "id": "malinivijayottara",
  "title": "Mālinīvijayottaratantra",
  "translation_status": "partial",
  "verified": "true",
  "traditions": ["Bhairava/Vidyāpīṭha", "Trika"],
  "period": {"start": 800, "end": 950, "approximate": true},
  "edition_count": 2,
  "etext_count": 0,
  "text_sources": [
    {"type": "edition", "coverage": "complete", "provider": "Muktabodha M00160", "tier": "B"},
    {"type": "critical_edition", "coverage": "chs. 1–4, 7, 12–17", "editor": "Somadeva Vasudeva", "year": 2004, "tier": "A"}
  ],
  "translations": [
    {"language": "en", "translator": "Somadeva Vasudeva",
     "work": "The Yoga of the Mālinīvijayottaratantra",
     "coverage": "chs. 1–4, 7, 12–17", "complete": false, "type": "scholarly",
     "year": 2004, "url": "http://www.ifpindia.org/bookstore/ci97/", "tier": "A"}
  ]
}
```

### In the API

> Fetch a single Work — `/works/malinivijayottara` — or a list with `filter=/search=/sort=/select=/
> cursor=` over the fields above.

---

## 5. External-ID crosswalks (crosswalk-outward, never canonical)

External identity is **crosswalk evidence**, never canonical identity. Declared schemes
(`docs/atlas-contracts/atlas-database.md`):

`NCC · NMM · NGMCP · GRETIL · SARIT · MUKTABODHA · IIIF · OCLC · ISBN · DOI · OPENALEX · ORCID · ROR · CTS`

| Identity system | What it gives Pāṭala | Pāṭala stance |
|---|---|---|
| **CTS (Canonical Text Services)** | citable passage IDs (`urn:cts:...`) | adopt citation semantics, not the server — maps to Passage/Passage-version |
| **VIAF** | clusters of author names | crosswalk for historical persons |
| **ORCID** | persistent IDs for living researchers | `sameAs` on Person |
| **ROR** | persistent IDs for institutions | `sameAs` on Institution |
| **ISNI** | global ISO 27729 public-entity ID | catch-all for authors not in VIAF/ORCID |
| **PANDiT / GRETIL / SARIT / Muktabodha** | rights-gated discovery/provenance sources | record id + license per object; never promote a crosswalk hit to `MULTI_SOURCE_MATCHED` |

**The rule** (from `resolver.py`): a crosswalk is **internal identity mapping**, NOT external
corroboration — `LEGACY_ATLAS_ID` maps legacy→UUID, and a crosswalk alone never inflates authority.

---

## 6. Rights & licensing (the firewall)

Record the license per object. PANDiT is **CC BY-NC-SA 4.0** — discovery/index/provenance only, never
unrestricted commercial. Muktabodha is **CC BY-NC 4.0**. GRETIL/SARIT are per-file/per-document. The
`rights` object (`{status, notes}`) records the status (`open | public_domain | permission | restricted |
unknown`) — **unknown ≠ missing**.

---

*This is the semantics. For the wire grammar see `docs/api-reference.md`; for failures
`docs/errors.md`; for agents `docs/llm-guide.md`. The identity is Pāṭala-native; the crosswalks point
outward; the moat is the textual-transmission chain + per-dimension authority.*
