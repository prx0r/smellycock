# COMPATIBILITY MATRIX — 14 product engines → canonical patalaorg model

*2026-08-15 · the machine-resolvable mapping: each product engine (built + live-tested in
`/root/patalacheckpoints/pipeline/products/`) → its canonical layer + PT* identity + authority +
validator. This is the seam where my epistemic layer meets the production patalaorg DAG.*

**Canonical source of truth:** `OBJECT-MODEL.md` (the DAG) + `AXIOMS.md` (naming, ladders, banned words)
+ `openpatala/entity-model.md` (PT* identities).

---

## The compatibility matrix

| # | Product | Canonical layer | PT* identity | Deterministic | Authority ceiling | Proof | Validator |
|---|---|---|---|---|---|---|---|
| 1 | `translation_proof` | `translation_proof` (L200, the moat) | PTL200 | yes | `SCHOLARLY_CORROBORATED` only if gate PASS | 6/6 | `test.py` + audit vector |
| 2 | `claim` | `argument` proposition floor | PTPROP | yes | `MACHINE_PROPOSED` (PĀṬALA-INFERS) / `SCHOLARLY_CORROBORATED` (SOURCE-SAYS) | 7/7 | `test.py` + honesty gate |
| 3 | `argument` | `argument` | PTARG | yes | `MACHINE_PROPOSED` | 6/6 | `test.py` + closed-vocab gate |
| 4 | `crux` | `synthesis` (minimal divergence) | PTCRUX | yes | `MACHINE_PROPOSED` | 4/4 | `test.py` |
| 5 | `comparison` | `synthesis` (AGREEMENT/CRUX) | PTCOMP | yes | `MACHINE_PROPOSED` | 3/3 | `test.py` |
| 6 | `research_packet` | `synthesis`/read-plane | PTPACK | yes | `MACHINE_PROPOSED` (retrieval) | 5/5 | `test.py` |
| 7 | `evidence_independence` | `commentary`/corroboration | PTCORR | yes | `MACHINE_PROPOSED` + live | 5/5 | `test.py` + live OpenCitations |
| 8 | `scholar_review` | `review` (human authority) | PTREV | yes | review ladder | 11/11 | `test.py` + gate |
| 9 | `context_bundle` | read-plane bundle (Phase 9) | PTPACK | yes | `MACHINE_PROPOSED` | 6/6 | `test.py` + token budget |
| 10 | `passage` | read-plane / passage | PTPASS | yes | `DETERMINISTIC_FACT` | 6/6 | `test.py` |
| 11 | `passage_workbench` | read-plane / philology | PTPASS | yes | `MACHINE_PROPOSED` → review | 5/5 | `test.py` + gate |
| 12 | `terminology` | read-plane / lexical | PTTERM | yes | curated (reviewed ladder) | 6/6 | `test.py` |
| 13 | `timeline` | read-plane / atlas | PTTL | yes | curated | 5/5 | `test.py` |
| 14 | `benchmark` | eval plane (anti-theatre) | PTBENCH | yes | — | 5/5 + inspect 1.000 | `test.py` + inspect_ai |

### The scholar-workflow layer (products #15-19)
| # | Product | Canonical layer | PT* identity | Deterministic | Authority ceiling | Proof | Validator |
|---|---|---|---|---|---|---|---|
| 15 | `review_queue` | `review` (prioritization) | PTREV | yes | `MACHINE_PROPOSED` (prioritizes, never decides) | 6/6 | `test.py` |
| 16 | `scholar_identity` | `review` (identity) | PTREV | yes | ORCID-verified | 7/7 | `test.py` |
| 17 | `review_workbench` | `review` (surface) | PTREV | yes | `MACHINE_PROPOSED` | 6/6 | `test.py` |
| 18 | `scholar_profile` | `review` (ledger) | PTREV | yes | `MACHINE_COMPILED` | 6/6 | `test.py` |
| 19 | `review_policy` | `review` (authority semantics) | PTREV | yes | invariant-preserving | 7/7 | `test.py` |

---

## The DAG placement (where each product sits on the canonical spine)

```text
source → draft_translation → tokenization → [argument_outline] → translation → translation_proof ──┐
                                                                        (L200: product #1)         │
                                                                                                  ▼
commentary (C1) → theme / argument ──► synthesis ──► essay ──► lesson
      │                 │              │
      │                 ├─ claim #2    ├─ crux #4
      │                 ├─ argument #3 ├─ comparison #5
      │                 │              ├─ research_packet #6
      │                 │
      └─ evidence_independence #7 (corroboration over real C1s + assertions)

READ-PLANE (all deterministic, compile-on-write):
   passage #10 · passage_workbench #11 · terminology #12 · timeline #13 · context_bundle #9
   scholar_review #8 (human authority, gates the upper spine)
   benchmark #14 (measures the whole epistemic layer)

```

---

## Identity + authority rules honored (from AXIOMS / entity-model)

- **Every product output** carries the 4-axis authority vector (`generation · evidence · review ·
  publication`), a partial order (`A ⪯ B ⟺ ∀i A_i ≤ B_i`), **never** a scalar max. `authority(projection)
  ≤ authority(parent)` holds on every edge.
- **Object TYPE ≠ epistemic STATE.** A real IPVV Source is not `SCHOLARLY_CORROBORATED` by type; only a
  gate/review raises it.
- **Banned words** never appear: outputs say `MACHINE_PROPOSED`, `SUPPORTED BY`, `PASSED CHECK X`,
  `REVIEWED BY`, `NO CONFLICT DETECTED` — never `PROVED / TRUTH / CORRECT / BEST / WINS`.
- **IDs:** products join on canonical object/version ids (never fuzzy string similarity), per the
  identity rule.

---

## The live truth reconciliation (verified 2026-08-15)

| Layer | Registry count (live) | My product |
|---|---|---|
| C1 | 43 | `claim` reads real C1 bodies |
| argument | 23 | `argument` derives from real C1 |
| synthesis | 7 | `crux`/`comparison`/`research_packet` feed |
| essay | 8 | consumed by `scholar_review`/`context_bundle` |
| education | 6 | consumed by `context_bundle` |
| assertion | 6 | `evidence_independence` reads |
| corroboration | 6 | `evidence_independence` reads + classifies |

**Total product proof:** 80/80 deterministic PASS + 16/16 live integration PASS (real
Crossref/OpenAlex/OpenCitations + real registries).

---

*This is the compatibility seam. The products integrate as the documented epistemic layer of the
production DAG, honoring the canonical object model, identity, and authority rules exactly.*
